import chess
import numpy as np
import sys

f = open("out.txt", "w")

def eprint(*args, **kwargs):
    print(*args, file=f, **kwargs)

#原始版的局面评估，需要后续优化
def evaluateBoard (board):
    str_fen=board.fen()
    dic={'P':10, 'R':50,'N':30,'B':30,'Q':90,'K':900 ,'p':-10,'r':-50,'n':-30,'b':-30,'q':-90,'k':-900}
    value = 0
    count = 0
    for i in str_fen:
        if(count<64):
            if(i<='8' and i>='1'):
                count+=int(i)-int('0')
            elif(i!='/'):
                value += dic.get(i,0)
                count+=1
    return value

# 价值相同时候的取值依赖于访问顺序，需要后续优化#
# alpha-beta 剪枝  ，board为棋盘状态， depth 为搜索深度
def calculateBestMove(board, alpha , beta , depth):
    if(depth==0):
        return evaluateBoard(board),None
    newGameMoves = board.legal_moves

    bestMove =None
    nextStep = None
    if(board.turn): #white
        bestMove=-99999
        for move in newGameMoves:
            board.push(move)
            bestMove = max(bestMove,calculateBestMove(board,alpha,beta,depth-1)[0])
            board.pop()
            if(alpha <bestMove):
                alpha = bestMove
                nextStep = move
            if(beta<=alpha):
                return bestMove , nextStep
    else :
        bestMove = 99999
        for move in newGameMoves:
            board.push (move)
            bestMove =min(bestMove , calculateBestMove(board,alpha,beta,depth-1)[0])
            board.pop()
            if(beta > bestMove):
                beta =bestMove
                nextStep = move
            if(alpha >=beta):
                return bestMove , nextStep
    return bestMove , nextStep


def getBestMove(board , len = 5):
    ALPHA = -99999
    BETA = 99999
#    if (board.is_game_over()):
#        eprint('Game over !')
#        return None
    bestMove = calculateBestMove(board,ALPHA,BETA,len)[1]
    return bestMove

def test() :
    board= chess.Board()
    evaluateBoard(board)
    for i in range(70):
        if(i%2==0):
            eprint(board.turn)
            BestMove= getBestMove(board,4)
        else :
            eprint(board.turn)
            BestMove=getBestMove(board,2)
        board.push(BestMove)
        eprint(board)
        eprint('----------------')
