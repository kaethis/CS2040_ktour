#!/usr/bin/env python3


# -----------------------------------------------------------------------------
""" This MODULE contains the data structures and implementation for attempting
    to solve the knight's tour problem using Warnsdorff's heuristic method.
""" # -------------------------------------------------------------------------

__author__ = '@kaethis'

__version__ = '1.0'


import random

import re

from argparse import ArgumentTypeError

from typing import Dict, List, Tuple, Optional, cast


class PositionInvalidError(Exception): # --------------------------------------
    """ This EXCEPTION is RAISED when a position is invalid.
    """ # ---------------------------------------------------------------------

    def __init__(self, pos: str): # -------------------------------------------

        super().__init__("position is invalid: '{0}'".format(pos))


class PositionTraversedError(Exception): # ------------------------------------
    """ This EXCEPTION is RAISED when a position has already been traversed.
    """ # ---------------------------------------------------------------------

    def __init__(self, pos: str, val: int): # ---------------------------------

        super().__init__(\
            "position already traversed: '{0}': {1:03d}".format(pos, val)\
        )
        

class Chessboard: # -----------------------------------------------------------
    """ This CLASS represents a square (n x n) chessboard.  The value of each
        square on the chessboard represents the order by which a knight piece
        has traversed the board.
    """ # ---------------------------------------------------------------------

    SIZE_MIN = 5

    SIZE_MAX = 30


    def __init__(self, size: int): # ------------------------------------------
        """ This CONSTRUCTOR ...
        """ # -----------------------------------------------------------------

        self.size = size 

        self.squares = [[0]*self.size for i in range(0, self.size)]


    def getSquare(self, pos: str) -> int: # -----------------------------------
        """ This FUNCTION ...
        """ # -----------------------------------------------------------------

        row, col = getRowColumn(pos)

        if not (0 <= row < self.size) or not (0 <= col < self.size):

            raise PositionInvalidError(pos)


        return self.squares[row][col]


    def setSquare(self, pos: str, val: int): # --------------------------------
        """ This FUNCTION ...
        """ # -----------------------------------------------------------------

        row, col = getRowColumn(pos)

        if not (0 <= row < self.size) or not (0 <= col < self.size):

            raise PositionInvalidError(pos)

        if not (self.squares[row][col] == 0):

            raise PositionTraversedError(pos, self.squares[row][col])


        self.squares[row][col] = val


    def isTraversed(self, pos: Optional[str]=None) -> bool: # -----------------
        """ This FUNCTION returns whether or not a square on the chessboard at
            the position specified (in algebraic notation) has already been
            traversed by a knight piece.

            If no position is specified, whether or not each and every square
            on the chessboard has been traversed is returned.
        """ # -----------------------------------------------------------------
        
        if pos is not None:

            row, col = getRowColumn(cast(str, pos))

            return False if (self.squares[row][col] == 0) else True

        else:

            for i in range(0, self.size):

                for j in range(0, self.size):

                    if (self.squares[i][j] == 0): return False

            return True


    def clear(self, pos: Optional[str]=None): # -------------------------------
        """ This FUNCTION ...
        """ # -----------------------------------------------------------------

        if pos is not None:

            row, col = getRowColumn(cast(str, pos))

            self.squares[row][col] = 0
            
        else:

            for i in range(0, self.size):

                for j in range(0, self.size):

                    self.squares[i][j] = 0


    def printBoard(self): # ---------------------------------------------------
        """ This FUNCTION ...
        """ # -----------------------------------------------------------------

        print("    ", end= '')

        for i in range (0, self.size):
  
            print("{0:3s}".format(getColumnLetter(i)),\
                end= '|' if (i < (self.size-1)) else ''\
            )

        print()


        for i, rows in reversed(list(enumerate(self.squares))):

            print("{0:3d}".format(i+1), end= '|')

            for val in rows:

                print("{0:03d} ".format(val), end= '')

            print()


    def printSquare(self, pos: str): # ----------------------------------------
        """ This FUNCTION ...
        """ # -----------------------------------------------------------------

        row, col = getRowColumn(pos)

        print("({0},{1}) '{2}' : {3:03d}"\
            .format(\
                str(row).rjust(2),\
                str(col).rjust(2),\
                ('\''+pos+'\'').rjust(5),\
                self.squares[row][col]\
            )
        )
       

    def printSquares(self): # -------------------------------------------------
        """ This FUNCTION ...
        """ # -----------------------------------------------------------------

        for i in range(0, self.size):

            for j in range(0, self.size):

                pos = getAlgebraicNotation(i, j)

                print("({0},{1}) {2} : {3:03d}"\
                    .format(\
                        str(i).rjust(2),\
                        str(j).rjust(2),\
                        ('\''+pos+'\'').rjust(5),\
                        self.squares[i][j]\
                    )
                )


