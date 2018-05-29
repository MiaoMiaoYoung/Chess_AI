import chess
import numpy as np
import time
"""
pst = {
    'P': (  ( 0,   0,   0,   0,   0,   0,   0,   0  ),
            (78,  83,  86,  73, 102,  82,  85,  90  ),
            (7,  29,  21,  44,  40,  31,  44,   7   ),
            (-17,  16,  -2,  15,  14,   0,  15, -13 ),
            (-26,   3,  10,   9,   6,   1,   0, -23 ),
            (-22,   9,   5, -11, -10,  -2,   3, -19 ),
            (-31,   8,  -7, -37, -36, -14,   3, -31 ),
             (0,   0,   0,   0,   0,   0,   0,   0 )),
    'N': (  ( -66, -53, -75, -75, -10, -55, -58, -70),
            (-3,  -6, 100, -36,   4,  62,  -4, -14  ),
            (10,  67,   1,  74,  73,  27,  62,  -2  ),
            (24,  24,  45,  37,  33,  41,  25,  17  ),
            (-1,   5,  31,  21,  22,  35,   2,   0  ),
            (-18,  10,  13,  22,  18,  15,  11, -14 ),
            (-23, -15,   2,   0,   2,   0, -23, -20 ),
            (-74, -23, -26, -24, -19, -35, -22, -69 )),
    'B': (( -59, -78, -82, -76, -23,-107, -37, -50),
           (-11,  20,  35, -42, -39,  31,   2, -22),
            ( -9,  39, -32,  41,  52, -10,  28, -14),
           (25,  17,  20,  34,  26,  25,  15,  10),
            (13,  10,  17,  23,  17,  16,   0,   7),
             (14,  25,  24,  15,   8,  25,  20,  15),
              (19,  20,  11,   6,   7,   6,  20,  16),
               ( -7,   2, -15, -12, -14, -15, -10, -10)),
    'R': (  (35,  29,  33,   4,  37,  33,  56,  50),
                (55,  29,  56,  67,  55,  62,  34,  60),
                (19,  35,  28,  33,  45,  27,  25,  15),
                 (0,   5,  16,  13,  18,  -4,  -9,  -6),
                  (-28, -35, -16, -21, -13, -29, -46, -30),
                   ( -42, -28, -42, -25, -25, -35, -26, -46),
                     (-53, -38, -31, -26, -29, -43, -44, -53),
                    (-30, -24, -18,   5,  -2, -18, -31, -32)),
    'Q': ((   6,   1,  -8,-104,  69,  24,  88,  26),
          (14,  32,  60, -10,  20,  76,  57,  24),
          ( -2,  43,  32,  60,  72,  63,  43,   2),
          (  1, -16,  22,  17,  25,  20, -13,  -6),
          (-14, -15,  -2,  -5,  -1, -10, -20, -22),
          (-30,  -6, -13, -11, -16, -11, -16, -27),
          (-36, -18,   0, -19, -15, -15, -21, -38),
          (-39, -30, -31, -13, -31, -36, -34, -42)),
    'K': ((   4,  54,  47, -99, -99,  60,  83, -62),
          ( -32,  10,  55,  56,  56,  55,  10,   3),
         (-62,  12, -57,  44, -67,  28,  37, -31),
         (    -55,  50,  11,  -4, -19,  13,   0, -49),
         (    -55, -43, -52, -28, -51, -47,  -8, -50),
        (    -47, -42, -43, -79, -64, -32, -29, -32),
        (     -4,   3, -14, -50, -57, -18,  13,   4),
         (     17,  30,  -3, -14,   6,  -1,  40,  18))
}
"""

piece = { 'P': 100, 'N': 280, 'B': 320, 'R': 479, 'Q': 929, 'K': 60000 }

pst = {
    'P': (   0,   0,   0,   0,   0,   0,   0,   0,
            78,  83,  86,  73, 102,  82,  85,  90,
             7,  29,  21,  44,  40,  31,  44,   7,
           -17,  16,  -2,  15,  14,   0,  15, -13,
           -26,   3,  10,   9,   6,   1,   0, -23,
           -22,   9,   5, -11, -10,  -2,   3, -19,
           -31,   8,  -7, -37, -36, -14,   3, -31,
             0,   0,   0,   0,   0,   0,   0,   0),
    'N': ( -66, -53, -75, -75, -10, -55, -58, -70,
            -3,  -6, 100, -36,   4,  62,  -4, -14,
            10,  67,   1,  74,  73,  27,  62,  -2,
            24,  24,  45,  37,  33,  41,  25,  17,
            -1,   5,  31,  21,  22,  35,   2,   0,
           -18,  10,  13,  22,  18,  15,  11, -14,
           -23, -15,   2,   0,   2,   0, -23, -20,
           -74, -23, -26, -24, -19, -35, -22, -69),
    'B': ( -59, -78, -82, -76, -23,-107, -37, -50,
           -11,  20,  35, -42, -39,  31,   2, -22,
            -9,  39, -32,  41,  52, -10,  28, -14,
            25,  17,  20,  34,  26,  25,  15,  10,
            13,  10,  17,  23,  17,  16,   0,   7,
            14,  25,  24,  15,   8,  25,  20,  15,
            19,  20,  11,   6,   7,   6,  20,  16,
            -7,   2, -15, -12, -14, -15, -10, -10),
    'R': (  35,  29,  33,   4,  37,  33,  56,  50,
            55,  29,  56,  67,  55,  62,  34,  60,
            19,  35,  28,  33,  45,  27,  25,  15,
             0,   5,  16,  13,  18,  -4,  -9,  -6,
           -28, -35, -16, -21, -13, -29, -46, -30,
           -42, -28, -42, -25, -25, -35, -26, -46,
           -53, -38, -31, -26, -29, -43, -44, -53,
           -30, -24, -18,   5,  -2, -18, -31, -32),
    'Q': (   6,   1,  -8,-104,  69,  24,  88,  26,
            14,  32,  60, -10,  20,  76,  57,  24,
            -2,  43,  32,  60,  72,  63,  43,   2,
             1, -16,  22,  17,  25,  20, -13,  -6,
           -14, -15,  -2,  -5,  -1, -10, -20, -22,
           -30,  -6, -13, -11, -16, -11, -16, -27,
           -36, -18,   0, -19, -15, -15, -21, -38,
           -39, -30, -31, -13, -31, -36, -34, -42),
    'K': (   4,  54,  47, -99, -99,  60,  83, -62,
           -32,  10,  55,  56,  56,  55,  10,   3,
           -62,  12, -57,  44, -67,  28,  37, -31,
           -55,  50,  11,  -4, -19,  13,   0, -49,
           -55, -43, -52, -28, -51, -47,  -8, -50,
           -47, -42, -43, -79, -64, -32, -29, -32,
            -4,   3, -14, -50, -57, -18,  13,   4,
            17,  30,  -3, -14,   6,  -1,  40,  18),
}

