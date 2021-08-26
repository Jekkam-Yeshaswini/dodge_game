# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 22:01:20 2021

@author: hp
"""
import pygame
import sys
import random

pygame.init()

WIDTH = 800
HEIGHT = 600


player_size = 50
player_position = (WIDTH/2, HEIGHT - 2*player_size)
STEP_SIZE = 50

enemy_size = 50
enemy_position = [random.randint(0,WIDTH-enemy_size), 0]
SPEED = 10
enemy_list = [enemy_position]

score = 0
myFont = pygame.font.SysFont('monospace', 35)

# create a screen with pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# set a frame rate for the game
clock = pygame.time.Clock()

# create a game loop
game_over = False

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, WIDTH-enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])
        
def draw_enemies(enemy_list):
    for enemy_position in enemy_list:
        pygame.draw.rect(screen, 'yellow', (enemy_position[0],enemy_position[1], enemy_size, enemy_size))
    
def update_enemy_pos(enemy_list, score):
    for idx, enemy_position in enumerate(enemy_list): 
        if enemy_position[1] >= 0 and enemy_position[1] < HEIGHT:
            enemy_position[1] += SPEED
        else:
            enemy_list.pop(idx)
            score += 1
    return score
            
def check_collision(enemy_list, player_position):
    for enemy_position in enemy_list:
        if detect_collision(player_position, enemy_position):
            return True
    return False
        
        
def detect_collision(player_position, enemy_position):
    p_x = player_position[0]
    p_y = player_position[1]
    
    e_x = enemy_position[0]
    e_y = enemy_position[1]
    
    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y +enemy_size)):
            return True
    return False
def set_level(score, SPEED):
    SPEED = score/6 + 5
    return SPEED
        
while not game_over:
    for event in pygame.event.get():
        
        # quit event
        if event.type == pygame.QUIT:
            sys.exit(1)
           
        # move player on keypress
        if event.type == pygame.KEYDOWN:
            x = player_position[0]
            y = player_position[1]
            
            if event.key == pygame.K_RIGHT:
                x += STEP_SIZE
            elif event.key == pygame.K_LEFT:
                x -= STEP_SIZE
            player_position = [x,y]
            
        
            
    screen.fill('blue')     
    
     # set player
    pygame.draw.rect(screen, 'red', (player_position[0], player_position[1], player_size, player_size))
    
    # set enemy   
    drop_enemies(enemy_list)
    score = update_enemy_pos(enemy_list, score)
    SPEED = set_level(score, SPEED)
    text = "Score:" + str(score)
    label = myFont.render(text, 1, 'green')
    screen.blit(label, (WIDTH - 200, HEIGHT - 40))
    
    if check_collision(enemy_list, player_position):
        game_over = True
        break
    draw_enemies(enemy_list)    
    
    clock.tick(30)
    pygame.display.update()