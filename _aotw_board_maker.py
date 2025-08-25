"""
_aotw_board_maker.py

This script lets the user generate a leaderboard via cmdline input.
Supports sorting by time and number scores.
Made by AlexCA
"""

from _functions import *
"""the following functions for whatever reason don't work as expected when imported from _functions.py"""
# displays the writeup for the given week
def writeup(weeknumber: str, fname: str) -> None:
    global writeupTable
    if fname == "zagfists" or fname == "demeter":
        fname = "zagfists_demeter"

    while fname not in writeupTable:
        fname = input("Invalid file name. Enter a valid aspect name: ")
        if fname == "zagfists" or fname == "demeter":
            fname = "zagfists_demeter"

    if fname[:-4] != ".txt":
        fname = fname + ".txt"

    try:
        print("```")
        with open(fname, "r", encoding="utf-8") as f:
            writeup = f.readlines()
            for i in range(len(writeup)):
                for title in ("# Aspect of the Week ", "## Category of the Week "):
                    if writeup[i][:len(title)] == title:
                        writeup[i] = title + weeknumber + writeup[i][len(title):]
            print("".join(writeup))
        print("```")
    except FileNotFoundError:
        print(f"File '{fname}' not found.")
    return

# load preset from "settingsX.set" where X is an integer from 0 to 9
def preset() -> None:
    global DEBUG, PRESET, INSEQUENCE, scoreTypeAotw, scoreTypeHotw, writeupTable
    for i in range(10):
        try:
            with open(f"_settings{i}.txt", "r") as f:
                response = input(f"Use _settings{i}.txt? (y/n): ").lower()
                if input(response == 'y' or response == 'yes'):
                    for line in f:
                        if not line.strip():
                            continue  # skip empty lines
                        line = line.strip()

                        if line.upper().startswith("PRESET = "):
                            PRESET = int(line.split('=')[1].strip().strip(' '))
                        elif line.upper().startswith("INSEQUENCE = "):
                            INSEQUENCE = [c.split('=')[1].strip().strip(' ') for c in line.split(",") if c.strip()]
                        elif line.lower().startswith("aotw = "):
                            scoreTypeAotw = [c.split('=')[1].strip().strip(' ') for c in line.split(",") if c.strip()]
                        elif line.lower().startswith("hotw = "):
                            scoreTypeHotw = [c.split('=')[1].strip().strip(' ') for c in line.split(",") if c.strip()]
                        elif line.lower().startswith("writeuptable = "):
                            writeupTable = [c.split('=')[1].strip().strip(' ') for c in line.split(",") if c.strip()]
                    return
                else:
                    continue
        except FileNotFoundError:
            continue

    if DEBUG:
        print(f"INSEQUENCE: {INSEQUENCE}")
        print(f"scoreTypeAotw: {scoreTypeAotw}")
        print(f"scoreTypeHotw: {scoreTypeHotw}")
        print(f"writeupTable: {writeupTable}")
    return

if __name__ == "__main__":
    """init"""
    widthplayers = -1
    widthscores = -1
    annotationSpace = -1

    """load preset"""
    #preset() # TODO

    """generate board"""
    if not INSEQUENCE:
        board()
    else:
        for i, s in enumerate(INSEQUENCE):
            print("\n")
            print(f"Generating board {i + 1} with score type '{s}'")
            board(s)
    
    """display writeup"""
    weeknumber = input("Week number (leave empty to quit): ")
    if weeknumber:
        fname = input("read from file: ")
        while not fname:
            fname = input("filename must be an aspect name: ")
        print("\n")
        writeup(weeknumber, fname)
