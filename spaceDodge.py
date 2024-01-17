import pygame
import time
import random
from pygame import mixer as mixer

pygame.font.init()

# Initialize Pygame
pygame.init()

#Initialize Pygame music mixer
mixer.init()  

# Load Background Music
mixer.music.load("./Sound/gameplay.mp3") 

# Set the dimensions of the game window
WIDTH, HEIGHT = 1000, 800 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Define player attributes (Width, Height, Velocity)
PLAYER_WIDTH = 40
PLAYER_HEIGHT = PLAYER_WIDTH * 2.046
PLAYER_VEL = 5

# Define star attributes (Width, Height, Velocity)
# The star is the "enemy" in this game it falls from the top of the screen
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 5

# Define the font for displaying text
FONT = pygame.font.SysFont("comicsans", 30)

# Load background image and player image
BG = pygame.transform.scale(pygame.image.load("./Images/bg.jpeg"), (WIDTH, HEIGHT))
PLAYER_IMG = pygame.transform.scale(pygame.image.load("./Images/rocket.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))

# Set the window caption
pygame.display.set_caption("Space Dodge")

# Function to display the start screen
def start_screen():
    # write "Space Dodge" in on the screen
    title_font = pygame.font.SysFont("comicsans", 60)
    title_text = title_font.render("Space Dodge", 1, "white")

    # write "Start Game" on the screen
    start_font = pygame.font.SysFont("comicsans", 40)
    start_text = start_font.render("Start Game", 1, "white")
    start_text_rect = start_text.get_rect(center=(WIDTH/2, HEIGHT/2))

    # Load the background image
    bg_image = pygame.transform.scale(pygame.image.load("./Images/bg.jpeg"), (WIDTH, HEIGHT))

    while True:
        # Display the background image and the text
        WIN.blit(bg_image, (0, 0))
        WIN.blit(title_text, (WIDTH/2 - title_text.get_width()/2, 100))
        WIN.blit(start_text, start_text_rect)

        # wait until the user clicks the mouse button or quits the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return

        # update the display
        pygame.display.update()

# Function to draw the game screen
def draw(player, elapsed_time, stars):
    # Draw the game screen
    WIN.blit(BG, (0,0))
    
    # Display the elapsed time
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text,(10, 10))

    # Display the player
    WIN.blit(PLAYER_IMG, (player.x, player.y))
    
    # Display the stars
    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    # Update the display
    pygame.display.update()

# Function to display the game over screen
def gameover_screen(elapsed_time):
    # Stop the background music
    mixer.music.stop()

    # Splash screen before game over screen
    # Duration of the splash screen in seconds and start the timer for the splash screen
    splash_duration = 3  
    splash_start_time = time.time()

    # Display the splash screen until the time timer reaches the defined duration
    while time.time() - splash_start_time < splash_duration:
        WIN.fill((0, 0, 0))  

        # Display Death message and survived time
        splash_text = FONT.render(f"Survived: {round(elapsed_time)}s", 1, "white")
        WIN.blit(splash_text, (WIDTH / 2 - splash_text.get_width() / 2, HEIGHT / 2 - splash_text.get_height() / 2))

        # Update the display
        pygame.display.update()

    # Game over screen
    run_gameover_screen = True

    while run_gameover_screen:
        # Display a black screen
        WIN.fill((0, 0, 0))  

        # Get the saved high score from the function get_high_score()
        high_score = get_high_score()

        # Check if the current score is higher than the saved high score
        # If the current score is higher than the saved high score, save the current score as the new high score
        if elapsed_time > high_score:
            high_score = elapsed_time
            save_high_score(high_score)

        # Display high score
        high_score_text = FONT.render(f"High Score: {round(high_score)}s", 1, "white")
        WIN.blit(high_score_text, (WIDTH / 2 - high_score_text.get_width() / 2, HEIGHT / 2 + -50))
        # Display game over message
        lost_text = FONT.render("GAME OVER", 1, "white")
        WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))
        # Display restart message
        restart_text = FONT.render("Press R to restart", 1, "white")
        WIN.blit(restart_text, (WIDTH / 2 - restart_text.get_width() / 2, HEIGHT / 2 - restart_text.get_height() / 2 + 50))

        # Update the display
        pygame.display.update()

        # Wait for the user to press the R key to restart the game or quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()  
                    run_gameover_screen = False

# Function to get the high score from a file
def get_high_score():
    # Try to read the high score from the file
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        # If the file is not found, create it and set the initial high score to 0
        with open("high_score.txt", "w") as file:
            file.write("0")
        return 0
    except ValueError:
        # Handle the case where the file contains invalid data
        # For example, if someone manually edits the file and enters non-numeric data
        print("Invalid data found in high_score.txt. Resetting to 0.")
        with open("high_score.txt", "w") as file:
            file.write("0")
        return 1


# Function to save the high score to a file
# we don't need to check if the file exists because we already did that in the get_high_score() function
# and this function is only called if the player has a new high score
def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

# Main game function
def main():
    # Start the background music
    mixer.music.play(-1)

    # Display the start screen
    start_screen()

    run = True
    # Create the player
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    # Create the clock
    clock = pygame.time.Clock()

    # Start the timer for the elapsed time
    start_time = time.time()
    elapsed_time = 0

    # Define star attributes
    star_add_increment = 2000
    star_count = 0

    # Create a list for the stars
    stars = []

    # Define the hit variable
    hit = False

    while run:
        # Every 60 Frames add 1 to the star_count
        star_count += clock.tick(60)

        # Update the elapsed time
        elapsed_time = time.time() - start_time

        # Add a new star every 2000 Frames
        # The number of frames is reduced by 50 every time a new star is added until a minimum of 200 frames is reached
        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        # Reset the Run variable to if the game quits
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        # Check if the player has pressed the left or right arrow key
        # If the player has pressed the left or right arrow key, change the x coordinate of the player by the player velocity
        Keys = pygame.key.get_pressed()
        if Keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if Keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_VEL

        # Move the stars down the screen
        for star in stars[:]:
            star.y += STAR_VEL
            # Remove the star if it is below the screen
            if star.y > HEIGHT:
                stars.remove(star)
            # Check if the player has collided with a star
            elif star.y >= player.y and star.colliderect(player):
                # Remove the star and set the hit variable to True
                stars.remove(star)
                hit = True
                # Stop the background music and play the explosion sound
                mixer.music.stop()
                mixer.Sound("./Sound/Explosion.flac").play()
                break
        
        # If the player has collided with a star, display the game over screen and stop the game loop
        if hit:
            gameover_screen(elapsed_time)  
            run = False  

        # Draw the game screen
        draw(player, elapsed_time, stars)

    # Quit the game
    pygame.quit()

# Run the game if the script is executed
if __name__ == "__main__":
    main()
