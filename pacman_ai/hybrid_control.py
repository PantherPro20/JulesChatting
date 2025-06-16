# pacman_ai/hybrid_control.py
import pyautogui
import mss
import mss.tools
import time
# import cv2 # We'll use OpenCV later for actual image processing
# import numpy as np # For OpenCV

# --- PyAutoGUI Configuration (Optional but Recommended) ---
# pyautogui.FAILSAFE = True # Raise exception if mouse moves to a corner
pyautogui.PAUSE = 0.05    # Small pause after each pyautogui call

def capture_game_screen(monitor_number=1, top_offset=0, left_offset=0, width=800, height=600):
    """
    Captures a portion of the screen.
    Adjust monitor_number, top_offset, left_offset, width, height as needed
    to capture the Pac-Man game window.
    This will require manual calibration by the user initially.
    """
    try:
        with mss.mss() as sct:
            # Define the capture area
            # User will need to figure out these coordinates.
            game_area = {"top": top_offset, "left": left_offset, "width": width, "height": height, "mon": monitor_number}

            # Check if the monitor number is valid
            if monitor_number >= len(sct.monitors):
                print(f"Error: Monitor {monitor_number} not found. Available monitors: {len(sct.monitors) -1 } (0 is all, 1 is primary, etc.)")
                # Fallback to primary monitor if specified monitor is out of range (excluding monitor 0)
                if monitor_number != 0 and len(sct.monitors) > 1:
                    print("Falling back to primary monitor (monitor 1).")
                    game_area["mon"] = 1
                elif len(sct.monitors) == 1 and monitor_number !=0 : # Only "all screens" monitor available
                     print("Falling back to 'all screens' monitor (monitor 0).")
                     game_area["mon"] = 0
                elif monitor_number == 0 and len(sct.monitors) == 1: # monitor 0 is the only one
                    pass # game_area["mon"] is already 0
                else: # No fallback possible or monitor 0 requested with multiple available
                    if game_area["mon"] == 0 and len(sct.monitors) > 1: # All monitors selected
                         print(f"Capturing from all monitors combined (monitor 0). Area is relative to virtual screen.")
                    else:
                         print(f"Cannot capture from monitor {game_area['mon']}. Please check monitor setup.")
                         return None

            print(f"Attempting to capture screen area: {game_area}")
            sct_img = sct.grab(game_area)

            print(f"Screen captured. Size: {sct_img.width}x{sct_img.height}")
            # output_filename = f"screenshot_{int(time.time())}.png"
            # mss.tools.to_png(sct_img.rgb, sct_img.size, output=output_filename)
            # print(f"Test screenshot saved to {output_filename}")

            return sct_img # In future, this would be a NumPy array for OpenCV

    except Exception as e:
        print(f"Error during screen capture: {e}")
        return None

def send_action_to_game(action: str):
    """
    Sends a keyboard command using pyautogui.
    'action' should be one of 'up', 'down', 'left', 'right', 'space'.
    Make sure the Pac-Man game window is ACTIVE and IN FOCUS.
    """
    valid_actions = ['up', 'down', 'left', 'right', 'space']
    if action not in valid_actions:
        print(f"Invalid action: {action}. Must be one of {valid_actions}")
        return

    try:
        print(f"Sending action: '{action}'")
        pyautogui.press(action)
        # print(f"Action '{action}' sent.") # Reduce verbosity for rapid actions
    except Exception as e:
        # PyAutoGUI can fail if it can't connect to a display server,
        # which is common in headless CI/CD environments.
        print(f"Error sending action '{action}': {e}")
        print("Ensure a display server (like Xvfb) is available if running in a headless environment.")


if __name__ == "__main__":
    print("Hybrid Control Script - Initial Test")
    print("------------------------------------")
    print("This script will attempt to capture a portion of the screen")
    print("and provides a function to send keyboard commands using PyAutoGUI.")
    print("IMPORTANT: For PyAutoGUI to work, the TARGET WINDOW (Pac-Man game)")
    print("MUST BE ACTIVE AND IN FOCUS when send_action_to_game is called.")
    print("The screen capture coordinates (top, left, width, height) in this test")
    print("are placeholders and will likely need adjustment for your specific screen setup.")
    print("PyAutoGUI may also require a running display server (e.g., Xvfb on Linux) if in a headless environment.")
    print("------------------------------------")

    # Example: Define where the game window is expected to be.
    GAME_WINDOW_TOP = 100
    GAME_WINDOW_LEFT = 100
    GAME_WINDOW_WIDTH = 600
    GAME_WINDOW_HEIGHT = 400
    TARGET_MONITOR = 1 # Primary monitor

    print(f"Taking a test screen capture in 3 seconds (monitor {TARGET_MONITOR}, area: top={GAME_WINDOW_TOP}, left={GAME_WINDOW_LEFT}, w={GAME_WINDOW_WIDTH}, h={GAME_WINDOW_HEIGHT})...")
    time.sleep(3)

    captured_image = capture_game_screen(
        monitor_number=TARGET_MONITOR,
        top_offset=GAME_WINDOW_TOP,
        left_offset=GAME_WINDOW_LEFT,
        width=GAME_WINDOW_WIDTH,
        height=GAME_WINDOW_HEIGHT
    )

    if captured_image:
        print("Screen capture successful (or attempted without error).")
    else:
        print("Screen capture failed or returned None.")

    print("\nTesting PyAutoGUI key presses (conceptual)...")
    print("Actual sending is commented out to prevent unintended input during automated tests.")
    # print("To actually test, you would run this script and quickly switch focus")
    # print("to an application like a text editor within 5 seconds.")
    # print("Test key presses will be sent in 5 seconds...")
    # time.sleep(5)
    # print("Sending 'space'...")
    # send_action_to_game('space')
    # time.sleep(1)
    # print("Sending 'up'...")
    # send_action_to_game('up')

    print("\nPyAutoGUI test key presses would have been conceptually sent.")
    print("Script finished.")
