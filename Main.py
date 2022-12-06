import pygame

from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

import game_functions as gf


def run_game():
    # Initialize game and create a screen object.
    pygame.init()

    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Create an instance to store game statistics
    stats = GameStats(settings)

    # Create a scoreboard
    sb = Scoreboard(settings, screen, stats)

    # Make a ship
    ship = Ship(settings, screen)

    # Make a group to store bullets in
    bullets = Group()

    # Make a group of aliens
    aliens = Group()

    # Create the fleet of aliens
    gf.create_fleet(settings, screen, ship, aliens)

    # Make a play button
    play_button = Button(settings, screen, "Play")

    # Setting Frame rate
    clock = pygame.time.Clock()

    # Start the main loop for the game.
    while True:
        gf.check_events(settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(settings, stats, screen, sb, ship, aliens, bullets)
        gf.update_screen(settings, screen, stats, sb, ship, aliens, bullets, play_button)
        clock.tick(120)


run_game()
