import pygame
from random import choice

MAZE_DIMENTIONS = (8, 8)
R_HEIGHT = R_WIDTH = 50
W_WIDTH = R_WIDTH * MAZE_DIMENTIONS[0] + 25 + 25 + 200 # Width of maze + 25px on each side +200 -> For adding buttons and stuff
W_HEIGHT = R_HEIGHT * MAZE_DIMENTIONS[1] + 25 + 25

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.thickness = 4
        
    def draw(self, sc, start, finish, current):
        x, y = self.x * R_WIDTH, self.y * R_WIDTH

        if current:
            pygame.draw.rect(sc, pygame.Color('black'), [x, y, R_WIDTH, R_WIDTH])
        elif start:
            pygame.draw.rect(sc, pygame.Color('red'), [x, y, R_WIDTH, R_WIDTH])
        elif finish:
            pygame.draw.rect(sc, pygame.Color('blue'), [x, y, R_WIDTH, R_WIDTH])
        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('black'), (x, y), (x + R_WIDTH, y), self.thickness)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('black'), (x + R_WIDTH, y), (x + R_WIDTH, y + R_WIDTH), self.thickness)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('black'), (x + R_WIDTH, y + R_WIDTH), (x , y + R_WIDTH), self.thickness)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('black'), (x, y + R_WIDTH), (x, y), self.thickness)

    def get_rects(self):
        rects = []
        x, y = self.x * R_WIDTH, self.y * R_WIDTH
        if self.walls['top']:
            rects.append(pygame.Rect( (x, y), (R_WIDTH, self.thickness) ))
        if self.walls['right']:
            rects.append(pygame.Rect( (x + R_WIDTH, y), (self.thickness, R_WIDTH) ))
        if self.walls['bottom']:
            rects.append(pygame.Rect( (x, y + R_WIDTH), (R_WIDTH , self.thickness) ))
        if self.walls['left']:
            rects.append(pygame.Rect( (x, y), (self.thickness, R_WIDTH) ))
        return rects

    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * MAZE_DIMENTIONS[0]
        if x < 0 or x > MAZE_DIMENTIONS[0] - 1 or y < 0 or y > MAZE_DIMENTIONS[1] - 1:
            return False
        return self.grid_cells[find_index(x, y)]

    def check_neighbors(self, grid_cells):
        self.grid_cells = grid_cells
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False


def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False

def generate_maze():
    grid_cells = [Cell(col, row) for row in range(MAZE_DIMENTIONS[1]) for col in range(MAZE_DIMENTIONS[0])]
    current_cell = grid_cells[0]
    array = []
    break_count = 1
    start = (0, 0)
    posibleFinishes = []

    while break_count != len(grid_cells):
        current_cell.visited = True
        next_cell = current_cell.check_neighbors(grid_cells)
        if next_cell:
            next_cell.visited = True
            break_count += 1
            array.append(current_cell)
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif array:
            posibleFinishes.append(current_cell)
            current_cell = array.pop()

    finish = choice(posibleFinishes)
    return grid_cells, start, (finish.x, finish.y)


def check_cell(grid_cells, x, y):
    if x < 0 or x > MAZE_DIMENTIONS[0] - 1 or y < 0 or y > MAZE_DIMENTIONS[1] - 1:
        return False
    else:
        index = x * MAZE_DIMENTIONS[1] + y
        return grid_cells[index]