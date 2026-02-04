"""
AOTW module
Made by AlexCA
"""

from csv import reader
from os import path
import sys

if __name__ == "__main__":
	print("Do not run this as a standalone script. Call main.py instead.")
	sys.exit(1)

class AOTW():
	def help(self) -> None:
		print("This is a tool to quickly make ASCII-looking leaderboards quickly.")
		print("Modify AOTW.presets() at will.")
		print("Call AOTW.main() to start.")

	def __init__(self, PRESET: int = 0) -> None:
		"""
		init
		"""
		self.DEBUG: bool = False # set to True to enable debug messages
		self.PRESET: int = PRESET
		self.INSEQUENCE: list[str] = []
		self.scoreTypeAotw: list[str] = []
		self.scoreTypeHotw: list[str] = []
		self.writeupTable: list[str] = []
		self.widthplayers: int = -1
		self.widthscores: int = -1
		self.widthscores: int = -1
		self.annotationSpace: int = -1
		self.board_data: list[list[str]] = []

	def main(self) -> None:
		"""
		main AOTW board pipeline (recommended).
		"""
		self.presets(self.PRESET)
		self.board_wrapper()
		self.writeup_wrapper()

	def set_preset(self, PRESET: int = 0) -> None:
		self.PRESET = PRESET

	def presets(self, *args: int) -> None:
		"""
		these are example-presets. modify this part at will.
		"""

		if args:
			self.PRESET = args[0]

		#TODO if PRESET == 0, load from file instead
		if self.PRESET == 0:
			print("CSV Mode Selected.")
			filename: str = input("Enter CSV filename (default: input.csv): ") or "input.csv"
			preset_data: dict = self.loadpreset(filename)
			
			if preset_data:
				self.INSEQUENCE = preset_data.get("INSEQUENCE", ["time"])
				self.board_data = preset_data.get("board_data", [])
			else:
				# Fallback if load fails or file not found
				print(f"File {filename} not found or invalid. Switching to manual input.")
				self.INSEQUENCE = ["time"]
				self.board_data = []
		
		if self.PRESET == 1:
			self.INSEQUENCE: list[str] = ["time", "heat", "time", "time"] # will generate multiple boards in a row with these as the scores
			self.scoreTypeAotw: list[str] = ["time", "aotw", "cotw", "uotw", "sotw"]
			self.scoreTypeHotw: list[str] = ["heat", "fear", "hotw", "ufotw", "sfotw"]
			# any other score type will not be sorted
			self.weeknumber: str = ""
			self.writeupTable: list[str] = [
				"zagsword", "nemesis", "poseidon", "arthur", "zagspear", "achilles", "hades", "guanyu", "zagshield", "chaos", "zeus", "beowulf", "zagbow", "chiron", "hera", "rama", "zagfists", "talos", "demeter", "gilgamesh", "zagrail", "eris", "hestia", "lucifer",
				
				"allaspects", "halfspects", "dashonly", "hitless", "swowo", "bowo", "showo", "spowo", "fowo", "rowo", "3weapons", "allweapons", "freshfile", "loyaltycard", "heatspeed", "supersoaker"
				]
			self.combined: list[tuple] = [("zagfists", "demeter"), ("hitless", "damageless"), ("allaspects", "halfspects")]
			self.fnameSep: str = "_"
			self.loc: str = "writeups/"
			self.ext: str = ".md"
			self.discord_format: str = "```"
			self.titles: tuple = ("# Aspect of the Week ", "## Category of the Week ", "## Mini of the Week ")
			self.enc: str = "utf-8"
			self.conclusion: str = "Good luck and have fun! To participate, tag your victory screens with"
			self.tags: list[str] = ["aotw", "hotw", "cotw", "motw"]

	def loadpreset(self, filename: str) -> dict[str, list]:
		"""
		Reads configuration/data from a file.
		Returns a dictionary where keys are field names.
		"""
		if path.exists(filename):
			try:
				with open(filename, newline='', encoding='utf-8') as csvfile:
					csv_reader = reader(csvfile)
					data = list(csv_reader)
					processed_data: list[list[str]] = []
					for row in data:
						if len(row) >= 2:
							p: str = row[0].strip()
							s: str = row[1].strip()
							a: str = row[2].strip() if len(row) > 2 else ""
							processed_data.append([p, s, a])
					
					return {
						"INSEQUENCE": ["time"], # Default for CSV
						"board_data": processed_data
					}
			except Exception as e:
				print(f"Error reading {filename}: {e}")
				return {}
		return {}

	def board_wrapper(self) -> None:
		"""
		generate boards
		"""
		if not self.INSEQUENCE:
			self.board()
			return


		if self.PRESET == 0:
			# Data is already loaded in presets()
			if self.board_data:
				self.board(data=self.board_data)
			else:
				# Manual fallback if board_data is empty
				self.board()
			return

		for i, s in enumerate(self.INSEQUENCE):
			print("\n")
			print(f"Generating board {i + 1} with score type '{s}'")
			self.board(s)

	def writeup_wrapper(self) -> None:
		"""
		display writeup
		"""
		weeknumber: str = input("Week number (leave empty to quit): ")
		if weeknumber:
			print("Pick files to display (leave empty to quit)...")
			fname: str = " "
			while fname:
				fname = input("read from file: ")
				if not fname:
					break
				print("\n")
				
				fname = fname.lower()
				self.writeup(weeknumber, fname)
			
			tags_m1: str = f"{weeknumber}, #".join(self.tags[:-1])
			print(f"{self.discord_format}\n## {self.conclusion} #{tags_m1} and #{self.tags[-1]}! :Dusa:{self.discord_format}")

	def board(self, s: str = "", data: list[list[str]] | None = None) -> None:
		"""
		displays the board. s is the score type, if empty, will prompt for a score type
		"""
		# get board details
		if not s:
			scoreType = input("scoreType (default: time): ") or "time"
		else:
			scoreType = s
		scoreType = scoreType[0].upper() + scoreType[1:] # first letter will always be a capital letter
		self.widthplayers = len("Player") + 2
		self.widthscores = len(scoreType) + 2
		self.annotationSpace = 0
		players = []

		if data:
			for row in data:
				player = row[0]
				score = row[1]
				annotation = ' ' + row[2] if len(row) > 2 else ' '
				
				if len(annotation) > self.annotationSpace:
					self.annotationSpace = len(annotation)
				
				players.append([player, score, annotation])
				self.widthplayers = max(self.widthplayers, len(player) + 2)
				self.widthscores = max(self.widthscores, len(score) + len(annotation) + 2)

		else:
			while 1:
				print() # blank line between each player
				
				player = input("Player: ")
				if not player:
					break
				
				score = input(f"{scoreType}: ")
				while not score:
					score = input(f"Please enter a {scoreType} for this player: ")
				
				annotation = input("Annotation (optional): ")
				annotation = ' ' + annotation
				if len(annotation) > self.annotationSpace:
					self.annotationSpace = len(annotation)
				players.append([player, score, annotation])
				
				self.widthplayers = max(self.widthplayers, len(player) + 2)
				self.widthscores = max(self.widthscores, len(score) + len(annotation) + 2)
				
				if self.DEBUG:
					print("DEBUG:", players[-1])

		"""sort board"""
		if len(players) > 1:
			if scoreType.lower() in self.scoreTypeAotw:
				players = sorted(players, key=lambda p: self.timeToFloat(p[1])[0])

			elif scoreType.lower() in self.scoreTypeHotw:
				players = sorted(players, key=lambda p: self.numberToFloat(p[1])[0])
				players.reverse()

			else: # feel free to add more score types here or modify this behavior
				print("Unknown score type, not sorting leaderboard.")

		"""display board"""
		if not players:
			emptyPlayer = ["", "", ""]
			self.annotationSpace += 1
			players = [emptyPlayer]
		print() # blank line before the leaderboard
		print("```")
		self.printSep()
		self.printP(["Player ", scoreType + ' ', ""])
		self.printSep()
		for p in players:
			self.printP(p)
		self.printSep()
		print("```")
		return

	def writeup(self, weeknumber: str, fname: str) -> None:
		"""
		displays the writeup for the given week
		"""
		while fname not in self.writeupTable:
			fname = input("Invalid file name. Enter a valid aspect name: ").lower()
		
		for e in self.combined:
			if fname in e:
				fname = self.fnameSep.join(e)
				break

		fname = self.loc + fname

		if fname[:-4] != self.ext:
			fname = fname + self.ext

		try:
			with open(fname, "r", encoding = self.enc) as f:
				print(self.discord_format)
				writeup: list[str] = f.readlines()
				for i in range(len(writeup)):
					for title in self.titles:
						lt: int = len(title)
						if writeup[i][:lt] == title:
							writeup[i] = title + weeknumber + writeup[i][lt:]
				print(("".join(writeup)).strip())
				print(self.discord_format)
		except FileNotFoundError:
			print(f"File '{fname}' not found. Make sure a folder called {self.loc} with a file inside called {fname[len(self.loc):]} exists.")

	def printSep(self) -> None:
		"""
		board separator (horizontal edge)
		"""
		print('+' + '-'*self.widthplayers + '+' + '-'*(self.widthscores + self.annotationSpace - 1) + '+')

	def printP(self, p: list[str]) -> None:
		"""
		print player-row. p is a list with [name, score, annotation]
		"""
		print("| " + p[0] + ' '*(self.widthplayers - 1 - len(p[0])) + "| " + p[1] + p[2] + ' '*(self.widthscores + self.annotationSpace - 2 - len(p[1]) - len(p[2])) + '|')

	def timeToFloat(self, score: str) -> tuple[int, list[str]]:
		"""
		converts time to a floating point number. please format time like the following: "days:hours:minutes:seconds.centiseconds"
		"""
		if not score:
			return (0, [])
		indices_to_remove = []
		notes = []
		for i in range(len(score)):
			if '0' <= score[i] <= '9': pass
			elif score[i] == ':': pass
			else: 
				indices_to_remove.append(i)
				notes.append(score[i])
		# remove notes from the time string (reverse order to maintain indices)
		for i in reversed(indices_to_remove):
			score = score[:i] + score[i+1:]
		
		# If score is empty after stripping (e.g. "ww"), return 0
		if not score:
			return (0, notes)

		total: int = 0
		time: list[str] = score.split(':')
		try:
			time_l: list = [int(i) for i in time]
			total += time_l.pop()
			if time_l:
				total += time_l.pop() * 60 # seconds -> minutes
			if time_l:
				total += time_l.pop() * 60 * 60 # minutes -> hours
			if time_l:
				total += time_l.pop() * 60 * 60 * 24 # hours -> days
		except ValueError:
			return (0, notes)
		return (total, notes)

	def numberToFloat(self, score: str) -> tuple[int, list]:
		"""
		destringify an integer string, return result and annotations
		"""
		if not score:
			return (0, [])
		indices_to_remove = []
		notes = []
		for i in range(len(score)):
			if '0' <= score[i] <= '9': pass
			else: 
				indices_to_remove.append(i)
				notes.append(score[i])
		# remove notes from the number string
		for i in reversed(indices_to_remove):
			score = score[:i] + score[i+1:]
		
		if not score:
			return (0, notes)

		try:
			return (int(score), notes)
		except ValueError:
			return (0, notes)

	def compareTime(self, player1: list[str], player2: list[str]) -> list[list]:
		"""
		compares two times. please format time and number strings like the following: "days:hours:minutes:seconds.centiseconds"
		"""
		time1, _ = self.timeToFloat(player1[1])
		time2, _ = self.timeToFloat(player2[1])
		if time2 > time1:
			return [player2, player1]
		return [player1, player2]
