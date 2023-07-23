import pygame
import sys
import time
import random

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

text_font = None
font = pygame.font.Font(text_font, 36)

press_times = []

### Money from space
money = []
moneyX = []
moneyY = []
money_number = 0

moneyImg = pygame.image.load("assets/images/coin/coin.png")
moneyImg = pygame.transform.scale(moneyImg, (25, 25)).convert()

### shop 
shop_rect = pygame.Rect(100, 150, 200, 300)
shop_bg = (220, 220, 220)

def mf_space_create(moneyImg, money, moneyX, moneyY, money_number):
    money.append(moneyImg)
    moneyX.append(random.randint(100, 275))
    moneyY.append(475)
    money_number += 1
    for i in range(money_number):
        surface.blit(money[i], (moneyX[i],  moneyY[i]))

    for i in range(len(money)-1, -1, -1):
        if moneyY[i] <= 0:
            money.pop(i)
            moneyY.pop(i)
            moneyX.pop(i)
            money_number -= 1
    
    print(len(money))
    return money_number
    
def mf_space_update(money_number, moneyX, moneyY): ##
    for i in range(money_number):
        moneyY[i] -= 1/3
        moneyX[i] = moneyX[i] + random.uniform(-1,1)
        surface.blit(money[i], (moneyX[i], moneyY[i]))

    return 

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
            print("GAME: Exited by click")
            pygame.quit()
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("GAME: Exited by escape")
                pygame.quit()
                running = False

            if event.key == pygame.K_SPACE:
                space = True
                if state == "game":
                    score += 1
                    press_times.append(pygame.time.get_ticks() // 1000)
                    money_number = mf_space_create(moneyImg, money, moneyX, moneyY, money_number)

            if event.key == pygame.K_LALT:
                if state == "game":
                    state = "shop"
                else:
                    state = "game"

            if event.key == pygame.K_RETURN:
                print("Game: Open store")
                pass
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                space = False

    if state == "game":
            surface.fill(BG_COLOR)
            sp_draw(space)
            score_text = font.render(f'Score: {score}', True, (0, 0, 0))
            pps_text = font.render(f'PPS: {count_presses_in_last_6_seconds()}', True, (0, 0, 0))
            clock_text = time_draw()
            mf_space_update(money_number, moneyX, moneyY)
            surface.blit(score_text, (10, 10))
            surface.blit(clock_text, (290, 10))
            surface.blit(pps_text, (10, 30))

            pygame.display.flip()
        
    elif state == "shop":
        surface.fill((255,255,255), (270, 0, 130, 30))
        pygame.draw.rect(surface, shop_bg, shop_rect)
        shop_text = font.render("Shop", True, (0, 0, 0))
        surface.blit(shop_text, (100, 150))
        clock_text = time_draw()
        surface.blit(clock_text, (290, 10))
        pygame.display.flip()