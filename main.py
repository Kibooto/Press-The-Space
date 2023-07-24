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

clock = pygame.time.Clock()

surface.fill(BG_COLOR)
pygame.display.flip()

sp_image = pygame.image.load("assets/images/s_pressed.png").convert()
sr_image = pygame.image.load("assets/images/s_released.png").convert()
sp_image = pygame.transform.scale(sp_image, (200, 50))
sr_image = pygame.transform.scale(sr_image, (200, 50))

music_volume = 0.4
mixer.init()
mixer.music.load("assets/music.mp3")
mixer.music.set_volume(music_volume)
mixer.music.play()
pause = 0

text_font = None
font = pygame.font.Font(text_font, 36)
shop_font = pygame.font.Font(text_font, 28)
clock_font = pygame.font.Font(text_font, 22)

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
shop_rect = pygame.Rect(50, 150, 300, 300)
shop_bg = (220, 220, 220)

class Item:
    def __init__(self, name, price, level, max_level, price_mult, kkey):
        self.name = name
        self.price = price
        self.level = level
        self.max_level = max_level
        self.price_mult = price_mult
        self.kkey = kkey

class Shop:
    def __init__(self):
        self.items = []
        self.items.append(Item("Coin doubler", 100, 0, 10, 1.2, "Q"))
        self.items.append(Item("Coin price", 70, 0, 10, 1.1, "W"))
    
    def show(self):
        surface.fill((255, 255, 255), (270, 0, 130, 30))
        pygame.draw.rect(surface, shop_bg, shop_rect)
        shop_text = font.render("Shop", True, (0, 0, 0))
        surface.blit(shop_text, (50, 150))
        clock_text = time_draw()
        surface.blit(clock_text, (290, 10))

        text_y = 200
        for item in self.items:
            item_text = shop_font.render(f"{item.level}/{item.max_level} {item.name}: ${item.price}, press: {item.kkey}", True, (0, 0, 0))
            surface.blit(item_text, (50, text_y))
            text_y += 40
        
        pygame.display.flip()
        
    def process_purchase(self, item, score):
        if item.price <= score:
            if item.level < item.max_level:
                item.level += 1
                score -= item.price
                item.price = round(item.price * item.price_mult)
                print("bught 1 item")
            else:
                print("Max level")
            return score
        else:
            enought_money = shop_font.render("Not enought money!", True, (0, 0, 0))
            surface.blit(enought_money, (50, 400))


shop = Shop()

def mf_space_create(moneyImg, money, moneyX, moneyY, moneyV, moneyA, moneyG):
    for i in range(0, 1+shop.items[0].level):
        money.append(moneyImg)
        moneyX.append(random.randint(100, 275))
        moneyY.append(475)
        moneyV.append(random.uniform(60, 70))
        moneyA.append(random.uniform(60, 120))
        moneyG.append(0.5)

def mf_space_update(moneyX, moneyY, moneyV, moneyA, moneyG):
    dt = clock.tick(60) / 1000
    remove = []
    for i in range(len(moneyX)):
        moneyX[i] += moneyV[i] * math.cos(math.radians(moneyA[i])) * dt
        moneyY[i] -= moneyV[i] * math.sin(math.radians(moneyA[i])) * dt - 0.5 * moneyG[i] * dt**2

        if moneyY[i] < -20:
            remove.append(i)

    for index in reversed(remove):
        money.pop(index)
        moneyX.pop(index)
        moneyY.pop(index)
        moneyV.pop(index)
        moneyA.pop(index)
        moneyG.pop(index)

    return money

def time_draw():
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
                if state == "game":
                    pygame.quit()
                    running = False
                    print("GAME: Exited by escape")
                else:
                    state = "game"

            if event.key == pygame.K_SPACE:
                space = True
                if state == "game":
                    score += (1 + shop.items[0].level) * 1 + (0.4 * shop.items[1].level)
                    press_times.append(pygame.time.get_ticks() // 1000)
                    mf_space_create(moneyImg, money, moneyX, moneyY, moneyV, moneyA, moneyG)

            if event.key == pygame.K_LALT:
                if state == "game":
                    state = "shop"
                else:
                    state = "game"
            
            if event.key == pygame.K_q:
                if state == "shop":
                    new_score = shop.process_purchase(shop.items[0], score)
                    if new_score is not None:
                        score = new_score
            
            if event.key == pygame.K_w:
                if state == "shop":
                    new_score = shop.process_purchase(shop.items[1], score)
                    if new_score is not None:
                        score = new_score

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

            if event.key == pygame.K_v:
                score += 100000

            if event.key == pygame.K_b:
                shop.items[0].level += 50
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                space = False

    if state == "game":
        surface.fill(BG_COLOR)
        sp_draw(space)
        open_shop_text = clock_font.render(("Press ALT to open store"), True, (0, 0, 0))
        music_text = clock_font.render(("Music: Z - , X + , C ="), True, (0, 0, 0))
        score_text = font.render((f'Score: %.2f' %score), True, (0, 0, 0))
        pps_text = font.render(f'PPS: {count_presses_in_last_6_seconds()}', True, (0, 0, 0))
        clock_text = time_draw()

        money = mf_space_update(moneyX, moneyY, moneyV, moneyA, moneyG)

        money_len = font.render(f"Coins on screen: {len(money)}", True, (0, 0, 0))

        for i in range(len(money)):
            surface.blit(money[i], (moneyX[i], moneyY[i]))

        surface.blit(money_len, (10, 50))
        surface.blit(music_text, (250, 564))
        surface.blit(open_shop_text, (10, 564))
        surface.blit(score_text, (10, 10))
        surface.blit(clock_text, (290, 10))
        surface.blit(pps_text, (10, 30))
    elif state == "shop":
        shop.show()

    pygame.display.flip()