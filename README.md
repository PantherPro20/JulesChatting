# AI Pac-Man using Reinforcement Learning

## Project Overview
This project aims to develop an Artificial Intelligence agent that can learn to play Pac-Man. It includes:
1.  A game simulation environment built in Python.
2.  A rule-based AI (`ai_logic.py`) for basic gameplay (now considered legacy).
3.  A Reinforcement Learning (RL) agent using a Deep Q-Network (DQN) trained on the simulated environment (`train_rl.py`).
4.  Experimental support for a "hybrid visual" agent (`run_live_agent.py`) that uses screen capture and visual perception to play the Google Doodle Pac-Man game, controlled by a (potentially RL-trained) model.

## How it Works

### 1. Simulated Environment & RL Training
The primary AI agent learns through trial and error in a simulated game environment.
- **Reinforcement Learning (DQN):** The agent uses a Deep Q-Network to learn the optimal action to take in any given game state. It learns by receiving rewards or penalties for its actions (e.g., +10 for eating a pellet, -500 for being caught by a ghost).
- **Key Components for Simulated RL:**
  - **`pacman_ai/game_state.py`**: Defines the `GameState` class, representing all aspects of the game (maze, Pac-Man, ghosts, pellets) for the simulation.
  - **`pacman_ai/rl_agent.py`**: Contains the `RLAgent` class, which implements the DQN algorithm. This includes the neural network model (built with TensorFlow/Keras), experience replay memory, and the logic for action selection (epsilon-greedy) and learning.
  - **`pacman_ai/train_rl.py`**: The main script for training the RL agent against the simulated environment. It manages the training loop, interaction between the agent and the game simulation, state vectorization (from `GameState`), and reward processing. The `step()` function within this script advances the game simulation one timestep.
  - **`pacman_ai/simulation.py`**: Provides the core Pac-Man game mechanics for the simulation, entity definitions (PacMan, Ghost, Pellet), and reward constants used by `train_rl.py`.

### 2. Hybrid Visual Agent (Experimental)
This approach allows an agent to play the web-based Google Doodle Pac-Man by "seeing" the screen and sending keyboard commands.
- **Visual Perception:** Uses OpenCV to process screen captures, identify game elements (Pac-Man, ghosts, pellets) by color, and determine their positions. HSV color thresholds are defined in `hsv_config.json` and require user calibration.
- **Hybrid Control:** Uses `mss` for screen capture and `pyautogui` for sending keyboard commands.
- **Key Components for Hybrid Visual Agent:**
  - **`pacman_ai/visual_perception.py`**: Contains functions to load images, convert to HSV, apply color masks, and find game objects (Pac-Man, ghosts by color including frightened state, normal/power pellets by color and size). Loads HSV thresholds from `hsv_config.json`.
  - **`pacman_ai/hybrid_control.py`**: Provides functions to capture specified screen regions and send keyboard actions ('up', 'down', 'left', 'right').
  - **`pacman_ai/live_agent_utils.py`**: Contains functions (`get_visual_state_vector`, `calculate_visual_state_size`) to convert the raw visual detection data into a fixed-size numerical state vector suitable for an RL agent. This includes normalizing coordinates and padding lists of detected objects.
  - **`pacman_ai/run_live_agent.py`**: Orchestrates the live visual agent. It captures the screen, uses visual perception to identify game elements, creates a state vector, gets an action from an `RLAgent` (which would ideally be trained on this visual state), and sends the action to the game window.
  - **`pacman_ai/hsv_config.json`**: Stores HSV color thresholds for visual detection, requiring user calibration.

