import sys

from bullet import Bullet
from alien import Alien
from time import sleep

import pygame


def check_keydown_events(event, settings, screen, ship, bullets):

    keys = pygame.key.get_pressed()

    # Check for key presses
    if event.key == pygame.K_d:
        # Move the ship to the right
        ship.moving_right = True
    elif event.key == pygame.K_a:
        # Move the ship to the left
        ship.moving_left = True
    elif event.key == pygame.K_LEFT:
        fire_bullet(settings, screen, ship, bullets)
    elif event.key == pygame.K_BACKSPACE:
        pygame.display.quit()
        sys.exit()

    if keys[pygame.K_d] and keys[pygame.K_RIGHT]:
        # Dash right
        if ship.rect.right <= ship.screen_rect.right - 300:
            ship.center += 200
        else:
            # Out of bounds prevention
            ship.center += ship.screen_rect.right - ship.rect.right - 25
    if keys[pygame.K_a] and keys[pygame.K_RIGHT]:
        # Dash left
        if ship.rect.left >= 300:
            ship.center -= 200
        else:
            # Out of bounds prevention
            ship.center -= ship.rect.left - 25


def check_keyup_events(event, ship):
    # Check for key releases
    if event.key == pygame.K_d:
        # Stop moving to the right
        ship.moving_right = False
    elif event.key == pygame.K_a:
        # Stop moving to the left
        ship.moving_left = False


def check_events(settings, screen, stats, sb, play_button, ship, aliens, bullets):
    # respond to key presses and mouse events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    # Start a new game when a player hits the play button\
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset game settings
        settings.initialize_dynamic_settings()

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

        # Reset statistics
        stats.reset_stats()
        stats.game_active = True

        # Remove aliens and bullets
        aliens.empty()
        bullets.empty()

        # Reset scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Create a new fleet and center the ship
        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(settings, screen, stats, sb, ship, aliens, bullets, play_button):
    # update images on the screen and make it visible
    # redraw screen every pass through loop
    screen.fill(settings.bg_color)

    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blit_me()
    aliens.draw(screen)

    # Draw the score information
    sb.show_score()

    # Draw play button if game is inactive
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def update_bullets(settings, screen, stats, sb, ship, aliens, bullets):
    # Update bullet positions
    bullets.update()

    # Get rid of bullets outside the screen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(settings, screen, stats, sb, ship, aliens, bullets)


def fire_bullet(settings, screen, ship, bullets):
    # Create a new bullet and add it to the bullet group
    if len(bullets) < settings.bullets_allowed:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens(settings, alien_width):
    # Determine the number of aliens in a row
    available_space_x = settings.screen_width - (2 * alien_width)
    number_of_aliens = int(available_space_x / (2 * alien_width))
    return number_of_aliens


def get_number_of_rows(settings, ship_height, alien_height):
    # Determine the number of rows
    available_space_y = settings.screen_height - 3 * alien_height - ship_height
    number_of_rows = int(available_space_y / (2 * alien_height))
    return number_of_rows


def create_alien(settings, screen, aliens, alien_number, row_numbers):
    # Create an alien and place it in the row
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_numbers
    aliens.add(alien)


def create_fleet(settings, screen, ship, aliens):
    alien = Alien(settings, screen)
    number_of_aliens = get_number_aliens(settings, alien.rect.width)
    number_of_rows = get_number_of_rows(settings, ship.rect.height, alien.rect.height)

    # Create the fleet
    for row in range(number_of_rows):
        for alien_number in range(number_of_aliens):
            create_alien(settings, screen, aliens, alien_number, row)


def check_fleet_edges(settings, aliens):
    # Respond appropriately when any alien reaches an edge
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break


def change_fleet_direction(settings, aliens):
    # Drop the entire fleet and change direction
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1


def check_bullet_alien_collisions(settings, screen, stats, sb, ship, aliens, bullets):
    # Respond to bullet-alien collisions
    # Delete bullets and aliens that have collided
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Destroy existing bullets, increase the level, speed up the game and create new fleet
        bullets.empty()
        stats.level += 1
        sb.prep_level()
        settings.increase_speed()
        create_fleet(settings, screen, ship, aliens)


def update_aliens(settings, stats, screen, sb, ship, aliens, bullets):
    # Check if fleet is at edge, then update the position of all aliens
    check_fleet_edges(settings, aliens)
    aliens.update()

    # Check for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, stats, screen, sb, ship, aliens, bullets)

    # Check for aliens hitting the bottom of the screen
    check_aliens_bottom(settings, stats, screen, sb, ship, aliens, bullets)


def check_aliens_bottom(settings, stats, screen, sb, ship, aliens, bullets):
    # Check if any aliens have reached the bottom of the screen
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat the same way as ship being hit
            ship_hit(settings, stats, screen, sb, ship, aliens, bullets)
            break


def ship_hit(settings, stats, screen, sb, ship, aliens, bullets):
    # Response to ship being hit by alien / alien hit the bottom

    if stats.ships_left > 0:
        # Decrease ship count
        stats.ships_left -= 1

        # Show scoreboard
        sb.prep_ships()

        # Remove all bullets and aliens
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_high_score(stats, sb):
    # Check to see if there's a new high score
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
