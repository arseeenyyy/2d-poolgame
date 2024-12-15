import pygame
import math

class Cue:
  def __init__(self, cue_image, pos):
    self.original_image = cue_image
    self.angle = 0
    self.image = pygame.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_rect()
    self.rect.center = pos

  def update(self, angle):
    if math.isnan(angle):
        angle = 0
    self.angle = angle

  def draw(self, surface):
    if math.isnan(self.angle):
        self.angle = 0
    # if self.original_image is None:
    #     raise ValueError("Cue image is missing or corrupted.")
    # print(f"Original Image Size: {self.original_image.get_width()}x{self.original_image.get_height()}")
    # print(f"Angle: {self.angle}")
    self.image = pygame.transform.rotate(self.original_image, self.angle)
    surface.blit(self.image,
      (self.rect.centerx - self.image.get_width() / 2,
      self.rect.centery - self.image.get_height() / 2)
    )