
import pygame
import random

pygame.init()

# Настройки окна
WIDTH = 600
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Уклоняйся от блоков")

clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
RED = (255, 60, 60)
BLACK = (20, 20, 30)
GRAY = (100, 100, 100)
GREEN = (50, 220, 100)

# Игрок
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - 100
player_speed = 7

# Враги
enemy_size = 40
enemies = []
enemy_speed = 5
spawn_timer = 0

# Очки
score = 0
font = pygame.font.Font(None, 40)
big_font = pygame.font.Font(None, 70)

game_over = False
running = True


def draw_text(text, font, color, x, y):
    image = font.render(text, True, color)
    screen.blit(image, (x, y))


def restart_game():
    global player_x, enemies, score
    global enemy_speed, spawn_timer, game_over

    player_x = WIDTH // 2 - player_size // 2
    enemies = []
    score = 0
    enemy_speed = 5
    spawn_timer = 0
    game_over = False


while running:
    clock.tick(60)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                restart_game()

    screen.fill(BLACK)

    if not game_over:
        # Управление игроком
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= player_speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += player_speed

        # Не даём игроку выйти за экран
        player_x = max(0, min(WIDTH - player_size, player_x))

        # Создание врагов
        spawn_timer += 1

        if spawn_timer >= 35:
            spawn_timer = 0

            enemy_x = random.randint(
                0, WIDTH - enemy_size
            )

            enemies.append([
                enemy_x,
                -enemy_size
            ])

        # Движение врагов
        for enemy in enemies:
            enemy[1] += enemy_speed

        # Удаление врагов и начисление очков
        for enemy in enemies[:]:
            if enemy[1] > HEIGHT:
                enemies.remove(enemy)
                score += 1

        # Усложнение игры
        enemy_speed = 5 + score // 10

        # Проверка столкновений
        player_rect = pygame.Rect(
            player_x,
            player_y,
            player_size,
            player_size
        )

        for enemy in enemies:
            enemy_rect = pygame.Rect(
                enemy[0],
                enemy[1],
                enemy_size,
                enemy_size
            )

            if player_rect.colliderect(enemy_rect):
                game_over = True

        # Отрисовка игрока
        pygame.draw.rect(
            screen,
            BLUE,
            player_rect,
            border_radius=10
        )

        # Отрисовка врагов
        for enemy in enemies:
            pygame.draw.rect(
                screen,
                RED,
                (enemy[0], enemy[1], enemy_size, enemy_size),
                border_radius=8
            )

        # Очки
        draw_text(
            f"Score: {score}",
            font,
            WHITE,
            20,
            20
        )

    else:
        # Экран проигрыша
        draw_text(
            "GAME OVER",
            big_font,
            RED,
            WIDTH // 2 - 160,
            HEIGHT // 2 - 80
        )

        draw_text(
            f"Your score: {score}",
            font,
            WHITE,
            WIDTH // 2 - 100,
            HEIGHT // 2
        )

        draw_text(
            "Press R to restart",
            font,
            GREEN,
            WIDTH // 2 - 150,
            HEIGHT // 2 + 60
        )

    pygame.display.update()

pygame.quit()
