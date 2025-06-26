# AI Pac-Man using Reinforcement Learning

## Project Overview
This project aims to develop an Artificial Intelligence agent that can learn to play Pac-Man. It includes:
1.  A game simulation environment built in Python for training an RL agent.
2.  Exploratory implementations for a "live visual" agent that can interact with a web browser version of Pac-Man. Two approaches for browser interaction have been developed:
    *   A Hybrid approach using OS-level screen capture and keyboard control.
    *   A Playwright-based approach using browser automation APIs.

## How it Works

### 1. Simulated Environment & RL Training
The primary AI agent learns through trial and error in a simulated game environment.
- **Reinforcement Learning (DQN):** The agent uses a Deep Q-Network to learn the optimal action to take in any given game state. It learns by receiving rewards or penalties for its actions (e.g., +10 for eating a pellet, -500 for being caught by a ghost).
- **Key Components for Simulated RL:**
  - **`pacman_ai/game_state.py`**: Defines the `GameState` class for the simulation.
  - **`pacman_ai/rl_agent.py`**: Contains the `RLAgent` class (DQN algorithm).
  - **`pacman_ai/train_rl.py`**: Main script for training the RL agent against the simulation.
  - **`pacman_ai/simulation.py`**: Provides game mechanics and reward constants for simulated training.
  - Other modules like `maze.py`, `pacman.py`, `ghost.py`, `pellet.py`, `pathfinding.py` support the simulation.

### 2. Browser Interaction Approaches for Live Visual Agent

This project explores two methods for enabling an AI to play a web-based version of Pac-Man (e.g., the Google Doodle) by observing the screen and sending commands. The visual perception (`visual_perception.py`) and state generation (`live_agent_utils.py`) modules are designed to be potentially usable by either control method.

  **a) Hybrid Approach (PyAutoGUI + MSS + OpenCV):**
  - **Mechanism:** Operates at the OS level. It captures screen regions using `mss`, processes these images with `OpenCV` (via `visual_perception.py`) to understand the game state, and sends keyboard commands using `pyautogui`.
  - **Key Components:**
    - **`pacman_ai/hybrid_control.py`**: Functions for screen capture and sending keyboard actions.
    - **`pacman_ai/run_live_agent.py`**: Orchestrates this hybrid approach, integrating screen capture, visual perception, state vector creation (from `live_agent_utils.py`), RL agent decisions, and action sending.

  **b) Playwright Approach:**
  - **Mechanism:** Uses the Playwright library to control a web browser programmatically. It can navigate pages, interact with page elements (like a game canvas), and take screenshots directly from the browser's rendering engine.
  - **Key Components:**
    - **`pacman_ai/playwright_control.py`**: Contains functions to launch a browser with Playwright, navigate to the game URL, and includes placeholders for interacting with the game canvas.

## Current Status of Browser Interaction Approaches

*   **Hybrid Approach (PyAutoGUI - `run_live_agent.py`):**
    *   The script `run_live_agent.py` implements a full perception-action loop using this method.
    *   **Requires a graphical desktop environment** (cannot run headless without a virtual framebuffer like Xvfb).
    *   **Crucially depends on user calibration:**
        1.  **Screen Coordinates (`IMAGE_CAPTURE_PARAMS` in `run_live_agent.py`):** User must precisely define the game window's top-left corner (offsets) and its width/height for screen capture.
        2.  **HSV Color Thresholds (`hsv_config.json`):** User must tune these values for Pac-Man, ghosts (normal and frightened), and pellets for their specific display and game appearance.
    *   The `RLAgent` in this script is currently initialized with untrained weights for the visual state.

*   **Playwright Approach (`playwright_control.py`):**
    *   The Playwright Python package and its browser binaries have been successfully installed in the development environment (though this can be time-consuming).
    *   **Host System Dependencies:** Successful execution of Playwright browsers heavily depends on the host system having many GUI/graphics-related shared libraries (e.g., GTK, X11 libraries on Linux). Missing dependencies (often warned during `playwright install`) can prevent browsers from launching.
    *   The `pacman_ai/playwright_control.py` script provides basic functionality to launch a browser and navigate to the Pac-Man URL. It includes conceptual logic for finding the game canvas.
    *   **Not yet integrated** into a full perception-action loop with the `RLAgent` or the visual perception modules for screenshotting and state processing. This would be a next step for this approach. The AI is also untrained for this path.

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
│   ├── pathfinding.py        # A* pathfinding
│   ├── ai_logic.py           # Rule-based AI (legacy)
│   ├── simulation.py         # Simulation engine, RL reward constants for training
│   ├── rl_agent.py           # DQN Reinforcement Learning Agent
│   ├── train_rl.py           # Script to train the RL Agent using the simulation
│   ├── visual_perception.py  # Image processing for detecting game elements
│   ├── hybrid_control.py     # Screen capture (MSS) & keyboard control (PyAutoGUI)
│   ├── playwright_control.py # Browser control using Playwright (experimental)
│   ├── live_agent_utils.py   # Utilities for visual state vector creation
│   ├── run_live_agent.py     # Main script for running the hybrid visual agent
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
    *   **Playwright Browser Binaries:** If you intend to use the Playwright approach, after the pip install, run:
        ```bash
        python -m playwright install
        ```
        This downloads browser binaries. Note: Successful execution of Playwright also depends on the host system having required GUI/graphics libraries (e.g., GTK, X11 libs on Linux). Warnings during `playwright install` might indicate missing system dependencies.
    *   **Hybrid Agent System Dependencies:** `pyautogui` might have additional system dependencies on Linux for interacting with the display server (e.g., `sudo apt-get install scrot python3-tk python3-dev` and potentially Xvfb for headless virtual display). `mss` also relies on X server capabilities.

