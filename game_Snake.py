import pygame
import random

pygame.init()
pygame.mixer.init()

sound = pygame.mixer.Sound('break.wav')

font = pygame.font.Font(None, 36)

game_h = 600
game_w = 600

screen = pygame.display.set_mode((game_w, game_h))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()


# меню
def menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        mouse = pygame.mouse.get_pos()  # позиция курсора

        # создание кнопок
        start_btn = pygame.Rect(game_w // 2 - 100, game_h // 2 - 100, 200, 50)
        quit_btn = pygame.Rect(game_w // 2 - 100, game_h // 2 - 30, 200, 50)

        # создаем текст для кнопок
        start_text = font.render('Старт', True, (0, 0, 0))
        quit_text = font.render('Выход', True, (0, 0, 0))

        screen.fill((0, 0, 0))
        # рисуем кнопки
        if start_btn.collidepoint(mouse):
            pygame.draw.rect(screen, (255, 255, 0), start_btn)
        else:
            pygame.draw.rect(screen, (255, 255, 255), start_btn)

        if quit_btn.collidepoint(mouse):
            pygame.draw.rect(screen, (255, 255, 0), quit_btn)
        else:
            pygame.draw.rect(screen, (255, 255, 255), quit_btn)

            # выводим текст
        screen.blit(start_text,
                    (start_btn.centerx - start_text.get_width() // 2, start_btn.centery - start_text.get_height() / 2))
        screen.blit(quit_text,
                    (quit_btn.centerx - quit_text.get_width() // 2, quit_btn.centery - quit_text.get_height() / 2))

        # нажатие на кнопки
        mouse_click = pygame.mouse.get_pressed()
        if quit_btn.collidepoint(mouse) and mouse_click[0] == True:
            quit()
        if start_btn.collidepoint(mouse) and mouse_click[0] == True:
            return

        pygame.display.update()


menu()


def food():
    x = random.randint(0, game_w - 20)  # 138 --> 140
    y = random.randint(0, game_h - 20)  # 104 --> 120

    while x % 20 != 0:
        x += 1

    while y % 20 != 0:
        y += 1

    return x, y


x = game_w / 2
y = game_h / 2

step_x = 0
step_y = 0

x_food, y_food = food()  # (100, 122)
snake_len = 1
snake = []

score = 0
running = True
# основной цикл игры
while running:
    screen.fill((3, 143, 143))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # перемещение игрока
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        step_x = 0
        step_y = -20
    if keys[pygame.K_d]:
        step_x = 20
        step_y = 0
    if keys[pygame.K_s]:
        step_x = 0
        step_y = 20
    if keys[pygame.K_a]:
        step_x = -20
        step_y = 0

    x += step_x
    y += step_y

    # границы игры
    if x < 0 or x > game_w or y < 0 or y > game_h:
        x = game_w / 2
        y = game_h / 2
        score = 0
        snake_len = 1
        for i in snake[1:]:
            snake.remove(i)
        menu()


    # a = b = 0
    # for i in range(game_w // 20):
    #     pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(a, b, 20, game_h), 1)
    #     a += 20
    # a = 0
    # for i in range(game_h // 20):
    #     pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(a, b, game_w, 20), 1)
    #     b += 20

    # координаты головы
    snake_head = [x, y]

    # добавляем голову в змейку
    snake.append(snake_head)
    if len(snake) > snake_len:
        snake.pop(0)

    # пересечение головы и еды
    if x == x_food and y == y_food:
        sound.play()
        snake_len += 1
        score += 1
        x_food, y_food = food()  # перемещаем еду

    # пересечение головы и тела
    for item in snake[:-1]:
        if item == snake_head:
            x = game_w / 2
            y = game_h / 2
            score = 0
            snake_len = 1
            for i in snake[1:]:
                snake.remove(i)
            menu()

    pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(x_food, y_food, 20, 20))
    # рисуем змейку
    for item in snake:
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(item[0], item[1], 20, 20))
    # отображаем счет игры
    score_text = font.render('Score: ' + str(score), True, (255, 255, 255))
    screen.blit(score_text, (20, 20))
    pygame.display.update()
    clock.tick(10)
