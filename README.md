# AOTW Board Maker
**AOTW (Aspect of the Week)** is a command-line tool designed to generate ASCII-formatted leaderboards quickly. It is primarily used for organizing weekly competitions in the Hades speedrunning community, but can be used for any leaderboard needs that require time-based or numeric scores. Feel free to adapt any of these at will to suit your needs.

## Features
- **CSV Input Support:** Load player data instantly from a file `input.csv` (Default).
- **Manual Input Mode:** Interactive command-line interface for manual data entry.
- **Smart Parsing:** Automatically handles time formats (`mm:ss`, `hh:mm:ss`) and numeric scores (e.g., `50 heat`).
- **Auto-Sorting:** Sorts players by best time (ascending) or highest score (descending) automatically.
- **Writeup Generator:** Helper for generating weekly writeup posts (optional). Some lines will automatically add the week number near the end ("# Aspect of the Week ", "## Category of the Week ", and "## Mini of the Week ").

## Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/alexmaichen/aotw.git
   cd aotw
   ```

2. **Ensure Python 3 is installed:**
   ```bash
   python3 --version
   ```

## Usage

You can run the tool in two modes: **CSV Mode (Recommended)** or **Manual Mode**.
The board contains 3 columns: the player's name, the scores (representing what the board should be sorted by), and an optional bonus annotation.

The scores can either be sorted by time (low is better) or heat/fear (high is better). If the scoretype is not time-like or heat-/fear-like, the scores are not sorted.
Annotations may be added to the end, though it is recommended to abbreviate these (use a special symbol like an `*` or `+` or `°` or `^` or `?` or whatever, then define what every symbol means in a separate part below the leaaderboard).

### Method 1: CSV Input (Default)
1. Create a file named `input.csv` in the project folder.
2. Add your data in the following format: `Player Name, Score, Annotation (Optional)`

If you don't have a CSV file, the tool will switch to manual mode.
   
   **Example `input.csv`:**
   ```csv
   PlayerOne, 10:25, First try!
   PlayerTwo, 12:00, 
   PlayerThree, 09:45, New PB
   ```

4. Run the script:
   ```bash
   python3 main.py
   ```
5. The tool will automatically detect the file, read the scores, sort them, and print the ASCII table.

### Method 2: Manual Input
1. Run the script without an `input.csv` file of a given name.
2. Follow the interactive prompts:
   - Enter **Player Name**.
   - Enter **Score** (Time like `10:20` or Number like `50`).
   - Enter **Annotation** (Optional).
   - Press **Enter** on an empty player name line to finish and generate the board.

## Example Output
```
+-------------+-----------------------+
| Player      | Time                  |
+-------------+-----------------------+
| PlayerThree | 9:45 New PB           |
| PlayerOne   | 10:25 First try!      |
| PlayerTwo   | 12:00                 |
+-------------+-----------------------+
```

(or, with the formatting advice taken into account:)
```
+-------------+----------+
| Player      | Time     |
+-------------+----------+
| PlayerThree | 9:45 *   |
| PlayerOne   | 10:25 +  |
| PlayerTwo   | 12:00    |
+-------------+----------+
```

## Configuration (Presets)
The tool uses a preset system in `aotw_board_maker.py`.
- **PRESET=0 (Default):** Loads from CSV or Manual Input (Single board).
- **PRESET=1:** Generates a sequence of boards (Time, Heat, etc.) used for specific weekly events.

## Contributing
1. Fork the repo.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes.
4. Push to the "dev" branch and open a Pull Request. If no dev-branch currently exists, ask for one to be opened.

---
*Made by AlexCA, maintained by the community.*
