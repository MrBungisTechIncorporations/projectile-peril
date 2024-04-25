import pygame
import time
import random
import sys

pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Projectile Peril")

BG = pygame.transform.scale(pygame.image.load("img.png"), (WIDTH, HEIGHT))
PAUSE_SYMBOL = pygame.transform.scale(pygame.image.load("pause.png"), (50, 50))  # Adjust size
PLAY_SYMBOL = pygame.transform.scale(pygame.image.load("play.png"), (50, 50))  # Adjust size

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

PLAYER_VEL = 5
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3

FONT = pygame.font.SysFont("comicsans", 30)


def draw_button(text, position, width=100, color=(0, 255, 0)):
    button_rect = pygame.Rect(position[0], position[1], width, 50)
    pygame.draw.rect(WIN, color, button_rect)
    button_text = FONT.render(text, 1, (255, 255, 255))
    text_rect = button_text.get_rect(center=button_rect.center)
    WIN.blit(button_text, text_rect)


def draw_pause_symbol(is_paused):
    # Adjust position and color
    if is_paused:
        WIN.blit(PLAY_SYMBOL, (WIDTH - PLAY_SYMBOL.get_width() - 20, 20))
    else:
        WIN.blit(PAUSE_SYMBOL, (WIDTH - PAUSE_SYMBOL.get_width() - 20, 20))


def draw(player, elapsed_time, stars, score, is_alive, death_alpha, is_paused):
    WIN.blit(BG, (0, 0))
    draw_pause_symbol(is_paused)
    if is_paused and is_alive:
        pause_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pause_surface.fill((0, 0, 0, 150))
        WIN.blit(pause_surface, (0, 0))
        draw_button("Resume", (WIDTH // 2 - 100, HEIGHT // 2), width=200)  # Expanded width
    else:
        time_text = FONT.render(f"Time: {round(elapsed_time, 2)}s", 1, "white")
        WIN.blit(time_text, (10, 10))
        score_text = FONT.render("Score: " + str(score), 1, "white")
        score_rect = score_text.get_rect(midtop=(WIDTH // 2, 10))
        WIN.blit(score_text, score_rect)
        pygame.draw.rect(WIN, "red", player)
        for star in stars:
            pygame.draw.rect(WIN, "yellow", star)
        if not is_alive:
            death_alpha += 3
            if death_alpha > 255:
                death_alpha = 255
            death_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            death_surface.fill((0, 0, 0, death_alpha))
            WIN.blit(death_surface, (0, 0))
            draw_button("Try Again?", (WIDTH // 2 - 100, HEIGHT // 2 + 50), width=200)
            draw_button("Quit?", (WIDTH // 2 - 50, HEIGHT // 2 + 120), color=(255, 0, 0))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and not is_alive:
            mouse_pos = pygame.mouse.get_pos()
            if (WIDTH // 2 - 50) <= mouse_pos[0] <= (WIDTH // 2 + 50) and (HEIGHT // 2 + 120) <= mouse_pos[1] <= (HEIGHT // 2 + 170):
                pygame.quit()
                sys.exit()



def main():
    run = True
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    star_add_increment = 2000
    star_count = 0
    stars = []
    score = 0
    is_alive = True
    death_alpha = 0
    is_paused = False

    while run:
        star_count += clock.tick(60)

        if is_alive and not is_paused:
            elapsed_time = time.time() - start_time

        if star_count > star_add_increment and is_alive:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not is_alive:
                mouse_pos = pygame.mouse.get_pos()
                button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 50)
                if button_rect.collidepoint(mouse_pos):
                    run = True
                    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
                    start_time = time.time()
                    elapsed_time = 0
                    star_add_increment = 2000
                    star_count = 0
                    stars = []
                    score = 0
                    is_alive = True
                    death_alpha = 0
                    is_paused = False
            if event.type == pygame.MOUSEBUTTONDOWN and is_paused:
                mouse_pos = pygame.mouse.get_pos()
                resume_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2, 100, 50)
                if resume_button_rect.collidepoint(mouse_pos):
                    is_paused = False

            if event.type == pygame.MOUSEBUTTONDOWN and not is_paused:
                mouse_pos = pygame.mouse.get_pos()
                pause_symbol_rect = PAUSE_SYMBOL.get_rect(topleft=(WIDTH - PAUSE_SYMBOL.get_width() - 20, 20))
                if pause_symbol_rect.collidepoint(mouse_pos):
                    is_paused = not is_paused and is_alive  # Only pause if the player is alive

                # Check if the game is paused and the pause symbol is displayed
                if is_paused and not pause_symbol_rect.collidepoint(mouse_pos):
                    play_button_rect = PLAY_SYMBOL.get_rect(topleft=(WIDTH - PLAY_SYMBOL.get_width() - 20, 20))
                    if play_button_rect.collidepoint(mouse_pos):
                        is_paused = False
                        start_time = time.time() - elapsed_time

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    is_paused = not is_paused and is_alive  # Only pause if the player is alive
                    if is_paused:
                        start_time = time.time() - elapsed_time

        if is_alive and not is_paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
                player.x -= PLAYER_VEL
            if keys[pygame.K_RIGHT] and player.x - PLAYER_VEL + player.width <= WIDTH:
                player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
                if is_alive:
                    score += 1
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.clear()
                is_alive = False

        draw(player, elapsed_time, stars, score, is_alive, death_alpha, is_paused)

    pygame.quit()


if __name__ == "__main__":
    main()




