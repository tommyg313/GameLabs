import pygame, sys
from pygame.locals import * #load constants

# Handle sound loading error exception
def load_sound(sound_name):
        try:
            sound = pygame.mixer.Sound(sound_name)
        except pygame.error, message:
            print "Cannot load sound: " + sound_name
            raise SystemExit, message
        return sound



# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PADDLE_START_X = 10
PADDLE_START_Y = 20

OPP_PADDLE_START_X = 780
OPP_PADDLE_START_Y = 20

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SPEED = 10
BALL_WIDTH_HEIGHT = 16

PADDLE_SPEED = 17

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# Loads sound for the paddle rebound
boing = load_sound("boing.wav")

# This is a rect that contains the ball at the beginning it is set in the center of the screen
ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))

# Speed of the ball (x, y)
ball_speed = [BALL_SPEED, BALL_SPEED]

# Your and opponent's paddle vertically centered on the left and right side
player_paddle_rect = pygame.Rect((PADDLE_START_X, PADDLE_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))

opponent_paddle_rect = pygame.Rect((OPP_PADDLE_START_X, OPP_PADDLE_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))


# Scoring: 1 point if you hit the ball, -5 point if you miss the ball
player_score = 0
opponent_score = 0

# Handles end of game options/screens
game_over = False
restart = False

# Fonts for the game over, final score and rematch texts
gameover_font = pygame.font.Font(None, 50)
final_score_font = pygame.font.Font(None, 40)

# Stores who won
player1_win = False

# Load the font for displaying the score
font = pygame.font.Font(None, 30)

# Game loop
while True:
    if game_over == False:
        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
                pygame.quit()
            # Control the paddle with the mouse
            elif event.type == pygame.MOUSEMOTION:
                player_paddle_rect.centery = event.pos[1]
                # correct paddle position if it's going out of window
                if player_paddle_rect.top < 0:
                    player_paddle_rect.top = 0
                elif player_paddle_rect.bottom >= SCREEN_HEIGHT:
                    player_paddle_rect.bottom = SCREEN_HEIGHT

        # This test if up or down keys are pressed; if yes, move the paddle
        if pygame.key.get_pressed()[pygame.K_UP] and player_paddle_rect.top > 0:
            player_paddle_rect.top -= BALL_SPEED
        elif pygame.key.get_pressed()[pygame.K_DOWN] and player_paddle_rect.bottom < SCREEN_HEIGHT:
            player_paddle_rect.top += BALL_SPEED

        #Uncomment this if you want to play against the computer, otherwise comment this out
        elif ball_rect.top < (opponent_paddle_rect.top) and opponent_paddle_rect.top >= 0:
            opponent_paddle_rect.top -= PADDLE_SPEED
        elif ball_rect.top > (opponent_paddle_rect.bottom) and opponent_paddle_rect.bottom <= SCREEN_HEIGHT:
            opponent_paddle_rect.top += PADDLE_SPEED

        #Uncomment this if you want to play against a friend, otherwise comment this out
        #elif pygame.key.get_pressed()[pygame.K_w] and opponent_paddle_rect.top > 0:
        #    opponent_paddle_rect.top -= BALL_SPEED
        #elif pygame.key.get_pressed()[pygame.K_s] and opponent_paddle_rect.bottom < SCREEN_HEIGHT:
        #    opponent_paddle_rect.top += BALL_SPEED


        elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
            sys.exit(0)
            pygame.quit()

        # Checks to see if the score limit has been reached
        if player_score > opponent_score and player_score >=11:
            game_over = True
            player1_win = True
        elif player_score < opponent_score and opponent_score >= 11:
            game_over = True
            player1_win = False

        # Update ball position
        ball_rect.left += ball_speed[0]
        ball_rect.top += ball_speed[1]

        # Ball collision with rails
        if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
            ball_speed[1] = -ball_speed[1]

        # Test if the ball is hit by the paddle; if yes reverse speed and add a point
        if player_paddle_rect.colliderect(ball_rect) or opponent_paddle_rect.colliderect(ball_rect):
            ball_speed[0] = -ball_speed[0]
            boing.play()

        # If the ball goes past the paddles, check to see who score and what side to start the ball on
        if ball_rect.right >= SCREEN_WIDTH:
            player_score += 1
            ball_speed[0] = BALL_SPEED
            ball_speed[1] = -BALL_SPEED
            ball_rect.left = SCREEN_WIDTH/2
            ball_rect.top = SCREEN_HEIGHT/2

        elif ball_rect.left <= 0:
            opponent_score += 1
            ball_speed[0] = -BALL_SPEED
            ball_speed[1] = -BALL_SPEED
            ball_rect.left = SCREEN_WIDTH/2
            ball_rect.top = SCREEN_HEIGHT/2


        # Clear screen
        screen.fill((255, 255, 255))

        # Render the ball, the paddle, and the score
        pygame.draw.rect(screen, (0, 0, 0), player_paddle_rect) # Your paddle
        pygame.draw.rect(screen, (0, 0, 0), opponent_paddle_rect)

        pygame.draw.circle(screen, (0, 0, 0), ball_rect.center, ball_rect.width / 2) # The ball

        pygame.draw.line(screen, (255,0,0), ((SCREEN_WIDTH/2), 0), ((SCREEN_WIDTH/2), SCREEN_HEIGHT), 1) # The center line


        # Scores for player and opponent
        player_score_text = font.render(str(player_score), True, (0, 0, 0))
        screen.blit(player_score_text, ((SCREEN_WIDTH * .2) - font.size(str(player_score))[0] / 2, 5)) # The score

        opponent_score_text = font.render(str(opponent_score), True, (0,0,0))
        screen.blit(opponent_score_text, ((SCREEN_WIDTH * .8) - font.size(str(opponent_score))[0] / 2, 5))


        # Update screen and wait 20 milliseconds
        pygame.display.flip()
        pygame.time.delay(20)

    else:

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_n:
                    quit()
                if event.key == K_y:
                    restart = True

        screen.fill((255,255,255))

        # Game over text
        text = gameover_font.render("GAME OVER", 1, (255, 10, 10))
        screen.blit(text,(300,250))

        # Final score and rematch texts
        if player1_win == True:
            final_score_text = final_score_font.render("Player 1 WINS!", 1, (61, 255, 255))
        else:
            final_score_text = final_score_font.render("Player 2 WINS!", 1, (61, 255, 255))

        rematch_text = final_score_font.render("Rematch? (y/n)",1, (255, 150, 150))
        screen.blit(rematch_text, (300, 350))

        # Resets the game if the player chooses a rematch
        if restart == True:
            player_score = 0
            opponent_score = 0
            game_over = False
            ball_speed[0] = BALL_SPEED
            ball_speed[1] = BALL_SPEED
            ball_rect.left = SCREEN_WIDTH/2
            ball_rect.top = SCREEN_HEIGHT/2
            restart = False

        screen.blit(final_score_text,(300,300))

        pygame.display.flip()