## How to Run

### 1. Training the RL Agent (Simulated Environment)
   *   Ensure virtual environment is activated.
   *   Navigate to project root.
   *   Run: `python -m pacman_ai.train_rl`
   *   Model weights (e.g., `pacman_rl_agent_final_ep<N>.weights.h5`) are saved in the project root.

### 2. Running the Live Visual Agent (Hybrid Approach - `run_live_agent.py`)

This mode uses PyAutoGUI and MSS to play the Google Doodle Pac-Man.
*   **Crucial Prerequisites & Calibration:**
    *   **Graphical Environment:** Must be run in a graphical desktop environment.
    *   **Game Window:** The Google Doodle Pac-Man game (`https://www.google.com/logos/2010/pacman10-i.html`) must be open in a browser window.
    *   **Window Focus:** The Pac-Man game window **must be the active, focused window** when `run_live_agent.py` is active.
    *   **Screen Capture Calibration (`IMAGE_CAPTURE_PARAMS` in `run_live_agent.py`):** You **MUST** adjust `top_offset`, `left_offset`, `width`, `height`, and `monitor_number` to accurately define the game area on your screen. Use OS screenshot tools or screen coordinate utilities.
    *   **HSV Color Threshold Tuning (`pacman_ai/hsv_config.json`):** You **MUST** tune the HSV values for Pac-Man, ghosts (normal and frightened), and pellets based on your screen's appearance of the game. Use an image editor with an HSV color picker on a game screenshot. Test iteratively using `pacman_ai/visual_perception.py`'s test block if run locally.
*   **Running the Script:**
    1.  Ensure prerequisites and calibration are done.
    2.  Activate your virtual environment.
    3.  Navigate to the project root.
    4.  Run: `python -m pacman_ai.run_live_agent`
    5.  Quickly switch focus to the Pac-Man game window before the 5-second countdown in the script ends.

### 3. Running the Playwright Control Script (Conceptual - `playwright_control.py`)
   *   This script (`pacman_ai/playwright_control.py`) demonstrates launching a browser and navigating to the Pac-Man URL using Playwright.
   *   Run (from project root, venv active): `python -m pacman_ai.playwright_control`
   *   **Status:** This is a basic demonstration. It's not yet integrated into a full perception-action loop with the AI agent. Successful execution depends on Playwright being correctly installed (including browser binaries and system dependencies).

## Training the Live Visual Agent (Advanced - Conceptual)

Training an agent (either Hybrid or Playwright based) directly on live visual input is a complex future step. The current `run_live_agent.py` is for inference with an untrained agent.
*   **Challenges:** Deriving rewards and `done` signals from visual input (e.g., score changes, Pac-Man dying) is non-trivial. Game speed, perception accuracy, and action timing are critical.
*   **Conceptual Steps for Live Training:**
    1.  Modify the main loop in `run_live_agent.py` (or a similar script for Playwright).
    2.  After sending an action, capture the next screen state.
    3.  Implement robust visual logic to determine `reward` and `done` status.
    4.  Generate the `next_state_vector`.
    5.  Use `agent.remember()` and `agent.replay()` to train.
    6.  Manage exploration (`agent.epsilon`).

## Development Notes
- **Simulated Training:** State representation in `train_rl.py` (`get_state_vector`), rewards from `simulation.py`.
- **Visual Agent:**
    - State representation from visual input: `live_agent_utils.py` (`get_visual_state_vector`).
    - HSV Color tuning: `hsv_config.json` (CRITICAL).
    - Screen capture coordinates: `run_live_agent.py` (`IMAGE_CAPTURE_PARAMS`) (CRITICAL).
- DQN agent architecture: `pacman_ai/rl_agent.py`.

---
*(Replace `<your_repository_url_here>` and `<repository_directory_name>` with actual values if applicable when this is pushed to a remote repository.)*
