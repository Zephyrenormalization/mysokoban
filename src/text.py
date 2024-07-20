import pygame

class Text():
    def __init__(self, window):
        self.window = window
        self.font = pygame.font.Font(None, 40)
        self.text = 'use arrow left and right to choose level, use `s` to solve, use `g` to generate level'
        self.text_surface = self.font.render(self.text, True, (255, 100, 100))
        self.rect = self.text_surface.get_rect()
        self.rect.x = 10
        self.rect.y = 10
    
    def draw(self):
        self.window.blit(self.text_surface, self.rect)