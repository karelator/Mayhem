# Import pygame with abbreviated alias
import pygame as pg
# Import config
import config
# Used for making sure code is exited fully when game is closed
import sys

# Function to scale a image object so it covers the display without distortion
def scale_to_cover(img_obj, x, y):
    # If taller than original ratio
    if x / y <= img_obj.get_width() / img_obj.get_height():
        new_img = pg.transform.scale(img_obj, (y *  (img_obj.get_width() / img_obj.get_height()), y))
    # If wider than original ratio
    else:
        new_img = pg.transform.scale(img_obj, (x, x * (img_obj.get_height() / img_obj.get_width())))
    new_img.convert()
    return new_img

# Function to scale a image object so it fits within the display without distortion
def scale_to_fit(img_obj, x, y):
    # If taller than original ratio
    if x / y <= img_obj.get_width() / img_obj.get_height():
        new_img = pg.transform.scale(img_obj, (x, x * (img_obj.get_height() / img_obj.get_width())))
    # If wider than original ratio
    else:
        new_img = pg.transform.scale(img_obj, (y *  (img_obj.get_width() / img_obj.get_height()), y))
    new_img.convert()
    return new_img




if __name__ != "__main__":
    sys.exit()

# Object for monitor size
pg.init()
infoObject = pg.display.Info() 
# File directories and screen size
SCREEN_X = infoObject.current_w if config.FULLSCREEN else config.SCREEN_X
SCREEN_Y = infoObject.current_h if config.FULLSCREEN else config.SCREEN_Y


# Initialize screen
screen = pg.display.set_mode((SCREEN_X, SCREEN_Y), pg.FULLSCREEN) if config.FULLSCREEN else pg.display.set_mode((SCREEN_X, SCREEN_Y), pg.RESIZABLE)

# Initialize background object and scale to cover screen
origbg = pg.image.load(config.BG_FILENAME)
origbg.convert()
background = scale_to_cover(origbg, SCREEN_X, SCREEN_Y)

clock = pg.time.Clock()

running = True
while running:
    # Draw background such that bg_img center aligns with display center
    screen.blit(background, ((SCREEN_X / 2) - (background.get_width() / 2), (SCREEN_Y / 2) - (background.get_height() / 2)))

    # Exit application if player pressed quit button or escape
    for event in pg.event.get():
        if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            running = False
        elif event.type == pg.VIDEORESIZE:
            SCREEN_X, SCREEN_Y = event.w, event.h
            pg.display.set_mode((SCREEN_X, SCREEN_Y), pg.RESIZABLE)
            background = scale_to_cover(origbg, SCREEN_X, SCREEN_Y)
           
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