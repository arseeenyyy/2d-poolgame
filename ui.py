import pygame
from settings import SCREEN_WIDTH

def draw_text_with_shadow(text, font, text_col, shadow_col, x, y, surface):
    shadow = font.render(text, True, shadow_col)
    surface.blit(shadow, (x + 3, y + 3))
    img = font.render(text, True, text_col)
    surface.blit(img, (x, y))
  
def draw_text_centered_with_shadow(text, font, text_col, shadow_col, surface, y):
    img = font.render(text, True, text_col)
    rect = img.get_rect(center=(SCREEN_WIDTH // 2, y))
    shadow_rect = rect.copy()
    shadow_rect.topleft = (rect.topleft[0] + 3, rect.topleft[1] + 3)
    shadow = font.render(text, True, shadow_col)
    surface.blit(shadow, shadow_rect.topleft)
    surface.blit(img, rect.topleft)

def draw_text(text, font, text_col, x, y, surface):
    img = font.render(text, True, text_col)
    surface.blit(img, (x, y))
