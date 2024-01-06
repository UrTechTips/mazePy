import pygame
import solution 
import generation

# Defining Static Variables 
MAZE_DIMENTIONS = (8, 8)
R_HEIGHT = R_WIDTH = 50
W_WIDTH = R_WIDTH * MAZE_DIMENTIONS[0] + 25 + 25 + 200 # Width of maze + 25px on each side +200 -> For adding buttons and stuff
W_HEIGHT = R_HEIGHT * MAZE_DIMENTIONS[1] + 25 + 25

walls = set()
path = set()
start = None
finish = None

isStartDefining = False
isFinishDefining = False

# Initialization
pygame.init()

screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
title = pygame.display.set_caption("Laybrinth Legend")
finished = False
gameFinished = False
scene = 'gen'

# Functions related to generation
def setRectangle(index):
    '''Run's when a rectangle is clicked. i.e. oka box ni click cheste adhi wall ani artham tesukuntundi'''
    global start, finish, isStartDefining, isFinishDefining
    
    if isStartDefining:
        start = (index // MAZE_DIMENTIONS[1], index % MAZE_DIMENTIONS[1])
        isStartDefining = False

    elif isFinishDefining:
        finish = (index // MAZE_DIMENTIONS[1], index % MAZE_DIMENTIONS[1])
        isFinishDefining = False

    else:
        print('Added wall at ({}, {})'.format(index // MAZE_DIMENTIONS[1], index % MAZE_DIMENTIONS[1]))
        walls.add((index // MAZE_DIMENTIONS[1], index % MAZE_DIMENTIONS[1]))

maze, genStart, genFinish = generation.generate_maze()
keys = {'a': pygame.K_a, 'd': pygame.K_d, 'w': pygame.K_w, 's': pygame.K_s}
generate_current_position = genStart

while not finished:
    screen.fill((125, 179, 75))

    if scene == 'sol':
        rectangles = solution.draw_rectangles(screen, start, finish, walls, path)
        mouse_position = pygame.mouse.get_pos()
        start_button, finish_button, solve_button, reset_button = solution.draw_buttons(screen, mouse_position)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if solve_button.collidepoint(mouse_position):
                    solution.solveMaze(path, walls, start, finish)
                if start_button.collidepoint(mouse_position):
                    print('start')
                    isStartDefining = True
                if finish_button.collidepoint(mouse_position):
                    print('finish')
                    isFinishDefining = True
                if reset_button.collidepoint(mouse_position):
                    walls = set()
                    path = set()
                    start = None
                    finish = None
                for rectangle in rectangles:  
                    if rectangle.collidepoint(mouse_position):
                        setRectangle(rectangles.index(rectangle))

    elif scene == 'gen':
        if gameFinished:
            scene = 'sol'
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
        else:
            if generate_current_position == genFinish:
                gameFinished = True

            availableMovements = []
            for cell in maze:
                if cell == generation.check_cell(maze, generate_current_position[0], generate_current_position[1]):
                    cell.draw(screen, False, False, True)
                    for key, value in cell.walls.items():
                        if value == False:
                            availableMovements.append(key)
                elif cell == generation.check_cell(maze, genStart[0], genStart[1]):
                    cell.draw(screen, True, False, False)
                elif cell == generation.check_cell(maze, genFinish[0], genFinish[1]):
                    cell.draw(screen, False, True, False)
                else:
                    cell.draw(screen, False, False, False)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True

                if event.type == pygame.KEYDOWN:
                    if event.key in list(keys.values()):
                        if event.key == pygame.K_a and 'left' in availableMovements:
                            generate_current_position = generate_current_position[0], generate_current_position[1] - 1
                        elif event.key == pygame.K_w and 'top' in availableMovements:
                            generate_current_position = generate_current_position[0] - 1, generate_current_position[1]
                        elif event.key == pygame.K_s and 'bottom' in availableMovements:
                            generate_current_position = generate_current_position[0] + 1, generate_current_position[1]
                        elif event.key == pygame.K_d and 'right' in availableMovements:
                            generate_current_position = generate_current_position[0], generate_current_position[1] + 1

    pygame.display.flip()
pygame.quit()