## Directory Structure
```
.
├── pacman_ai/
│   ├── __init__.py
│   ├── game_state.py         # Core game state for simulation
│   ├── ghost.py              # Ghost class for simulation
│   ├── maze.py               # Maze class for simulation
│   ├── pacman.py             # PacMan class for simulation
│   ├── pellet.py             # Pellet classes for simulation
│   ├── pathfinding.py        # A* pathfinding (used by simulated ghosts/rule-based AI)
│   ├── ai_logic.py           # Rule-based AI (legacy)
│   ├── simulation.py         # Simulation engine, reward constants for RL training
│   ├── rl_agent.py           # DQN Reinforcement Learning Agent (for simulation & visual)
│   ├── train_rl.py           # Script to train the RL Agent using the simulation
│   ├── visual_perception.py  # Image processing for detecting game elements
│   ├── hybrid_control.py     # Screen capture and keyboard control
│   ├── live_agent_utils.py   # Utilities for visual state vector creation
│   ├── run_live_agent.py     # Main script for running the live visual agent
│   ├── hsv_config.json       # HSV color thresholds for visual perception
│   └── tests/                # Unit tests
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Setup and Installation (Windows 11 Example)

1.  **Install Python:**
    *   **Recommended Python Versions:** For compatibility with TensorFlow (a core dependency), it is highly recommended to use **Python 3.9, 3.10, 3.11, or 3.12**. As of late 2024/early 2025, TensorFlow does not yet have stable releases for Python 3.13 or newer. Using Python 3.13+ will likely lead to installation errors for TensorFlow.
    *   You can download specific Python versions from [python.org](https://www.python.org/downloads/windows/).
    *   During installation, make sure to check the box "Add Python to PATH".
    *   If you currently have a newer, incompatible version of Python (like 3.13+), you will need to uninstall it and install one of the recommended versions, or use a Python version manager (e.g., `pyenv-win`) to manage multiple Python installations.

2.  **Get the Code:**
    *   **Git (Recommended):**
        *   Install Git from [git-scm.com](https://git-scm.com/download/win).
        *   Clone the repository: `git clone <your_repository_url_here>`
        *   `cd <repository_directory_name>`
    *   **Manual Download:** Download and extract ZIP.

3.  **Create a Virtual Environment (Recommended):**
    *   In the project root: `python -m venv venv`
    *   Activate: `.\venv\Scripts\activate` (You should see `(venv)` in your prompt).

4.  **Install Dependencies:**
    *   With venv activated: `pip install -r requirements.txt`
    *   **Note for Hybrid Visual Agent:** `pyautogui` might have additional system dependencies on Linux for interacting with the display server (e.g., `sudo apt-get install scrot python3-tk python3-dev` and potentially Xvfb for headless virtual display). `mss` also relies on X server capabilities.

## How to Run

### 1. Training the RL Agent (Simulated Environment)
   *   Ensure virtual environment is activated.
   *   Navigate to project root.
   *   Run: `python -m pacman_ai.train_rl`
   *   **Training Process:** Console output shows episode progress, rewards, epsilon, and steps. Model weights (e.g., `pacman_rl_agent_final_ep<N>.weights.h5`) are saved in the project root.
   *   Modify `EPISODES`, etc., in `pacman_ai/train_rl.py` to control training.

### 2. Running the Live Visual Agent (`run_live_agent.py`)

This mode allows the agent to play the Google Doodle Pac-Man game by watching the screen and sending keyboard commands.

*   **Crucial Prerequisites:**
    *   **Graphical Environment:** Must be run in a graphical desktop environment (not a headless server without Xvfb or similar).
    *   **Dependencies:** Python and all packages from `requirements.txt` installed.
    *   **Game Ready:** The Google Doodle Pac-Man game (`https://www.google.com/logos/2010/pacman10-i.html`) must be open in a browser window.
    *   **Window Focus:** The Pac-Man game window **must be the active, focused window** on your desktop when `run_live_agent.py` is active. This is critical for `pyautogui` to send keyboard commands to the correct application.

