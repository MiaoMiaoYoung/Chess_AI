# coding=utf-8
from __future__ import print_function
import chessmodc as chess
import random
from utils import eprint, fprint
import enum
import time
import itertools
import os

INFINITY = 999999

class NodeType(enum.Enum):
    EXACT = 0
    LOWER_BOUND = 1   # 意味着这个节点里存的值经过了 Beta-剪枝，值等于现行 Beta，只是一个下界，实际值可能要更大
    UPPER_BOUND = 2   # 意味着这个节点遍历了所有的 Move 之后，没有一个是超过现行 Alpha 的，值等于现行 Alpha，只是一个上界，实际值可能更小

class FailType(enum.Enum):
    FAILSOFT = 0
    FAILHARD = 1

class Transposition(object):
    def __init__(self, thisHash, game, depthLeft, score, nodeType, bestMove):
        self.key = thisHash
        self.depthLeft = depthLeft
        self.nodeType = nodeType
        self.score = score
        self.bestMove = bestMove

def logPrint(*args, **kwargs):
    return
    fprint(*args, **kwargs)

def cut(string):
    return [string[i*8:i*8+8] for i in range(8)]

        
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

reversePst = {}
for pi, val in pst.iteritems():
    val = list(val)
    newVal = []
    for i in range(0, 8):
        newVal += val[(7-i)*8 : (7-i)*8+8]
    reversePst[pi] = tuple(newVal)


def staticEval(game):    # 在静态评估中作为静态评估函数（Standing Pat）
    # 注意，我们的 Alpha-beta 搜索采用了 Negamax（取反极大）的框架，所以在静态评估的时必须知道是对哪一方评估的
    currTurn = game.board.turn
    whiteMap = game.board.occupied_co[chess.WHITE]
    blackMap = game.board.occupied_co[chess.BLACK]
    pawnMap = game.board.pawns
    knightMap = game.board.knights
    bishopMap = game.board.bishops
    rookMap = game.board.rooks
    queenMap = game.board.queens
    kingMap = game.board.kings
    counter = 0
    score = 0
    for sq in chess.BB_SQUARES:
        if whiteMap & sq:
            score += (reversePst['P'][counter] + piece['P'] if pawnMap & sq else 0) | (reversePst['N'][counter] + piece['N'] if knightMap & sq else 0)  | (reversePst['B'][counter] + piece['B'] if bishopMap & sq else 0) | (reversePst['R'][counter] + piece['R'] if rookMap & sq else 0) | (reversePst['Q'][counter] + piece['Q'] if queenMap & sq else 0) | (reversePst['K'][counter] + piece['K'] if kingMap & sq else 0)
        elif blackMap & sq:
            score -= (pst['P'][counter] + piece['P'] if pawnMap & sq else 0) | (pst['N'][counter] + piece['N'] if knightMap & sq else 0)  | (pst['B'][counter] + piece['B'] if bishopMap & sq else 0) | (pst['R'][counter] + piece['R'] if rookMap & sq else 0) | (pst['Q'][counter] + piece['Q'] if queenMap & sq else 0) | (pst['K'][counter] + piece['K'] if kingMap & sq else 0)
        counter += 1

    if currTurn == chess.BLACK:
        score = -score
    return score


class CheckmatedException(Exception):
    def __init__(self, message = ""):
        super().__init__(message)


WINNING_SCORE = 50000
NOMOVESTHRESHOLD = 0
MAX_MOVES = 200


