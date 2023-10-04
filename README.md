# wordle_helper
Help to solve Wordle puzzles (a la NYT)
On the command line give each 5 letter word guess followed by a sequence of 5 digits that represent the result of that guess:
0=letter not used
1=letter used but wrong location
2=letter used and correct location.
e.g. here's a sequence of 4 guesses.
python3 whelp.py adieu 00210 spine 00202 trite 00202 olive 01202
