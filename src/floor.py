import pygame

class Floor(pygame.sprite.Sprite):
    def __init__(self, *group, x, y):
        super().__init__(*group)
        self.image = pygame.image.load('pic/background.png')
        self.image = pygame.transform.scale(self.image, (64, 64))

        self.rect = pygame.Rect(x * 64, y * 64, 64, 64)
        self.rect.x = x * 64
        self.rect.y = y * 64
        self.x = x
        self.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def __del__(self):
        self.kill()
