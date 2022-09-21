## CS 2040 - Algorithms I
**Assignment #1:** Heuristics and the Knight’s Tour

**Author:** Matt W. Martin

### About

This program implements Warnsdorff's heuristic for attempting to solve the [knight's tour](https://en.wikipedia.org/wiki/Knight%27s_tour), described as the following:
> "A knight's tour is a sequence of moves of a knight on a chessboard such that the knight visits every square exactly once." (Wikipedia)

Warnsdorff's heuristic prescribes the following solution:
> "The knight is moved so that it always proceeds to the square from which the knight will have the fewest onward moves. When calculating the number of onward moves for each candidate square, we do not count moves that revisit any square already visited." (Wikipedia)

In the event that two or more choices for which the number of onward moves is equal, one of these positions is chosen at random.

---
### Contents
The contents of this repository include the following files:
```
./
    README.md    # this file
    driver.py    # for executing the program
    ktour.py     # implementation and data structures for Warnsdorff's
                 # heuristic solution for the knight's tour problem
```

---
### Dependencies
This program requires the following modules from the Python 3.10 standard library:
```
argparse    # parser for command-line options, args and sub-commands
curses      # terminal handling for character-cell displays
random      # generates pseudo-random numbers
re          # regular expression operations
typing      # support for type hints
```

---
### Instructions
Program execution instructions can be found by entering `python3 driver.py --help`:
```
usage: driver.py [-h] [--size N] [--start P] [--seed SEED]

This PROGRAM implements Warnsdorff's heuristic for attempting to solve the knight's tour problem.

options:
  -h, --help   show this help message and exit
  --size N     number of squares per row/column
  --start P    start position of knight (in algebraic notation)
  --seed SEED  seed for pseudo-random number generation

~created by @kaethis
```
The size of the square chessboard (8 × 8 by default) can be specified using the `--size N` option (min: 5, max: 30).  Current system time is used as the seed for pseudo-random number generation if no seed number is provided with `--seed SEED`.  A pseudo-random position on the chessboard is chosen unless the starting position of the knight is specified (in algebraic notation) by `--start P`.

For example, the program can execute with the knight positioned in the 2nd row of the 4th column on a 5 × 5 chessboard with a seed number of 920 by entering `python3 driver.py --size 5 --start c1 --seed 920`.

Of course, the program can also execute with default parameters by entering `python3 driver.py`.

The program will move the knight piece according to Warnsdorff's heuristic until no more moves can be performed.  Every iteration of the heuristic will display the values of each square on the chessboard representing the order by which it was traversed by the knight.  The knight's current position will be colored blue and all possible moves from that square will be colored magenta except for the knight's next move which will be colored green.  Proceed to the next iteration of the heuristic by pressing any key on the keyboard.

After the heuristic completes, the value of each square on the chessboard as a square grid followed by the value of each square (in ascending order of algebraic notation) will be printed to the console:
```
    A  |B  |C  |D  |E
  5|023 016 009 004 021
  4|008 003 022 015 010
  3|017 024 013 020 005
  2|002 007 018 011 014
  1|025 012 001 006 019

( 0, 0)  'A1' : 025
( 0, 1)  'B1' : 012
( 0, 2)  'C1' : 001
( 0, 3)  'D1' : 006
( 0, 4)  'E1' : 019
             ...
( 4, 0)  'A5' : 023
( 4, 1)  'B5' : 016
( 4, 2)  'C5' : 009
( 4, 3)  'D5' : 004
( 4, 4)  'E5' : 021

```

Lastly, each move performed by the knight piece (in ascending order of the number of moves performed) will be printed to the console:
```
001 :  '__' -> 'C1'
002 :  'C1' -> 'A2'
003 :  'A2' -> 'B4'
004 :  'B4' -> 'D5'
005 :  'D5' -> 'E3'
            ...
021 :  'D3' -> 'E5'
022 :  'E5' -> 'C4'
023 :  'C4' -> 'A5'
024 :  'A5' -> 'B3'
025 :  'B3' -> 'A1'
```

---
### Links
Here are some resources I found useful when developing this program:

- [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/) With few exceptions, I did my best to adhere to the strict coding style conventions described here.
- [Python Virtual Environments: A Primer](https://realpython.com/python-virtual-environments-a-primer/) While it may not be necessary for this program, I strongly suggest becoming familar with Python virtual environments.
- [Pros and Cons of Type Hints](https://realpython.com/lessons/pros-and-cons-type-hints/) I am often in favour of static typing (mostly for the sake of readability and easier debugging), but it is important to understand the consequences of type hints before adopting these practices.
- [Type Checking With Mypy](https://realpython.com/lessons/type-checking-mypy/) Type checking can be performed with a handy application called mypy (http://mypy-lang.org/).
- [Solution: Convert column index into corresponding column letter](https://stackoverflow.com/a/21231012/) This solution was instrumental in my implementation for computing any column letter from a corresponding index number (and vice versa).
- [Curses Programming with Python](https://docs.python.org/3/howto/curses.html/)
