import cv2
import numpy as np
import json # Added for loading config

# --- Color Definitions are now loaded from JSON ---
# Default path for the HSV configuration file
DEFAULT_CONFIG_PATH = "pacman_ai/hsv_config.json"

def load_hsv_config(config_path: str = DEFAULT_CONFIG_PATH):
    """
    Loads HSV threshold configurations from a JSON file.
    Args:
        config_path (str): Path to the JSON configuration file.
    Returns:
        dict: A dictionary with color names as keys and their HSV threshold dicts as values.
              HSV threshold values are converted to NumPy arrays.
              Returns None if loading fails.
    """
    try:
        with open(config_path, 'r') as f:
            config_data = json.load(f)

        # Convert list-based HSV values to NumPy arrays
        processed_config = {}
        for color_key, thresholds in config_data.items():
            processed_thresholds = {}
            for key, value in thresholds.items():
                if isinstance(value, list) and ("lower" in key or "upper" in key) : # Check if it's an HSV array
                    processed_thresholds[key] = np.array(value, dtype=np.uint8)
                else:
                    processed_thresholds[key] = value # e.g., 'name_for_detection'
            processed_config[color_key] = processed_thresholds

        print(f"HSV config loaded successfully from {config_path}")
        return processed_config
    except FileNotFoundError:
        print(f"Error: HSV Config file not found at {config_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {config_path}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while loading HSV config: {e}")
        return None

def load_image(image_path: str):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not load image from path: {image_path}")
        return None
    return image

def convert_to_hsv(image: np.ndarray):
    if image is None:
        print("Error: Cannot convert None image to HSV.")
        return None
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

def get_color_mask(hsv_image: np.ndarray, lower_bound_hsv: np.ndarray, upper_bound_hsv: np.ndarray):
    if hsv_image is None:
        print("Error: Cannot get color mask from None HSV image.")
        return None
    return cv2.inRange(hsv_image, lower_bound_hsv, upper_bound_hsv)