*   **Calibration Steps (User Responsibility - CRITICAL for visual agent):**

    1.  **Screen Capture Area (`IMAGE_CAPTURE_PARAMS` in `run_live_agent.py`):**
        *   You **must** adjust the `IMAGE_CAPTURE_PARAMS` dictionary in `pacman_ai/run_live_agent.py`.
        *   `top_offset`, `left_offset`: Pixels from the top-left corner of your primary screen to the top-left corner of the Pac-Man game area (canvas).
        *   `width`, `height`: The pixel dimensions of the Pac-Man game area itself.
        *   `monitor_number`: Typically 1 for the primary monitor. Use tools like `mss.mss().monitors` in a Python console to list monitors if needed.
        *   **How to find coordinates:** Use your OS's screenshot tool (e.g., Snipping Tool on Windows with a ruler mode, or GIMP/Photoshop rulers) or a dedicated screen coordinate utility to measure these pixel values accurately.

    2.  **HSV Color Threshold Tuning (`pacman_ai/hsv_config.json`):**
        *   The accuracy of the visual perception heavily depends on the HSV color thresholds defined in `pacman_ai/hsv_config.json`. The provided values are **estimates and will likely need significant tuning** for your specific screen, browser, and lighting conditions.
        *   **Methodology for Tuning:**
            1.  Open the Pac-Man game.
            2.  Take a screenshot of the game.
            3.  Open the screenshot in an image editor that has a color picker tool capable of displaying HSV values (e.g., GIMP, Photoshop, online color pickers).
            4.  For each game element (Pac-Man yellow, each distinct ghost color, frightened blue ghosts, pellets), use the color picker to sample HSV values from multiple points on that element. Note the range of H, S, and V values.
            5.  Update the `lower` and `upper` lists in `hsv_config.json` for each element. Remember OpenCV's Hue range is typically 0-179. Red might require two ranges if its hue values wrap around 0/180.
            6.  You can test your HSV thresholds locally by adapting the `if __name__ == "__main__":` block in `pacman_ai/visual_perception.py`. Load your sample screenshot, call the detection functions with your new HSV values, and use `cv2.imshow()` to display the original image with detected contours/masks overlaid. This iterative process is key to good detection.

*   **RL Agent State for Visual Mode:**
    *   The `RLAgent` in `run_live_agent.py` is initialized with a `state_size` derived from `calculate_visual_state_size` in `live_agent_utils.py`. This state vector is based purely on the detected visual elements.
    *   By default, the script initializes a new, untrained agent for this visual state.
    *   The line `agent.load("path_to_visual_model.weights.h5")` in `run_live_agent.py` is commented out. To use a trained model, you would uncomment this and provide the path to weights file that was trained specifically on this visual state representation.

*   **Running the Script:**
    1.  Ensure prerequisites and calibration are done.
    2.  Activate your virtual environment.
    3.  Navigate to the project root.
    4.  Run: `python -m pacman_ai.run_live_agent`
    5.  Quickly switch focus to the Pac-Man game window before the 5-second countdown in the script ends.

### 3. Training the Live Visual Agent (Advanced - Conceptual)

The current `run_live_agent.py` is set up for "inference" (acting with `epsilon=0.0`) and does not implement a live training loop using visual input. Training an agent directly on live visual input is a more complex task.

*   **Challenges for Live Training:**
    *   **Reward Engineering:** Deriving a reward signal directly from screen images is non-trivial. It would require robust visual logic or OCR to detect score changes, Pac-Man dying, pellets being eaten, level completion, etc. This is a significant development step.
    *   **Game State Consistency:** Unlike a simulation, the live game state is only observable through potentially noisy visual perception.
    *   **Speed and Stability:** The perception-action loop must be fast enough to play the game effectively. Live game interaction can be less stable than a simulation.

*   **Conceptual Steps for Implementing Live Training (Future Development):**
    1.  Modify the main loop in `run_live_agent.py`.
    2.  After `send_action_to_game()`, add a short delay to allow the game to react.
    3.  Capture the `next_screen_image`.
    4.  Implement robust visual logic to determine the `reward` for the action taken (e.g., did score increase? Did Pac-Man get caught? Was a pellet eaten?) and the `done` status (game over or level cleared).
    5.  Generate the `next_state_vector` from this new visual information.
    6.  Call `agent.remember(current_state_vector, action_index, reward, next_state_vector, done)`.
    7.  Call `agent.replay(BATCH_SIZE)` periodically to train the model.
    8.  Set `agent.epsilon` to a value greater than `epsilon_min` to allow for exploration during training.

## Development Notes
- **Simulated Training:** State representation is in `train_rl.py` (`get_state_vector`), rewards from `simulation.py`.
- **Visual Agent:** State representation from visual input is in `live_agent_utils.py` (`get_visual_state_vector`). HSV Color tuning is critical (`hsv_config.json`). Screen capture coordinates in `run_live_agent.py` also need calibration.
- The DQN agent's neural network architecture and hyperparameters are in `pacman_ai/rl_agent.py`.

---
*(Replace `<your_repository_url_here>` and `<repository_directory_name>` with actual values if applicable when this is pushed to a remote repository.)*
