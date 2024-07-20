import random
import time
import numpy as np
from .game import Game, GeneratorGame
from .player import GeneratorPlayer
import pygame

def play_generation(generatorGame,map_size):
    generatorGame.player.update(map_size)
    generatorGame.floor_group.draw(generatorGame.window)
    generatorGame.goal_group.draw(generatorGame.window)
    generatorGame.object_group.draw(generatorGame.window)
    pygame.display.update()
    pygame.time.delay(10)

def generate(window = None):
    path = './levels/lvl0.dat'
    random.seed(int(time.time()))
    valid = False
    while not valid:
        width = random.randint(6, 14)
        height = random.randint(6, 9)
        # 生成地图初始化全为墙
        map_string = np.full((height, width), 'W',dtype='<U1')
        boxes = 4
        boxes_hash = set()
        # 地图的最两端一定是墙
        player_pos = random.randint(1, height - 2), random.randint(1, width - 2)
        map_string[player_pos] = 'P'
        map_size = height, width
        # 生成箱子
        boxes_created = 0
        while boxes_created < boxes:
            box_pos = random.randint(1, height - 2), random.randint(1, width - 2)
            if box_pos in boxes_hash or box_pos == player_pos:
                continue
            # 先让箱子和目标点重合，这样可以通过后续算法使之有解
            map_string[box_pos] = 'O'
            boxes_hash.add(box_pos)
            boxes_created += 1
        # 后面通过反转游戏和拉箱子来生成地图
        generate_map = GeneratorGame(window,level=0)
        generate_map.load_floor()
        generate_map.load_screen(map_string)
        player = generate_map.player
        steps = height * width * random.randint(2, 4)
        while steps:
            play_generation(generate_map,map_size)
            # 如果同一个状态在hash表中重复多次则截止
            if player.states[player.cur_state] > 15:
                break
            steps -= 1
        slice_x = slice(generate_map.pad_x, generate_map.pad_x + width)
        slice_y = slice(generate_map.pad_y, generate_map.pad_y + height)
        matrix = generate_map.screen[slice_y, slice_x]
        player.kill()
        boxes_on_goal = np.sum(matrix == 'O')
        # 如果箱子数的一半以下在目标点上则认为是有效地图
        if boxes_on_goal < boxes//2:
            valid = True

            np.savetxt(path, matrix, fmt='%s')
        else:
            valid = False
        del generate_map
        

