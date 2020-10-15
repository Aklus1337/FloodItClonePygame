import random, pygame, sys, pygame.font
import tkinter as tk
from tkinter import messagebox as mb
from buttons import *
pygame.init()
boxSize = 20
FONT = pygame.font.SysFont('arial', 20, True)

WHITE    = (255, 255, 255)
BLACK    = (  0,   0,   0)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)

COLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, BLACK)

def drawBoard(board, width):
    for x in range(width):
        for y in range(width):
            left, top = leftTopPixelCoordOfBox(x, y, width)
            r, g, b = COLORS[board[x][y]]

            pygame.draw.rect(DISPLAYSURF, (r, g, b), (left, top, boxSize, boxSize))

def leftTopPixelCoordOfBox(boxx, boxy, width):
    # Returns the x and y of the left-topmost pixel of the xth & yth box.
    xmargin = int((WINDOWWIDTH - (width * boxSize)) / 2)
    ymargin = int((WINDOWHEIGHT - (width * boxSize)) / 2)
    return (boxx * boxSize + xmargin, boxy * boxSize + ymargin)

def printBoard(board, width):
    for i in range(0, width):
        for j in range(0, width):
            print(board[i][j], end=", ")
        print()

def floodFill(board, oldColor, newColor, x, y, width):
    # This is the flood fill algorithm.
    if oldColor == newColor or board[x][y] != oldColor:
        return
    board[x][y] = newColor # change the color of the current box

    if x > 0:
        floodFill(board, oldColor, newColor, x - 1, y, width) # on box to the left
    if x < width - 1:
        floodFill(board, oldColor, newColor, x + 1, y, width) # on box to the right
    if y > 0:
        floodFill(board, oldColor, newColor, x, y - 1, width) # on box to up
    if y < width - 1:
        floodFill(board, oldColor, newColor, x, y + 1, width) # on box to down

def generateBoard(width, n):
    #generate the board, gameboard is a square, WIDTH is amount of boxes on the side
    gameBoard = []
    for x in range(width):
        column = []
        for y in range (width):
            column.append(random.randint(0, n-1)) #n means the number of colours
        gameBoard.append(column)
    return gameBoard


def drawText(count):
    countText = FONT.render("Number of turns: " + str(count), False, BLACK)
    DISPLAYSURF.blit(countText, (600, 20))
    resetText = FONT.render("Change size of the board and reset: ", False, BLACK)
    DISPLAYSURF.blit(resetText, (40,20))
    difficulty = FONT.render("Difficulty", False, BLACK)
    DISPLAYSURF.blit(difficulty, (0, 150))



def hasWon(board, width):
    #if the entire board is the same color, player has won
    for x in range(0,width):
        for y in range(0, width):
            if board[x][y] != board[0][0]:
                return False #wrong color, player has to keep playing
    return True

def createButtons():
    buttons = []
    for x in range(1, 4):  # create 3 buttons for
        buttons.append(PyGameButton(RED, 275 + x * 50, 20, 30, 30, str(x * 10)))
    buttons.append(PyGameButton((255, 200, 255), 770, 0, 30, 30, "BG"))
    for x in range(3, 7):  # create 4 buttons, each for amount of colors
        buttons.append(PyGameButton(BLUE, 0, 100+25*x, 25,25, str(x), True))
    return buttons

def createPallete(nColors, width):
    pallete = []
    for x in range (nColors):
        pallete.append(Pallete(50*x, 750, x, width))
    return pallete

def gameLoop(width, nColors, bgColor):
    global COLORS, WINDOWWIDTH, WINDOWHEIGHT, DISPLAYSURF, FONT
    root = tk.Tk()
    root.withdraw()
    buttons = createButtons()
    pallete = createPallete(nColors, 50)

    FPS = 20

    WINDOWWIDTH = WINDOWHEIGHT = 800
    pygame.display.set_caption("Flood me!")
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    gameBoard = generateBoard(width, nColors) #generate based on the number of boxes in line and colors
    count = 0
    while True:
        DISPLAYSURF.fill(bgColor)

        for x in range (len(buttons)):
            buttons[x].draw(DISPLAYSURF)
        for x in range(len(pallete)):
            pallete[x].draw(DISPLAYSURF, COLORS)

        for event in pygame.event.get():
            mousePos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for x in range (len(buttons)): #check whether buttons were clicked
                    if buttons[x].isOver(mousePos)[0]: #check whether we click any of the buttons
                        second = buttons[x].isOver(mousePos)[1]
                        if type(second) is not list: #check if we dont click random background color button
                            if type(second) is str: #if said value is a string
                                gameLoop(int(second), nColors, bgColor)
                            else: #if we click one of the numbers that indicate amount of colors
                                gameLoop(width, second, bgColor)
                        else:
                            bgColor = second
                for x in range (len(pallete)):
                    if pallete[x].isOver(mousePos)[0] and pallete[x].isOver(mousePos)[1] != gameBoard[0][0]:
                        floodFill(gameBoard, gameBoard[0][0], pallete[x].isOver(mousePos)[1], 0, 0, width)
                        count+=1

            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            drawText(count)
            drawBoard(gameBoard, width)
            FPSCLOCK.tick(FPS)
            pygame.display.update()
            if hasWon(gameBoard, width):
                mb.showinfo("Reset", "Congratulations! You've won in " + str(count) + " turns!")
                gameLoop(width, nColors, bgColor)

gameLoop(20, 4, WHITE) #there will be 20 boxes at the start and 4 colors, default bg color is white