class Knight: # ---------------------------------------------------------------
    """ This CLASS represents a knight piece that traverses a chessboard two
        squares vertically and one square horizontally or one square vertically
        and one square horizontally per move.
    """ # ---------------------------------------------------------------------

    def __init__(self, board: Chessboard, start: str): # ----------------------
        """ This CONSTRUCTOR ...
        """ # -----------------------------------------------------------------

        row, col = getRowColumn(start)

        if not (0 <= row < board.size) or not (0 <= col < board.size):

            raise PositionInvalidError(start)

        if board.isTraversed(start):

            raise PositionTraversedError(start, board.getSquare(start))


        self.moves = {}

        self.move_n = 1

        self.moves[self.move_n] = ("__", start)
       
        self.pos = start


        board.setSquare(self.pos, self.move_n)

    
    def move(self, board:Chessboard, pos: str): # ------------------------------
        """ This FUNCTION moves the knight piece from its current position to
            a position specified (in algebraic notation).
        """ # -----------------------------------------------------------------
        
        row, col = getRowColumn(pos)

        if not (0 <= row < board.size) or not (0 <= col < board.size):

            raise PositionInvalidError(pos)
        
        if board.isTraversed(pos):

            raise PositionTraversedError(pos, board.getSquare(pos))


        self.move_n += 1

        self.moves[self.move_n] = (self.pos, pos)

        self.pos = pos


        board.setSquare(self.pos, self.move_n)


    def getMove(self, move_i: int) -> Tuple[str, str]: # ---------------------
        """ This FUNCTION ...
        """ # -----------------------------------------------------------------

        if not (0 < move_i <= self.move_n):

            raise IndexError


        return self.moves[move_i]


    def getLastMove(self) -> Tuple[str, str]: # -------------------------------
        """ This FUNCTION ...
        """ # ----------------------------------------------------------------

        return self.getMove(self.move_n)


    def getActions(\
            self, board: Chessboard, pos: str=None\
        ) -> Dict[str, int]: # ------------------------------------------------
        """ This FUNCTION returns a dictionary containing every position (as
            key) and corresponding number of actions from that position (as
            value) of all valid squares on a chessboard not yet traversed from
            a specified position (in algebraic notation).

            If no position is specified, the knight's current position is used.
        """ # -----------------------------------------------------------------

        if pos is None: pos = self.pos

        row, col = getRowColumn(pos)


        acts = {}

        jmps = (\
            ( 2,  1), ( 2, -1), (-2,  1), (-2, -1),\
            ( 1,  2), ( 1, -2), (-1,  2), (-1, -2)\
        )

        for jmp in jmps:

            row_to, col_to = (row + jmp[0]), (col + jmp[1])

            if (0 <= row_to < board.size) and (0 <= col_to < board.size):

                if (board.squares[row_to][col_to] == 0):
                    
                    pos_to = getAlgebraicNotation(row_to, col_to)

                    act_n = self.getActionsCount(board, pos_to)


                    acts[pos_to] = act_n

        
        return acts


    def getActionsCount(self, board: Chessboard, pos: str) -> int: # ----------
        """ This FUNCTION returns the number of all valid squares on a
            chessboard not yet traversed from a specified position (in
            algebraic notation).
        """ # -----------------------------------------------------------------

        row, col = getRowColumn(pos)


        act_n = 0

        jmps = (\
            ( 2,  1), ( 2, -1), (-2,  1), (-2, -1),\
            ( 1,  2), ( 1, -2), (-1,  2), (-1, -2)\
        )

        for jmp in jmps:

            row_to, col_to = (row + jmp[0]), (col + jmp[1])

            if (0 <= row_to < board.size) and (0 <= col_to < board.size):

                if (board.squares[row_to][col_to] == 0):

                    act_n += 1

        return act_n


    def printMove(\
            self, move_i: int, move: Optional[Tuple[str, str]]= None\
        ): # ------------------------------------------------------------------
        """ This FUNCTION ...
        """ # -----------------------------------------------------------------

        if move is None: move = self.moves[move_i]


        print("{0:03d} : {1} -> {2}"
            .format(\
                move_i,\
                ('\''+move[0]+'\'').rjust(5),\
                ('\''+move[1]+'\'').ljust(5)\
            )\
        )


    def printMoves(self): # ---------------------------------------------------
        """ This FUNCTION ...
        """ # -----------------------------------------------------------------

        for move_i in self.moves.keys():

            self.printMove(move_i)


    def printActions(self, move_i: int, pos: str, acts: Dict[str, int]): # ----
        """ This FUNCTION ...
        """ # -----------------------------------------------------------------
        
        act_n = len(acts)

        indent_n = len("{0:03d} : '{1}' -> {{".format(move_i, pos))


        print("{0:03d} : '{1}' -> {{".format(move_i, pos), end='')

        for i, act in enumerate(acts.keys()):

            print(" " * indent_n, end='') if (i > 0) else ...

            print("'{0}' ({1})".format(act, acts[act]),\
                end='' if (i == (act_n-1)) else '\n'\
            )

        print("}} ({})".format(act_n))


    def printPositions(\
            self, move_i: int, pos: str, poses: Tuple[str, ...]\
        ): # ------------------------------------------------------------------
        """ This FUNCTION ...
        """ # -----------------------------------------------------------------

        pos_n = len(poses)

        
        print("{0:03d} : '{1}' -> {{".format(move_i, pos), end='')

        for i, p in enumerate(poses):

            print("'{}'".format(p), end=", " if (i < (pos_n-1)) else "} ")
        
        print("({})".format(pos_n))


