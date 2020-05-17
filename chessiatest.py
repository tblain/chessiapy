import time
import chess
from chess import polyglot
board = chess.Board()
book = chess.polyglot.open_reader("Formula12.bin")

# ----- variables -----

depth = 4
abandon = False
# 0 => human / 1 => minimax / 2 => alphaBeta
whitePlayer = 0
blackPlayer = 2
positions = 0
global turnNumber
turnNumber = 1
useBook = True
maxTime = 10

# ----- PieceTable -----

whitePawnTable = [
    100, 100, 100, 100, 100, 100, 100, 100,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5, 5, 10, 27, 27, 10, 5, 5,
    0, 0, 0, 25, 25, 0, 0, 0,
    5, -5, -10, 0, 0, -10, -5, 5,
    5, 10, 10, -25, -25, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0
]

whiteBishopTable = [
    0, 0, -30, 0, 0, -30, 0, 0,
    0, 0, 0, 30, 30, 0, 0, 0,
    0, 0, 30, 45, 45, 30, 0, 0,
    0, 30, 45, 60, 60, 45, 30, 0,
    0, 30, 45, 60, 60, 45, 30, 0,
    0, 0, 30, 45, 45, 30, 0, 0,
    0, 0, 0, 30, 30, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0
]

whiteKnightTable = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -50, -40, -20, -30, -30, -20, -40, -50
]

blackPawnTable = whitePawnTable[::-1]
blackBishopTable = whiteBishopTable[::-1]
blackKnightTable = whiteKnightTable[::-1]

print(blackPawnTable)

# ----- evalBoard -----
def evalBoard(board):
    score = 0
    fen = board.fen()
    i = 0
    j = 0
    letter = fen[0]

    while letter != " ":
        # print(j)
        if letter == "p":
            score -= 100 - blackPawnTable[j]
            j+=1
        elif letter == "P":
            score += 100 + whitePawnTable[j]
            j+=1

        elif letter == "b":
            score -= 325 - blackBishopTable[j]
            j+=1
        elif letter == "n":
            score -= 325 - blackKnightTable[j]
            j+=1

        elif letter == "B":
            score += 325 + whiteBishopTable[j]
            j+=1
        elif letter == "N":
            score += 325 + whiteKnightTable[j]
            j+=1

        elif letter == "r":
            score -= 550
            j+=1
        elif letter == "q":
            score -= 1000
            j+=1
        elif letter == "R":
            score += 550
            j+=1

        elif letter == "Q":
            score += 1000
            j+=1
        elif letter == "k":
            score -= 100
            j+=1
        elif letter == "K":
            score += 100
            j+=1

        elif letter != "/":
            j+= int(letter)
        # print(letter)
        i += 1
        letter = fen[i]


    return score

# ----- swapElementsIn2Arrays -----

def swapElementsIn2Arrays(arr1, arr2, f, t):
    # array 1
    tmp = arr1[f]
    arr1[f] = arr1[t]
    arr1[t] = tmp

    # arr2
    tmp = arr2[f]
    arr2[f] = arr2[t]
    arr2[t] = tmp

# ----- getKillerMoves -----

def getKillerMoves(board):
    legalMoves = board.legal_moves
    movesEval = []
    moves = []
    i = 0
    for move in legalMoves:
        board.push(move)
        moves.append(move)
        if depth > 4:
            movesEval.append(alphaBeta(3, board, not board.turn, -999999, 999999))
        else:
            movesEval.append(minimax(1, board, not board.turn))
        board.pop()
    # print("moves")
    # print(move)
    # print("movesEval")

    leng = len(moves)

    for i in range(0, leng):
        for j in range(0, leng):
            if board.turn and movesEval[j-1]<movesEval[j]:
                swapElementsIn2Arrays(moves, movesEval, j-1, j)
            elif not board.turn and movesEval[j-1]>movesEval[j]:
                swapElementsIn2Arrays(moves, movesEval, j-1, j)

    return moves

# ----- alphaBeta -----

def alphaBeta(depth, board, isMaximisingWhite,a , b):
    global positions
    positions += 1
    if depth == 0:
        score = evalBoard(board)
        return score, score

    moves = board.legal_moves

    if isMaximisingWhite:
        for move in moves:
            board.push(move)
            if board.is_checkmate():
                board.pop()
                return 999999, b
            else:
                dump, y = alphaBeta(depth - 1, board, not isMaximisingWhite, a, b)

                a = max(a, y)

                if a >= b:
                    board.pop()
                    return a, b
                # print("max : " + str(bestScore))
                board.pop()

        return a, b

    else:
        for move in moves:
            board.push(move)
            if board.is_checkmate():
                board.pop()
                return a, 999999
            else:
                x, dump = alphaBeta(depth - 1, board, not isMaximisingWhite, a, b)

                b = min(b, x)

                if a >= b:
                    board.pop()
                    return a, b

                # print("min : " + str(bestScore))
                board.pop()

        return a, b

