# Import pygame with abbreviated alias
import pygame as pg
# Import config and functions file
import config as cfg
import functions as fun
# Used for making sure code is exited fully when game is closed
import sys

if __name__ != "__main__":
    sys.exit()

# Object for monitor size
pg.init()
infoObject = pg.display.Info() 
# File directories and screen size
FULLSCREEN = cfg.FULLSCREEN
SCREEN_X = infoObject.current_w if cfg.FULLSCREEN else cfg.SCREEN_X
SCREEN_Y = infoObject.current_h if cfg.FULLSCREEN else cfg.SCREEN_Y


# Initialize screen depending on launched with fullscreen or not
screen = pg.display.set_mode((SCREEN_X, SCREEN_Y), pg.FULLSCREEN) if FULLSCREEN else pg.display.set_mode((SCREEN_X, SCREEN_Y), pg.RESIZABLE)

# Initialize background object and scale to cover screen
origbg = pg.image.load(cfg.BG_FILENAME)
origbg.convert()
background = fun.scale_to_cover(origbg, SCREEN_X, SCREEN_Y)

# Initialize game surface to 4:3 aspect ratio and scale to fit within screen, with padding
orig_playarea = pg.Surface((4, 3), pg.SRCALPHA)
# temp to test intended behaviour
orig_playarea.fill((200, 0, 0))
playarea = fun.scale_to_fit(orig_playarea, SCREEN_X - cfg.MARGIN, SCREEN_Y - cfg.MARGIN)



clock = pg.time.Clock()

running = True
while running:
    # Draw bg and game surface such that centers aligns with display center
    screen.blit(background, ((SCREEN_X / 2) - (background.get_width() / 2), (SCREEN_Y / 2) - (background.get_height() / 2)))
    screen.blit(playarea, ((SCREEN_X / 2) - (playarea.get_width() / 2), (SCREEN_Y / 2) - (playarea.get_height() / 2)))


    # Accept user input
    for event in pg.event.get():
        # Exit application if player pressed quit button or escape
        if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            running = False
        # Resize window properly
        elif event.type == pg.VIDEORESIZE:
            if not FULLSCREEN:
                SCREEN_X, SCREEN_Y = event.w, event.h
                pg.display.set_mode((SCREEN_X, SCREEN_Y), pg.RESIZABLE)
                background = fun.scale_to_cover(origbg, SCREEN_X, SCREEN_Y)
                playarea = fun.scale_to_fit(orig_playarea, SCREEN_X - cfg.MARGIN, SCREEN_Y - cfg.MARGIN)


        # Toggle between Fullscreen and Windowed
        elif event.type == pg.KEYDOWN and event.key == pg.K_F11:
            # Toggle Fullscreen bool
            FULLSCREEN = not FULLSCREEN
            SCREEN_X = infoObject.current_w if FULLSCREEN else cfg.SCREEN_X
            SCREEN_Y = infoObject.current_h if FULLSCREEN else cfg.SCREEN_Y
            screen = pg.display.set_mode((SCREEN_X, SCREEN_Y), pg.FULLSCREEN) if FULLSCREEN else\
                     pg.display.set_mode((SCREEN_X, SCREEN_Y), pg.RESIZABLE)
            background = fun.scale_to_cover(origbg, SCREEN_X, SCREEN_Y)
            playarea = fun.scale_to_fit(orig_playarea, SCREEN_X - cfg.MARGIN, SCREEN_Y - cfg.MARGIN)


        # Accept game input
        elif event.type == pg.KEYDOWN:
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
    clock.tick(cfg.FRAMERATE)

pg.quit()
sys.exit()