def getAlgebraicNotation(row: int, col: int) -> str: # ------------------------
    """ This FUNCTION returns the algebraic notation of the corresponding row
        and column of a square on a chessboard (of any size).
    """ # ---------------------------------------------------------------------

    return (getColumnLetter(col) + str(row+1))


def getRowColumn(pos: str) -> Tuple[int, int]: # ------------------------------
    """ This FUNCTION returns a tuple containing the row and column of the
        corresponding position of a square (in algebraic notation) on a
        chessboard (of any size).
    """ # ---------------------------------------------------------------------

    try:
        
        result = re.search(r'(^[a-zA-Z]+)(\d+)', pos)
    
        assert result is not None

    except AssertionError:

        raise ValueError 


    row, col = result.group(2), result.group(1)
      

    return ((int(row)-1), getColumnNumber(col))


def getColumnLetter(col: int) -> str : # --------------------------------------
    ''' This FUNCTION returns the column letter of the corresponding column
        number on a chessboard (of any size).
    ''' # ---------------------------------------------------------------------

    # NOTE: A = 0, B = 1, ... Z = 25.  Column numbers greater than 25 are
    #       represented by repeating letters in ascending order, (i.e. 26 = AA,
    #       27 = AB, ... 702 = AAA, 703 = AAB and so on).

    s = ""
        
    n = (col+1)

    while (n > 0):

        c = ((n-1) % 26)

        s = (chr(65+c) + s)

        n = ((n-c) // 26)


    return s


def getColumnNumber(ltr: str) -> int : # --------------------------------------
    ''' This FUNCTION returns the column number of the corresponding column
        letter on a chessboard (of any size).
    ''' # ---------------------------------------------------------------------

    n = 0

    for i, c in enumerate(ltr):

        n += (((ord(c)-65) % 26)+1) * (26 ** (len(ltr)-i-1))

    n -= 1


    return n


def getFewestPositions(acts: Dict[str, int]) -> Tuple[str, ...]: # ------------
    """ This FUNCTION returns a tuple of positions (in algebraic notation) with
        the fewest number of actions from a dictionary of positions (as key)
        and corresponding number of actions from that position (as value).
    """ # ---------------------------------------------------------------------

    act_min = min(acts.values())


    poses = tuple(pos for pos, act_n in acts.items() if (act_n == act_min))

    return poses


def getRandomPosition(\
        size: int, poses: Optional[Tuple[str, ...]]= None\
    ) -> str : # --------------------------------------------------------------
    ''' This FUNCTION returns a pseudo-random position (in algebraic notation)
        from a tuple of positions.

        If no actions are specified, any pseudo-random position on a square (n
        x n) chessboard is returned.
    ''' # ---------------------------------------------------------------------

    if poses is not None:

        pos = random.choice(poses)


        row, col = getRowColumn(pos)

        if not (0 <= row < size) or not (0 <= col < size):

            raise PositionInvalidError(pos)


        return pos 

    else:

        row, col = random.randint(0, (size-1)), random.randint(0, (size-1))

        return getAlgebraicNotation(row, col)


def validateSize(size: str) -> int: # -----------------------------------------
    """ This FUNCTION ...
    """ # ---------------------------------------------------------------------

    if not (Chessboard.SIZE_MIN <= int(size) <= Chessboard.SIZE_MAX):

        msg = "invalid num of squares per row/column (min {0:3d}, max {1:3d})"\
            .format(Chessboard.SIZE_MIN, Chessboard.SIZE_MAX)

        raise ArgumentTypeError(msg)


    return int(size) 


def validateStartPosition(pos: str, size: int) -> str: # ----------------------
    """ This FUNCTION ...
    """ # ---------------------------------------------------------------------

    pos = pos.upper()

    row, col = getRowColumn(pos)

    if not (0 <= row < size) or not (0 <= col < size):

        msg = "invalid start position for size of chessboard ({0} x {0})"\
            .format(size)

        raise ArgumentTypeError(msg)


    return pos
