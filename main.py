import pygame
import solution 
import generation
from pygame import mixer

# Defining Static Variables 
MAZE_DIMENTIONS = (16, 16)
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
icon = pygame.image.load('./assets/logo.png')
name = pygame.image.load('./assets/name.png')
name = pygame.transform.smoothscale(name, (W_WIDTH / 2, (name.get_height() / name.get_width()) * W_WIDTH / 2))
player = pygame.transform.smoothscale(pygame.image.load('./assets/player.png'), (R_WIDTH - 10, R_WIDTH - 10))
isPlayerRight = True
finish = pygame.transform.smoothscale(pygame.image.load('./assets/Finish.png'), (R_WIDTH, R_WIDTH))


pygame.display.set_icon(icon)
finished = False
gameFinished = False
scene = None

maze, genStart, genFinish = generation.generate_maze()
keys = {'a': pygame.K_a, 'd': pygame.K_d, 'w': pygame.K_w, 's': pygame.K_s}
generate_current_position = genStart

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


def resetGeneration():
    global maze, genStart, genFinish, generate_current_position
    maze, genStart, genFinish = generation.generate_maze()
    generate_current_position = genStart

def drawHomeScreen(mouse_pos):
    screen.blit(name, ((W_WIDTH / 2) - (name.get_width() / 2), 100))

    buttonStartPos = (W_WIDTH / 2) - (name.get_width()  / 4)
    buttonEndPos = (W_WIDTH / 2) + (name.get_width()  / 4)
    buttonTopPos = 200 + name.get_height()
    buttonWidth = (name.get_width() // 2 ) 
    buttonHeight = 50
    
    # Buttons
    if buttonStartPos <= mouse_pos[0] <= buttonEndPos and buttonTopPos <= mouse_pos[1] <= buttonTopPos + buttonHeight: 
        generationBtn = pygame.draw.rect(screen, (0, 255, 154), [buttonStartPos, buttonTopPos, buttonWidth, buttonHeight])
    else: 
        generationBtn = pygame.draw.rect(screen, (0, 154, 255), [buttonStartPos, buttonTopPos, buttonWidth, buttonHeight]) 

    if buttonStartPos <= mouse_pos[0] <= buttonEndPos and buttonTopPos + 100 <= mouse_pos[1] <= buttonTopPos + 100 + buttonHeight: 
        solutionBtn = pygame.draw.rect(screen, (0, 255, 154), [buttonStartPos, buttonTopPos + 100, buttonWidth, buttonHeight]) 
    else: 
        solutionBtn = pygame.draw.rect(screen, (0, 154, 255), [buttonStartPos, buttonTopPos + 100, buttonWidth, buttonHeight]) 
    
    return generationBtn, solutionBtn


while not finished:
    screen.fill((139, 195, 75))

    if scene == None:
        mouse_position = pygame.mouse.get_pos()
        genBtn, solBtn = drawHomeScreen(mouse_position)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if genBtn.collidepoint(mouse_position):
                    scene = 'gen'
                elif solBtn.collidepoint(mouse_position):
                    scene = 'sol'

    elif scene == 'sol':
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
        if generate_current_position == genFinish:
            ding = mixer.Sound('./assets/ding-36029.mp3')
            ding.play()
            resetGeneration()

        availableMovements = []
        for cell in maze:
            if cell == generation.check_cell(maze, generate_current_position[0], generate_current_position[1]):
                cell.draw_current(screen, player)
                
                for key, value in cell.walls.items():
                    if value == False:
                        availableMovements.append(key)
            elif cell == generation.check_cell(maze, genStart[0], genStart[1]):
                cell.draw_start(screen)
            elif cell == generation.check_cell(maze, genFinish[0], genFinish[1]):
                cell.draw_finish(screen, finish)
            else:
                cell.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True

            if event.type == pygame.KEYDOWN:
                if event.key in list(keys.values()):
                    if event.key == pygame.K_a and 'left' in availableMovements:
                        if isPlayerRight:
                            isPlayerRight = not isPlayerRight
                            player = pygame.transform.flip(player, True, False) 
                        generate_current_position = generate_current_position[0], generate_current_position[1] - 1
                    elif event.key == pygame.K_w and 'top' in availableMovements:
                        generate_current_position = generate_current_position[0] - 1, generate_current_position[1]
                    elif event.key == pygame.K_s and 'bottom' in availableMovements:
                        generate_current_position = generate_current_position[0] + 1, generate_current_position[1]
                    elif event.key == pygame.K_d and 'right' in availableMovements:
                        if not isPlayerRight:
                            isPlayerRight = not isPlayerRight
                            player = pygame.transform.flip(player, True, False) 
                        generate_current_position = generate_current_position[0], generate_current_position[1] + 1

    pygame.display.flip()
pygame.quit()
