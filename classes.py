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
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        # Initialize rect to starting position with size of width and height
        self.rect = pg.rect.Rect(x, y, self.width, self.height)

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
        self.inputs = [0, 0, 0]
        # Player is only movable object with heading angle seperate from speed, initialize to straight up
        self.heading = pg.math.Vector2(0, -1)
        
    def update(self):
        super().update()
        
    # Convert user input to changes in parameters
        # Add heading to acceleration if thrusting
        self.acc += self.heading * self.inputs[0] * cfg.THRUSTFORCE
        # Attempt to shoot
        if self.inputs[1]:
            self.shoot()
        # Add rotation input to heading angle
        self.heading.rotate_ip(-self.inputs[2] * 5)
        new_angle = self.heading.angle_to(pg.math.Vector2(0, -1))
        rotated_image = pg.transform.rotate(asset.rocket_img, new_angle)
        self.rect = rotated_image.get_rect(center=self.rect.center)
        self.image = rotated_image
        pass

    def set_inputs(self, input_list):
        self.inputs = input_list

    # Function to handle shooting logic, spawning the projectiles and enforcing cooldown
    def shoot(self):
        pass

class Asteroid(Movable_object):
    def __init__(self, x, y):
        super().__init__("asteroid_circle.png", x, y)

    def update(self):
        super().update()
        pass

class Projectile(Movable_object):
    def __init__(self, x, y):
        super().__init__("projectile_circle.png", x, y)

    def update(self):
        super().update()
        pass

class Platform(Item):
    def __init__(self, x, y):
        super().__init__("platform_base.png", x, y)
    
    def update(self):
        super().update()
        pass