class Searcher(object):
    def __init__(self, game, usualTime, stopRatio):
        self.game = game
        # 采用 Fail-Hard （硬超限，也就是说估值超过 [Alpha, Beta] 窗口时，返回 Alpha（上界）或者 Beta（下界）而不是估值本身）
        self.failType = FailType.FAILHARD
        # 跨局面表
        self.transpositionTable = dict()
        # 杀手表，以 Ply 数做索引，每个 Ply 存两个杀手操作
        self.killerMoves = [[None, None]] * MAX_MOVES
        # 历史表，以 Move 做索引，每个 Move 有一个评分
        self.moveRatings = dict()
        self.currTime = None
        self.totalTime = 0
        self.usualTime = usualTime
        self.stopRatio = stopRatio

    def mvvLva(self, move):
        pieceAtTo = self.game.board.piece_at(move.to_square)
        if pieceAtTo == None:
            pieceAtTo = chess.Piece.from_symbol('P')
        return (piece[pieceAtTo.symbol().upper()] << 3) - piece[self.game.board.piece_at(move.from_square).symbol().upper()]

    def quiescenceEval(self, alpha, beta, ply, important=False):
        bestScore = -INFINITY
        if important or self.game.board.is_check():
            legalMoves = list(self.game.board.legal_moves)
            legalMoves.sort(key = self.sortKey, reverse = True)
        else:
            score = staticEval(self.game)
            if score >= beta:
                return beta if self.failType == FailType.FAILHARD else score
            elif score > alpha:
                alpha = score
            bestScore = score
            legalMoves = list(self.game.board.generate_legal_captures())
            legalMoves.sort(key = self.mvvLva, reverse = True)

        for move in legalMoves:
            self.game.board.push(move)
            score = -self.quiescenceEval(-beta, -alpha, not(move.promotion is None))
            self.game.board.pop()

            if score > bestScore:
                bestScore = score
                if score >= beta:
                    if self.failType == FailType.FAILHARD:
                        return beta
                    else:
                        return score
                if score > alpha:
                    alpha = score

        if bestScore == -INFINITY:
            # 我方被將死
            return ply - INFINITY
        return bestScore

    def getBestMove(self):
        eprint("<Socrates Ancient %s> " % ("BLACK", "WHITE")[self.game.board.turn] + os.path.basename(__file__))
        self.moveRatings = dict()
        self.moveSequence = []
        self.transpositionTable = dict()
        # self.killerMoves = [[None, None]] * MAX_MOVES
        self.currTime = time.time()
        if(self.totalTime < 300):
            timeGap = self.usualTime
        elif (self.totalTime < 500):
            timeGap = 12
        elif (self.totalTime < 570):
            timeGap = 7
        else:
            timeGap = 2
        self.futureTime = self.currTime + timeGap
        
        depth = 0
        bestMove = None
        bestScore = -INFINITY

        while time.time() <= self.futureTime:
            depth += 1
            thisMove, bestScore = self.pvSearch(-INFINITY + 1, INFINITY - 1, depth << 3, True)
            if thisMove != chess.Move.null():
                bestMove = thisMove
            else:
                break
            eprint(str(time.time() - self.currTime) + " - Depth : " + str(depth) , "Best Move", str(bestMove), ", Best Score", str(bestScore))
            if time.time() - self.currTime > timeGap * self.stopRatio:
                break
        self.totalTime += time.time() - self.currTime
        eprint("Total time :",self.totalTime)
        return bestMove

    def storeTranspositionTable(self, thisHash, depthLeft, score, nodeType, bestMove):
        t = Transposition(thisHash, self.game, depthLeft, score, nodeType, bestMove)
        self.transpositionTable[thisHash] = t

    def lookupTranspositionTable(self, thisHash, alpha, beta, depthLeft):
        iCanReplaceThisTransposition = True

        thisTransposition = self.transpositionTable.get(thisHash)

        if thisTransposition is not None:
            iCanReplaceThisTransposition = thisTransposition.depthLeft <= depthLeft
            isCheckmateMove = thisTransposition.score >= WINNING_SCORE or thisTransposition.score <= -WINNING_SCORE

            # 当跨局面表中之前记录的局面满足深度要求，或者能保证将死（杀棋，很快游戏就结束，所以不需要考虑深度）
            if thisTransposition.depthLeft >= depthLeft or isCheckmateMove:
                if thisTransposition.nodeType == NodeType.EXACT:
                    # 非常好，这是一个之前搜索时在窗口内的分数，因此是准确的分数
                    return thisTransposition.score, iCanReplaceThisTransposition, thisTransposition
                elif thisTransposition.nodeType == NodeType.LOWER_BOUND:
                    # 之前搜索时，这个节点的子节点经过了 Beta-裁切，强制返回了 Beta，所以该分数是一个下界
                    if thisTransposition.score >= beta:
                        # 若该下界仍然大过现行 Beta（仍旧太大了），返回现行 Beta（硬）或是该下界（软）
                        return beta if self.failType == FailType.FAILHARD else thisTransposition.score, iCanReplaceThisTransposition, thisTransposition
                    else:
                        # 这个下界还没有大过现行 Beta，所以说不好实际值到底是多少，有待重新搜索
                        return None, iCanReplaceThisTransposition, None
                else: # thisTransposition.nodeType == NodeType.UPPER_BOUND:
                    # 之前搜索时，所有的 Move 都没有超过那时的 Alpha（都是弱鸡局面），所以该分数是一个上界
                    if thisTransposition.score <= alpha:
                        # 若该上界在现在来看还是弱鸡，返回现行 Alpha（硬）或是该上界（软）
                        return alpha if self.failType == FailType.FAILHARD else thisTransposition.score, iCanReplaceThisTransposition, thisTransposition
                    else:
                        # 该上界不那么弱鸡了
                        return None if self.failType == FailType.FAILHARD else thisTransposition.score, iCanReplaceThisTransposition, thisTransposition
            else:
                # 该估值是不可信的
                return None, iCanReplaceThisTransposition, thisTransposition
        else:
            # 未找到
            return None, iCanReplaceThisTransposition, None

    def sortKey(self, m):
        return self.moveRatings.get(m, 0)

    def moveIter(self, transposition, legalMoves, ply):
        if transposition is not None and self.game.board.is_legal(transposition.bestMove):
            yield transposition.bestMove
        currKillerMoves = self.killerMoves[ply]
        if currKillerMoves[1] is not None and self.game.board.is_legal(currKillerMoves[1]):
            yield currKillerMoves[1]

        if currKillerMoves[0] is not None and self.game.board.is_legal(currKillerMoves[0]):
            yield currKillerMoves[0]

        legalMoves = list(legalMoves)
