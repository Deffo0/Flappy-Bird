import pygame
import sys

pygame.init()
clock = pygame.time.Clock()
WIDTH = 1600
HEIGHT = 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
font = pygame.font.Font(None, 32)
bg_img = pygame.image.load("Resources/BG.png")
bird_images = [pygame.image.load(f"Resources/bird/skeleton-animation_{i}.png") for i in range(11)]
pipe_img = pygame.image.load("Resources/pipe.png")
pipe_reverse_img = pygame.image.load("Resources/pipe-reverse.png")
game_over_img = pygame.image.load("Resources/game-over.png")
game_over_sound = pygame.mixer.Sound("Resources/game_over.wav")

animation_state = 0
bird_x = 100
bird_y = HEIGHT // 2
pipe_x = WIDTH
pipe_y = 500
pipe_reverse_y = 0
pipe_type = 0
score = 0
bird_speed = 2
pipe_speed = 10


def update_pipe():
    global pipe_speed, pipe_type, pipe_x
    pipe_x -= pipe_speed
    if pipe_x < -100:
        pipe_x = WIDTH
        pipe_type = 1 - pipe_type


def update_bird():
    global bird_x, bird_y
    bird_x += 10
    bird_y += 5
    if bird_x > WIDTH:
        bird_x = -50


def draw():
    global bird_x, bird_y, pipe_x, pipe_y, pipe_reverse_y, pipe_type, animation_state
    win.blit(bg_img, (0, 0))
    win.blit(bird_images[animation_state], (bird_x, bird_y))
    if pipe_type:
        win.blit(pipe_reverse_img, (pipe_x, pipe_reverse_y))
    else:
        win.blit(pipe_img, (pipe_x, pipe_y))

    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    score_rect = score_text.get_rect(topleft=(10, 10))
    win.blit(score_text, score_rect)
    animation_state = (animation_state + 1) % 11


def game_over():
    game_over_sound.play()
    win.blit(game_over_img, ((WIDTH / 2) - 215, (HEIGHT / 2) - 206))
    pygame.display.flip()
    pygame.time.delay(6000)


while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    update_pipe()
    update_bird()
    draw()
    pygame.display.flip()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        bird_y -= 50
    else:
        bird_y += bird_speed

    bird_rect = bird_images[animation_state].get_rect(topleft=(bird_x, bird_y))
    if pipe_type:
        pipe_rect = pipe_reverse_img.get_rect(topleft=(pipe_x, pipe_reverse_y))
    else:
        pipe_rect = pipe_img.get_rect(topleft=(pipe_x, pipe_y))

    if bird_rect.colliderect(pipe_rect):
        game_over()
        pygame.quit()
        sys.exit()

    if pipe_x < bird_x < pipe_x + pipe_rect.width:
        score += 1
