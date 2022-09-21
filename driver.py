#!/usr/bin/env python3


# -----------------------------------------------------------------------------
""" ...
""" # -------------------------------------------------------------------------

__author__ = '@kaethis'

__version__ = '1.0'


import curses

import argparse

import random

import ktour


def prog(stdscr): # -----------------------------------------------------------
    """ This FUNCTION ...
    """ # ---------------------------------------------------------------------

    global board

    global knight


    # NOTE: This program presumes the terminal is capable of displaying color.

    # TODO: Check to see whether or not the terminal is capable of displaying
    #       colors.  If it cannot, skip over color pair initializations and
    #       opt for basic color palette instead.

    colors = {\
        1 : (curses.COLOR_WHITE, curses.COLOR_BLACK),\
        2 : (curses.COLOR_WHITE, curses.COLOR_GREEN),\
        3 : (curses.COLOR_WHITE, curses.COLOR_BLUE),\
        4 : (curses.COLOR_WHITE, curses.COLOR_MAGENTA),\
        5 : (curses.COLOR_WHITE, curses.COLOR_RED),\
        6 : (curses.COLOR_BLACK, curses.COLOR_WHITE)\
    }

    for c in colors.keys():

        curses.init_pair(c, colors[c][0], colors[c][1])


    # NOTE: This program presumes the terminal has a sufficiently large screen.

    # TODO: Determine whether or not the constraints of the terminal screen are
    #       sufficient for displaying the size of the chessboard window.

    board_win = stdscr.subwin(\
        (board.size+3), ((board.size * 4)+5), 1, 1\
    )

    for i in range (0, board.size):

        board_win.move(0, ((i * 4)+6))

        board_win.addstr(ktour.getColumnLetter(i))

        board_win.move((board.size-i+1), 0)

        board_win.addstr("{0:3d}".format(i+1))

    board_win.refresh()


    squares_win = board_win.subwin(\
        (board.size+2), ((board.size*4)+1), 2, 5\
    )
    
    squares_win.bkgd(curses.color_pair(1))

    squares_win.box()


    while True:

        # Populate a dictionary with all positions (as key) not yet traversed
        # and the number of actions from that position (as value) from the
        # knight's current position.

        acts = knight.getActions(board)


        if not (len(acts) == 0):

            if (len(acts) == 1):

                # If there is only one possible action from the knight's
                # current position, choose that action's position.

                pos = next(iter(acts))

            else:

                # If there are multiple positions with the same number of
                # fewest possible actions, populate a tuple with the positions
                # of fewest possible actions.

                poses = ktour.getFewestPositions(acts)

                # If there is only one position with the fewest number of
                # actions, choose that position.  Otherwise, select a pseudo-
                # random position from the tuple of positions of fewest
                # possible actions.

                pos = poses[0] if (len(poses) == 1)\
                    else ktour.getRandomPosition(board.size, poses)

        else:

            # If these no more possible actions from the knight's current
            # position, indicate no such position.

            pos = None


        for i in range(0, board.size):
            
            for j in range(0, board.size):

                v = board.squares[i][j]

                p = ktour.getAlgebraicNotation(i, j)

                c = 2 if (p == pos) else \
                    (3 if (p == knight.pos) else\
                        (4 if (p in acts.keys()) else\
                            (5 if (((j+i) % 2) == 0) else 6)\
                        )\
                    )\


                squares_win.move((board.size-i), (j*4)+1)

                squares_win.addstr(\
                    "{0:03d}".format(v) if (v > 0) else "   ",\
                    curses.color_pair(c)\
                )

        squares_win.refresh()


        stdscr.move(0, 0)   # Move cursor somewhere inconsequential.
 
        stdscr.getch()      # Block for input before proceeding with loop.


        if not (pos == None):
        
            # Move the knight from its current position to the next position
            # and indicate its order of traversal on the chessboard.

            knight.move(board, pos)

        else:

            break   # If there is no such position, break out of the loop.


def exit(): # -----------------------------------------------------------------
    """ This FUNCTION exits the program.
    """ # ---------------------------------------------------------------------

    global board

    global knight


    print()


    # Print the value of each square on the chessboard after the very last move
    # performed by the knight piece as a square (n x n) grid.  The value of
    # each square represents the order by which a knight piece has traversed
    # the board.

    board.printBoard()
    
    print()


    # Print the value of each square on the chessboard (in ascending order of
    # algebraic notation).

    board.printSquares()

    print()


    # Print each move performed by the knight piece (in ascending order by of
    # the number of moves performed).

    knight.printMoves()

    print()


    quit()


def main(): # -----------------------------------------------------------------
    """ This MAIN FUNCTION ...
    """ # ---------------------------------------------------------------------

    global board

    global knight


    argparser = argparse.ArgumentParser(\
        description= "This PROGRAM implements Warnsdorff's heuristic for\
                      attempting to solve the knight's tour problem.",\
        epilog=      "~created by " + __author__\
    )

    argparser.add_argument(\
        '--size',\
        metavar= "N",\
        type=    ktour.validateSize,\
        default= "8",\
        help=    "number of squares per row/column"\
    )

    argparser.add_argument(\
        '--start',\
        metavar= "P",\
        type=    str,\
        help=    "start position of knight (in algebraic notation)"\
    )

    argparser.add_argument(\
        '--seed',\
        type=    int,\
        help=    "seed for pseudo-random number generation"\
    )


    args = argparser.parse_args()


    # If no seed was provided as an argument, initialize pseudo-randomization
    # with current system time as seed.  Otherwise, use seed number provided.

    random.seed() if args.seed is None else random.seed(args.seed)

    # If no starting position was provided as an argument, initialize the start
    # position with a pseudo-random position on the chessboard.  Otherwise,
    # validate the argument provided and use that starting position.

    start = ktour.getRandomPosition(args.size) if args.start is None\
        else ktour.validateStartPosition(args.start, args.size)


    board = ktour.Chessboard(args.size)

    knight = ktour.Knight(board, start)


    # NOTE: To avoid complications with returning the state of the terminal
    #       back to normal in the event that the program ends unexpectedly,
    #       we'll provide our prog() FUNCTION as a callable object to the
    #       curses.wrapper() FUNCTION.
    #
    #       This FUNCTION initializes curses (and captures stdscr window object
    #       representing the entire screen), turns off automatic key echoing,
    #       disables the usual buffered input mode (i.e. key entry no longer
    #       requires Enter), and passes key codes to the stdscr window object
    #       instead.  It also initializes colors (if color support is present).
    #
    #       The prog() FUNCTION is called within a TRY-EXCEPT that catches an
    #       EXCEPTION, restores the state of the terminal, and then re-raises
    #       the EXCEPTION.  How cool is that?!

    curses.wrapper(prog)


    exit()  # Exit the program formally.


if __name__ == '__main__': main()