#       try:
#           legalMoves.remove(transpositionBestMove)
#       except:
#           pass
#       try:
#           legalMoves.remove(currKillerMoves[1])
#       except:
#           pass
#       try:
#           legalMoves.remove(currKillerMoves[0])
#       except:
#           pass

        legalMoves.sort(key = self.sortKey, reverse = True)
        legalMoves = iter(legalMoves)
        while True:
            yield next(legalMoves)

    def pvSearch(self, alpha, beta, depthLeft, root = False):
        ply = len(self.game.board.move_stack)
        if depthLeft <= 0:
            return self.quiescenceEval(alpha, beta, ply)

        thisHash = self.game.hash()
        
        if not root:
            history = self.game.historyBoard.get(thisHash)
            if history is not None:
                if len(history) >= 2:
                    return INFINITY

        transpositionScore, iCanReplaceThisTransposition, transposition = self.lookupTranspositionTable(thisHash, alpha, beta, depthLeft)


        if transpositionScore != None:
            if root:
                return transposition.bestMove, transpositionScore
            else:
                return transpositionScore

        legalMoves = iter(self.game.board.legal_moves)
        legalMoves, legalMoves_check = itertools.tee(legalMoves)

        if next(legalMoves_check, None) == None:
            if self.game.board.is_checkmate():
                # 遭将死，返回分数加上一个杀棋步数修正（对我方来说越晚越好）
                score = ply - INFINITY
                if root:
                    return None, score
                else:
                    return score
            # 为和，看看局势是否对我不利。如不利，则为和是最好结果；否则是最差结果
            val = staticEval(self.game)
            if root:
                if val > NOMOVESTHRESHOLD:
                    score = ply - INFINITY
                    return None, score
                else:
                    score = -ply + INFINITY
                    return None, score
            else:
                if val > NOMOVESTHRESHOLD:
                    score = ply - INFINITY
                    return score
                else:
                    score = -ply + INFINITY
                    return score
            
            
        moves = self.moveIter(transposition, legalMoves, ply)

        thisNodeType = NodeType.UPPER_BOUND
        thisBestScore = -INFINITY
        
        thisBestMove = None
        counter = 0

        #logPrint(depthLeft, "开始遍历走子", "alpha", alpha, "beta", beta)
        for move in moves:
            counter += 1
            #logPrint(depthLeft, "处理走子：", move)
            
            self.game.board.push(move)
            
            if self.game.board.is_check():
                nextDepth = depthLeft - 2
            else:
                nextDepth = depthLeft - 8
            if thisNodeType == NodeType.EXACT:
                #logPrint(depthLeft, "之前已有PVMove，故对", move, "采取空窗口搜索", -alpha - 1, -alpha)
                score = -self.pvSearch(-alpha - 1, -alpha, depthLeft - 8)
                if score > alpha and score < beta:
                    #logPrint(depthLeft, move, "的分数为", score, "重新搜索", -beta, -alpha)
                    # score 在 Alpha 和 Beta 之间，截断失败，窗口设小了，重搜
                    score = -self.pvSearch(-beta, -alpha, depthLeft - 8)
                    
                elif score >= beta:
                    pass
            else:
                #logPrint(depthLeft, "之前没PVMove，故对", move, "采取全窗口搜索", -beta, -alpha)
                score = -self.pvSearch(-beta, -alpha, depthLeft - 10)

            # 现在已经得出了一个分数
            self.game.board.pop()
            
            if score == INFINITY + 1 or score == INFINITY - 1:
                if root:
                    if thisBestMove != None:
                        eprint("[INTERRUPT ROOT] %s %d @ Move %d" % (thisBestMove, thisBestScore, counter))
                        return thisBestMove, thisBestScore
                    else:
                        eprint("[INTERRUPT ROOT] %s %d @ Move %d" % (thisBestMove, thisBestScore, counter))
                        return chess.Move.null(), -INFINITY - 1
                else:
                    eprint("[INTERRUPT] %s %d @ Move %d" % (thisBestMove, thisBestScore, counter))
                    return -INFINITY - 1

            if not root and time.time() > self.futureTime:
                return - INFINITY - 1

            #logPrint(depthLeft, move, "最终分数为", score)
            if score > beta:
                # 这个走子是引起了 Beta-裁切的好走子
                #logPrint(depthLeft, move, "引起了 Beta 裁切", beta)
                thisNodeType = NodeType.LOWER_BOUND
                thisBestScore = score
                thisBestMove = move
                break

            if score > thisBestScore:
                #logPrint(depthLeft, move, "更新了 thisBestScore", thisBestScore, "为", score)
                thisBestScore = score
                thisBestMove = move

            if score <= alpha:
                # 这一步连 Alpha 都没超过，弱的
                pass
            else:
                # 这一步超过了 Alpha，落在 [Alpha, Beta] 窗口内，是一个 PV Move
                thisNodeType = NodeType.EXACT
                #logPrint(depthLeft, move, "更新了 alpha", alpha, "为", score)
                alpha = score

        #logPrint(depthLeft, "thisBestScore", thisBestScore, "thisBestMove", thisBestMove)
        #assert(thisBestScore != -INFINITY)

        if iCanReplaceThisTransposition:
            self.storeTranspositionTable(thisHash, depthLeft, thisBestScore if self.failType == FailType.FAILSOFT else (beta if thisNodeType == NodeType.LOWER_BOUND else alpha), thisNodeType, thisBestMove)
                
        if thisNodeType == NodeType.LOWER_BOUND:
            if thisBestMove in self.moveRatings:
                self.moveRatings[thisBestMove] += 2 << (depthLeft >> 3)
            else:
                self.moveRatings[thisBestMove] = 2 << (depthLeft >> 3)
            
            if self.killerMoves[ply][0] != thisBestMove and self.killerMoves[ply][1] != thisBestMove:
                self.killerMoves[ply][0] = self.killerMoves[ply][1]
                self.killerMoves[ply][1] = thisBestMove

            if root:
                return thisBestMove, beta if self.failType == FailType.FAILHARD else thisBestScore
            else:
                return beta if self.failType == FailType.FAILHARD else thisBestScore

        elif thisNodeType == NodeType.EXACT:
            if thisBestMove in self.moveRatings:
                self.moveRatings[thisBestMove] += 2 << (depthLeft >> 3)
            else:
                self.moveRatings[thisBestMove] = 2 << (depthLeft >> 3)

            if self.killerMoves[ply][0] != thisBestMove and self.killerMoves[ply][1] != thisBestMove:
                self.killerMoves[ply][0] = self.killerMoves[ply][1]
                self.killerMoves[ply][1] = thisBestMove

        if root:
            return thisBestMove, alpha
        else:
            return alpha


