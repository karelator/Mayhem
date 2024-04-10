# FILE FOR ALL GAME ASSETS
import pygame as pg

BG_FILENAME = "mayhem-bg.png"
origbg = pg.image.load(BG_FILENAME)
# origbg.convert()

# Make rocket white triangle
rocket_img = pg.Surface((40, 40), pg.SRCALPHA)
pg.draw.polygon(rocket_img, (255, 255, 255), [(8, 40), (20, 32), (32, 40), (20, 0)], 0)
# Add black outline
pg.draw.polygon(rocket_img, (0, 0, 0), [(8, 40), (20, 32), (32, 40), (20, 0)], 3)

# Make projectile img a white ball
projectile_img = pg.Surface((11, 11), pg.SRCALPHA)
pg.draw.circle(projectile_img, (255, 255, 255), (6, 6), 5, 0)
# Add black outline
pg.draw.circle(projectile_img, (0, 0, 0), (6, 6), 5, 1)

# Make asteroid img a dark greyish circle
asteroid_img = pg.Surface((41, 41), pg.SRCALPHA)
pg.draw.circle(asteroid_img, (20, 20, 20), (21, 21), 20, 0)