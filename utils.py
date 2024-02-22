import pygame

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 25)

def text(screen, text, color, position, center = False, textSize = 25):
    textFont = pygame.font.SysFont('Comic Sans MS', textSize)
    text_surface = textFont.render(text, True, color)
    if center:
        screen.blit(text_surface, (position[0] - text_surface.get_width() // 2, position[1]))
    else:
        screen.blit(text_surface, position)


def button(screen, mouse_position, position, text, size = None, center = None):
    text_surface = my_font.render(text, True, (255, 255, 255))
    if not size:
        size = (text_surface.get_width() + 40, text_surface.get_height() + 10)

    if center:
        if position[0] - size[0] //2 <= mouse_position[0] <= position[0] - size[0] //2 + size[0] and position[1] <= mouse_position[1] <= position[1] + size[1]: 
            button = pygame.draw.rect(screen, (0, 255, 154), [position[0] - size[0] //2, position[1], size[0], size[1]]) 
        else: 
            button = pygame.draw.rect(screen, (0, 154, 255), [position[0] - size[0] //2, position[1], size[0], size[1]]) 
    else:
        if position[0] <= mouse_position[0] <= position[0] + size[0] and position[1] <= mouse_position[1] <= position[1] + size[1]: 
            button = pygame.draw.rect(screen, (0, 255, 154), [position[0], position[1], size[0], size[1]]) 
        else: 
            button = pygame.draw.rect(screen, (0, 154, 255), [position[0], position[1], size[0], size[1]]) 
    # Comment
    screen.blit(text_surface, (button.center[0] - text_surface.get_width()/2, button.center[1] - text_surface.get_height()/2))

    return button