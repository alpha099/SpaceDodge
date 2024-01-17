import pygame
import time
import random
from pygame import mixer as mixer
import math

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

# Define the PowerUp class
# The power-up is the "power-up" in this game it falls from the top of the screen
class PowerUp(pygame.Rect):
    def __init__(self):
        super().__init__(random.randint(0, WIDTH - 15), -15, 15, 15)
        self.velocity = STAR_VEL  # Adjust the velocity if needed

# Load power-up image
POWERUP_IMG = pygame.transform.scale(pygame.image.load("./Images/powerup.png"), (15, 15))
# Load power-up pickup sound
POWERUP_PICKUP_SOUND = mixer.Sound("./Sound/powerup_sound.flac")


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
def draw(player, elapsed_time, stars, powerup):
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

    # Display the power-up
    if powerup is not None:
        WIN.blit(POWERUP_IMG, (powerup.x, powerup.y))

    # Update the display
    pygame.display.update()

# Function to display the game over screen
def gameover_screen(starcount, elapsed_time):
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

        high_score=math.ceil(starcount*elapsed_time*0.1)

        # Get the saved high score from the function get_high_score()
        saved_elapsed_time = float(get_high_score(1))
        saved_high_score = float(get_high_score(2))

        # Check if the current score is higher than the saved high score
        # If the current score is higher than the saved high score, save the current score as the new high score
        if elapsed_time > saved_elapsed_time:
            new_elapsed_time = elapsed_time
            save_high_score(1, new_elapsed_time)

        if high_score > saved_high_score:
            new_high_score = high_score
            save_high_score(2, new_high_score)

        # Display high score
        high_score_text = FONT.render(f"your Score: {round(high_score)}", 1, "white")
        WIN.blit(high_score_text, (WIDTH / 2 - high_score_text.get_width() / 2, HEIGHT / 2 + -400))
        # Display saved high score
        saved_high_score_text = FONT.render(f"High Score: {round(saved_high_score)}", 1, "white")
        WIN.blit(saved_high_score_text, (WIDTH / 2 - saved_high_score_text.get_width() / 2, HEIGHT / 2 + -350))
        # Display elapsed time
        elapsed_time_text = FONT.render(f"survived time: {round(elapsed_time)}s", 1, "white")
        WIN.blit(elapsed_time_text, (WIDTH / 2 - elapsed_time_text.get_width() / 2, HEIGHT / 2 + -200))
        # Display saved elapsed time
        saved_elapsed_time_text = FONT.render(f"Highest survived time: {round(saved_elapsed_time)}s", 1, "white")
        WIN.blit(saved_elapsed_time_text, (WIDTH / 2 - saved_elapsed_time_text.get_width() / 2, HEIGHT / 2 + -150))
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
def get_high_score(command):
    # Try to read the high score from the file
    # Depending on the command (1 or 2) return the elapsed time or the high score
    try:
        with open("high_score.txt", "r") as file:
            lines = file.readlines()

            for line in lines:
                parts = line.strip().split(" : ")
                if len(parts) == 2:
                    current_command, value = parts
                    if current_command == str(command):
                        if value==None:
                            return int(0)
                        return float(value)

            # If the command is not found, create it and set the initial value to an empty string
            with open("high_score.txt", "a") as file:
                file.write(f"{command} : 0\n")
            return ""

    except FileNotFoundError:
        # If the file is not found, create it and set the initial value to an empty string
        with open("high_score.txt", "w") as file:
            file.write("1 : 0\n2 : 0\n")
        return ""

    except ValueError:
        # Handle the case where the file contains invalid data
        # For example, if someone manually edits the file and enters non-numeric data
        print("Invalid data found in high_score.txt. Resetting to empty values.")
        with open("high_score.txt", "w") as file:
            file.write("1 : 0\n2 : 0\n")
        return ""



# Function to save the high score to a file

def save_high_score(command, score):
    try:
        with open("high_score.txt", "r") as file:
            lines = file.readlines()
            file.close()

        with open("high_score.txt", "w") as file:
            for line in lines:
                parts = line.strip().split(" : ")
                if len(parts) == 2:
                    current_command, _ = parts
                    if current_command == str(command):
                        file.write(f"{command} : {score}\n")
                    else:
                        file.write(line)

            # If the command is not found, create it and set the initial score
            if str(command) not in [part.split(" : ")[0] for part in lines]:
                file.write(f"{command} : {score}\n")

    except FileNotFoundError:
        # If the file is not found, create it and set the initial score
        with open("high_score.txt", "w") as file:
            file.write(f"1 : {score}\n2 : 0\n" if command == 1 else f"1 : 0\n2 : {score}\n")

    except ValueError:
        # Handle the case where the file contains invalid data
        # For example, if someone manually edits the file and enters non-numeric data
        print("Invalid data found in high_score.txt. Resetting to default values.")
        with open("high_score.txt", "w") as file:
            file.write("1 : 0\n2 : 0\n")

# Main game function
def main():
    # Start the background music
    mixer.music.play(-1)

    # Display the start screen
    start_screen()

    run = True
    # Create the player
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    powerup = None
    powerup_spawn_time = random.randint(30,90)  # random time between 30 and 90 seconds
    powerup_interval = random.randint(20,60)     # random time between 20 and 60 seconds
    powerup_duration = random.randint(5,20)     # random time between 5 and 20 seconds
    powerup_timer = 0         # Timer for power-up duration

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


        # Check if the powerup is ready to span and if it is, create a new power-up
        if elapsed_time >= powerup_spawn_time and powerup is None:
            powerup = PowerUp()
            powerup_spawn_time += powerup_interval

        # Move and draw power-up
        if powerup is not None:
            powerup.y += powerup.velocity
            WIN.blit(POWERUP_IMG, (powerup.x, powerup.y))  # Draw power-up

            # Check for collision with the player
            if player.colliderect(powerup):
                # Apply power-up effects
                POWERUP_PICKUP_SOUND.play()
                powerup = None  # Deactivate the power-up
                # Disable a random half of the stars
                stars_to_disable = random.sample(stars, len(stars) // 2)
                for star in stars_to_disable:
                    stars.remove(star)
                # Set a timer for the power-up duration
                powerup_timer = powerup_duration

                # Decrement the power-up timer
                if powerup_timer > 0:
                    powerup_timer -= 1
                else:
                    # Re-enable the stars
                    powerup_timer = 0
                    stars = []
                    for y in range(0, HEIGHT, STAR_HEIGHT):
                        for x in range(0, WIDTH, STAR_WIDTH):
                            stars.append(pygame.Rect(x, y, STAR_WIDTH, STAR_HEIGHT))

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
            gameover_screen(star_count, elapsed_time)  
            run = False  

        # Draw the game screen
        draw(player, elapsed_time, stars, powerup)

    # Quit the game
    pygame.quit()

# Run the game if the script is executed
if __name__ == "__main__":
    main()
