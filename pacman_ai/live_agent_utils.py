import numpy as np
import math

PAD_VALUE_COORD = -1.0
PAD_VALUE_GHOST_STATE = -1.0 # For ghost state if not detected or padded

def normalize_coords(coords, image_width, image_height):
    if image_width == 0 or image_height == 0:
        return (PAD_VALUE_COORD, PAD_VALUE_COORD)
    return (coords[0] / image_width, coords[1] / image_height)

def get_visual_state_vector(pacman_data, ghost_data_list, normal_pellet_list, power_pellet_list,
                            image_dims, max_ghosts=4, max_normal_pellets=10, max_power_pellets=2):
    image_width, image_height = image_dims
    state_features = []

    pacman_center_abs = None
    if pacman_data and "center" in pacman_data:
        pacman_center_abs = pacman_data["center"]
        norm_px, norm_py = normalize_coords(pacman_center_abs, image_width, image_height)
        state_features.extend([norm_px, norm_py])
    else:
        state_features.extend([PAD_VALUE_COORD, PAD_VALUE_COORD])

    def sort_by_distance(item_list, reference_point):
        if reference_point is None or not item_list:
            return item_list
        return sorted(item_list, key=lambda item: math.sqrt(
            (item["center"][0] - reference_point[0])**2 + (item["center"][1] - reference_point[1])**2
        ) if "center" in item else float('inf'))

    sorted_ghosts = sort_by_distance(ghost_data_list, pacman_center_abs)
    for i in range(max_ghosts):
        if i < len(sorted_ghosts) and "center" in sorted_ghosts[i]:
            g_center = sorted_ghosts[i]["center"]
            g_label = sorted_ghosts[i].get("label", "") # e.g., "red", "frightened_blue"

            # Determine ghost state code
            ghost_state_code = 0.0 # Default to chase/normal
            if "frightened" in g_label: # Covers "frightened_blue", etc.
                ghost_state_code = 1.0
            # Future: Add code for 'eaten' if vision can detect that, or if inferred.
            # For now, assuming 'eaten' ghosts are not passed in ghost_data_list from perception,
            # or they are filtered out before this function. If they can appear, a third state code is needed.

            if pacman_center_abs:
                rel_gx = (g_center[0] - pacman_center_abs[0])
                rel_gy = (g_center[1] - pacman_center_abs[1])
                norm_gx, norm_gy = normalize_coords((rel_gx, rel_gy), image_width, image_height)
            else:
                norm_gx, norm_gy = normalize_coords(g_center, image_width, image_height)

            state_features.extend([norm_gx, norm_gy, ghost_state_code])
        else:
            state_features.extend([PAD_VALUE_COORD, PAD_VALUE_COORD, PAD_VALUE_GHOST_STATE]) # x, y, state

    sorted_normal_pellets = sort_by_distance(normal_pellet_list, pacman_center_abs)
    for i in range(max_normal_pellets):
        if i < len(sorted_normal_pellets) and "center" in sorted_normal_pellets[i]:
            p_center = sorted_normal_pellets[i]["center"]
            if pacman_center_abs:
                rel_px = (p_center[0] - pacman_center_abs[0])
                rel_py = (p_center[1] - pacman_center_abs[1])
                norm_px, norm_py = normalize_coords((rel_px, rel_py), image_width, image_height)
            else:
                norm_px, norm_py = normalize_coords(p_center, image_width, image_height)
            state_features.extend([norm_px, norm_py])
        else:
            state_features.extend([PAD_VALUE_COORD, PAD_VALUE_COORD])

    sorted_power_pellets = sort_by_distance(power_pellet_list, pacman_center_abs)
    for i in range(max_power_pellets):
        if i < len(sorted_power_pellets) and "center" in sorted_power_pellets[i]:
            pp_center = sorted_power_pellets[i]["center"]
            if pacman_center_abs:
                rel_ppx = (pp_center[0] - pacman_center_abs[0])
                rel_ppy = (pp_center[1] - pacman_center_abs[1])
                norm_ppx, norm_ppy = normalize_coords((rel_ppx, rel_ppy), image_width, image_height)
            else:
                norm_ppx, norm_ppy = normalize_coords(pp_center, image_width, image_height)
            state_features.extend([norm_ppx, norm_ppy])
        else:
            state_features.extend([PAD_VALUE_COORD, PAD_VALUE_COORD])

    return np.array(state_features).flatten()

def calculate_visual_state_size(max_ghosts=4, max_normal_pellets=10, max_power_pellets=2,
                                features_per_pacman=2,
                                features_per_ghost=3, # Now x, y, state_code
                                features_per_normal_pellet=2,
                                features_per_power_pellet=2):
    size = features_per_pacman + \
           (max_ghosts * features_per_ghost) + \
           (max_normal_pellets * features_per_normal_pellet) + \
           (max_power_pellets * features_per_power_pellet)
    return size

