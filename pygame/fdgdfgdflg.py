# Создание окна игры

import random 
import pygame as  pg
import time
import sys


# Инициализация модулей Pygame
pg.init()


# Основные цвета
WHITE = (255, 255, 255)   # большие буквы - АТРИБУТЫ
RED = (255, 0, 0)
BLUE = (0, 255, 0)
BLACK = (0, 0, 0)


# Размеры экрана
SCREEN_WIDTH = 1111
SCREEN_HEIGHT = 777



# Создание экрана
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Реквием")
background_image = pg.image.load("hacker.jpg")


font_style = pg.font.Font(None, 25)
score_font = pg.font.Font(None, 35)


# Инициализация таймера
start_time = pg.time.get_ticks()  # время в миллисекундах
elapsed_time = 0

font = pg.font.Font(None, 36)


# Определение текста меню
particle = score_font.render('Меню', True, RED)
paragraph_menu1 = font_style.render('1. Начать игру', True, BLACK)
paragraph_menu2 = font_style.render('2. Настройки', True, BLACK)
paragraph_menu3 = font_style.render('3. Выйти', True, BLACK)

# Определение позиций текста меню
    # position_prg = (SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2 - particle.get_width() // 2, 50)
         # position_prg1 = (SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2 - paragraph_menu1.get_width() // 2, 150)
        #position_prg2 = (SCREEN_HEIGHT // 2,SCREEN_WIDTH //2 - paragraph_menu2.get_width() // 2, 200)
        #position_prg3 = (SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2 - paragraph_menu3.get_width() // 2, 250)







# Определение классов
class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((30, 30))   # размеры игрока на экране
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.level = 1 # Уровень игрока
        
    def update(self, dx, dy):
        self.rect.x += dx    # Обновляет положение по оси X на dx
        self.rect.y += dy    # обновляет положение по оси Y НА DY




class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y, level):
        super().__init__()
        self.image = pg.Surface((10 * level, 10 * level))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.level = level

        # Создание текстовой надписи для отображения уровня врага
        self.font = pg.font.Font(None, 20 + self.level * 5)
        self.text = self.font.render(str(self.level), True, WHITE)
        self.text_rect = self.text.get_rect(center=(self.rect.centerx, self.rect.centery + 10))
    def update(self, player, enemies_group):
        if self.level > player.level:
            for enemy in enemies_group:
                if enemy != self:
                    if self.rect.colliderect(enemy.rect):
                        if self.rect.x >= enemy.rect.x:
                            self.rect.x += 5
                        else:
                            self.rect.x -= 5
                        if self.rect.y >= enemy.rect.y:
                            self.rect.y += 5
                        else:
                            self.rect.y -= 5
        if self.level > player.level:
            if self.rect.x >= player.rect.x:
                self.rect.x -= 1
            else:
                self.rect.x += 0.5
            if self.rect.y >= player.rect.y:
                self.rect.y -= 1
            else:
                self.rect.y += 0.5

        self.text = self.font.render(str(self.level), True, WHITE)
        self.text_rect.center = (self.rect.centerx, self.rect.centery + 5)
    
# Группы спрайтов
all_sprites = pg.sprite.Group()
enemies = pg.sprite.Group()

score = 1

# Создание объектов
player = Player()



# Создание врагов
for i in range(10):
    enemy = Enemy(random.randrange(SCREEN_WIDTH), random.randrange(SCREEN_HEIGHT),  i+1)
    all_sprites.add(enemy)
    enemies.add(enemy)








# Настройка игрового цикла
clock = pg.time.Clock()
running = True # флажок
game_over = False 
win = False

# Игровой цикл
while running:
    screen.fill(WHITE)
    текст = score_font.render('Your Score: {}'.format(score), True, BLACK)
    screen.blit(текст, (50, 50))
    
    # Рассчитываем прошедшее время
    current_time = pg.time.get_ticks()
    elapsed_time = (current_time - start_time) // 1000  # преобразуем миллисекунды в секунды

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        #elif event.type == pg.KEYDOWN:
            #if event.key == pg.K_1:
              #  print("Выбран пункт меню 1: Начать игру")
                # Здесь можно добавить код для начала игры
            #elif event.key == pg.K_2:
             #   print("Выбран пункт меню 2: Настройки")
                # Здесь можно добавить код для открытия настроек
            #elif event.key == pg.K_3:
             #   pg.quit()
              #  sys.exit()

    if game_over == False:
        keys = pg.key.get_pressed()
        dx, dy = 0, 0
        if keys[pg.K_LEFT]:
            dx = -5
        if keys[pg.K_RIGHT]:
            dx = 5
        if keys[pg.K_UP]:
            dy = -5
        if keys[pg.K_DOWN]:
            dy = 5

        player.update(dx, dy)
        screen.blit(player.image, player.rect)

        text = font.render(f"Time: {elapsed_time}", True, BLACK)
        screen.blit(text, (15, 15))



        all_sprites.update(player, enemies)
        for enemy in all_sprites:
            screen.blit(enemy.image, enemy.rect)
            screen.blit(enemy.text, enemy.text_rect)   # Отображаем текстовую надпись с уровнем врага

            
        # ОБРАБОТКА СТОЛКНОВЕНИЙ игрока с врагами
        hits = pg.sprite.spritecollide(player, enemies, True)
        for hit in hits:
            if hit.level <= player.level:
                player.level += 1
                score += 1

                if player.level == 11:
                    game_over = True
                    win = True
            else:
                game_over = True

            



        pg.display.flip()
        
    else:
        if win == False:
            
            # Если игра окончена, выводим сообщение о конце игры
            font = pg.font.Font(None, 36)
            text = font.render("Game Over", True, RED)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)
            pg.display.flip()
        else:
            font = pg.font.Font(None, 36)
            text = font.render("YOU WIN!!! ", True, RED)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)
            pg.display.flip()
    
    
    screen.blit(background_image, (0, 0))


    clock.tick(60)

pg.quit()