def find_objects_by_color(image: np.ndarray, object_label: str,
                          lower_hsv1: np.ndarray, upper_hsv1: np.ndarray,
                          lower_hsv2: np.ndarray = None, upper_hsv2: np.ndarray = None,
                          min_area_threshold=50):
    if image is None:
        print(f"Error: Input image is None for find_objects_by_color ({object_label}).")
        return []
    hsv_image = convert_to_hsv(image)
    if hsv_image is None: return []
    mask1 = get_color_mask(hsv_image, lower_hsv1, upper_hsv1)
    if mask1 is None: return []
    final_mask = mask1
    if lower_hsv2 is not None and upper_hsv2 is not None:
        mask2 = get_color_mask(hsv_image, lower_hsv2, upper_hsv2)
        if mask2 is not None: final_mask = cv2.bitwise_or(mask1, mask2)

    contours, _ = cv2.findContours(final_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    found_objects = []
    if contours:
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > min_area_threshold:
                x, y, w, h = cv2.boundingRect(contour)
                center = (x + w // 2, y + h // 2)
                found_objects.append({
                    "label": object_label, # Changed from "color" to "label" for more general use
                    "center": center,
                    "bbox": (x, y, w, h),
                    "area": area
                })
    return found_objects

def find_pacman(image: np.ndarray, pacman_hsv_thresholds: dict, min_area_threshold=50):
    if image is None:
        print("Error: Input image is None for find_pacman.")
        return None, None
    if not pacman_hsv_thresholds or "lower" not in pacman_hsv_thresholds or "upper" not in pacman_hsv_thresholds:
        print("Error: Invalid HSV thresholds for Pac-Man.")
        return None, None

    # Pac-Man is assumed to be the largest object of its color
    found_pacman_objects = find_objects_by_color(image, "pacman",
                                               pacman_hsv_thresholds["lower"],
                                               pacman_hsv_thresholds["upper"],
                                               min_area_threshold=min_area_threshold)
    if not found_pacman_objects:
        return None, None

    # Find the object with the largest area among those detected as "pacman"
    largest_pacman = max(found_pacman_objects, key=lambda p: p["area"])
    return largest_pacman["center"], largest_pacman["bbox"]


def find_all_ghosts(image: np.ndarray, ghost_color_config: dict, min_area_threshold=50):
    """
    Finds all types of ghosts based on their defined colors.
    Args:
        image (numpy.ndarray): Input image in BGR format.
        ghost_color_config (dict): Dict from loaded config, where keys are e.g. "ghost_red", "ghost_frightened_blue".
                                   Each sub-dict contains HSV ranges and a 'name_for_detection'.
        min_area_threshold (int): Minimum contour area.
    Returns:
        list: A list of dictionaries, each representing a found ghost object.
              The 'label' will indicate the specific ghost type (e.g., "red", "frightened_blue").
    """
    all_found_ghosts = []
    for ghost_key, defs in ghost_color_config.items():
        if not ghost_key.startswith("ghost_"): # Process only ghost entries
            continue

        label = defs.get("name_for_detection", ghost_key) # Use specific name or the key itself
        lower1 = defs.get("lower1")
        upper1 = defs.get("upper1")
        lower2 = defs.get("lower2", None)
        upper2 = defs.get("upper2", None)

        if lower1 is None or upper1 is None:
            print(f"Warning: Missing primary HSV range for {label}. Skipping.")
            continue

        # The label passed to find_objects_by_color will be used in the output dict
        # This label should distinguish between normal states (red, pink, etc.) and frightened.
        # e.g., label could be "red_chase", "pink_chase", "frightened_blue"
        # The 'name_for_detection' in JSON should convey this.
        found_objects = find_objects_by_color(image, label,
                                              lower1, upper1,
                                              lower2, upper2,
                                              min_area_threshold)
        all_found_ghosts.extend(found_objects)
    return all_found_ghosts

def find_all_pellets(image: np.ndarray, pellet_hsv_thresholds: dict,
                     min_pellet_area=5, max_pellet_area=50,
                     min_power_pellet_area=51, max_power_pellet_area=150):
    if image is None:
        print("Error: Input image is None for find_all_pellets.")
        return [], []
    if not pellet_hsv_thresholds or "lower" not in pellet_hsv_thresholds or "upper" not in pellet_hsv_thresholds:
        print("Error: Invalid HSV thresholds for pellets.")
        return [],[]

    # Use find_objects_by_color to get all pellet-colored items
    all_pellet_colored_objects = find_objects_by_color(image, "pellet_color",
                                                       pellet_hsv_thresholds["lower"],
                                                       pellet_hsv_thresholds["upper"],
                                                       min_area_threshold=min_pellet_area) # Use min_pellet_area as initial filter

    found_normal_pellets = []
    found_power_pellets = []

    for p_obj in all_pellet_colored_objects:
        area = p_obj["area"]
        if min_pellet_area <= area <= max_pellet_area:
            p_obj["label"] = "normal_pellet" # Re-label based on size
            found_normal_pellets.append(p_obj)
        elif min_power_pellet_area <= area <= max_power_pellet_area:
            p_obj["label"] = "power_pellet" # Re-label based on size
            found_power_pellets.append(p_obj)

    return found_normal_pellets, found_power_pellets


if __name__ == "__main__":
    print("Visual Perception Script - Config & Frightened Ghost Test")
    print("----------------------------------------------------------")

    hsv_config = load_hsv_config()
    if hsv_config is None:
        print("FATAL: Could not load HSV config. Exiting test.")
        exit()

    dummy_image_bgr = np.zeros((200, 300, 3), dtype=np.uint8)

    # BGR colors for drawing - these are for placing objects in the dummy image.
    # The detection relies on the HSV ranges in hsv_config.json matching these.
    YELLOW_BGR = (0, 220, 220)    # Approx for Pacman Yellow [20-30, 100-255, 100-255]
    RED_BGR = (0, 0, 200)         # Approx for Ghost Red [0-10/170-180,...]
    PINK_BGR = (180, 100, 200)    # Approx for Ghost Pink [140-170,...]
    FRIGHT_BLUE_BGR = (200, 0, 0) # Approx for Ghost Frightened Blue [100-130,...]
    PELLET_WHITE_BGR = (220, 220, 220) # Approx for Pellet White [0-180, 0-40, 180-255]

    # Draw Pac-Man
    cv2.rectangle(dummy_image_bgr, (20, 20), (40, 40), YELLOW_BGR, -1) # Area ~400

    # Draw Ghosts (some normal, one frightened)
    cv2.rectangle(dummy_image_bgr, (60, 20), (80, 40), RED_BGR, -1)    # Red ghost
    cv2.rectangle(dummy_image_bgr, (100, 20), (120, 40), PINK_BGR, -1)  # Pink ghost
    cv2.rectangle(dummy_image_bgr, (140, 20), (160, 40), FRIGHT_BLUE_BGR, -1) # Frightened Blue ghost

    # Draw Pellets
    cv2.rectangle(dummy_image_bgr, (30, 100), (30+5, 100+5), PELLET_WHITE_BGR, -1) # Normal
    cv2.rectangle(dummy_image_bgr, (30, 120), (30+10, 120+10), PELLET_WHITE_BGR, -1) # Power

    print("\n--- Testing Pac-Man Detection (using config) ---")
    pacman_thresh = hsv_config.get("pacman_yellow")
    pacman_center, pacman_bbox = find_pacman(dummy_image_bgr, pacman_thresh, min_area_threshold=100)
    if pacman_center: print(f"Pac-Man found: Center {pacman_center}, BBox {pacman_bbox}")
    else: print("Pac-Man not found.")

    print("\n--- Testing Ghost Detection (including frightened, using config) ---")
    # Pass only the ghost-related parts of the config to find_all_ghosts
    ghost_defs_for_find = {k:v for k,v in hsv_config.items() if k.startswith("ghost_")}
    found_ghosts = find_all_ghosts(dummy_image_bgr, ghost_defs_for_find, min_area_threshold=100)
    if found_ghosts:
        print(f"Found {len(found_ghosts)} ghost(s):")
        for g_obj in found_ghosts:
            print(f"  - Label: {g_obj['label']}, Center: {g_obj['center']}, Area: {g_obj['area']:.0f}")
    else: print("No ghosts found.")

    print("\n--- Testing Pellet Detection (using config) ---")
    pellet_thresh = hsv_config.get("pellet_white")
    # Area thresholds for dummy pellets
    norm_pellets, pow_pellets = find_all_pellets(dummy_image_bgr, pellet_thresh,
                                               min_pellet_area=15, max_pellet_area=40,
                                               min_power_pellet_area=80, max_power_pellet_area=120)
    print(f"Found {len(norm_pellets)} normal pellet(s):")
    for p in norm_pellets: print(f"  - Label: {p['label']}, Center: {p['center']}, Area: {p['area']:.0f}")
    print(f"Found {len(pow_pellets)} power pellet(s):")
    for pp in pow_pellets: print(f"  - Label: {pp['label']}, Center: {pp['center']}, Area: {pp['area']:.0f}")

    # Basic verification
    expected_pacman = 1
    expected_ghosts = 3 # red, pink, frightened_blue
    expected_normal_pellets = 1
    expected_power_pellets = 1

    if (pacman_center is not None) and \
       len(found_ghosts) == expected_ghosts and \
       len(norm_pellets) == expected_normal_pellets and \
       len(pow_pellets) == expected_power_pellets:
        print("\nTest Summary: PASSED - Correct number of each item type detected.")
    else:
        print(f"\nTest Summary: FAILED - Detection count mismatch. Pacman: {1 if pacman_center else 0}/{expected_pacman}, Ghosts: {len(found_ghosts)}/{expected_ghosts}, NormalP: {len(norm_pellets)}/{expected_normal_pellets}, PowerP: {len(pow_pellets)}/{expected_power_pellets}")

    print("\nVisual Perception script (config & frightened) finished its test block.")
