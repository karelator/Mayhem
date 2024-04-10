# FILE FOR ALL GAME ASSETS
import pygame as pg

BG_FILENAME = "mayhem-bg.png"
origbg = pg.image.load(BG_FILENAME)
# origbg.convert()

rocket_img = pg.Surface((40, 40), pg.SRCALPHA)
# Make rocket a simple trianglular polygon
pg.draw.polygon(rocket_img, (0, 0, 0), [(8, 40), (20, 32), (32, 40), (20, 0)], 3)

asteroid_img = pg.Surface((41, 41), pg.SRCALPHA)
pg.draw.circle(asteroid_img, (0, 0, 0), (21, 21), 20, 1)