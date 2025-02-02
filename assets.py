# CODE BY Thomas Lillealter Nygård AND Andreas Karel Eriksen

# FILE FOR ALL GAME ASSETS
import pygame as pg

BG_FILENAME = "mayhem-bg.png"
origbg = pg.image.load(BG_FILENAME)

# Score text image: 100 x 500 pixels
SCORE_TEXT = "Score_Image.png"
score_img = pg.image.load(SCORE_TEXT)

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
pg.draw.circle(asteroid_img, (100, 47, 36), (31, 31), 30, 0)

# Make platform a grey rectangle
platform_img = pg.Surface((100, 15), pg.SRCALPHA)
platform_img.fill((38, 30, 33))

# Make fuel img a red square
fuel_img = pg.Surface((20, 20), pg.SRCALPHA)
fuel_img.fill((255,57,57))

score_font = pg.font.Font(None, 36)