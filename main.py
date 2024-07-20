import pygame
# import random
# import time
from src.text import Text
from src.astar import Astar 
from src.generator import generate
from src.game import Game

def play_solution(game, solution):
    for move in solution:
        game.player.update(move)
        game.floor_group.draw(game.window)
        game.goal_group.draw(game.window)
        game.object_group.draw(game.window)
        game.player_group.draw(game.window)
        pygame.display.flip()
        pygame.time.delay(150)
    pygame.display.flip()

def main():
    pygame.init()
    Logo = pygame.image.load('pic/logo.png')
    pygame.display.set_icon(Logo)
    window = pygame.display.set_mode((1280, 768))
    pygame.display.set_caption('sokoban')
    level = 19
    playing = True
    text = Text(window)

    while playing:
        game = Game(window=window, level=level)
        
        if not playing:
            pygame.quit()
            quit()
        game.floor_group.draw(window)
        game.goal_group.draw(window)
        game.object_group.draw(window)
        game.player_group.draw(window)
        text.draw()
        font = pygame.font.Font(None, 40)
        text_level = font.render(f'Level {level}', True, (100, 255, 100))
        window.blit(text_level, (100, 100))
        pygame.display.flip()
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                    wait = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        random = True
                        wait = False
                        level = 0 
                        generate(window)
                    if event.key == pygame.K_s:
                        wait = True
                        solution,time_cost = Astar(game)
                        font1 = pygame.font.Font(None, 40)
                        text_time = font1.render(f'Time cost {time_cost:.2f}s', True, (100, 100, 255))
                        window.blit(text_time, (100, 200))
                        pygame.display.flip()
                        play_solution(game, solution)
                    if event.key == pygame.K_LEFT and level > 1:
                        level -= 1
                        wait = False
                    if event.key == pygame.K_RIGHT and level < 20:
                        level += 1
                        wait = False

          

if __name__ == '__main__':
    main()