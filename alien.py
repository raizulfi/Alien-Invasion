import pygame

from pygame.sprite import Sprite


class Alien(Sprite):
    # A class for an alien in the fleet
    def __init__(self, settings, screen):
        # Initialize and set starting position
        super().__init__()
        self.screen = screen
        self.settings = settings

        # Load image and get rect
        self.image = pygame.image.load("Images/Alien.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()

        # Start each new alien at the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's position
        self.x = float(self.rect.x)

    def blit_me(self):
        # Draw the alien at its current location
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        # Return true when alien is at edge of screen
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        # Move the alien right or left
        self.x += (self.settings.alien_speed_factor * self.settings.fleet_direction)
        self.rect.x = self.x
