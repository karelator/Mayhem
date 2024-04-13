# FILE FOR ALL GAME ASSETS
import pygame as pg

BG_FILENAME = "mayhem-bg.png"
origbg = pg.image.load(BG_FILENAME)

# Make rocket white triangular polygon
rocket_img = pg.Surface((40, 40), pg.SRCALPHA)
pg.draw.polygon(rocket_img, (255, 255, 255), [(8, 40), (20, 32), (32, 40), (20, 0)], 0)
# Add black outline
pg.draw.polygon(rocket_img, (0, 0, 0), [(8, 40), (20, 32), (32, 40), (20, 0)], 3)

# Add thrusting version of image
rocket_thrusting_img = rocket_img.copy()
pg.draw.polygon(rocket_thrusting_img, (200, 40, 0), [(14, 36), (20, 32), (26,36), (20, 40)], 0)

# Smoke from thrusting
smoke_particle_img = pg.Surface((11, 11), pg.SRCALPHA)
pg.draw.circle(smoke_particle_img, (120, 120, 120, 120), (6, 6), 5, 0)

# Make projectile img a white ball
projectile_img = pg.Surface((11, 11), pg.SRCALPHA)
pg.draw.circle(projectile_img, (255, 255, 255), (6, 6), 5, 0)
# Add black outline
pg.draw.circle(projectile_img, (0, 0, 0), (6, 6), 5, 1)

# Make asteroid img a circle
asteroid_img = pg.Surface((61, 61), pg.SRCALPHA)
pg.draw.circle(asteroid_img, (108, 50, 83), (31, 31), 30, 0)

# Make platform a grey rectangle
platform_img = pg.Surface((75, 12), pg.SRCALPHA)
platform_img.fill((38, 30, 33))