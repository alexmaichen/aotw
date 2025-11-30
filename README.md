# AOTW
Small personal tool for creating ASCII leaderboards, used by myself to help organize a weekly competition in the Hades speedrunning community called "Aspect of the Week" (hence the name).

The code is split into roughly 2 distinct parts:
The first displays a sequence of leaderboards in the terminal. Valid leaderboard scores are numeric ("heat" by default), or time (days : hours : minutes : seconds).
The second is a writeup-display for the next competition. It requires a filepath of the entered name to exist inside of a "writeups\" folder located in the same directory. This part can be skipped by leaving a filename or week number empty. By default, the tool will only recognize .md files to read from, but this can be changed if necessary in the init method (attribute "ext").

Call the .help() method on an AOTW object to get started.