INF = 999999

def Sf_evaluateBoard (board ):
    fen = board.fen()
    count = 0
    score = 0
    for pi in fen:
        if (count < 64):

            if (pi <= '8' and pi >= '1'):
                count += int(pi) - int('0')
            elif (pi == '/'):
                continue
            else:
                if pi.islower():
                    pi = pi.upper()
                    score -= piece[pi]
                    i = int(count / 8)
                    j = count - 8 * i
                    score -= pst[pi][(7 - i) * 8 + j]
                else:
                    score += piece[pi]
                    score += pst[pi][count]
                count += 1
    return score


class Sunfish:

    def Update(self,board):
        self.board = board
        #self.Fen2data()
        return

    def Fen2data(self):
        board = self.board
        fen = board.fen()
        fen = fen.split(' ')[0]
        fen = fen.replace('1','.')
        fen = fen.replace('2','..')
        fen = fen.replace('3','...')
        fen = fen.replace('4','....')
        fen = fen.replace('5','.....')
        fen = fen.replace('6','......')
        fen = fen.replace('7','.......')
        fen = fen.replace('8','........')
        fen = fen.split('/')
        self.data = fen
        return

    def Push(self,move):
        board = self.board
        board.push(move)
        self.Update(board)

    def Pop(self):
        board = self.board
        board.pop()
        self.Update(board)

    def __init__(self,board):
        self.Update(board)
        return

    def AbCut(self,alpha,beta,depth):
        board = self.board
        newGameMoves = board.legal_moves
        newGameMoves = list(newGameMoves)
        bestMove = None
        nextStep = None
        if(len(newGameMoves)==0):
            if board.turn ==chess.WHITE:
                return -99999,None
            else:
                return 99999,None
        else :
            nextStep =newGameMoves[0]
        if (depth == 0):
            self.Update(board)
            return Sf_evaluateBoard(self.board),None

        #np.random.shuffle(newGameMoves)
        if (len(newGameMoves) == 0):
            print('No move !')
        else:
            nextStep = newGameMoves[0]
        if (board.turn):  # white
            bestMove = -INF
            for move in newGameMoves:
              #  board.push(move)
              #  self.Update(board)
                self.Push(move)
                bestMove = max(bestMove, self.AbCut(alpha, beta, depth - 1)[0])
                #board.pop()
                #self.Update(board)
                self.Pop()
                if (alpha < bestMove):
                    alpha = bestMove
                    nextStep = move
                if (beta <= alpha):
                    return bestMove, nextStep
        else:
            bestMove = INF
            for move in newGameMoves:
                #board.push(move)
                #self.Update(board)
                self.Push(move)
                bestMove = min(bestMove, self.AbCut( alpha, beta, depth - 1)[0])
                #board.pop()
                #self.Update(board)
                self.Pop()
                if (beta > bestMove):
                    beta = bestMove
                    nextStep = move
                if (alpha >= beta):
                    return bestMove, nextStep
        return bestMove, nextStep

    def NextMove (self,depth):
        board = self.board
        ALPHA = -INF
        BETA = INF
        start = time.time()
        if board.fullmove_number <=5 :
            bestMove= self.AbCut(ALPHA,BETA,3)[1]
        else:
            bestMove = self.AbCut( ALPHA, BETA, depth)[1]
        print('cost :',time.time()-start)
        return bestMove

"""
    def evaluateBoard(self):
        board = self.data
        score =  0
        for i in range(8):
            for j in range(8):
                pi = board[i][j]
                if pi == '.':
                    continue
                elif(pi.islower()):
                    pi = pi.upper()
                    score -= piece[pi]
                    score -= pst[pi][7 - i][j]
                    #if(pi=='Q'or pi == 'K'):
                        #score -= pst[pi][7-i][j]
                    #else:
                        #score -= pst[pi][7-i][j]
                else:
                    score +=piece[pi]
                    score +=pst[pi][i][j]
        return score
"""

def test():
    board = chess.Board()
    show = Sunfish(board)
    score = show.evaluateBoard()
    print(score)
    print('ready')
    move = show.NextMove(4)
    print(move)
    board.push(move)
    show.Update(board)
    score = show.evaluateBoard()
    print(score)

#test()





