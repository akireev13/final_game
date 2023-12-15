#### made by akireev13 as a University project 14.12.2023


import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HS Final Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 50, 0, 87, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont('Arial', 50)
WINNER_FONT = pygame.font.SysFont('Arial', 120)

FPS = 120
VEL = 3
BULLET_VEL = 9
MAX_BULLETS = 5
SOLDIER_WIDTH, SOLDIER_HEIGHT = 67, 88
RED_BULLET_COLOR = (99, 31, 31)
YELLOW_BULLET_COLOR = (99, 71, 10)
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SOLDIER_IMAGE = pygame.image.load(
    os.path.join('Assets', 'soldier1.png'))
YELLOW_SOLDIER = pygame.transform.scale(YELLOW_SOLDIER_IMAGE, (SOLDIER_WIDTH, SOLDIER_HEIGHT))
YELLOW_SOLDIER = pygame.transform.rotate(YELLOW_SOLDIER, 90)

RED_SOLDIER_IMAGE = pygame.image.load(
    os.path.join('Assets', 'soldier2.png'))
RED_SOLDIER = pygame.transform.flip(pygame.transform.scale(RED_SOLDIER_IMAGE, (SOLDIER_WIDTH, SOLDIER_HEIGHT)), True, False)
RED_SOLDIER = pygame.transform.rotate(RED_SOLDIER, 270)


grass = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'grass.jpg')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(grass, (0, 0))

    # Create a separate surface for the transparent border
    border_surface = pygame.Surface((BORDER.width, BORDER.height), pygame.SRCALPHA)
    pygame.draw.rect(border_surface, (0, 0, 0, 0), border_surface.get_rect())

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, RED)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, YELLOW)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SOLDIER, (yellow.x, yellow.y))
    WIN.blit(RED_SOLDIER, (red.x, red.y))

    # Blit the transparent border onto the main surface
    WIN.blit(border_surface, (BORDER.x, BORDER.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED_BULLET_COLOR, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW_BULLET_COLOR, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    #removing intersective bullets
    try:
        for bullet1 in yellow_bullets:
            for bullet2 in red_bullets:
                if bullet1.colliderect(bullet2) or bullet2.colliderect(bullet1):
                        yellow_bullets.remove(bullet1)
                        red_bullets.remove(bullet2)
    except ValueError as e:
        print('Occured:',e)



    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    if text == "Red Wins!":
        draw_text = WINNER_FONT.render(text, 1, RED)
    else:
        draw_text = WINNER_FONT.render(text, 1, YELLOW)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(WIDTH - 200, HEIGHT / 2, SOLDIER_WIDTH, SOLDIER_HEIGHT)
    yellow = pygame.Rect(200, HEIGHT / 2, SOLDIER_WIDTH, SOLDIER_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health)

    main()


if __name__ == "__main__":
    main()
