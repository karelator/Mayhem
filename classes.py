# Import pygame with abbreviated alias
import pygame as pg
from typing import Any
import config as cfg
import assets as asset
import random, time

class Sprite(pg.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.original_image = image
        self.image = image
        self.mask = pg.mask.from_surface(self.image)
        # Initialize rect to image located at coords
        self.rect = self.image.get_rect(center=(x, y))

class Movable_object(Sprite):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.speed = pg.math.Vector2()
        self.acc = pg.math.Vector2()

    def update(self, dt):
        # Add acceleration to speed, then reset acceleration for calculation next frame
        self.speed += (self.acc * dt)
        self.acc = pg.math.Vector2()

        # Update new position with speed
        self.rect.x += (self.speed.x * dt)
        self.rect.y += (self.speed.y * dt)
        pass

    # Make gravity calculation available for all movable objects, consider usage object by object
    def add_gravity(self, multiplier=1):
        # Adjust speed GRAVITY pixels down per frame
        self.acc.y += cfg.GRAVITY * multiplier

    def explode(self, min_particles, max_particles, speed_multiplier):
        n_smoke = random.randint(min_particles, max_particles)
        smoke_list = []
        for _ in range(n_smoke):
            smoke_heading = pg.math.Vector2(1, 0) 
            smoke_heading.rotate_ip(random.uniform(-180, 180))
            smoke_heading *= cfg.SMOKESPEED * speed_multiplier
            smoke_list.append(Smoke_Particle(self.rect.centerx, self.rect.centery, smoke_heading))
        return smoke_list


class Player(Movable_object):
    def __init__(self, x, y):
        super().__init__(asset.rocket_img, x, y)
        
        self.startpos = (x, y)

        # Store inputs in field so it is accessible in update [Thrust, Rotate]
        self.inputs = [0, 0]
        self.last_shot = time.time()
        # Player is only movable object with heading angle seperate from speed, initialize to straight up
        self.heading = pg.math.Vector2(0, -1)
        # Starting value for fuel
        self.fuel = cfg.MAX_FUEL
        # Initialize score value
        self.score = 0
        
    def update(self, dt):
        super().update(dt)

        # Add Gravity to acceleration
        self.add_gravity()
        # Accept player inputs
        self.accept_inputs(dt)
    
    def is_thrusting(self):
        return self.inputs[0]

    def get_fuel(self):
        return self.fuel

    # Convert user input to changes in parameters
    def accept_inputs(self, dt):
        # Add rotation input to heading angle
        self.heading.rotate_ip(self.inputs[1] * 5 * dt)
        new_angle = self.heading.angle_to(pg.math.Vector2(0, -1))
        rotated_image = pg.transform.rotate(asset.rocket_thrusting_img, new_angle) if self.inputs[0] and self.fuel > 0\
                   else pg.transform.rotate(asset.rocket_img, new_angle)
        self.rect = rotated_image.get_rect(center=self.rect.center)
        self.image = rotated_image

    def set_inputs(self, input_list):
        self.inputs = input_list

    def thrust(self, dt):
        smoke_list = []
        if self.fuel > 0:
            self.acc += self.heading * self.inputs[0] * cfg.THRUSTFORCE
            # Decrease fuel and set to 0 if negative
            self.fuel -= (cfg.FUEL_DRAIN * dt)
            if self.fuel < 0:
                self.fuel = 0
            if cfg.SMOKE:
                n_smoke = random.randint(3, 5)
                smoke_heading = (self.speed / 2) - (self.heading * cfg.SMOKESPEED)
                for _ in range(n_smoke):
                    smoke_list.append(Smoke_Particle(self.rect.centerx, self.rect.centery, smoke_heading))
        return smoke_list

    def refuel(self, dt):
        if self.fuel < cfg.MAX_FUEL:
            self.fuel += cfg.REFUEL_RATE * dt
        self.fuel = min(self.fuel, cfg.MAX_FUEL)

    # Function to handle shooting logic: spawning the projectiles and enforcing cooldown
    def shoot(self):
        # Cancel if not long enough since last shot
        if time.time() - self.last_shot < cfg.SHOOT_CD:
            return None
        self.last_shot = time.time()
        # TODO: Consider if bullet speed should be affected by rocket velocity? Add recoil?
        new_projectile = Projectile(self.rect.centerx + self.heading.x * 50,
                                    self.rect.centery + self.heading.y * 50, self.heading)
        return new_projectile
    
    def shot_other(self):
        self.score += cfg.KILL_REWARD

    def got_shot(self, other_player):
        other_player.shot_other()
        smoke = self.explode(30, 40, 2) if cfg.SMOKE else []
        self.rect.x = -200
        return smoke

    def crashed(self):
        self.score += cfg.CRASH_PENALTY
        smoke = self.explode(30, 40, 2) if cfg.SMOKE else []
        self.rect.x = -200
        return smoke

    def reset_pos(self):
        self.heading = pg.math.Vector2(0, -1)
        new_angle = self.heading.angle_to(pg.math.Vector2(0, -1))
        rotated_image = pg.transform.rotate(asset.rocket_img, new_angle)
        self.rect = rotated_image.get_rect(center=self.rect.center)
        self.image = rotated_image
        self.rect.center = self.startpos
        self.speed *= 0
        self.fuel = cfg.MAX_FUEL
        


class Projectile(Movable_object):
    def __init__(self, x, y, heading_vector):
        super().__init__(asset.projectile_img, x, y)
        self.speed = heading_vector * cfg.BULLETSPEED

    def update(self, dt):
        super().update(dt)
        self.add_gravity()
        pass

class Smoke_Particle(Movable_object):
    def __init__(self, x, y, avg_trajectory):
        super().__init__(asset.smoke_particle_img, x, y)
        self.speed = pg.math.Vector2(avg_trajectory * cfg.SMOKESPEED) * random.uniform(0.8, 1.2)
        self.speed.rotate_ip(random.randint(-10, 10))
        self.start_time = time.time()

    def update(self, dt):
        super().update(dt)
        if (time.time() - self.start_time) > cfg.SMOKELIFETIME:
            self.kill()
        else:
            new_image = pg.Surface((11, 11), pg.SRCALPHA)
            pg.draw.circle(new_image, (120, 120, 120, 120 * (1 - ((time.time() - self.start_time) / cfg.SMOKELIFETIME))), (6, 6), 5, 0)
            self.image = new_image


class Asteroid(Movable_object):
    def __init__(self):
        # Spawn 50 pixels above the screen, with random x val
        super().__init__(asset.asteroid_img, random.randint((0 - int(cfg.PLAY_AREA_X * 0.2)), int(cfg.PLAY_AREA_X * 1.2)), -50)
        random_dir = pg.math.Vector2(0, 1)
        random_dir.rotate_ip(random.randint(5, 30))
        random_speed = random.uniform(5, 10)
        self.speed = random_dir * random_speed
        self.times_shot = 0


    def update(self, dt):
        super().update(dt)
        self.add_gravity()
        if self.rect.top > cfg.PLAY_AREA_Y:
            self.kill()
        pass

    def got_shot(self):
        self.times_shot += 1
        smoke_list = []
        if self.times_shot >= cfg.ASTEROID_HP:
            smoke_list = self.explode(20, 30, 1) if cfg.SMOKE else []
            self.kill()
        return smoke_list



class Level_Design(Sprite):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
    
    def update(self, dt):
        pass


class Platform(Level_Design):
    def __init__(self, x, y):
        super().__init__(asset.platform_img, x, y)
    
    def update(self, dt):
        super().update(dt)
        pass

class Wall(Level_Design):
    def __init__(self, x1, x2, y1, y2):
        new_wall = pg.Surface((x2-x1, y2-y1))
        new_wall.fill((255, 255, 255))
        super().__init__(new_wall, (x1+x2)/2, (y1+y2)/2)