import pygame
import solution 
import generation
from pygame import mixer
import time
import pyttsx3

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
mixer.init()

screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
title = pygame.display.set_caption("Laybrinth Legend")
icon = pygame.image.load('./assets/logo.png')
name = pygame.image.load('./assets/logoReveal.jpg')
name = pygame.transform.smoothscale(name, (W_WIDTH / 2, (name.get_height() / name.get_width()) * W_WIDTH / 2))
player = pygame.transform.smoothscale(pygame.image.load('./assets/player.png'), (R_WIDTH - 10, R_WIDTH - 10))
isPlayerRight = True
finishIco = pygame.transform.smoothscale(pygame.image.load('./assets/Finish.png'), (R_WIDTH, R_WIDTH))
footprintIco = pygame.transform.smoothscale(pygame.image.load('./assets/footprint.png'), (R_WIDTH - 5, R_HEIGHT - 5))
my_font = pygame.font.SysFont('Comic Sans MS', 30)
mixer.music.load("./assets/bgm.mp3")
mixer.music.play()

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
    y = 0
    screen.blit(name, ((W_WIDTH / 2) - (name.get_width() / 2), 0))

    buttonStartPos = (W_WIDTH / 2) - (name.get_width()  / 4)
    buttonEndPos = (W_WIDTH / 2) + (name.get_width()  / 4)
    buttonTopPos = 50 + name.get_height() + y
    buttonWidth = (name.get_width() // 2 ) 
    buttonHeight = 50

    # Buttons
    solTxt = my_font.render("I'll solve", True, (27, 26, 50))
    if buttonStartPos <= mouse_pos[0] <= buttonEndPos and buttonTopPos <= mouse_pos[1] <= buttonTopPos + buttonHeight: 
        generationBtn = pygame.draw.rect(screen, (245, 247, 247), [buttonStartPos, buttonTopPos, buttonWidth, buttonHeight])
    else: 
        generationBtn = pygame.draw.rect(screen, (186, 183, 210), [buttonStartPos, buttonTopPos, buttonWidth, buttonHeight]) 
    screen.blit(solTxt, (generationBtn.center[0] - solTxt.get_width()/2, generationBtn.center[1] - solTxt.get_height()/2))

    genTxt = my_font.render("I'll create", False, (27, 26, 50))
    if buttonStartPos <= mouse_pos[0] <= buttonEndPos and buttonTopPos + 100 <= mouse_pos[1] <= buttonTopPos + 100 + buttonHeight: 
        solutionBtn = pygame.draw.rect(screen, (245, 247, 247), [buttonStartPos, buttonTopPos + 100, buttonWidth, buttonHeight]) 
    else: 
        solutionBtn = pygame.draw.rect(screen, (186, 183, 210), [buttonStartPos, buttonTopPos + 100, buttonWidth, buttonHeight]) 
    screen.blit(genTxt, (solutionBtn.center[0] - genTxt.get_width()/2, solutionBtn.center[1] - genTxt.get_height()/2))
    
    return generationBtn, solutionBtn

startTime = None
def switchScene(currentScene):
    global startTime
    if currentScene == "gen":
        newScene = "sol"
    elif currentScene == "sol":
        newScene = "gen"
        startTime = time.time()
    return newScene


while not finished:
    screen.fill((139, 195, 75))

    if scene == None:
        screen.fill((27, 26, 50))
        mouse_position = pygame.mouse.get_pos()
        genBtn, solBtn = drawHomeScreen(mouse_position)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if genBtn.collidepoint(mouse_position):
                    scene = 'gen'
                    startTime = time.time()
                elif solBtn.collidepoint(mouse_position):
                    scene = 'sol'

    elif scene == 'sol':
        rectangles = solution.draw_rectangles(screen, start, finish, walls, path, finishIco, footprintIco)
        mouse_position = pygame.mouse.get_pos()
        start_button, finish_button, solve_button, reset_button, sceneChange_button = solution.draw_buttons(screen, mouse_position, my_font)
        
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
                if sceneChange_button.collidepoint(mouse_position):
                    scene = switchScene(scene)
                if reset_button.collidepoint(mouse_position):
                    walls = set()
                    path = set()
                    start = None
                    finish = None
                for rectangle in rectangles:  
                    if rectangle.collidepoint(mouse_position):
                        setRectangle(rectangles.index(rectangle))

    elif scene == 'gen':
        now = time.time()
        duration = now - startTime
        if generate_current_position == genFinish:
            startTime = time.time()
            ding = mixer.Sound('./assets/ding-36029.mp3')
            ding.play()
            resetGeneration()

        timerText = my_font.render("{}s".format(round(duration, 2)), True, (255, 255, 255))
        screen.blit(timerText, (R_WIDTH * MAZE_DIMENTIONS[0] + 80, W_HEIGHT/2 - 100))
        modeButtonTxt = my_font.render("I'll Create", True, (255, 255, 255))
        mouse_pos = pygame.mouse.get_pos()
        if R_WIDTH * MAZE_DIMENTIONS[0] + 40 <= mouse_pos[0] <= R_WIDTH * MAZE_DIMENTIONS[0] + 40+140 and W_HEIGHT/2 <= mouse_pos[1] <= W_HEIGHT/2+40: 
            sceneChange_button = pygame.draw.rect(screen, (0, 255, 154), [R_WIDTH * MAZE_DIMENTIONS[0] + 40, W_HEIGHT/2, modeButtonTxt.get_width() + 40, 40]) 
        else: 
            sceneChange_button = pygame.draw.rect(screen, (0, 154, 255), [R_WIDTH * MAZE_DIMENTIONS[0] + 40, W_HEIGHT/2, modeButtonTxt.get_width() + 40, 40]) 
        screen.blit(modeButtonTxt, (sceneChange_button.center[0] - modeButtonTxt.get_width()/2, sceneChange_button.center[1] - modeButtonTxt.get_height()/2))


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
                cell.draw_finish(screen, finishIco)
            else:
                cell.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if sceneChange_button.collidepoint(mouse_pos):
                    print('SceneSwitch')
                    scene = switchScene(scene)
                    
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
