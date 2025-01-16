from cmu_graphics import *
import matplotlib
cellSize = 43 
gridSize = 3 * 3
windowSize = gridSize * cellSize 

import random


def onAppStart(app):
    app.localBoards = []  

    for i in range(9):
        board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        app.localBoards.append(board)

    app.globalBoard = [' '] * 9

    app.currentPlayer = 'X'
    app.activeBoard = None
    app.gameOver = False
    app.screen = "menu"

    app.scoreX = 0
    app.scoreY = 0
    app.timer = 30
    app.stepsPerSecond = 1
    app.boardWon = False
    app.doSettings = False
    app.isMultiplayer = False
    app.useTimer = False
    app.waiting = True
    app.elapsedTime = 0

def mainScreen(app):
    g = gradient('lightblue', 'blue', start='center')
    drawRect(0,0,550,500, fill=g)
    centerX = 275  
    titleY = 90   

    drawLabel("ULTIMATE TIC TAC TOE", centerX, titleY, size=38, bold=True, fill="navy", font="Herculanum")
    drawLabel("Challenge your mind with this expanded version!", centerX, titleY + 40, size=15, fill="white", font="Herculanum")

    buttonWidth = 200
    buttonHeight = 50
    buttonSpacing = 50

    playY = titleY + 80
    instructionsY = playY + buttonHeight + buttonSpacing
    quitY = instructionsY + buttonHeight + buttonSpacing
    creditsY = quitY + buttonHeight + buttonSpacing

    drawRect(centerX - buttonWidth // 2, playY, buttonWidth, buttonHeight, fill="darkgreen", border="black", borderWidth=3)
    drawLabel("Play", centerX, playY + buttonHeight // 2, size=25, fill="white", font="Herculanum")

    drawRect(centerX - buttonWidth // 2, instructionsY, buttonWidth, buttonHeight, fill="darkblue", border="black", borderWidth=3)
    drawLabel("Instructions", centerX, instructionsY + buttonHeight // 2, size=20, fill="white", font="Herculanum")

    drawRect(centerX - buttonWidth // 2, quitY, buttonWidth, buttonHeight, fill="darkred", border="black", borderWidth=3)
    drawLabel("Quit", centerX, quitY + buttonHeight // 2, size=25, fill="white", font="Herculanum")

    drawRect(centerX - buttonWidth // 4, creditsY, buttonWidth // 2, buttonHeight // 2, fill="white", border="black", borderWidth=2)
    drawLabel("Credits", centerX, creditsY + buttonHeight // 4, size=15, fill="black", font="Herculanum")


    


def instructionsScreen(app):
    g = gradient('lightyellow', 'gold', start='top')
    drawRect(0,0,550,500, fill=g)
    drawLabel("Instructions", 275, 50, size=30, bold=True, fill="darkblue", font="Herculanum")

    instructionText = [
        "1. Players take turns marking a cell with their symbol (X or O). X is first.",
        "2. The active board for the opponent's next move is determined by the cell you play in.",
        "3. Example: If you play in the top-right cell of a local board,",
        "   your opponent must play on the top-right local board.",
        "4. If the designated board is already won or full, the opponent",
        "   can choose any local board to play on.",
        "5. Win a local board by completing a row, column, or diagonal.",
        "6. A won local board counts as a single cell on the global board.",
        "7. Win the global board by controlling three local boards in a row.",
        "8. A local board full without a winner is considered a draw.",
        "9. The game ends in a tie if no one controls three in a row.",
    ]

    x = 50  
    y = 100
    lineSpacing = 25
    for line in instructionText:
        drawLabel(line, x, y, size=12, fill="black", align="left")
        y += lineSpacing

    drawRect(50, 400, 100, 50, fill="gray", border="black", borderWidth=2)
    drawLabel("Back", 100, 425, size=20, fill="white",font = "Herculanum")


    drawRect(400, 400, 100, 50, fill="blue", border="black", borderWidth=2)
    drawLabel("Demo", 450, 425, size=20, fill="white",font = "Herculanum")



def drawBoard(app):
    boardWidthTop = 300 
    boardWidthBottom = 350  
    boardHeight = 250  
    depth = 80 
    boardColor = gradient('lightgrey', 'darkslategrey', start='top')
    borderColor = 'black'

    topLeft = (50,100)
    topRight = (440,100)
    bottomLeft = (50,490)
    bottomRight = (440,490)

    drawPolygon(
        topLeft[0], topLeft[1],
        topRight[0], topRight[1],
        bottomRight[0], bottomRight[1],
        bottomLeft[0], bottomLeft[1],
        fill=boardColor
    )
    drawLine(bottomLeft[0], bottomLeft[1], bottomRight[0], bottomRight[1], fill="black", lineWidth=10)

def draw_x(app, center_x, center_y, cellSize):
    coords = [
        (150, 200),  
        (175, 200),  
        (250, 285),  
        (325, 200),  
        (350, 200),  
        (275, 300),  
        (350, 400),  
        (325, 400),  
        (250, 315),  
        (175, 400),  
        (150, 400),  
        (225, 300),  
    ]

    
    originalSize = 200  
    size_factor = cellSize / originalSize

    scaledCoords = []
    for x, y in coords:
        scaled_x = (x - 250) * size_factor  # Center around (250, 300) before scaling
        scaled_y = (y - 300) * size_factor
        scaled_x += center_x
        scaled_y += center_y
        scaledCoords.append((scaled_x, scaled_y))

    L = []
    for x, y in scaledCoords:
        L.append(x)
        L.append(y)

    M = copy.copy(L)
    for i in range(0, len(L)):
        if i % 2 == 0:
            M[i] += 4  

    drawPolygon(*M, fill="black")        
    drawPolygon(*L, fill="white", border="black") 

def draw_o(app, center_x, center_y, cellSize):
    outer_radius = 170
    middle_radius = 160
    inner_radius_black = 100
    inner_radius_white = 90  # smaller white circle for contrast

    # Calculate the scaling factor to fit the O within the cell
    original_size = outer_radius * 2 
    size_factor = cellSize / original_size

    # ALL OF THIS IS MY ORIGINAL SETUP OF THE CIRCLE, I SCALE BELOW
    
    # Scale radii
    scaled_outer_radius = outer_radius * size_factor
    scaled_middle_radius = middle_radius * size_factor
    scaled_inner_radius_black = inner_radius_black * size_factor
    scaled_inner_radius_white = inner_radius_white * size_factor

    # repositioned to center at x,y
    drawCircle(center_x, center_y, scaled_outer_radius, fill='black')
    drawCircle(center_x - 8, center_y, scaled_middle_radius, fill='white', border="black") 
    drawCircle(center_x - 8, center_y, scaled_inner_radius_black, fill='black') 
    drawCircle(center_x - 4, center_y, scaled_inner_radius_white, fill='white', border="black")  


def drawGrid():
    for i in range(1,gridSize):
        
        if i % 3 == 0: # thick lines
           drawLine(i * cellSize + 50, 100, i *cellSize + 50, windowSize + 100, fill='black', lineWidth=5)
           drawLine(50, i * cellSize + 100, windowSize + 50, i * cellSize + 100, fill='black', lineWidth=5)
        else: 
            drawLine(i * cellSize + 50, 100, i * cellSize + 50, windowSize + 100, fill='black', lineWidth=2)
            drawLine(50, i * cellSize + 100, windowSize + 50, i * cellSize + 100, fill='black', lineWidth=2)
    


def drawMarks(app):
    for boardIndex in range(9):
        boardRow = boardIndex // 3
        boardCol = boardIndex % 3
        boardX = boardCol * 3 * cellSize + 50 # Top left
        boardY = boardRow * 3 * cellSize + 100 # Top Right

        winner = app.globalBoard[boardIndex]
        if winner != ' ':
            if winner == 'X':
                draw_x(app,boardX + 3 * cellSize // 2,boardY + 3 * cellSize // 2,129)
            else:
                draw_o(app,boardX + 3 * cellSize // 2,boardY + 3 * cellSize // 2,129)

            continue
        

        for row in range(3):
            for col in range(3):
                mark = app.localBoards[boardIndex][row][col]
                if mark != ' ':
                    x = boardX + col * cellSize + cellSize // 2  # cellsize//2 is for centering, col * cellSize is for manuevering   
                    y = boardY + row * cellSize + cellSize // 2 

                    if mark == 'X':
                        draw_x(app,x,y,43)
                    if mark == 'O':
                        draw_o(app,x,y,43)




def checkWinner(board, current_player):
    for row in board:
        if row[0] == row[1] == row[2] == current_player:
            return True
    
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == current_player:
            return True
    
    if board[0][0] == board[1][1] == board[2][2] == current_player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == current_player:
        return True
    
    return False  

def checkWinnerGlobal(board,player):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for combo in winning_combinations:
        win = True
        for i in combo:
            if board[i] != player:
                win = False
        if win == True:
            return True
            
    return False


def onStep(app):
    if app.screen == "game" and not app.gameOver:
        app.timer -= 1
        if app.timer <= 0:
            app.currentPlayer = 'O' if app.currentPlayer == 'X' else 'X'
            app.activeBoard = None  
            app.timer = 30
    


def handleMove(app, x, y):
    if app.gameOver:
        return

    offsetX = 50
    offsetY = 100

    adjustedX = x - offsetX
    adjustedY = y - offsetY

    if adjustedX < 0 or adjustedX >= gridSize * cellSize or adjustedY < 0 or adjustedY >= gridSize * cellSize:
        return

    boardRow = int(adjustedY // (cellSize * 3))
    boardCol = int(adjustedX // (cellSize * 3))
    boardIndex = boardRow * 3 + boardCol

    if app.activeBoard is not None and app.activeBoard != boardIndex:
        return

    # Calculate the local cell coordinates within the board
    localRow = int((adjustedY % (cellSize * 3)) // cellSize)
    localCol = int((adjustedX % (cellSize * 3)) // cellSize)

    if app.localBoards[boardIndex][localRow][localCol] == ' ':
        app.localBoards[boardIndex][localRow][localCol] = app.currentPlayer

        if checkWinner(app.localBoards[boardIndex], app.currentPlayer):
            app.globalBoard[boardIndex] = app.currentPlayer
            app.boardWon = True

            if checkWinnerGlobal(app.globalBoard, app.currentPlayer):
                app.gameOver = True
                print(f'{app.currentPlayer} wins the game!')
        else:
            app.boardWon = False

        nextCellIndex = localRow * 3 + localCol
        if app.globalBoard[nextCellIndex] == ' ':
            app.activeBoard = nextCellIndex
        else:
            app.activeBoard = None

        app.currentPlayer = 'O' if app.currentPlayer == 'X' else 'X'

        app.timer = 30




#   GPT HELPED ME WRITE the available cells part
def aiMove(app):
    if app.gameOver:
        return

    if app.activeBoard is None:
        availableBoards = [
            boardIndex for boardIndex in range(9)
            if app.globalBoard[boardIndex] == ' '
        ]
        app.activeBoard = random.choice(availableBoards)

    # Find available cells in the active board
    availableCells = [
        (row, col) for row in range(3)
        for col in range(3)
        if app.localBoards[app.activeBoard][row][col] == ' '
    ]

    if availableCells:
        localRow, localCol = random.choice(availableCells)

        app.localBoards[app.activeBoard][localRow][localCol] = app.currentPlayer

        if checkWinner(app.localBoards[app.activeBoard], app.currentPlayer):
            app.globalBoard[app.activeBoard] = app.currentPlayer

            if checkWinnerGlobal(app.globalBoard, app.currentPlayer):
                app.gameOver = True  
                print(f'{app.currentPlayer} wins the demo! Returning to menu...')
                app.screen = "menu"  

        # Update the active board for the next turn
        nextCellIndex = localRow * 3 + localCol
        if app.globalBoard[nextCellIndex] == ' ':
            app.activeBoard = nextCellIndex
        else:
            app.activeBoard = None

        app.currentPlayer = 'X'

def is_draw(board):
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    
    return not checkWinner(board, 'X') and not checkWinner(board, 'O')


import copy

def getPossibleMoves(board, activeBoard):
    moves = []
    
    if activeBoard is None:
        for board_idx in range(9):
            for i in range(3):
                for j in range(3):
                    if board[board_idx][i][j] == ' ':
                        moves.append((board_idx, i, j))
    else:
        for i in range(3):
            for j in range(3):
                if board[activeBoard][i][j] == ' ':
                    moves.append((activeBoard, i, j))
    
    # Sort moves by distance from center for move ordering
    moves.sort(key=distanceFromCenter)
    
    return moves

def distanceFromCenter(move):
    board_idx, row, col = move
    board_row = board_idx // 3
    board_col = board_idx % 3
    
    center_row = board_row * 3 + 1
    center_col = board_col * 3 + 1
    
    return abs(row - 1 + board_row * 3 - center_row) + abs(col - 1 + board_col * 3 - center_col)

def makeMove(board, move, player):
    board_idx, row, col = move
    newBoard = copyBoard(board)
    newBoard[board_idx][row][col] = player
    return newBoard

def copyBoard(board):
    return [[[cell for cell in row] for row in local_board] for local_board in board]

def copyGlobalBoard(global_board):
    return [cell for cell in global_board]


def evaluateBoard(board, globalBoard):
    for player in ['O', 'X']:
        for i in range(3):
            if globalBoard[i*3] == globalBoard[i*3+1] == globalBoard[i*3+2] == player:
                return 100 if player == 'O' else -100
            if globalBoard[i] == globalBoard[i+3] == globalBoard[i+6] == player:
                return 100 if player == 'O' else -100

        # Diagonals
        if globalBoard[0] == globalBoard[4] == globalBoard[8] == player:
            return 100 if player == 'O' else -100
        if globalBoard[2] == globalBoard[4] == globalBoard[6] == player:
            return 100 if player == 'O' else -100

    score = 0

    score += globalBoard.count('O') * 10
    score -= globalBoard.count('X') * 10

    # Strategic board control
    strategic_boards = [4, 0, 2, 6, 8]  # Center and corners are prioritized
    for board_idx in strategic_boards:
        if globalBoard[board_idx] == ' ':
            local_board = board[board_idx]
            o_count = 0
            x_count = 0
            for row in local_board:
                o_count += row.count('O')
                x_count += row.count('X')
            if o_count > 0 and x_count == 0:
                score += 5  
            elif x_count > 0 and o_count == 0:
                score -= 5  

    # Add score based on the number of open boards in the globalBoard
    score += globalBoard.count(' ')

    strategic_spots = [
        (1, 1), 
        (0, 0), (0, 2), (2, 0), (2, 2),  
        (0, 1), (1, 0), (1, 2), (2, 1)   
    ]
    
    for spot in strategic_spots:
        if board[spot[0]][spot[1]] == ' ':
            score += 3

    return score

def minimax(depth, board, globalBoard, alpha, beta, maximizer, maxDepth, activeBoard,app):
    # Check terminal states
        
    global_winner = checkWinnerGlobal(app.globalBoard,app.currentPlayer)

    if global_winner:
        return 100 if global_winner == 'O' else -100
    
    if depth >= maxDepth:
        return evaluateBoard(board, globalBoard)
    
    # Determine player
    player = 'O' if maximizer else 'X'
    
    # Get possible moves
    possible_moves = getPossibleMoves(board, activeBoard)
    
    if maximizer:
        max_eval = float('-inf')
        for move in possible_moves:
            # Make a copy of the board
            new_board = makeMove(board, move, player)
            
            # Check if local board is won
            local_winner = checkWinner(new_board[move[0]],app.currentPlayer)
            new_global_board = copyGlobalBoard(globalBoard)
            
            if local_winner:
                new_global_board[move[0]] = local_winner
            
            # Determine next active board
            next_active_board = move[1] * 3 + move[2] if local_winner is None else None
            
            # Recursive call
            eval_score = minimax(depth + 1, new_board, new_global_board, alpha, beta, False, maxDepth, next_active_board,app)
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in possible_moves:
            # Make a copy of the board
            new_board = makeMove(board, move, player)
            
            # Check if local board is won
            local_winner = checkWinner(new_board[move[0]],app.currentPlayer)
            new_global_board = copyGlobalBoard(globalBoard)
            
            if local_winner:
                new_global_board[move[0]] = local_winner
            
            # Determine next active board
            next_active_board = move[1] * 3 + move[2] if local_winner is None else None
            
            # Recursive call
            eval_score = minimax(depth + 1, new_board, new_global_board, alpha, beta, True, maxDepth, next_active_board,app)
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            
            if beta <= alpha:
                break
        return min_eval

def find_best_move(board, globalBoard, maxDepth, activeBoard,app):
    bestValue = float('-inf')
    bestMoves = []
    
    for move in getPossibleMoves(board, activeBoard):
        new_board = makeMove(board, move, 'O')
        
        # Check if local board is won
        local_winner = checkWinner(new_board[move[0]],app.currentPlayer)
        new_global_board = copyGlobalBoard(globalBoard)
        
        if local_winner:
            new_global_board[move[0]] = local_winner
        
        # Determine next active board
        next_active_board = move[1] * 3 + move[2] if local_winner is None else None
        
        moveVal = minimax(5, new_board, new_global_board, float('-inf'), float('inf'), False, maxDepth, next_active_board,app)

        if moveVal > bestValue:
            bestValue = moveVal
            bestMoves = [move]
        elif moveVal == bestValue:
            bestMoves.append(move)
    
    # Randomly choose from best moves if multiple exist
    if bestMoves != None:
        if app.activeBoard != None and checkTwoInARow(app.localBoards[app.activeBoard],app.currentPlayer,app.activeBoard) != None:
            return checkTwoInARow(app.localBoards[app.activeBoard],app.currentPlayer,app.activeBoard)
        else:
            return random.choice(bestMoves)
    else:
        return None


def checkTwoInARow(board, player, activeBoard):

    # Check rows for two-in-a-row
    for i in range(3):
        if board[i][0] == board[i][1] == player and board[i][2] == ' ':
            return (activeBoard, i, 2)  # Empty spot to complete the row
        if board[i][1] == board[i][2] == player and board[i][0] == ' ':
            return (activeBoard, i, 0)
        if board[i][0] == board[i][2] == player and board[i][1] == ' ':
            return (activeBoard, i, 1)

    # Check columns for two-in-a-row
    for j in range(3):
        if board[0][j] == board[1][j] == player and board[2][j] == ' ':
            return (activeBoard, 2, j)
        if board[1][j] == board[2][j] == player and board[0][j] == ' ':
            return (activeBoard, 0, j)
        if board[0][j] == board[2][j] == player and board[1][j] == ' ':
            return (activeBoard, 1, j)

    # Check diagonals for two-in-a-row
    if board[0][0] == board[1][1] == player and board[2][2] == ' ':
        return (activeBoard, 2, 2)
    if board[1][1] == board[2][2] == player and board[0][0] == ' ':
        return (activeBoard, 0, 0)
    if board[0][0] == board[2][2] == player and board[1][1] == ' ':
        return (activeBoard, 1, 1)
    if board[0][2] == board[1][1] == player and board[2][0] == ' ':
        return (activeBoard, 2, 0)
    if board[1][1] == board[2][0] == player and board[0][2] == ' ':
        return (activeBoard, 0, 2)
    if board[0][2] == board[2][0] == player and board[1][1] == ' ':
        return (activeBoard, 1, 1)

    # No two-in-a-row found
    return None


def singlePlayerAiMove(app, maxDepth=3):
    if app.gameOver:
        return


    if app.activeBoard == None:
        for i in range(0,len(app.globalBoard)):
            if app.globalBoard[i] == ' ':
                bestMove = find_best_move(app.localBoards, app.globalBoard, maxDepth, i, app)
                break
    # Find the best move
    else:
        bestMove = find_best_move(app.localBoards, app.globalBoard, maxDepth, app.activeBoard, app)

    if bestMove is not None:
        boardIndex, row, col = bestMove

        app.localBoards[boardIndex][row][col] = 'O'

        local_winner = checkWinner(app.localBoards[boardIndex], 'O')
        if local_winner:
            app.globalBoard[boardIndex] = 'O'

        global_winner = checkWinnerGlobal(app.globalBoard, 'O')
        if global_winner:
            app.gameOver = True
            print(f'AI wins the game!')
            app.screen = "menu"
        
        next_board = row * 3 + col
        
        if app.globalBoard[next_board] != ' ' or all(app.localBoards[next_board][r][c] != ' ' for r in range(3) for c in range(3)):
            app.activeBoard = None  
        else:
            app.activeBoard = next_board

        if app.globalBoard[next_board] != ' ':
            app.activeBoard = None  

        app.currentPlayer = 'X'

def onMousePress(app, mouseX, mouseY):
    centerX = 275
    buttonWidth = 200
    buttonHeight = 50
    buttonSpacing = 50

    playY = 90 + 80
    instructionsY = playY + buttonHeight + buttonSpacing
    quitY = instructionsY + buttonHeight + buttonSpacing
    creditsY = quitY + buttonHeight + buttonSpacing

    if app.screen == "menu":
        if centerX - buttonWidth // 2 <= mouseX <= centerX + buttonWidth // 2 and playY <= mouseY <= playY + buttonHeight:
            app.screen = "game"
        elif centerX - buttonWidth // 2 <= mouseX <= centerX + buttonWidth // 2 and instructionsY <= mouseY <= instructionsY + buttonHeight:
            app.screen = "instructions"
        elif centerX - buttonWidth // 2 <= mouseX <= centerX + buttonWidth // 2 and quitY <= mouseY <= quitY + buttonHeight:
            app.quit()
        elif centerX - buttonWidth // 4 <= mouseX<= centerX + buttonWidth // 4 and creditsY <= mouseY <= creditsY + buttonHeight // 2:
            app.screen = "credits"
        
    elif app.screen == "game":
        if 10 <= mouseX <= 60 and 10 <= mouseY <= 35:
            app.screen = "menu"
            app.gameOver = False
            return

        if not app.doSettings:
            controlSettings(app,mouseX,mouseY)
        else:
            if app.gameOver:
                app.screen = "menu"  
                app.gameOver = False
                clearBoard(app)
                app.doSettings = False
            else:
                if app.isMultiplayer and app.doSettings:
                    handleMove(app, mouseX, mouseY)
                if not app.isMultiplayer:
                    if app.currentPlayer == 'O':
                        singlePlayerAiMove(app,3)
                    else:
                        handleMove(app,mouseX,mouseY)

    elif app.screen == "instructions":
        if 50 <= mouseX <= 150 and 400 <= mouseY <= 450:
            app.screen = "menu"
        if 400 <= mouseX <= 500 and 400 <= mouseY <= 450:
            app.screen = "demo"
            if app.gameOver:
                app.gameOver = False
                app.currentPlayer = 'X'

    elif app.screen == "demo":
        if 480 <= mouseX <= 530 and 10 <= mouseY <= 35:
            app.screen = "menu"
            return
        handleMove(app, mouseX, mouseY)
        if app.currentPlayer == 'O':
            aiMove(app)
        if app.gameOver == True:
            clearBoard(app)
            app.gameOver = not app.gameOver
    
    elif app.screen == "credits":
        if 225 <= mouseX <= 325 and 400 <= mouseY <= 450:
            app.screen = "menu"
    
def clearBoard(app):
    for i in range(len(app.localBoards)):
        for j in range(len(app.localBoards[i])):
            for k in range(len(app.localBoards[i][j])):
                app.localBoards[i][j][k] = ' '

    for i in range(len(app.globalBoard)):
        app.globalBoard[i] = ' '

def demoScreen(app):
    g = gradient('white', 'lightgreen', start='top')
    drawRect(0,0,550,550, fill=g)
    drawBoard(app)
    drawGrid()
    drawMarks(app)
    drawLabel(f'Current Player: {app.currentPlayer}', 250,50,size=25)

    drawRect(480, 10, 50, 25, fill='gray', border='black')
    drawLabel("Back", 505,22,size=15, fill='white')

    if app.activeBoard is not None and not app.gameOver:
        if app.currentPlayer == 'X':
            if app.boardWon:
                drawLabel("Nice Job! You have won a square!",300,510, size=13)
            activeRow = app.activeBoard // 3
            activeCol = app.activeBoard % 3
            drawRect(50 + activeCol * 3 * cellSize, activeRow * 3 * cellSize + 100,
                3 * cellSize, 3 * cellSize, fill=None, border='green', borderWidth=5)
            if not app.boardWon:
                drawLabel("Place your next move in the highlighted square.",300,540, size=16, fill='darkgreen')
        elif app.currentPlayer == 'O' and app.boardWon:
            drawLabel("The opponent has captured a square! Be careful!", 300, 560, size=14, fill='red')

    elif app.currentPlayer == 'X':
        if app.boardWon:
            drawLabel("You have won a square!",300,510, size=13, fill='darkgreen')
        drawLabel("No highlighted square means you can place anywhere.",275,540, size=14, fill='darkblue')

    else:
        drawLabel("You won the demo! Returning to main menu will reset.", 300 , 510, size=13, fill='purple')
        


    
def drawTimerBar(app):
    barWidth = (app.timer / 30) * 400  

    drawRect(100, 50, barWidth, 20, fill='lightgrey', border='black')  

    drawLabel(f"Time Left: {app.timer}s", 230, 40, size=15, bold=True,font = "Herculanum")  
    

def showSettings(app):
    g = gradient('white', 'lightpink', start='top')
    drawRect(0,0,550,550, fill=g)
    centerX = 275  
    titleY = 50   
    drawLabel("Settings", centerX, titleY, size=30, bold=True, fill="darkblue")

    modeY = 120
    drawLabel("Game Mode:", 150, modeY, size=20, fill="black", align="left")
    drawRect(centerX, modeY - 20, 150, 40, fill="white", border="black", borderWidth=2)
    drawLabel("Single Player" if not app.isMultiplayer else "Multiplayer", centerX + 75, modeY, size=15, fill="black", align="center")

    timerY = 200
    drawLabel("Use Timer:", 150, timerY, size=20, fill="black", align="left")
    drawRect(centerX, timerY - 20, 150, 40, fill="white", border="black", borderWidth=2)
    drawLabel("Off" if not app.useTimer else "On", centerX + 75, timerY, size=15, fill="black", align="center")

    buttonY = 300
    buttonWidth = 100
    buttonHeight = 50

    drawRect(centerX - 75 - buttonWidth, buttonY, buttonWidth, buttonHeight, fill="green", border="black", borderWidth=2)
    drawLabel("Save", centerX - 75 - (buttonWidth // 2), buttonY + buttonHeight // 2, size=20, fill="white", align="center")

    drawRect(centerX + 75, buttonY, buttonWidth, buttonHeight, fill="gray", border="black", borderWidth=2)
    drawLabel("Back", centerX + 75 + (buttonWidth // 2), buttonY + buttonHeight // 2, size=20, fill="white", align="center")


def controlSettings(app, mouseX, mouseY):
    centerX = 275
    buttonY = 300
    buttonWidth = 100
    buttonHeight = 50
    if centerX <= mouseX <= centerX + 150 and 100 <= mouseY <= 140:
        app.isMultiplayer = not app.isMultiplayer
    if centerX <= mouseX <= centerX + 150 and 180 <= mouseY <= 220:
        app.useTimer = not app.useTimer  
    if centerX - 75 - buttonWidth <= mouseX <= centerX - 75 and buttonY <= mouseY <= buttonY + buttonHeight:
        app.doSettings = True  
    if centerX + 75 <= mouseX <= centerX + 75 + buttonWidth and buttonY <= mouseY <= buttonY + buttonHeight:
        app.screen = "menu"  


def redrawAll(app):
    if app.screen == "menu":
        mainScreen(app)
    elif app.screen == "credits":
        credits()
    elif app.screen == "game":
        if not app.doSettings:
            showSettings(app)
            drawRect(10,10,50,25,fill='gray',border='black')
            drawLabel("Back",35,22,size=15,fill='white')
        else:
            bgColor = 'lightcyan' if app.isMultiplayer else 'lightcoral'
            drawRect(0,0,550,550, fill=bgColor)
            drawBoard(app)
            drawGrid()
            drawMarks(app)
            drawRect(10,10,50,25,fill='gray',border='black')
            drawLabel("Back",35,22,size=15,fill='white')
            if app.activeBoard is not None and not app.gameOver:
                activeRow = app.activeBoard // 3
                activeCol = app.activeBoard % 3
                drawRect(50 + activeCol * 3 * cellSize, activeRow * 3 * cellSize + 100,
                3 * cellSize, 3 * cellSize, fill=None, border='green', borderWidth=5)
            if app.useTimer:
                drawTimerBar(app)
            drawLabel(f"Current Player: {app.currentPlayer}", 250, 510, size=20, bold=True, fill="black")

            if app.gameOver == True:
                victoryColor = "gold" if app.currentPlayer == 'O' else "orange"
                winner = "O" if app.currentPlayer == 'X' else "X"
                drawRect(100,200,350,100, fill="white", border="black", borderWidth=5)
                drawLabel(f"{winner} wins!", 275, 250, size=40, fill=victoryColor, bold=True)
                drawLabel("Click anywhere to return to menu", 275, 280, size=15)
    elif app.screen == "instructions":
        instructionsScreen(app)
    elif app.screen == "demo":
        demoScreen(app)
        if app.gameOver == True:
            clearBoard(app)

def runApp(height, width):
    redrawAll()

cmu_graphics.runApp(height = 550, width = 550)
