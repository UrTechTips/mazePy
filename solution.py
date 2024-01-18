import pygame
from search import *  
from utils import button
# Static variables related to generation
MAZE_DIMENTIONS = (16, 16)
R_HEIGHT = R_WIDTH = 50
W_WIDTH = R_WIDTH * MAZE_DIMENTIONS[0] + 25 + 25 + 200 # Width of maze + 25px on each side +200 -> For adding buttons and stuff
W_HEIGHT = R_HEIGHT * MAZE_DIMENTIONS[1] + 25 + 25

def solveMaze(path, walls, start, finish):
    breadthfs = BFS(MAZE_DIMENTIONS, start, finish, walls)
    solution = breadthfs.solve()
    currentPos = start

    print(solution[1::])
    for i in solution:
        if i == 'Right':
            currentPos = (currentPos[0], currentPos[1]+1)
        elif i == 'Left':
            currentPos = (currentPos[0], currentPos[1]-1)
        elif i == 'Up':
            currentPos = (currentPos[0]-1, currentPos[1])
        elif i == 'Down':
            currentPos = (currentPos[0]+1, currentPos[1])

        path.add(currentPos)


def draw_rectangles(screen, start, finish, walls, path, finish_icon, path_icon):
    left = 25
    top = 25
    rectangles = []
    # Display the rectangles
    for i in range(MAZE_DIMENTIONS[1]):
        for j in range(MAZE_DIMENTIONS[0]):
            if (i, j) == start:
                rectangle = pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(left, top, R_WIDTH, R_HEIGHT))
            elif (i, j) == finish:
                rectangle = pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(left, top, R_WIDTH, R_HEIGHT), -1)
                screen.blit(finish_icon, (rectangle.topleft[0], rectangle.topleft[1]))
            elif (i, j) in walls:
                rectangle = pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(left, top, R_WIDTH, R_HEIGHT))
            elif (i, j) in path:
                rectangle = pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(left, top, R_WIDTH, R_HEIGHT), -1)
                screen.blit(path_icon, (rectangle.topleft[0], rectangle.topleft[1]))
            else:
                rectangle = pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(left, top, R_WIDTH, R_HEIGHT), 2)
            rectangles.append(rectangle)
            left = left + R_WIDTH 
        top = top + R_HEIGHT
        left = 25
    
    return rectangles

def draw_buttons(screen, mouse_pos, my_font):
    startBtn = button(screen, mouse_pos, (R_WIDTH * MAZE_DIMENTIONS[0] + 80, W_HEIGHT/2 - 70), "S")
    finishBtn = button(screen, mouse_pos, (R_WIDTH * MAZE_DIMENTIONS[0] + 160, W_HEIGHT/2 - 70), "F")
    
    solveMazeBtn = button(screen, mouse_pos, (R_WIDTH * MAZE_DIMENTIONS[0] + 80, W_HEIGHT/2), 'Solve')
    resetBtn = button(screen, mouse_pos, (R_WIDTH * MAZE_DIMENTIONS[0] + 80, W_HEIGHT/2 + 70), 'Reset')
    sceneChange = button(screen, mouse_pos, (R_WIDTH * MAZE_DIMENTIONS[0] + 80, W_HEIGHT/2 + 140), "I'll Solve")

    return (startBtn, finishBtn, solveMazeBtn, resetBtn, sceneChange)

