import pygame

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 25)

def text(screen, text, color, position):
    text_surface = my_font.render(text, True, color)
    screen.blit(text_surface, position)

def button(screen, mouse_position, position, text, size = None):
    text_surface = my_font.render(text, True, (255, 255, 255))
    if not size:
        size = (text_surface.get_width() + 40, text_surface.get_height() + 10)

    if position[0] <= mouse_position[0] <= position[0] + size[0] and position[1] <= mouse_position[1] <= position[1] + size[1]: 
        button = pygame.draw.rect(screen, (0, 255, 154), [position[0], position[1], size[0], size[1]]) 
    else: 
        button = pygame.draw.rect(screen, (0, 154, 255), [position[0], position[1], size[0], size[1]]) 
    screen.blit(text_surface, (button.center[0] - text_surface.get_width()/2, button.center[1] - text_surface.get_height()/2))

    return button