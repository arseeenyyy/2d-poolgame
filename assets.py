import pygame

def load_assets():
    cue_image = pygame.image.load("assets/images/cue.png").convert_alpha()
    table_image = pygame.image.load("assets/images/table.png").convert_alpha()
    ball_images = [
        pygame.image.load(f"assets/images/ball_{i}.png").convert_alpha()
        for i in range(1, 17)
    ]
    return table_image, ball_images, cue_image
