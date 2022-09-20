#!/usr/bin/env python3


# -----------------------------------------------------------------------------
""" ...
""" # -------------------------------------------------------------------------

__author__ = '@kaethis'

__version__ = '1.0'


import argparse

import random

import ktour


global board

global knight


def exit(): # -----------------------------------------------------------------
    """ This FUNCTION exits the program.
    """ # ---------------------------------------------------------------------

    global board

    global knight


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
        description= "DESCRIPTION GOES HERE",\
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


    # If a seed was provided as an argument, initialize pseudo-randomization
    # with that seed number.  Otherwise, initialize with the seed number
    # provided.

    random.seed() if args.seed is None else random.seed(args.seed)

    # If a starting position was provided as an argument, initialize the start
    # position with a pseudo-random position on the chessboard.  Otherwise,
    # validate the argument provided and initialize the starting position with
    # that position.

    start = ktour.getRandomPosition(args.size) if args.start is None\
        else ktour.validateStartPosition(args.start, args.size)


    board = ktour.Chessboard(args.size)

    knight = ktour.Knight(board, start)


    while True:

        knight.printMove(knight.move_n, knight.getLastMove())

        print()


        board.printBoard()

        print()


        # Populate a dictionary with all positions (as key) not yet traversed
        # and the number of actions from that position (as value) from the
        # knight's current position.

        acts = knight.getActions(board)

        if not (len(acts) == 0):

            knight.printActions((knight.move_n+1), knight.pos, acts)


            if (len(acts) == 1):

                # If there is only one possible action from the knight's
                # current position, choose that action's position.

                pos = next(iter(acts))

            else:

                # If there are multiple positions with the same number of
                # fewest possible actions, populate a tuple with the positions
                # of fewest possible actions.

                poses = ktour.getFewestPositions(acts)

                knight.printPositions((knight.move_n+1), knight.pos, poses)


                # If there is only one position with the fewest number of
                # actions, choose that position.  Otherwise, select a pseudo-
                # random position from the tuple of positions of fewest
                # possible actions.

                pos = poses[0] if (len(poses) == 1)\
                    else ktour.getRandomPosition(board.size, poses)


            knight.printMove((knight.move_n+1), (knight.pos, pos))

        else:

            # If there are no possible actions from the knight's current
            # position, break out of the loop.

            break;


        # Move the knight from its current position to the position with the
        # fewest number of actions and indicate its order of traversal on the
        # chessboard.

        knight.move(board, pos)


        # Block for input before proceeding with the loop's next iteration.

        input()


    exit()


if __name__ == '__main__': main()
