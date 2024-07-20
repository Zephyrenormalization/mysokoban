import pygame

class Box(pygame.sprite.Sprite):
    def __init__(self, *group, x, y, game = None):
        super().__init__(*group)
        self.game = game
        self.image1 = pygame.image.load('pic/box.png')
        self.image1 = pygame.transform.scale(self.image1, (64, 64))
        #箱子在目标点上的图片
        self.image2 = pygame.image.load('pic/boxon.png')
        self.image2 = pygame.transform.scale(self.image2, (64, 64))
        self.image = self.image1 if game and not self.game.screen[y, x].ground else self.image2
        self.rect = pygame.Rect(x * 64, y * 64, 64, 64)
        self.rect.x = x * 64
        self.rect.y = y * 64
        self.x = x
        self.y = y
        
    def can_move(self, move):
        dx, dy = move[0]//64,move[1]//64
        target = self.x + dx, self.y + dy
        cur = self.x, self.y 
        cur_element = self.game.screen[self.y, self.x]
        target_element = self.game.screen[self.y + dy, self.x + dx]
        if not isinstance(target_element.obj, Box):
            # 如果目标点不是箱子或者墙（墙是箱子的子类），说明可以移动
            self.rect.x += dx * 64
            self.rect.y += dy * 64
            self.x += dx
            self.y += dy
            cur_element.obj = None
            cur_element.chr = '-' if not cur_element.ground else 'G'
            target_element.obj = self
            target_element.chr = 'B' if not target_element.ground else 'O'
            self.update_sprite()
            return True
        return False
    
    #由于是被拉的时候生效，所以无需判断目标位置的元素（之前肯定是人）
    def reverse_move(self, move):
        dy,dx = move[0]//64,move[1]//64
        target = self.x + dx, self.y + dy
        cur_element = self.game.screen[self.y, self.x]
        target_element = self.game.screen[self.y + dy, self.x + dx]
        self.rect.y,self.rect.x = target[1] * 64, target[0] * 64
        self.x, self.y = target
        cur_element.obj = None
        cur_element.chr = 'G' if cur_element.ground else '-'
        target_element.obj = self
        target_element.chr = 'O' if target_element.ground else 'B'
        self.update_sprite()
    
    def update_sprite(self):
        self.image = self.image2 if self.game.screen[self.y, self.x].ground else self.image1

    def __del__(self):
        self.kill()


class Wall(Box):
    def __init__(self, *group, x, y):
        super().__init__(*group, x=x, y=y)
        self.image = pygame.image.load('pic/wall.png')
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = pygame.Rect(x * 64, y * 64, 64, 64)
        self.rect.x = x * 64
        self.rect.y = y * 64
        self.x = x
        self.y = y

    def can_move(self, move):
        return False