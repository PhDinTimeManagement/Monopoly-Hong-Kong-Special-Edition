# Monopoly Hong Kong Special Edition

![Application: Desktop Board Game](https://img.shields.io/badge/Application-Desktop%20Board%20Game-brown.svg)

**Monopoly Hong Kong Special Edition** is a Python/Tkinter desktop board game inspired by Monopoly-style gameplay and themed around Hong Kong locations. It provides a click-driven GUI for starting games, loading saved progress, customizing the board, rolling dice, buying properties, paying rent, handling jail turns, and saving game or board state as JSON.

> The repository is organized using a Model-View-Controller (MVC) architecture and is implemented with Python standard-library modules only.

## Authors

[Kent Max CHANDRA<sup>*</sup>](https://github.com/Yutatsu-KMC) <br>
[Cheuk Tung George CHAR<sup>*</sup>](https://github.com/Georgehyuvuhjb) <br>
[Tommaso Fabrizio COSTANTINI<sup>*</sup>](https://github.com/CLEM-9) <br>
[Xin DAI<sup>*</sup>](https://github.com/PhDinTimeManagement) <br>

<sup>*</sup> These authors contributed equally to this work.

## Project Demo

Note: The demo is high-resolution and may take a few moments to load.

<p align="center">
  <img src="Media/video_demo.gif" width="520" alt="Monopoly Hong Kong Special Edition demo">
</p>

## Features

- **Desktop GUI gameplay** built with `tkinter` and `ttk`.
- **Hong Kong-themed board** with default locations such as Central, Wan Chai, Stanley, Mong Kok, Sha Tin, Tai Po, Sai Kung, Yuen Long, and Tai O.
- **2-6 player support** with sequential player-name entry, duplicate-name validation, and random name generation.
- **Turn-based game loop** with two four-sided dice, player movement, property purchase prompts, rent payments, chance outcomes, income tax, jail, and go-to-jail behavior.
- **Board customization** for editable property attributes: name, color, price, and rent.
- **Save and load support** for full game state and reusable board layouts.
- **JSON-based persistence** under `Monopoly-HK/saves/`.
- **Unit tests** for model, controller, and GUI-facing logic using Python `unittest`.
- **Project documentation** in PDF form, including user, developer, design, presentation, and coverage-report documents.

## Tech Stack

| Area | Technology |
| --- | --- |
| Language | Python 3.11 recommended by the project documentation |
| GUI | `tkinter`, `tkinter.ttk` |
| Persistence | JSON files written with Python `json` |
| Architecture | Model-View-Controller (MVC) |
| Tests | `unittest`, `unittest.mock` |
| External dependencies | None declared; the code uses Python standard-library modules |

## Repository Structure

```text
Monopoly Hong Kong Special Edition
├── Documentation/
│   ├── Design_Document.pdf
│   ├── Developer_Manual.pdf
│   ├── Presentation.pdf
│   ├── Unit_Test_Line_Coverage_Report.pdf
│   └── User_Manual.pdf
├── Media/
│   ├── video_demo.gif
│   └── video_demo.mov
├── Monopoly-HK/
│   ├── assets/
│   │   ├── edit_gameboard_frame/
│   │   ├── gameplay_frame/
│   │   ├── info_frame/
│   │   ├── load_game_frame/
│   │   ├── main_menu_frame/
│   │   ├── new_game_frame/
│   │   └── save_game_frame/
│   ├── play_game.py
│   ├── saves/
│   │   ├── gameboard_setups/
│   │   └── games/
│   ├── src/
│   │   ├── Controller/
│   │   ├── Model/
│   │   └── View/
│   └── tests/
├── LICENSE
└── README.md
```

## Architecture Overview

The source code follows an MVC structure:

| Layer | Key files | Responsibility |
| --- | --- | --- |
| Model | `src/Model/Gameboard.py`, `src/Model/GameLogic.py`, `src/Model/Player.py` | Tile definitions, default board data, player state, dice rolls, movement, jail logic, winner calculation, and end-of-game rules. |
| View | `src/View/GUI.py`, `src/View/DisplayManager.py` | Tkinter window setup, frame rendering, assets, buttons, canvas drawing, dice animation, player display, save/load screens, info screen, and board editor screen. |
| Controller | `src/Controller/GameController.py`, `src/Controller/InputHandler.py` | Game flow orchestration, GUI event binding, player input validation, model/view synchronization, save/load operations, and JSON serialization. |

`Monopoly-HK/play_game.py` is the entry point. It creates the GUI, attaches a `GameController`, and starts the Tkinter main loop.

## Game Rules Implemented

The implementation uses a compact 20-tile board and a 100-round game limit.

- Each player starts with **1500 HKD**.
- A game ends when only one player remains or when the round counter reaches **100**.
- The winner is the player, or players in a tie, with the highest balance at the end of the game.
- Passing or landing on `Go` awards the configured pass prize, which is **150 HKD** by default.
- `Income Tax` charges the configured tax percentage, **10%** by default.
- `Chance` randomly adds or removes money.
- `Go To Jail` moves the player to the jail tile.
- In jail, a player may roll doubles to leave or pay a **150 HKD** fine according to the implemented jail-turn rules.
- If a player's balance becomes negative after a turn, they are moved to the broke-player list and their properties are cleared.

### Default Board

| Position | Tile | Type | Default values |
| ---: | --- | --- | --- |
| 0 | Go | Special | Pass prize: 150 HKD |
| 1 | Central | Property | Price: 800, rent: 90, color: cyan |
| 2 | Wan Chai | Property | Price: 700, rent: 65, color: cyan |
| 3 | Income Tax | Special | Tax: 10% |
| 4 | Stanley | Property | Price: 600, rent: 60, color: cyan |
| 5 | Jail | Special | Jail tile |
| 6 | Shek O | Property | Price: 400, rent: 10, color: red |
| 7 | Mong Kok | Property | Price: 500, rent: 40, color: red |
| 8 | Chance | Special | Random gain/loss |
| 9 | Tsing Yi | Property | Price: 400, rent: 15, color: red |
| 10 | Free Parking | Special | No action |
| 11 | Sha Tin | Property | Price: 700, rent: 75, color: grey |
| 12 | Chance | Special | Random gain/loss |
| 13 | Tuen Mun | Property | Price: 400, rent: 20, color: grey |
| 14 | Tai Po | Property | Price: 500, rent: 25, color: grey |
| 15 | Go To Jail | Special | Sends player to Jail |
| 16 | Sai Kung | Property | Price: 400, rent: 10, color: yellow |
| 17 | Yuen Long | Property | Price: 400, rent: 25, color: yellow |
| 18 | Chance | Special | Random gain/loss |
| 19 | Tai O | Property | Price: 600, rent: 25, color: yellow |

## Installation

### Requirements

- Python 3.11 is the documented development version.
- A Python installation with `tkinter` available.
- No `requirements.txt`, `pyproject.toml`, or third-party package installation step is provided in this repository.

To check whether Tkinter is available:

```bash
python -m tkinter
```

A small Tkinter test window should open. If the command fails, install or enable Tk/Tcl support for your Python distribution before running the game.

### Clone the Repository

```bash
git clone https://github.com/PhDinTimeManagement/Monopoly-Hong-Kong-Special-Edition.git
cd Monopoly-Hong-Kong-Special-Edition/Monopoly-HK
```

If you are using a downloaded ZIP archive, open the extracted project directory and then enter `Monopoly-HK/`.

## Running the Game

From the `Monopoly-HK/` directory:

```bash
python play_game.py
```

On Windows, depending on your Python launcher configuration, this may also be:

```powershell
py -3.11 play_game.py
```

The main menu should open in a fixed-size Tkinter window.

## Usage Guide

### Start a New Game

1. Click **New Game** from the main menu.
2. Enter player names in order, or use the dice button to generate random names.
3. Provide at least two valid player names.
4. Click **Play** to begin.

Player-name validation is implemented in `InputHandler` and the new-game frame:

- names must be entered sequentially;
- names must be 1-20 characters long;
- duplicate player names are rejected.

### Customize a Board

1. From the new-game screen, click **Edit Board**.
2. Select an editable property tile.
3. Update the property name, color, price, and rent.
4. Click **Confirm** for the selected tile.
5. Click **Apply Changes** to use the edited board for the next game, or **Save Board Profile** to store the layout.

Board-edit validation rejects duplicate property names and non-integer price or rent values.

### Save and Load

The game stores runtime data as JSON:

| Data type | Directory |
| --- | --- |
| Saved game progress | `Monopoly-HK/saves/games/` |
| Saved board layouts | `Monopoly-HK/saves/gameboard_setups/` |

The GUI displays up to five saved records at a time in the save/load screens.

## Configuration

No environment variables are required.

The project uses fixed local paths derived from source-file locations for assets and save data. The `saves/` directories are created automatically by the controller if they are missing during save operations.

## Testing

The repository contains `unittest` test modules in `Monopoly-HK/tests/`.

Run model-level tests from `Monopoly-HK/`:

```bash
python -m unittest tests.test_Gameboard tests.test_GameLogic
```

Run the controller and GUI-facing tests from `Monopoly-HK/tests/` so their relative save-file paths resolve as expected:

```bash
cd tests
PYTHONPATH=.. python -m unittest discover -p "test_*.py"
```

On a headless Linux environment, wrap GUI tests with `xvfb-run`:

```bash
cd tests
PYTHONPATH=.. xvfb-run -a python -m unittest discover -p "test_*.py"
```

The controller tests instantiate Tkinter windows and may create or delete JSON files under `saves/games/` and `saves/gameboard_setups/`.

A coverage report is included at [`Documentation/Unit_Test_Line_Coverage_Report.pdf`](Documentation/Unit_Test_Line_Coverage_Report.pdf).

## Documentation

| File | Description |
| --- | --- |
| [`Documentation/User_Manual.pdf`](Documentation/User_Manual.pdf) | Player-facing walkthrough of menus, board editing, save/load flows, and gameplay states. |
| [`Documentation/Developer_Manual.pdf`](Documentation/Developer_Manual.pdf) | Development setup, platform notes, and PyCharm run/debug guidance. |
| [`Documentation/Design_Document.pdf`](Documentation/Design_Document.pdf) | MVC architecture, class relationships, and turn-flow design notes. |
| [`Documentation/Unit_Test_Line_Coverage_Report.pdf`](Documentation/Unit_Test_Line_Coverage_Report.pdf) | Coverage summary and testing examples. |
| [`Documentation/Presentation.pdf`](Documentation/Presentation.pdf) | Project presentation slides. |
