# -*- coding: utf-8 -*-

import pygame
import sys
import chess
import cutOri as cut

from cut import eprint

from pygame.locals import *
from sys import exit




#初始化pygame,为使用硬件做准备
pygame.init()

#建立一个棋谱
board=chess.Board()

board_edge_x=['a','b','c','d','e','f','g','h']
board_edge_y=['1','2','3','4','5','6','7','8']

whoseTurn = input()

if whoseTurn == "white":
    myMove = cut.getBestMove(board)
    sanOutString = board.san(myMove)
    board.push(myMove)

    eprint("Write to output : " + sanOutString)
    print(sanOutString)
    eprint("Current board\n" + str(board))
elif whoseTurn == "black":
    pass
else:
    raise ValueError()
    

while True:
    sanInString = input()

    eprint("Read from outside : " + sanInString)
    board.push_san(sanInString)
    eprint("Current board\n" + str(board))

    myMove = cut.getBestMove(board)
    sanOutString = board.san(myMove)
    board.push(myMove)

    eprint("Write to output : " + sanOutString)
    print(sanOutString)
    eprint("Current board\n" + str(board))
    