class SocratesGame(object):
    def __init__(self, usualTime, stopRatio, fenStr = ""):
        if fenStr != "":
            self.board = chess.Board(fenStr)
        else:
            self.board = chess.Board()
        self.searcher = Searcher(self, usualTime, stopRatio)
        self.historyBoard = dict()

    def hash(self):
        return (self.board.pawns, self.board.knights, self.board.bishops, self.board.rooks, self.board.queens, self.board.kings, self.board.occupied_co[True])

    def moveAndReturnsSAN(self):
        myMove = self.searcher.getBestMove()
        sanOutStr = self.board.san(myMove)
        self.board.push(myMove)
        thisHash = self.hash()
        if thisHash in self.historyBoard:
            self.historyBoard[self.hash()] += [len(self.board.move_stack)]
        else:
            self.historyBoard[self.hash()] = [len(self.board.move_stack)]
        return sanOutStr

    def readInAndReturnsSAN(self):
        sanInStr = raw_input().strip()
        self.board.push_san(sanInStr)
        thisHash = self.hash()
        if thisHash in self.historyBoard:
            self.historyBoard[self.hash()] += [len(self.board.move_stack)]
        else:
            self.historyBoard[self.hash()] = [len(self.board.move_stack)]
        return sanInStr

    def run(self):
        myPlayer = raw_input().strip()
        if(myPlayer == "white"):
            sanOutStr = self.moveAndReturnsSAN()
            eprint("Write to output : " + sanOutStr)
            print(sanOutStr)
            eprint("Current board\n" + str(self.board))
        elif myPlayer == "black":
            pass
        else:
            raise ValueError("The player string must be `white` or `black`", myPlayer, "received")

        while True:
            sanInStr = self.readInAndReturnsSAN()
                
            eprint("Read from outside : " + sanInStr)
            eprint("Current board\n" + str(self.board))

            sanOutStr = self.moveAndReturnsSAN()

            eprint("Write to output : " + sanOutStr)
            print(sanOutStr)
            eprint("Current board\n" + str(self.board))

if __name__ == "__main__":
    game = SocratesGame()
    game.run()