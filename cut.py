import chess
import numpy as np
import sunfish


numTotal =[0]

def evaluateBoard (board):
    numTotal[0]+=1

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

def calculateBestMove(board, alpha , beta , depth):
    if(depth==0):
        return evaluateBoard(board),None
    newGameMoves = board.legal_moves
    newGameMoves = list(newGameMoves)

    np.random.shuffle(newGameMoves)
    bestMove =None
    nextStep =None
    if(len(newGameMoves)!=0):
        nextStep = newGameMoves[0]
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

def getBestMove(board , len = 4):
    numTotal[0]=0

    ALPHA = -99999
    BETA = 99999
    bestMove = calculateBestMove(board, ALPHA, BETA, len)[1]
    #print('Total =',numTotal[0])
    return bestMove

def test() :
    board= chess.Board()
    evaluateBoard(board)
    ss = sunfish.Sunfish(board)
    for i in range(150):
        if(board.is_game_over()):
            print('Game over !')
            break
        print('step', i, board.turn)
        if(i%2):
            BestMove = getBestMove(board,2)
            board.push(BestMove)
            print(BestMove)
        else :
            #BestMove = sunfish.Sunfish(board).NextMove(2)
            BestMove = getBestMove(board, 1)
            print(BestMove)
            board.push(BestMove)

        print(board)
        print('----------------')

if __name__ == "__main__":
    test()