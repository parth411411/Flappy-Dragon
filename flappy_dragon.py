import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.25
FLAP_STRENGTH = -7
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Dragon')
clock = pygame.time.Clock()

# Load images
try:
    dragon_img = pygame.image.load('dragon.png.png')
    dragon_img = pygame.transform.scale(dragon_img, (50, 50))
except:
    print("Error loading dragon image")
    sys.exit()

class Dragon:
    def __init__(self):
        self.x = SCREEN_WIDTH // 3
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.rect = dragon_img.get_rect(center=(self.x, self.y))

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.center = (self.x, self.y)

    def draw(self):
        screen.blit(dragon_img, self.rect)

class Pipe:
    def __init__(self):
        self.gap_y = random.randint(100, SCREEN_HEIGHT - 100)
        self.x = SCREEN_WIDTH
        self.top_height = self.gap_y - PIPE_GAP // 2
        self.bottom_height = SCREEN_HEIGHT - (self.gap_y + PIPE_GAP // 2)
        self.top_rect = pygame.Rect(self.x, 0, 50, self.top_height)
        self.bottom_rect = pygame.Rect(self.x, SCREEN_HEIGHT - self.bottom_height, 50, self.bottom_height)
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.top_rect)
        pygame.draw.rect(screen, GREEN, self.bottom_rect)

def main():
    dragon = Dragon()
    pipes = []
    score = 0
    last_pipe = pygame.time.get_ticks()
    font = pygame.font.Font(None, 36)
    game_over = False

    while True:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        # Reset game
                        dragon = Dragon()
                        pipes = []
                        score = 0
                        last_pipe = current_time
                        game_over = False
                    else:
                        dragon.flap()

        if not game_over:
            # Update dragon
            dragon.update()

            # Generate new pipes
            if current_time - last_pipe > PIPE_FREQUENCY:
                pipes.append(Pipe())
                last_pipe = current_time

            # Update pipes
            for pipe in pipes[:]:
                pipe.update()
                if pipe.x < -50:
                    pipes.remove(pipe)
                if not pipe.passed and pipe.x < dragon.x:
                    pipe.passed = True
                    score += 1

            # Check collisions
            for pipe in pipes:
                if dragon.rect.colliderect(pipe.top_rect) or dragon.rect.colliderect(pipe.bottom_rect):
                    game_over = True

            # Check if dragon hits the ground or ceiling
            if dragon.y < 0 or dragon.y > SCREEN_HEIGHT:
                game_over = True

        # Draw everything
        screen.fill(BLACK)
        dragon.draw()
        for pipe in pipes:
            pipe.draw()

        # Draw score
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        if game_over:
            game_over_text = font.render('Game Over! Press SPACE to restart', True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2))

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main() 