# ----- getAlphaBetaMove -----

def getAlphaBetaMove(color):
    global positions

    t1 = time.time()

    if useBook and color == 1:
        main_entrys = book.find_all(board)
        if sum(1 for x in main_entrys) > 0:
            main_entry = book.find(board)
            entryMove = main_entry.move()
            # print("entryMove : " + str(entryMove))
            if entryMove:
                print(" by book")
                print("move : " + str(entryMove))
                t2 = time.time()
                print("time : " + str(t2 - t1))
                positions = 0
                return entryMove

    print(" killerMoves")
    moves = getKillerMoves(board)
    print(" ")
    print("  EVAL = " + str(evalBoard(board)))
    print(" ")
    print(" ")

    bestMove = False
    currentDepth = 2

    t3 = time.time()
    while t3 - t1 < maxTime:
        print(" currentDepth : " + str(currentDepth) + " | time " + str(t3 - t1))
        a = -999999
        b =  999999
        i = 1
        for move in moves:
            if not bestMove:
                bestMove = move

            # print("========================================")
            # print("alphaBeta sur " + str(move) + " | " + str(i) + "/" + str(len(moves)))
            i+=1

            board.push(move)

            # x => alpha value returned, y beta value returned
            x, y = alphaBeta(currentDepth - 1, board, board.turn, a, b)
            if color == 1 and y > a:
                bestMove = move
                a = y

            elif color == 0 and x < b:
                bestMove = move
                b = x

            board.pop()

            if time.time() - t1 > maxTime:
                break
        t3 = time.time()
        currentDepth += 1

    print("by alphaBeta")
    t2 = time.time()
    print("time : " + str(t2 - t1) + " | p : " + str(positions) + " | p/s : " + str(positions/(t2-t1)))
    positions = 0
    return bestMove

# ----- minimax -----

def minimax(depth, board, isMaximisingWhite):
    if depth == 0:
        return evalBoard(board)

    moves = board.legal_moves

    if isMaximisingWhite:
        bestScore = -99999
        for move in moves:
            board.push(move)
            minimaxScore = minimax(depth - 1, board, not isMaximisingWhite)
            bestScore = max(bestScore, minimaxScore)
            # print("max : " + str(bestScore))
            board.pop()

        return bestScore

    else:
        bestScore = 99999
        for move in moves:
            board.push(move)
            minimaxScore = minimax(depth - 1, board, not isMaximisingWhite)
            bestScore = min(bestScore, minimaxScore)
            # print("min : " + str(bestScore))
            board.pop()

        return bestScore

# ----- getMiniMaxMove -----
# This part return the move choosen by the minimax algo

def getMiniMaxMove(color):
    moves = board.legal_moves
    print(moves)

    colorCoeff = 1
    if not board.turn:
        colorCoeff = colorCoeff - 1

    bestMove = False
    bestScore = -99999 * colorCoeff

    for move in moves:
        if not bestMove:
            bestMove = move

        board.push(move)
        moveScore = minimax(depth - 1, board, not board.turn)
        # print(moveScore)
        if (moveScore > bestScore and color == 1) or (moveScore < bestScore and color == 0):
            bestMove = move
            bestScore = moveScore
            print(" bestScore : " + str(bestScore) + " with move : " + str(bestMove))

        board.pop()

    print(" bestScore : " + str(bestScore))
    return bestMove

# ----- Get human player move -----
# This part return the move choosen by the human player

def getHumanPlayerMove(color):
    # posFrom = input("posFrom : ")
    # posTo = input("posTo : ")

    passmove = input("Move : ")

    return chess.Move.from_uci(move)

# ----- Get white player move -----

def getWhiteMove():
    if whitePlayer == 0:
        return getHumanPlayerMove(1)
    elif whitePlayer == 1:
        return getMiniMaxMove(1)
    elif whitePlayer == 2:
        return getAlphaBetaMove(1)

# ----- Get black player move -----

def getBlackMove():
    if blackPlayer == 0:
        return getHumanPlayerMove(0)
    elif blackPlayer == 1:
        return getMiniMaxMove(0)
    elif blackPlayer == 2:
        return getAlphaBetaMove(0)

# ==================================================
# ==================================================
# ----- gestion of who plays, terminal display, etc.

while not board.is_game_over() and not abandon:
    # ----- Text separator in terminal between moves

    print(" ")
    print("===============================================")
    print("===============================================")
    print(" ")
    if board.turn:
        print(" turn " + str(turnNumber) + " : White")
    else:
        print(" turn " + str(turnNumber) + " : Black")
    print(board)
    print(" ")

    # ----------------------------------------------

    if board.turn:
        move = getWhiteMove()
        # getWhiteMove()
    else:
        move = getBlackMove()
        # getBlackMove()
    print(" Choosed move : " + str(move))
    turnNumber += 1

    board.push(move)


if board.is_game_over():
    print(" ")
    print(" la partie est finie !")
    print(board)
