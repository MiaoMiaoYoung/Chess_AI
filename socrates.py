import chessmod as chess
import chessmod.polyglot as polyglot
import random
from utils import eprint
import enum

INFINITY = 999999

class NodeType(enum.Enum):
    EXACT = enum.auto()
    LOWER_BOUND = enum.auto()   # 意味着这个节点里存的值经过了 Beta-剪枝，值等于现行 Beta，只是一个下界，实际值可能要更大
    UPPER_BOUND = enum.auto()   # 意味着这个节点遍历了所有的 Move 之后，没有一个是超过现行 Alpha 的，值等于现行 Alpha，只是一个上界，实际值可能更小

class Transposition(object):
    def __init__(self, thisHash, game, depthLeft, score, nodeType, bestMove):
        self.key = thisHash
        self.depthLeft = depthLeft
        self.nodeType = nodeType
        self.score = score
        self.bestMove = bestMove

def quiescenceEval(game):    # 静态评估（实际上是二次搜索吃子走子）
    return 0

def staticEval(game):    # 在静态评估中作为静态评估函数（Standing Pat）
    # 注意，我们的 Alpha-beta 搜索采用了 Negamax（取反极大）的框架，所以在静态评估的时必须知道是对哪一方评估的
    currTurn = game.board.turn
    if currTurn == chess.WHITE:
        pass
    elif currTurn == chess.BLACK:
        pass
    else:
        raise ValueError()
    return 0

class CheckmatedException(Exception):
    def __init__(self, message = "")
        super().__init__(message)

class Searcher(object):
    def __init__(self, game):
        self.game = game

    def getBestMove(self):
        pass

    def lookupTranspositionTable(self, thisHash, alpha, beta, depthLeft):
        iCanReplaceThisTransposition = True
        if thisHash in self.game.transpositionTable:
            thisTransposition = self.game.transpositionTable[thisHash]
            iCanReplaceThisTransposition = thisTransposition.depthLeft <= depthLeft
            isCheckingMove = 
            if thisTransposition.depthLeft >= depthLeft:
                if thisTrasposition.nodeType == NodeType.EXACT:
                    # 非常好，这是一个之前搜索时在窗口内的分数，因此是准确的分数
                    return thisTransposition.score
                elif thisTransposition.nodeType == NodeType.LOWER_BOUND:
                    # 之前搜索时，这个节点的子节点经过了 Beta-裁切，强制返回了 Beta，所以该分数是一个下界
                    if thisTransposition.score >= beta:
                        # 若该下界仍然大过现行 beta
                        return beta
                elif thisTransposition.nodeType == NodeType.UPPER_BOUND:
                    if thisTransposition.score <= alpha:
                        return alpha
                else:
                    # 这个得分数据派不上用场，但是由于它搜索了比较多层，所以其 BestMove 值得一用（起码是子节点中最好的，或者是引起过 Beta-裁切的）
                    bestMove = thisTransposition.bestMove

    NOMOVESTHRESHOLD = 0
    def pvSearch(self, alpha, beta, depthLeft):
        if depthLeft <= 0:
            return quiescenceEval(self.game)
        if self.game.board.is_checkmate():
            return self.game.board.full_move_number() - INFINITY

        bestMove = None
        thisHash = self.game.hash()
        

        legalMoves = list(self.game.legal_moves)
        if legalMoves == []:
            # 走法为空，我方无法动弹
            if self.game.board.is_checkmate()
                # 如果遭将，那就最糟糕了
                return self.game.board.full_move_number() - INFINITY
            # 如果为和，看看局势是否对我不利。如不利，则为和是最好结果；否则是最差结果
            val = staticEval(self.game)
            if val > NOMOVESTHRESHOLD:
                return self.game.board.full_move_number() - INFINITY
            else:
                return -self.game.board.full_move_number() + INFINITY
            
            
        legalMoves.sort(key = self.moveSortKey)
        if bestMove != None:
            # 之前查表查出了一个 BestMove，和 sort 过后的第 0 位稍微交换下
            bestMoveIndex = legalMoves.index(bestMove)
            sortedLegalMovesIndexZero = legalMoves[0]
            legalMoves[0] = bestMove
            legalMoves[bestMoveIndex] = sortedLegalMovesIndexZero

        thisNodeType = None
        thisBestMove = None
        for move in legalMoves:
            self.game.board.push(move)
            if thisNodeType != NodeType.EXACT:
                score = -self.pvSearch(-alpha - 1, -alpha, depthLeft - 10)
                if score > alpha and score < beta:
                    # score 在 Alpha 和 Beta 之间，截断失败，窗口设小了，重搜
                    score = -self.pvSearch(-beta, -alpha, depthLeft - 10)
                elif score >= beta:
                    pass
            else:
                score = -self.pvSearch(-alpha - 1, -alpha, depthLeft - 10)
            
            # 现在已经得出了一个分数
            self.game.board.pop()

            if score > beta:
                # 这个走子是引起了 Beta-裁切的好走子
                thisNodeType = NodeType.LOWER_BOUND
                break

            if score <= alpha:
                # 这一步连 Alpha 都没超过，弱的
                pass
            else:
                # 这一步超过了 Alpha，落在 [Alpha, Beta] 窗口内，是一个 PV Move
                thisNodeType = NodeType.EXACT
                alpha = score

        
        if foundPV:
            # 有一个走子的分数是落在 Alpha-beta 窗口内的（所以刷新了 Alpha 值），所以 nodeType 设为 EXACT
            thisNodeType = NodeType.EXACT
        else:
            # 所有走子都是弱鸡，我勉强取取 legalMoves[0] 吧
            # 这里可以改进：在 (# 这一步连 Alpha 都没超过，弱的) 时，不要什么都不做，要记录一下能让 score 最高的 move。
            thisNodeType = NodeType.UPPER_BOUND

        # 深度优先取代
        if iCanReplaceThisTransposition:
            self.game.transpositionTable[thisHash] = Transposition(thisHash, self.game, depthLeft, alpha, thisNodeType, legalMoves[0])
        return alpha
                



