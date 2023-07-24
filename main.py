import pygame
from pygame import mixer
import sys
import time
import random
import math

WIDTH = 400
HEIGHT = 600

surface = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Press the space')

BG_COLOR = (255, 255, 255)

state = "game"
score = 0
space = False

pygame.init()
pygame.font.init()

surface.fill(BG_COLOR)
pygame.display.flip()

sp_image = pygame.image.load("assets/images/s_pressed.png").convert()
sr_image = pygame.image.load("assets/images/s_released.png").convert()
sp_image = pygame.transform.scale(sp_image, (200, 50))
sr_image = pygame.transform.scale(sr_image, (200, 50))

music_volume = 0
mixer.init()
mixer.music.load("assets/music.mp3")
mixer.music.set_volume(music_volume)
mixer.music.play()
pause = 0

text_font = None
font = pygame.font.Font(text_font, 36)

press_times = []

### Money from space
money = []
moneyX = []
moneyY = []
moneyV = []
moneyA = []
moneyG = []

moneyImg = pygame.image.load("assets/images/coin/coin.png")
moneyImg = pygame.transform.scale(moneyImg, (25, 25)).convert()

### shop 
shop_rect = pygame.Rect(100, 150, 200, 300)
shop_bg = (220, 220, 220)

def mf_space_create(moneyImg, money, moneyX, moneyY, moneyV, moneyA, moneyG):
    money.append(moneyImg)
    moneyX.append(random.randint(100, 275))
    moneyY.append(475)
    moneyV.append(random.uniform(10, 15))
    moneyA.append(random.uniform(60, 120))
    moneyG.append(0.5)

def mf_space_update(moneyX, moneyY, moneyV, moneyA, moneyG):
    dt = 1 / 60 
    for i in range(len(moneyX)):
        moneyX[i] += moneyV[i] * math.cos(math.radians(moneyA[i])) * dt
        moneyY[i] -= moneyV[i] * math.sin(math.radians(moneyA[i])) * dt - 0.5 * moneyG[i] * dt**2
    if len(money) >= 1:
        for i in range(len(money)-1, -1, -1):
            if moneyY[i] <= -20:
                money.pop(i)
                moneyX.pop(i)
                moneyY.pop(i)
                moneyV.pop(i)
                moneyA.pop(i)
                moneyG.pop(i)
    
    print(len(money))


def time_draw():
    clock_font = pygame.font.Font(text_font, 22)
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return clock_font.render(f'Time: {current_time}', True, (0, 0, 0))

def sp_draw(space):
    if space:
        surface.blit(sp_image, (100, 500))
    else:
        surface.blit(sr_image, (100, 500))

def update_press_times():
    current_time = pygame.time.get_ticks() // 1000
    global press_times
    press_times = [t for t in press_times if t >= current_time - 6] 

def count_presses_in_last_6_seconds():
    current_time = pygame.time.get_ticks() // 1000
    update_press_times()
    return round(len(press_times) / 6)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
            print("GAME: Exited by click")

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                running = False
                print("GAME: Exited by escape")

            if event.key == pygame.K_SPACE:
                space = True
                if state == "game":
                    score += 1
                    press_times.append(pygame.time.get_ticks() // 1000)
                    mf_space_create(moneyImg, money, moneyX, moneyY, moneyV, moneyA, moneyG)

            if event.key == pygame.K_LALT:
                if state == "game":
                    state = "shop"
                else:
                    state = "game"

            if event.key == pygame.K_x:
                if music_volume <= 1:
                    music_volume += 0.1
                mixer.music.set_volume(music_volume)

            if event.key == pygame.K_z:
                if music_volume >= 0:
                    music_volume -= 0.1    
                mixer.music.set_volume(music_volume)

            if event.key == pygame.K_c:
                if pause == 0:
                    mixer.music.pause()
                    pause = 1
                else:
                    mixer.music.unpause()
                    pause = 0 
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                space = False

    if state == "game":
        surface.fill(BG_COLOR)
        sp_draw(space)
        score_text = font.render(f'Score: {score}', True, (0, 0, 0))
        pps_text = font.render(f'PPS: {count_presses_in_last_6_seconds()}', True, (0, 0, 0))
        clock_text = time_draw()

        mf_space_update(moneyX, moneyY, moneyV, moneyA, moneyG)

        for i in range(len(money)):
            surface.blit(money[i], (moneyX[i], moneyY[i]))

        surface.blit(score_text, (10, 10))
        surface.blit(clock_text, (290, 10))
        surface.blit(pps_text, (10, 30))
    elif state == "shop":
        surface.fill((255, 255, 255), (270, 0, 130, 30))
        pygame.draw.rect(surface, shop_bg, shop_rect)
        shop_text = font.render("Shop", True, (0, 0, 0))
        surface.blit(shop_text, (100, 150))
        clock_text = time_draw()
        surface.blit(clock_text, (290, 10))

    pygame.display.flip()