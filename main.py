import pygame
import pymunk
import math
from settings import *
from game_objects import create_ball, create_cushion, pockets, balls, initialize_balls, cushions
from ui import draw_text_centered_with_shadow, draw_text_with_shadow, draw_text
from cue import Cue
from assets import load_assets

pygame.init()

# Game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + BOTTOM_PANEL))
pygame.display.set_caption("Pool")

# Pymunk space
space = pymunk.Space()
static_body = space.static_body
cue_ball = initialize_balls(space)

# Load assets
table_image, ball_images, cue_image = load_assets()

# Create cue
cue = Cue(cue_image, cue_ball.body.position)
for cushion in cushions:
    create_cushion(cushion, space)

# Clock
clock = pygame.time.Clock()

# Game loop
run = True
menu_active = True
game_running = False
force = 0
force_direction = 1
powering_up = False
potted_balls = []

while run:
    clock.tick(FPS)
    space.step(1 / FPS)

    # Fill background
    screen.fill(BG)

    if menu_active:
        # Draw the main menu
        draw_text_centered_with_shadow("POOL GAME", large_font, HIGHLIGHT, SHADOW, screen, SCREEN_HEIGHT // 2 - 100)
        draw_text_centered_with_shadow("Press SPACE to Play", font, WHITE, SHADOW, screen, SCREEN_HEIGHT // 2)
        draw_text_centered_with_shadow("Press ESC to Quit", font, WHITE, SHADOW, screen, SCREEN_HEIGHT // 2 + 40)

        # Handle events for the menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu_active = False
                    game_running = True
                if event.key == pygame.K_ESCAPE:
                    run = False

    elif game_running:
        screen.fill(GREY)
        screen.blit(table_image, (0, 0))

        # Check for potted balls
        for i, ball in enumerate(balls):
            for pocket in pockets:
                ball_x_dist = abs(ball.body.position[0] - pocket[0])
                ball_y_dist = abs(ball.body.position[1] - pocket[1])
                ball_dist = math.sqrt((ball_x_dist ** 2) + (ball_y_dist ** 2))
                if ball_dist <= pocket_dia / 2:
                    # If the cue ball is potted, reset its position
                    if ball == cue_ball:
                        ball.body.position = (888, SCREEN_HEIGHT / 2)
                        ball.body.velocity = (0, 0)
                    else:
                        # Remove potted balls
                        space.remove(ball.body)
                        balls.remove(ball)
                        potted_balls.append(ball_images[i])
                        ball_images.pop(i)

        # Draw all balls
        for i, ball in enumerate(balls):
            screen.blit(ball_images[i], 
                        (ball.body.position[0] - dia // 2, 
                         ball.body.position[1] - dia // 2))

        # Check if all balls have stopped
        taking_shot = True
        for ball in balls:
            vx, vy = ball.body.velocity  # Получаем скорости по осям x и y
            if math.isnan(vx) or math.isnan(vy):
              ball.body.velocity = (0, 0) 
            if int(ball.body.velocity[0]) != 0 or int(ball.body.velocity[1]) != 0:
                taking_shot = False

        # Draw cue if it's time to take a shot
        if taking_shot:
            mouse_pos = pygame.mouse.get_pos()
            cue.rect.center = cue_ball.body.position
            x_dist = cue_ball.body.position[0] - mouse_pos[0]
            y_dist = -(cue_ball.body.position[1] - mouse_pos[1])  # Invert y-axis for correct angle
            cue_angle = math.degrees(math.atan2(y_dist, x_dist))
            cue.update(cue_angle)  # Обновляем угол и позицию кия 
            cue.draw(screen)

        # Handle cue power-up and hit
        if powering_up:
            force += 100 * force_direction
            if force >= max_force or force <= 0:
                force_direction *= -1
            # Draw power bar
            for b in range(math.ceil(force / 2000)):
                pygame.draw.rect(screen, RED, 
                                 (cue_ball.body.position[0] - 30 + (b * 15), 
                                  cue_ball.body.position[1] + 30, 10, 20))
        elif not powering_up and taking_shot:
            x_impulse = math.cos(math.radians(cue_angle))
            y_impulse = math.sin(math.radians(cue_angle))
            cue_ball.body.apply_impulse_at_local_point((force * -x_impulse, force * y_impulse), (0, 0))
            force = 0
            force_direction = 1
            draw_text_with_shadow(f"Max Force: {max_force}", font, WHITE, SHADOW, SCREEN_WIDTH - 200, SCREEN_HEIGHT + BOTTOM_PANEL - 40, screen)
        # Draw potted balls
        for i, ball in enumerate(potted_balls):
            screen.blit(ball, (10 + (i * 50), SCREEN_HEIGHT + 10))

        # Check win condition
        if len(balls) == 1:  # Only the cue ball is left
            draw_text_centered_with_shadow("YOU WIN!", large_font, WHITE, SHADOW, screen, SCREEN_HEIGHT // 2 - 100)
            game_running = False

        # Handle game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and taking_shot:
                powering_up = True
            if event.type == pygame.MOUSEBUTTONUP and taking_shot:
                powering_up = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_running = False
                    menu_active = True
                if event.key == pygame.K_UP:
                    max_force = min(20000, max_force + 1000)
                if event.key == pygame.K_DOWN:
                    max_force = max(2000, max_force - 1000)
                    
    pygame.display.update()

pygame.quit()
