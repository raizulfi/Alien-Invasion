class Settings:
    # A class to store all settings for the game

    def __init__(self):
        # Initialize static game settings

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (205, 205, 205)

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 51, 51, 255
        self.bullets_allowed = 3

        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien_points value increases
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # Initialize dynamic game settings
        self.ship_speed_factor = 8
        self.bullet_speed_factor = 6
        self.alien_speed_factor = 1

        # For fleet direction, 1 is right and -1 is left
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        # Increase speed settings and point values
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)


