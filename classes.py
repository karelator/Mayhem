# Import pygame with abbreviated alias
import pygame as pg
from typing import Any
import config as cfg
import assets as asset
import main as main
import random

class Sprite(pg.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.original_image = image
        self.image = image
        # Initialize rect to image located at coords
        self.rect = self.image.get_rect(center=(x, y))

class Movable_object(Sprite):
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
        # Starting value for fuel
        self.fuel_lvl = 1000
        # Starting value for score
        self.score = 0
        
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
        # Kill the sprite after collisions
        self.die()

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
        # Add rotation input to heading angle
        self.heading.rotate_ip(self.inputs[1] * 5)
        new_angle = self.heading.angle_to(pg.math.Vector2(0, -1))
        rotated_image = pg.transform.rotate(asset.rocket_img, new_angle) if not self.inputs[0]\
                   else pg.transform.rotate(asset.rocket_thrusting_img, new_angle)
        self.rect = rotated_image.get_rect(center=self.rect.center)
        self.image = rotated_image

    def set_inputs(self, input_list):
        self.inputs = input_list

    def thrust(self):
        self.acc += self.heading * self.inputs[0] * cfg.THRUSTFORCE
        smoke_list = []
        if cfg.SMOKE:
            n_smoke = random.randint(3, 5)
            smoke_heading = (self.speed / 2) - (self.heading * cfg.SMOKESPEED)
            for _ in range(n_smoke):
                smoke_list.append(Smoke_Particle(self.rect.centerx, self.rect.centery, smoke_heading))
        return smoke_list


    # Function to handle shooting logic, spawning the projectiles and enforcing cooldown
    def shoot(self):
        # Cancel if not long enough since last shot
        if self.frames_since_shoot < cfg.SHOOT_CD:
            return None
        self.frames_since_shoot = 0
        # TODO: Consider if bullet speed should be affected by rocket velocity? Add recoil?
        new_projectile = Projectile(self.rect.centerx + self.heading.x * 20,
                                    self.rect.centery + self.heading.y * 20, self.heading)
        return new_projectile
    

    # Function to handle collisions between sprites
    def die(self):
        # Collision detection with walls
        for wall in main.Game.wall_group:
            if pg.sprite.collide_rect(self, wall):
                self.kill()
                self.score -= 50
                return
        # Collision detection with other player
        for player in main.Game.player_group:
            if pg.sprite.collide_rect(self, player):
                self.kill()
                self.score -= 50
                return 
        # Collision detection with projectile
        for projectile in main.Game.proj_group:
            if pg.sprite.collide_rect(self, projectile):
                self.kill()
                self.score -= 50
                return


class Projectile(Movable_object):
    def __init__(self, x, y, heading_vector):
        super().__init__(asset.projectile_img, x, y)
        self.speed = heading_vector * cfg.BULLETSPEED

    def update(self):
        super().update()
        self.add_gravity()
        pass

class Smoke_Particle(Movable_object):
    def __init__(self, x, y, avg_trajectory):
        super().__init__(asset.smoke_particle_img, x, y)
        self.speed = pg.math.Vector2(avg_trajectory * cfg.SMOKESPEED) * random.uniform(0.8, 1.2)
        self.speed.rotate_ip(random.randint(-10, 10))
        self.lifetime = 0

    def update(self):
        super().update()
        self.lifetime += 1
        if self.lifetime > cfg.SMOKELIFETIME:
            self.kill()
        else:
            new_image = pg.Surface((11, 11), pg.SRCALPHA)
            pg.draw.circle(new_image, (120, 120, 120, 120 * (1 - (self.lifetime/ cfg.SMOKELIFETIME))), (6, 6), 5, 0)
            self.image = new_image


class Asteroid(Movable_object):
    def __init__(self):
        # Spawn 50 pixels above the screen, with random x val
        super().__init__(asset.asteroid_img, random.randint(0, int(cfg.PLAY_AREA_X * 1.2)), -50)
        random_dir = pg.math.Vector2(0, 1)
        random_dir.rotate_ip(random.randint(5, 30))
        random_speed = random.uniform(5, 10)
        self.speed = random_dir * random_speed


    def update(self):
        super().update()
        self.add_gravity()
        if self.rect.top > cfg.PLAY_AREA_Y:
            self.kill()
        pass


class Level_Design(Sprite):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
    
    def update(self):
        pass


class Platform(Level_Design):
    def __init__(self, x, y):
        super().__init__("platform_base.png", x, y)
    
    def update(self):
        super().update()
        pass

class Wall(Level_Design):
    def __init__(self, x1, x2, y1, y2):
        new_wall = pg.Surface((x2-x1, y2-y1))
        new_wall.fill((255, 255, 255))
        super().__init__(new_wall, (x1+x2)/2, (y1+y2)/2)