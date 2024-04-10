# Import pygame with abbreviated alias
import pygame as pg
from typing import Any
import config as cfg
import assets as asset

class Element(pg.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.original_image = image
        self.image = image
        # Initialize rect to image located at coords
        self.rect = self.image.get_rect(center=(x, y))

class Item(Element):
    def __init__(self, image):
        super().__init__(image)
    
    def update(self):
        pass


class Movable_object(Element):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.speed = pg.math.Vector2()
        self.acc = pg.math.Vector2()

    def update(self):
        # Add acceleration to speed, then reset acceleration for calculation next frame
        self.speed += self.acc
        self.acc = pg.math.Vector2()

        # Update new position with speed
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y
        pass

    # Make gravity calculation available for all movable objects, consider usage object by object
    def add_gravity(self):
        # Adjust speed GRAVITY pixels down per frame
        self.acc.y += cfg.GRAVITY

class Player(Movable_object):
    def __init__(self, x, y):
        super().__init__(asset.rocket_img, x, y)
        
        # Store inputs in field so it is accessible in update [Thrust, Shoot, Rotate]
        self.inputs = [0, 0]
        self.frames_since_shoot = 0
        # Player is only movable object with heading angle seperate from speed, initialize to straight up
        self.heading = pg.math.Vector2(0, -1)
        
    def update(self):
        super().update()
        
        # One more frame since rocket last shot
        self.frames_since_shoot += 1
        # Add Gravity to acceleration
        self.add_gravity()
        # Accept player inputs
        self.accept_inputs()
        # Keep rocket in play area (temporary)
        self.keep_in_screen()

        pass

    def keep_in_screen(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.speed.x = 0
        elif self.rect.right > cfg.PLAY_AREA_X:
            self.rect.right = cfg.PLAY_AREA_X
            self.speed.x = 0
        if self.rect.top < 0:
            self.rect.top = 0
            self.speed.y = 0
        elif self.rect.bottom > cfg.PLAY_AREA_Y:
            self.rect.bottom = cfg.PLAY_AREA_Y
            self.speed.y = 0

    # Convert user input to changes in parameters
    def accept_inputs(self):
        # Add heading to acceleration if thrusting
        self.acc += self.heading * self.inputs[0] * cfg.THRUSTFORCE
        # Add rotation input to heading angle
        self.heading.rotate_ip(-self.inputs[1] * 5)
        new_angle = self.heading.angle_to(pg.math.Vector2(0, -1))
        rotated_image = pg.transform.rotate(asset.rocket_img, new_angle)
        self.rect = rotated_image.get_rect(center=self.rect.center)
        self.image = rotated_image

    def set_inputs(self, input_list):
        self.inputs = input_list

    # Function to handle shooting logic, spawning the projectiles and enforcing cooldown
    def shoot(self):
        # Cancel if not long enough since last shot
        if self.frames_since_shoot < cfg.SHOOT_CD:
            return None
        self.frames_since_shoot = 0
        # TODO: Consider if bullet speed should be affected by rocket velocity?
        new_projectile = Projectile(self.rect.centerx + self.heading.x * 20,
                                    self.rect.centery + self.heading.y * 20, self.heading)
        return new_projectile

class Projectile(Movable_object):
    def __init__(self, x, y, heading_vector):
        super().__init__(asset.projectile_img, x, y)
        self.speed = heading_vector * cfg.BULLETSPEED

    def update(self):
        super().update()
        pass


class Asteroid(Movable_object):
    def __init__(self, x, y):
        super().__init__(asset.asteroid_img, x, y)

    def update(self):
        super().update()
        pass


class Platform(Item):
    def __init__(self, x, y):
        super().__init__("platform_base.png", x, y)
    
    def update(self):
        super().update()
        pass