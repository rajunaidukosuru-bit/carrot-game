import pygame
import random

pygame.init()

W, H = 800, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Carrot Catch Game")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 35)
big_font = pygame.font.SysFont(None, 60)

# Player basket
basket = pygame.Rect(350, 520, 120, 40)
basket_speed = 8

# Carrot
carrot = pygame.Rect(
    random.randint(30, 750),
    -50,
    30,
    45
)

carrot_speed = 5

score = 0
lives = 3

game_over = False

# Buttons
left_button = pygame.Rect(40, 510, 90, 70)
right_button = pygame.Rect(150, 510, 90, 70)
restart_button = pygame.Rect(300, 350, 200, 70)

left_pressed = False
right_pressed = False


def new_carrot():
    return pygame.Rect(
        random.randint(30, W - 60),
        -50,
        30,
        45
    )


running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            x, y = event.pos

            if not game_over:

                if left_button.collidepoint(x, y):
                    left_pressed = True

                if right_button.collidepoint(x, y):
                    right_pressed = True

            else:

                if restart_button.collidepoint(x, y):
                    score = 0
                    lives = 3
                    carrot = new_carrot()
                    basket.x = 350
                    game_over = False

        if event.type == pygame.MOUSEBUTTONUP:
            left_pressed = False
            right_pressed = False

    if not game_over:

        # Basket movement
        if left_pressed:
            basket.x -= basket_speed

        if right_pressed:
            basket.x += basket_speed

        # Keep basket inside screen
        basket.x = max(0, min(W - basket.width, basket.x))

        # Carrot movement
        carrot.y += carrot_speed

        # Catch carrot
        if carrot.colliderect(basket):

            score += 1
            carrot = new_carrot()

            # Make game slightly faster
            carrot_speed = min(12, 5 + score // 5)

        # Miss carrot
        if carrot.y > H:

            lives -= 1
            carrot = new_carrot()

            if lives <= 0:
                game_over = True

    # ---------------- DRAW ----------------

    screen.fill((120, 200, 255))

    # Ground
    pygame.draw.rect(
        screen,
        (80, 180, 80),
        (0, 0, W, H)
    )

    # Carrot
    pygame.draw.polygon(
        screen,
        (255, 130, 30),
        [
            (carrot.centerx, carrot.y + 45),
            (carrot.x, carrot.y),
            (carrot.right, carrot.y)
        ]
    )

    # Carrot leaves
    pygame.draw.line(
        screen,
        (20, 150, 50),
        (carrot.centerx, carrot.y),
        (carrot.centerx - 8, carrot.y - 12),
        5
    )

    pygame.draw.line(
        screen,
        (20, 150, 50),
        (carrot.centerx, carrot.y),
        (carrot.centerx + 8, carrot.y - 12),
        5
    )

    # Basket
    pygame.draw.rect(
        screen,
        (130, 80, 30),
        basket
    )

    pygame.draw.rect(
        screen,
        (180, 110, 40),
        (basket.x + 10, basket.y - 10,
         basket.width - 20, 15)
    )

    # Buttons
    pygame.draw.rect(
        screen,
        (70, 70, 70),
        left_button
    )

    pygame.draw.rect(
        screen,
        (70, 70, 70),
        right_button
    )

    screen.blit(
        font.render("LEFT", True, (255, 255, 255)),
        (left_button.x + 15, left_button.y + 20)
    )

    screen.blit(
        font.render("RIGHT", True, (255, 255, 255)),
        (right_button.x + 8, right_button.y + 20)
    )

    # Score
    screen.blit(
        font.render(
            "Score: " + str(score),
            True,
            (255, 255, 255)
        ),
        (20, 20)
    )

    screen.blit(
        font.render(
            "Lives: " + str(lives),
            True,
            (255, 255, 255)
        ),
        (20, 60)
    )

    # Game Over
    if game_over:

        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (180, 200, 440, 250)
        )

        text = big_font.render(
            "GAME OVER",
            True,
            (255, 255, 255)
        )

        screen.blit(
            text,
            (W // 2 - text.get_width() // 2, 220)
        )

        score_text = font.render(
            "Score: " + str(score),
            True,
            (255, 255, 255)
        )

        screen.blit(
            score_text,
            (W // 2 - score_text.get_width() // 2, 290)
        )

        pygame.draw.rect(
            screen,
            (50, 170, 70),
            restart_button
        )

        screen.blit(
            font.render(
                "RESTART",
                True,
                (255, 255, 255)
            ),
            (restart_button.x + 40,
             restart_button.y + 20)
        )

    pygame.display.flip()

pygame.quit()
