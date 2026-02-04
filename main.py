"""
This script lets the user generate a leaderboard via cmdline input.
Supports sorting by time and number scores, all others aren't sorted.
Made by AlexCA
"""

from aotw_board_maker import *

if __name__ == "__main__":
	aotw: AOTW = AOTW(0)
	aotw.main()