class SocratesGame(object):
    def __init__(self, fenStr = ""):
        self.hasher = polyglot.ZobristHasher(polyglot.POLYGLOT_RANDOM_ARRAY)
        self.transpositionTable = dict()
        if fenStr != "":
            self.board = chess.Board(fenStr)
        else:
            self.board = chess.Board()

    def hash()
        return polyglot.zobrist_hash(self.board, self.hasher)

    def moveAndReturnsSAN(self):
        myMoves = self.board.legal_moves
        myMoves = list(myMoves)
        myMove = random.choice(myMoves)
        sanOutStr = self.board.san(myMove)
        self.board.push(myMove)
        return sanOutStr

    def readInAndReturnsSAN(self):
        sanInStr = input()
        self.board.push_san(sanInStr)
        return sanInStr

    def run(self):
        myPlayer = input()
        if(myPlayer == "white"):
            sanOutStr = self.moveAndReturnsSAN()
            eprint("Write to output : " + sanOutStr)
            print(sanOutStr)
            eprint("Current board\n" + str(self.board))
        elif myPlayer == "black":
            pass
        else:
            raise ValueError("The player string must be `white` or `black`")

        while True:
            try:
                sanInStr = self.readInAndReturnsSAN()
            except Exception as e:
                eprint("Read from outside Error : " + sanInStr)
                eprint(e)
                break
                
            eprint("Read from outside : " + sanInStr)
            eprint("Current board\n" + str(self.board))

            try:
                sanOutStr = self.moveAndReturnsSAN()
            except Exception as e:
                eprint("Generate move error.")
                eprint(e)
                break

            eprint("Write to output : " + sanOutStr)
            print(sanOutStr)
            eprint("Current board\n" + str(self.board))

if __name__ == "__main__":
    game = SocratesGame()
    game.board.set_board_fen("r3r1k1/1bqn1p1p/ppnpp1p1/6P1/P2NPP2/2N4R/1PP2QBP/5R1K")
    print(game.board)
    print(polyglot.zobrist_hash(game.board))
    for m in game.board.legal_moves:
        print(m)
        print(polyglot.zobrist_hash(game.board))
        game.board.push(m)
        print(game.board)
        print(polyglot.zobrist_hash(game.board))
        game.board.pop()