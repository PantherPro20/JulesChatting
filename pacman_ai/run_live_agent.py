import time
import numpy as np
import cv2 # For image conversion

# Project-specific imports
from pacman_ai.hybrid_control import capture_game_screen, send_action_to_game
from pacman_ai.visual_perception import (
    load_hsv_config, # New: For loading HSV thresholds
    find_pacman,      # Renamed (was find_pacman_by_color)
    find_all_ghosts,  # Renamed (was find_ghosts)
    find_all_pellets  # Renamed (was find_pellets)
)
from pacman_ai.live_agent_utils import (
    get_visual_state_vector,
    calculate_visual_state_size # Updated to account for new ghost state feature
)
from pacman_ai.rl_agent import RLAgent # The DQN Agent

# --- Configuration Constants ---
IMAGE_CAPTURE_PARAMS = {
    "top_offset": 100, "left_offset": 100, "width": 600, "height": 480, "monitor_number": 1
}
IMAGE_DIMS = (IMAGE_CAPTURE_PARAMS["width"], IMAGE_CAPTURE_PARAMS["height"])

# State vector configuration (should match defaults in live_agent_utils or be passed if different)
MAX_GHOSTS_IN_STATE = 4
MAX_NORMAL_PELLETS_IN_STATE = 10
MAX_POWER_PELLETS_IN_STATE = 2
# Note: features_per_ghost is now 3 (x, y, state_code) in live_agent_utils.calculate_visual_state_size default

ACTION_MAP = {0: 'up', 1: 'down', 2: 'left', 3: 'right'}
ACTION_SIZE = len(ACTION_MAP)

LOOP_DELAY = 0.1
MAX_GAME_STEPS = 1000

# Visual perception parameters (area thresholds might need tuning)
PACMAN_MIN_AREA = 100
GHOST_MIN_AREA = 100
PELLET_MIN_NORMAL_AREA = 5
PELLET_MAX_NORMAL_AREA = 50
PELLET_MIN_POWER_AREA = 51
PELLET_MAX_POWER_AREA = 150


if __name__ == "__main__":
    print("Starting Live Pac-Man RL Agent (with external HSV config & ghost states)...")
    print("-------------------------------------------------------------------------")
    print("IMPORTANT: Ensure game window is visible, positioned, and IN FOCUS.")
    print(f"Image capture configured for: Monitor {IMAGE_CAPTURE_PARAMS['monitor_number']}, "
          f"Area: {IMAGE_CAPTURE_PARAMS['width']}x{IMAGE_CAPTURE_PARAMS['height']} "
          f"at (top={IMAGE_CAPTURE_PARAMS['top_offset']}, left={IMAGE_CAPTURE_PARAMS['left_offset']})")

    # Load HSV configuration
    hsv_config = load_hsv_config() # Uses default path "pacman_ai/hsv_config.json"
    if hsv_config is None:
        print("FATAL: Could not load HSV config. Please ensure 'pacman_ai/hsv_config.json' exists and is valid.")
        exit()

    # Extract specific thresholds for convenience (optional, could pass hsv_config parts directly)
    pacman_hsv_thresh = hsv_config.get("pacman_yellow")
    ghost_defs_for_find = {k:v for k,v in hsv_config.items() if k.startswith("ghost_")}
    pellet_hsv_thresh = hsv_config.get("pellet_white")

    if not all([pacman_hsv_thresh, ghost_defs_for_find, pellet_hsv_thresh]):
        print("FATAL: Essential color definitions (pacman_yellow, ghost_*, pellet_white) not found in HSV config.")
        exit()

    print("Giving you 5 seconds to focus the Pac-Man game window...")
    time.sleep(5)

    # Calculate state size (now includes ghost state feature)
    state_size = calculate_visual_state_size(
        max_ghosts=MAX_GHOSTS_IN_STATE,
        max_normal_pellets=MAX_NORMAL_PELLETS_IN_STATE,
        max_power_pellets=MAX_POWER_PELLETS_IN_STATE
        # features_per_ghost is 3 by default in the updated function
    )
    print(f"Calculated state size for RL Agent: {state_size}")

    agent = RLAgent(state_size=state_size, action_size=ACTION_SIZE)
    print("Note: Agent is using initial (untrained) weights.")
    agent.epsilon = 0.0 # Deterministic actions

    try:
        for step_num in range(MAX_GAME_STEPS):
            print(f"\n--- Step {step_num + 1} ---")
            sct_img = capture_game_screen(**IMAGE_CAPTURE_PARAMS)
            if sct_img is None:
                print("Failed to capture screen. Skipping this step.")
                time.sleep(LOOP_DELAY)
                continue

            img_np = np.array(sct_img)
            img_cv = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)

            pacman_center, pacman_bbox = find_pacman(img_cv, pacman_hsv_thresh, PACMAN_MIN_AREA)
            pacman_info_dict = {"center": pacman_center, "bbox": pacman_bbox} if pacman_center else None

            # find_all_ghosts returns list of dicts, each dict now has a 'label' (e.g., "red", "frightened_blue")
            ghosts_list = find_all_ghosts(img_cv, ghost_defs_for_find, GHOST_MIN_AREA)

            normal_pellets_list, power_pellets_list = find_all_pellets(
                img_cv, pellet_hsv_thresh,
                min_pellet_area=PELLET_MIN_NORMAL_AREA, max_pellet_area=PELLET_MAX_NORMAL_AREA,
                min_power_pellet_area=PELLET_MIN_POWER_AREA, max_power_pellet_area=PELLET_MAX_POWER_AREA
            )

            if pacman_info_dict: print(f"Pac-Man: {pacman_info_dict['center']}")
            else: print("Pac-Man: Not detected")
            print(f"Ghosts: {len(ghosts_list)} detected")
            # for g in ghosts_list: print(f"  - {g['label']} at {g['center']}") # label now includes state
            print(f"Normal Pellets: {len(normal_pellets_list)} detected")
            print(f"Power Pellets: {len(power_pellets_list)} detected")

            current_state_vector = get_visual_state_vector(
                pacman_info_dict, ghosts_list, normal_pellets_list, power_pellets_list,
                IMAGE_DIMS,
                max_ghosts=MAX_GHOSTS_IN_STATE,
                max_normal_pellets=MAX_NORMAL_PELLETS_IN_STATE,
                max_power_pellets=MAX_POWER_PELLETS_IN_STATE
            )

            action_index = agent.act(current_state_vector)
            game_action_str = ACTION_MAP.get(action_index, None)

            print(f"State (first {2 + MAX_GHOSTS_IN_STATE*3} features): {current_state_vector[:(2 + MAX_GHOSTS_IN_STATE*3)]}") # Pacman + Ghosts features
            print(f"Agent chose action index: {action_index}, mapped to: {game_action_str}")

            if game_action_str:
                send_action_to_game(game_action_str)
            else:
                print(f"Warning: Invalid action index {action_index} from agent.")

            time.sleep(LOOP_DELAY)

    except KeyboardInterrupt:
        print("\nUser interrupted the game. Exiting.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("Live agent script finished.")
