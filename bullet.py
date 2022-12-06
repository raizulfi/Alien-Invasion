import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    # A class to manage bullets

    def __init__(self, settings, screen, ship):
        # Create bullet at ship's location
        super().__init__()
        self.screen = screen

        # Create bullet at (0, 0) then set its correct position
        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Store bullet's position as decimal
        self.y = float(self.rect.y)

        self.color = settings.bullet_color
        self.speed_factor = settings.bullet_speed_factor

    def update(self):
        # Move the bullet up the screen
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        # Draw the bullet to the screen
        pygame.draw.rect(self.screen, self.color, self.rect)


