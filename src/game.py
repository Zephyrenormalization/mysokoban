import numpy as np
import pygame

from .floor import Floor
from .box import Box, Wall
from .player import Player, GeneratorPlayer
from .goal import Goal

# 设置默认game的窗口宽为64*20，高为64*15每个方块的大小为64*64
class Game:
    def __init__(self, window = None,width = 1280, height = 768, level = None, path = None):
        self.window = window
        self.level = level
        self.width = width
        self.height = height
        #创建screen数组用于存储地图元素
        self.screen = np.empty((self.height//64,self.width//64),dtype=Element)
        # 创建精灵组用于管理屏幕上的元素，方便逻辑处理和渲染
        self.floor_group = pygame.sprite.Group()
        self.object_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.goal_group = pygame.sprite.Group()
        self.map_size = None
        self.pad_x = 0
        self.pad_y = 0
       
        self.path = path or f'levels/lvl{level}.dat'
        self.load_floor()
        self.player = None
        if type(self) == Game:
            self.load_screen()
        
        
    def load_screen(self):
        try:
            with open(self.path) as f:
                lines = f.readlines()
                self.map_size = (len(lines),len(lines[0].strip().split()))
                # 引入pad的目的是让地图居中显示
                pad_x = (self.width//64 - self.map_size[1]-2)//2
                pad_y = (self.height//64 - self.map_size[0])//2
                self.pad_x = pad_x
                self.pad_y = pad_y
            with open(self.path) as f:    
                for y, line in enumerate(f):
                    for x, char in enumerate(line.strip().split()):
                        new_element = Element(char)
                        self.screen[y+pad_y, x+pad_x] = new_element
                        if char == 'P':
                            new_element.obj = Player(self.object_group, self.player_group,x = x+pad_x, y = y+pad_y, game = self)
                            self.player = new_element.obj
                        elif char == 'G':
                            new_element.ground = Goal(self.goal_group, x=x + pad_x, y=y + pad_y)
                        elif char == 'B':
                            new_element.obj = Box(self.object_group, x=x + pad_x, y=y + pad_y, game=self)    
                        elif char == 'W':
                            new_element.obj = Wall(self.object_group, x=x + pad_x, y=y + pad_y)
                        elif char == 'O':#箱子在目标点上
                            new_element.ground = Goal(self.goal_group, x=x + pad_x, y=y + pad_y)
                            new_element.obj = Box(self.object_group, x=x + pad_x, y=y + pad_y, game=self)
                        elif char == 'L':#玩家在目标点上
                            new_element.obj = Player(self.object_group, self.player_group,x = x+pad_x, y= y+pad_y, game = self)
                            self.player = new_element.obj
                            new_element.ground = Goal(self.goal_group, x=x + pad_x, y=y + pad_y)
                        
        except (OSError,ValueError) as e:
            print(e)
            self.clear_objects()
            return 

    #用于获取有效区域的切片
    def map_matrix(self):
        slice_x = slice(self.pad_x, self.pad_x + self.map_size[1])
        slice_y = slice(self.pad_y, self.pad_y + self.map_size[0])
        sliced = self.screen[slice_y, slice_x]
        matrix = np.empty((self.map_size), dtype='<U1')
        for h in range(len(sliced)):
            for w in range(len(sliced[0])):
                matrix[h, w] = sliced[h, w].chr
        return matrix

    def clear_objects(self):
        for sprite in self.floor_group:
            sprite.kill()
        for sprite in self.object_group:
            sprite.kill()

    def __del__(self):
        self.clear_objects()

    def load_floor(self):
        for y in range(self.height//64):
            for x in range(self.width//64):
                Floor(self.floor_group, x = x, y = y)

class Element:
    def __init__(self, chr,obj = None,ground = None):
        self.chr = chr
        self.obj = obj
        self.ground = ground

    def __str__(self):
        return self.chr
    
class GeneratorGame(Game):
    def __init__(self, window = None, width = 1280, height = 768, level = None):
        super().__init__(window = window, width = width, height = height, level = level,  path = None)
        self.pad_x = 0
        self.pad_y = 0

    # 覆写load_screen方法，用于生成地图,区别在于这里不需要读取文件，而是直接生成地图
    def load_screen(self,map):
        self.map_size = map.shape
        pad_x = (self.width//64 - self.map_size[1]-2)//2
        pad_y = (self.height//64 - self.map_size[0])//2
        self.pad_x = pad_x
        self.pad_y = pad_y
        for y in range(self.map_size[0]):
            for x in range(self.map_size[1]):
                char = map[y, x]
                new_element = Element(char)
                self.screen[y+pad_y, x+pad_x] = new_element
                if char == 'P':
                    new_element.obj = GeneratorPlayer(self.object_group, self.player_group,x = x+pad_x, y = y+pad_y, game = self)
                    self.player = new_element.obj
                elif char == 'G':
                    new_element.ground = Goal(self.goal_group, x=x + pad_x, y=y + pad_y)
                elif char == 'B':
                    new_element.obj = Box(self.object_group, x=x + pad_x, y=y + pad_y, game=self)    
                elif char == 'W':
                    new_element.obj = Wall(self.object_group, x=x + pad_x, y=y + pad_y)
                elif char == 'O':#箱子在目标点上
                    new_element.ground = Goal(self.goal_group, x=x + pad_x, y=y + pad_y) 
                    new_element.obj = Box(self.object_group, x=x + pad_x, y=y + pad_y, game=self)
                elif char == 'L':#玩家在目标点上
                    new_element.obj = GeneratorPlayer(self.object_group, self.player_group,x = x+pad_x, y= y+pad_y, game = self)
                    self.player = new_element.obj
                    new_element.ground = Goal(self.goal_group, x=x + pad_x, y=y + pad_y)