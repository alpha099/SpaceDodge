import pygame
import time
import random
import pygame.mixer
pygame.font.init()


pygame.init()
pygame.mixer.init()  # Intialize mixer module
pygame.mixer.music.load("./Sound/gameplay.mp3") # Load Music

WIDTH, HEIGHT = 1000, 800 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = PLAYER_WIDTH * 2.046 # keep correct aspect ratio of image
PLAYER_VEL = 5

STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 5
FONT = pygame.font.SysFont("comicsans", 30)

BG = pygame.transform.scale(pygame.image.load("./Images/bg.jpeg"), (WIDTH, HEIGHT))
PLAYER_IMG = pygame.transform.scale(pygame.image.load("./Images/rocket.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))

pygame.display.set_caption("Space Dodge")

def start_screen():
    title_font = pygame.font.SysFont("comicsans", 60)
    title_text = title_font.render("Space Dodge", 1, "white")

    start_font = pygame.font.SysFont("comicsans", 40)
    start_text = start_font.render("Start Game", 1, "white")
    start_text_rect = start_text.get_rect(center=(WIDTH/2, HEIGHT/2))

    bg_image = pygame.transform.scale(pygame.image.load("./Images/bg.jpeg"), (WIDTH, HEIGHT))

    while True:
        WIN.blit(bg_image, (0, 0))
        WIN.blit(title_text, (WIDTH/2 - title_text.get_width()/2, 100))
        WIN.blit(start_text, start_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return

        pygame.display.update()


def draw(player,elapsed_time,stars):
    WIN.blit(BG, (0,0))
    
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text,(10, 10))

    WIN.blit(PLAYER_IMG, (player.x, player.y))
    
    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()

def gameover_screen(elapsed_time):
    pygame.mixer.music.stop()

    # Splash screen
    splash_duration = 3  # seconds
    splash_start_time = time.time()

    while time.time() - splash_start_time < splash_duration:
        WIN.fill((0, 0, 0))  # Change the background color as needed

        splash_text = FONT.render(f"Survived: {round(elapsed_time)}s", 1, "white")
        WIN.blit(splash_text, (WIDTH / 2 - splash_text.get_width() / 2, HEIGHT / 2 - splash_text.get_height() / 2))

        pygame.display.update()

    # Game over screen
    run_gameover_screen = True

    while run_gameover_screen:
        WIN.fill((0, 0, 0))  # Change the background color as needed

        lost_text = FONT.render("GAME OVER", 1, "white")
        WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))
        restart_text = FONT.render("Press R to restart", 1, "white")
        WIN.blit(restart_text, (WIDTH / 2 - restart_text.get_width() / 2, HEIGHT / 2 - restart_text.get_height() / 2 + 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()  # Call main function to restart the game
                    run_gameover_screen = False


def main():
    pygame.mixer.music.play(-1)
    start_screen()

    run = True
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        Keys = pygame.key.get_pressed()
        if Keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if Keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                pygame.mixer.music.stop()
                pygame.mixer.Sound("./Sound/Explosion.flac").play()
                break

        if hit:
            gameover_screen(elapsed_time)  # Display splash screen and game over screen
            run = False  # Exit the game loop

        draw(player, elapsed_time, stars)

    pygame.quit()     


if __name__ == "__main__":
    main()
