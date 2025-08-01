"""
_aotw_board_maker.py

This script lets the user generate a leaderboard via cmdline input.
Supports sorting by time and number scores.
Made by AlexCA
"""

"""modify this part at will. touch nothing else."""
DEBUG = False
scoreTypeAotw = ["time", "aotw", "cotw", "uotw", "sotw"]
scoreTypeHotw = ["heat", "fear", "hotw", "ufotw", "sfotw"]
# any other score type will not be sorted

"""init"""
# line separator
def printSep() -> None:
    print("+" + "-"*widthplayers + "+" + "-"*(widthscores + annotationSpace - 1) + "+")

# print player. p is a list with [name, score, annotation]
def printP(p: list) -> None:
    print("| " + p[0] + " "*(widthplayers - 1 - len(p[0])) + "| " + p[1] + p[2] + " "*(widthscores + annotationSpace - 2 - len(p[1]) - len(p[2])) + "|")

# converts time to a floating point number. please format time like the following: "days:hours:minutes:seconds:milliseconds"
def timeToFloat(score: str) -> tuple:
    if not score:
        return 0
    notes = []
    for i in range(len(score)):
        if score[i] >= '0' and score[i] <= '9': pass
        elif score[i] == ':': pass
        else: notes[i].append(score[i])
    # remove notes from the time string
    for i in notes:
        score = score[:i] + score[i+1:]
    
    total = 0
    time1 = score.split(":")
    time1 = [float(i) for i in time1]
    total += time1.pop()
    if time1:
        total += time1.pop() * 60 # seconds -> minutes
    if time1:
        total += time1.pop() * 60 * 60 # minutes -> hours
    if time1:
        total += time1.pop() * 60 * 60 * 24 # hours -> days
    return (total, notes)

# destringify an integer string
def numberToFloat(score: str) -> tuple:
    if not score:
        return 0
    notes = []
    for i in range(len(score)):
        if score[i] >= '0' and score[i] <= '9': pass
        else: notes.append(score[i])
    # remove notes from the number string
    for i in notes:
        score = score[:i] + score[i+1:]
    
    return (float(score), notes)

# compares two times. please format time and number strings like the following: "days:hours:minutes:seconds:milliseconds"
def compareTime(player1: list, player2: list) -> list:
    # compare the two times, starting with the largest time-measure (usually hours or minutes)
    time1, _ = timeToFloat(player1[1])
    time2, _ = timeToFloat(player2[1])
    if time2 > time1:
        return [player2, player1]
    return [player1, player2]

if __name__ == "__main__":
    """get board details"""
    scoreType = input("scoreType: ") or "time"
    scoreType = scoreType[0].upper() + scoreType[1:] # first letter will always be a capital letter
    annotationSpace = 0
    widthplayers = len("Player") + 2
    widthscores = len(scoreType) + 2
    players = []

    while 1:
        print() # blank line between each player
        
        player = input("Player: ")
        if not player:
            break
        
        score = input(scoreType + ": ")
        while not score:
            score = input("Please enter a " + scoreType + " for this player: ")
        
        annotation = input("Annotation (optional): ")
        annotation = ' ' + annotation
        if len(annotation) > annotationSpace:
            annotationSpace = len(annotation)
        players.append([player, score, annotation])
        
        widthplayers = max(widthplayers, len(player) + 2)
        widthscores = max(widthscores, len(score) + len(annotation) + 2)

        if DEBUG:
            print("DEBUG:", players[-1])

    """sort board"""
    if len(players) > 1:
        if scoreType.lower() in scoreTypeAotw:
            players = sorted(players, key=lambda p: timeToFloat(p[1])[0])

        elif scoreType.lower() in scoreTypeHotw:
            players = sorted(players, key=lambda p: numberToFloat(p[1])[0])
            players.reverse()

        else: # feel free to add more score types here or modify this behavior
            print("Unknown score type, not sorting leaderboard.")

    """display board"""
    print() # blank line before the leaderboard
    print("```")
    printSep()
    printP(["Player ", scoreType, ''])
    printSep()
    for p in players:
        printP(p)
    printSep()
    print("```")
