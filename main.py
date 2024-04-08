# Import pygame with abbreviated alias
import pygame as pg
# Import config
import config
# Used for making sure code is exited fully when game is closed
import sys


# Settings:



# Object for monitor size
pg.init()
infoObject = pg.display.Info() 
# File directories and screen size
SCREEN_X = infoObject.current_w if config.FULLSCREEN else config.SCREEN_X
SCREEN_Y = infoObject.current_h if config.FULLSCREEN else config.SCREEN_Y


# Initialize screen
screen = pg.display.set_mode((SCREEN_X, SCREEN_Y), pg.FULLSCREEN) if config.FULLSCREEN else pg.display.set_mode((SCREEN_X, SCREEN_Y))

# Initialize background object and scale to fit screen
background = pg.image.load(config.BG_FILENAME)
background = pg.transform.scale(background, (SCREEN_X, SCREEN_Y))
background.convert()

clock = pg.time.Clock()

running = True
while running:

    screen.blit(background, (0, 0))

    # Exit application if player pressed quit button or escape
    for event in pg.event.get():
        if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            running = False
        elif event.type == pg.KEYDOWN:
            # Switch settings
            if event.key == pg.K_w:
                pass
            elif event.key == pg.K_a:
                pass
            elif event.key == pg.K_s:
                pass
            elif event.key == pg.K_d:
                pass

    # Update the screen after all events have taken place
    pg.display.update()
    clock.tick(config.FRAMERATE)

pg.quit()
sys.exit()