if __name__ == "__main__":
    print("Live Agent Utils - Test Block (with Ghost State)")
    print("------------------------------------------------")

    img_w, img_h = 640, 480
    test_image_dims = (img_w, img_h)

    # Default max values for standard size calculation
    default_max_ghosts = 4
    default_max_normal_pellets = 10
    default_max_power_pellets = 2

    # Test case 1: All data present, including a frightened ghost
    dummy_pacman = {"center": (320, 240), "bbox": (310,230,20,20)}
    dummy_ghosts = [
        {"label": "red", "center": (300, 200)},
        {"label": "frightened_blue", "center": (350, 220)} # This ghost is frightened
    ]
    dummy_pellets = [{"center": (100,100)}, {"center": (150,150)}]
    dummy_power_pellets = [{"center": (50,50)}]

    print("\n--- Test Case 1: All data present (incl. frightened ghost) ---")
    state_vec1 = get_visual_state_vector(
        dummy_pacman, dummy_ghosts, dummy_pellets, dummy_power_pellets,
        test_image_dims,
        max_ghosts=default_max_ghosts,
        max_normal_pellets=default_max_normal_pellets,
        max_power_pellets=default_max_power_pellets
    )
    calculated_size1 = calculate_visual_state_size(
        max_ghosts=default_max_ghosts,
        max_normal_pellets=default_max_normal_pellets,
        max_power_pellets=default_max_power_pellets
    )
    print(f"Generated state vector (sample): {state_vec1[:10]}...") # Show more features due to ghost state
    print(f"Length of state vector: {len(state_vec1)}")
    print(f"Calculated state size: {calculated_size1}")
    assert len(state_vec1) == calculated_size1, "Test Case 1 FAILED: Length mismatch"
    # Pacman (2) + G1(3) + G2(3) + G3(pad 3) + G4(pad 3) ...
    # G1 (red) state code should be 0.0. G2 (frightened_blue) state code should be 1.0.
    # G1 starts at index 2. Its state code is at index 2+2=4.
    # G2 starts at index 2+3=5. Its state code is at index 5+2=7.
    # Sorted order: "frightened_blue" (dist ~36) then "red" (dist ~44.7)
    print(f"Closest ghost (frightened_blue) features: {state_vec1[2:5]}")
    print(f"Second ghost (red) features: {state_vec1[5:8]}")
    assert state_vec1[4] == 1.0, "Test Case 1 FAILED: Closest ghost (frightened_blue) state code should be 1.0"
    assert state_vec1[7] == 0.0, "Test Case 1 FAILED: Second ghost (red) state code should be 0.0"
    print("Test Case 1 PASSED")

    # Test case 2: Fewer ghosts than max_ghosts, no power pellets
    dummy_ghosts_less = [{"label": "pink", "center": (280, 180)}] # One normal ghost
    dummy_power_pellets_none = []

    # Use smaller max values for this specific test to make checking padding easier
    current_max_ghosts = 2
    current_max_normal_pellets = 1
    current_max_power_pellets = 0

    print("\n--- Test Case 2: Fewer entities and specific max settings ---")
    state_vec2 = get_visual_state_vector(
        dummy_pacman, dummy_ghosts_less, dummy_pellets, dummy_power_pellets_none,
        test_image_dims,
        max_ghosts=current_max_ghosts,
        max_normal_pellets=current_max_normal_pellets,
        max_power_pellets=current_max_power_pellets
    )
    calculated_size2 = calculate_visual_state_size(
        max_ghosts=current_max_ghosts,
        max_normal_pellets=current_max_normal_pellets,
        max_power_pellets=current_max_power_pellets
    )
    print(f"Generated state vector (sample): {state_vec2[:10]}...")
    print(f"Length of state vector: {len(state_vec2)}")
    print(f"Calculated state size for this config: {calculated_size2}")
    assert len(state_vec2) == calculated_size2, "Test Case 2 FAILED: Length mismatch"
    # Pacman(2) + Ghost1(3) + Ghost2(pad 3) + Pellet1(2)
    # Ghost1 state (index 2+2=4) should be 0.0
    # Ghost2 (padding) state (index 2+3+2=7) should be PAD_VALUE_GHOST_STATE
    print(f"Ghost 1 features: {state_vec2[2:5]}")
    print(f"Ghost 2 (padding) features: {state_vec2[5:8]}")
    assert state_vec2[4] == 0.0, "Test Case 2 FAILED: Ghost 1 state incorrect"
    assert np.all(state_vec2[5:8] == PAD_VALUE_COORD) or \
           (state_vec2[5]==PAD_VALUE_COORD and state_vec2[6]==PAD_VALUE_COORD and state_vec2[7]==PAD_VALUE_GHOST_STATE), \
           "Test Case 2 FAILED: Ghost 2 padding incorrect"
    print("Test Case 2 PASSED")

    print("\nLive Agent Utils script (with ghost state) finished its test block.")
