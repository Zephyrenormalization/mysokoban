import pygame
from .box import Box, Wall
import random
from collections import defaultdict

class Player(pygame.sprite.Sprite):
    '''
    玩家类，继承自pygame.sprite.Sprite，用于推箱子
    '''
    def __init__(self, *group, x, y, game):
        super().__init__(*group)
        self.game = game
        self.image = pygame.image.load('pic/player.png')
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = pygame.Rect(x * 64, y * 64, 64, 64)
        self.rect.x = x * 64
        self.rect.y = y * 64
        self.x = x
        self.y = y
        
    def update(self,key = None):
        move = None
        if key:
            if key =='R':
                move = 64,0
            elif key == 'L':
                move = -64,0
            elif key == 'U':
                move = 0,-64
            elif key == 'D':
                move = 0,64
        if move:
            dx, dy = move[0]//64,move[1]//64
            target = self.y + dy, self.x + dx
            cur = self.y, self.x
            cur_element = self.game.screen[self.y, self.x]
            target_element = self.game.screen[self.y + dy, self.x + dx]
            if not (target_element and target_element.obj and not target_element.obj.can_move(move)):
                #判断可以移动那么更新参数   
                self.rect.x =  target[1] * 64
                self.rect.y = target[0] * 64
                self.y, self.x = target
                cur_element.obj = None
                cur_element.chr = '-' if not cur_element.ground else 'G'
                target_element.obj = self
                target_element.chr = 'P' if not target_element.ground else 'L'
                
                return 1
        return 0
    
    def __del__(self):
        self.kill()

class GeneratorPlayer(Player):
    '''
    这个生成玩家类用于生成操作，继承自Player，也就是拉箱子
    '''
    def __init__(self, *group, x, y, game=None,map = None):
        super().__init__(*group, x=x, y=y, game=game)
        self.map = map
        self.cur_state = ''
        self.states = defaultdict(int)
        self.prev_move = (0,0)
    
    def get_state(self):
        state = ''
        for y in range(self.game.screen.shape[0]):
            for x in range(self.game.screen.shape[1]):
                if self.game.screen[y, x]:
                    state += self.game.screen[y, x].chr
        return state

    def update(self,map_size):
        height, width = map_size
        replace_chrs = {
            'P':'-',
            'L':'G',
            'W':'P',
            'G':'L',
            'O':'G',
            'B':'-',
            '-':'P',
        }
        moves = [(64, 0), (-64, 0), (0, -64), (0, 64)]
        move = random.choices(
            moves,
            weights=[0.1 if m == self.prev_move else 1 for m in moves],
            k = 1
        )
        move = move[0]
        self.cur_state = self.get_state()
        self.states[self.cur_state] += 1
        cur_pos = self.y, self.x
        target = self.y + move[0]//64, self.x + move[1]//64
        reverse_target = self.y - move[0]//64, self.x - move[1]//64
        # 如果目标点出界,或者目标点是箱子，那么就不采纳这个移动，并且使下一次还是这个方向的概率降低
        if (target[1] <= self.game.pad_x or 
            target[0] <= self.game.pad_y or
            target[1] >= self.game.pad_x + width - 1 or 
            target[0] >= self.game.pad_y + height - 1 or
            (self.game.screen[target] and self.game.screen[target].chr in 'BO')):
            self.prev_move = move
            return
        # 如果这个随机的移动有效改变了地图，那么就采纳这个移动，并且改变game.screen
        # 我们不希望下一次的行动跟这次的行动刚好抵消，所以这样记录prev_move
        self.prev_move = -move[0], -move[1]
        self.game.screen[cur_pos].obj = None
        self.game.screen[cur_pos].chr = replace_chrs[self.game.screen[cur_pos].chr]
        self.game.screen[target].chr = replace_chrs[self.game.screen[target].chr]
        if self.game.screen[target].obj:
            self.game.screen[target].obj.kill()
        self.game.screen[target].obj = self
        
        #下面判断身后的情况，如果身后是箱子，那么就把箱子移动到现在的位置上（也就是拉）
        if  (self.game.screen[reverse_target].chr in 'BO'):
            self.game.screen[reverse_target].chr = replace_chrs[self.game.screen[reverse_target].chr]
            self.game.screen[reverse_target].obj.reverse_move(move)
        self.rect.x = target[1] * 64
        self.rect.y = target[0] * 64
        self.y, self.x = target





