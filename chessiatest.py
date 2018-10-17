import chess
board = chess.Board()

# ----- variables -----

depth = 4
abandon = False
# 1 => ia / 0 => human
whitePlayer = 0
blackPlayer = 1

# ---------------------

# ----- evalBoard -----
def evalBoard(board):
    score = 0
    fen = board.fen()
    i = 0
    letter = fen[0]

    while letter != " ":
        if letter == "p":
            score -= 1
        elif letter == "P":
            score += 1

        elif letter == "b":
            score -= 3
        elif letter == "n":
            score -= 3
        elif letter == "r":
            score -= 5
        elif letter == "q":
            score -= 9
        elif letter == "k":
            score -= 100

        elif letter == "B":
            score += 3
        elif letter == "N":
            score += 3
        elif letter == "R":
            score += 5
        elif letter == "Q":
            score += 9
        elif letter == "K":
            score += 100
        # print(letter)
        i += 1
        letter = fen[i]


    return score

# ----- minimax -----

def minimax(depth, board, isMaximisingPlayer):
    if depth == 0:
        return evalBoard(board)

    moves = board.legal_moves

    if isMaximisingPlayer:
        bestScore = -99999
        for move in moves:
            board.push(move)
            minimaxScore = minimax(depth - 1, board, not isMaximisingPlayer)
            bestScore = max(bestScore, minimaxScore)
            # print("max : " + str(bestScore))
            board.pop()

        return bestScore

    else:
        bestScore = 99999
        for move in moves:
            board.push(move)
            minimaxScore = minimax(depth - 1, board, not isMaximisingPlayer)
            bestScore = min(bestScore, minimaxScore)
            # print("min : " + str(bestScore))
            board.pop()

        return bestScore


# ----- Get ia move -----
# This part return the move choosen by the ia

def getIaMove(color):
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
    return bestMove;

# ----- Get human player move -----
# This part return the move choosen by the human player

def getHumanPlayerMove(color):
    # posFrom = input("posFrom : ")
    # posTo = input("posTo : ")
    move = input("Move : ")

    return chess.Move.from_uci(move)

# ----- Get white player move -----

def getWhiteMove():
    if whitePlayer == 1:
        return getIaMove(1)
    else:
        return getHumanPlayerMove(1)

# ----- Get black player move -----

def getBlackMove():
    if blackPlayer == 1:
        return getIaMove(0)
    else:
        return getHumanPlayerMove(0)


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
        print(" turn : White")
    else:
        print(" turn : White")
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
    board.push(move)


if board.is_game_over():
    print(" ")
    print(" la partie est finie !")
    print(board)
