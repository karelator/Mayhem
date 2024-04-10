# Import pygame with abbreviated alias, and initialize
import pygame as pg
pg.init()
# Import config and functions file
import config as cfg
import functions as fun
import classes as c
import assets as asset
# Used for making sure code is exited fully when game is closed
import sys

if __name__ != "__main__":
    pg.quit()
    sys.exit()

# Object for monitor size
infoObject = pg.display.Info() 
# File directories and screen size
FULLSCREEN = cfg.FULLSCREEN
SCREEN_X = infoObject.current_w if cfg.FULLSCREEN else cfg.SCREEN_X
SCREEN_Y = infoObject.current_h if cfg.FULLSCREEN else cfg.SCREEN_Y


# Initialize screen depending on launched with fullscreen or not
screen = pg.display.set_mode((SCREEN_X, SCREEN_Y), pg.FULLSCREEN) if FULLSCREEN else pg.display.set_mode((SCREEN_X, SCREEN_Y), pg.RESIZABLE)

# Initialize background object and scale to cover screen

background = fun.scale_to_cover(asset.origbg, SCREEN_X, SCREEN_Y)


# Initialize game surface to 4:3 aspect ratio 
orig_playarea = pg.Surface((cfg.PLAY_AREA_X, cfg.PLAY_AREA_Y), pg.SRCALPHA)
orig_playarea.fill((200, 0, 0, 80))
 

clock = pg.time.Clock()

# Make group for all sprites
all_sprites = pg.sprite.Group()

# Initialize the two players
Player1 = c.Player(100, 800)
Player2 = c.Player(1340, 800)

# Make group for player sprites, then add to all sprite group
player_group = pg.sprite.Group(Player1, Player2)
for player in player_group:
    all_sprites.add(player)

# TODO: Make groups for other sprite types
proj_group = pg.sprite.Group()
particle_group = pg.sprite.Group()

running = True
while running:

    # Reset playarea
    orig_playarea.fill((250, 0, 0, 90))


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
                background = fun.scale_to_cover(asset.origbg, SCREEN_X, SCREEN_Y)
                playarea = fun.scale_to_fit(orig_playarea, SCREEN_X - cfg.LR_MARGIN, SCREEN_Y - cfg.UD_MARGIN)


        # Toggle between Fullscreen and Windowed
        elif event.type == pg.KEYDOWN and event.key == pg.K_F11:
            # Toggle Fullscreen bool
            FULLSCREEN = not FULLSCREEN
            SCREEN_X = infoObject.current_w if FULLSCREEN else cfg.SCREEN_X
            SCREEN_Y = infoObject.current_h if FULLSCREEN else cfg.SCREEN_Y
            screen = pg.display.set_mode((SCREEN_X, SCREEN_Y), pg.FULLSCREEN if FULLSCREEN else pg.RESIZABLE)
            background = fun.scale_to_cover(asset.origbg, SCREEN_X, SCREEN_Y)
            playarea = fun.scale_to_fit(orig_playarea, SCREEN_X - cfg.LR_MARGIN, SCREEN_Y - cfg.UD_MARGIN)


    # Parse player input to rockets
    keys = pg.key.get_pressed()
    # [Thrust 0/1, Shoot 0/1, Rotate -1/0/1]
    P1_input = [keys[pg.K_w], keys[pg.K_d] - keys[pg.K_a]]
    P2_input = [keys[pg.K_UP], keys[pg.K_RIGHT] - keys[pg.K_LEFT]]
    # Store inputs in input field so it is accessable in update
    Player1.set_inputs(P1_input)
    Player2.set_inputs(P2_input)
    # Handle shooting, shoot functions return projectile object if it shot
    if keys[pg.K_LSHIFT] or keys[pg.K_s]:
        new_proj = Player1.shoot()
        if new_proj:
            proj_group.add(new_proj)
            all_sprites.add(new_proj)
    if keys[pg.K_SPACE] or keys[pg.K_DOWN]:
        new_proj = Player2.shoot()
        if new_proj:
            proj_group.add(new_proj)
            all_sprites.add(new_proj)
    # Handle thrusting, thrust function returns smoke particle objects
    if keys[pg.K_w]:
        new_smoke = Player1.thrust()
        if new_smoke:
            proj_group.add(new_smoke)
            all_sprites.add(new_smoke)
    if keys[pg.K_UP]:
        new_smoke = Player2.thrust()
        if new_smoke:
            proj_group.add(new_smoke)
            all_sprites.add(new_smoke)


    # Update sprites
    all_sprites.update()

    # Game event logic 

    # Draw sprites to playarea in correct order and make scaled version
    proj_group.draw(orig_playarea)
    particle_group.draw(orig_playarea)
    player_group.draw(orig_playarea)
    
    
    playarea = fun.scale_to_fit(orig_playarea, SCREEN_X - cfg.LR_MARGIN, SCREEN_Y - cfg.UD_MARGIN)
    
    # Draw bg and game surface such that centers aligns with display center
    screen.blit(background, ((SCREEN_X / 2) - (background.get_width() / 2), (SCREEN_Y / 2) - (background.get_height() / 2)))
    screen.blit(playarea, ((SCREEN_X / 2) - (playarea.get_width() / 2), (SCREEN_Y / 2) - (playarea.get_height() / 2)))

    # Update the screen after all events have taken place
    pg.display.update()
    clock.tick(cfg.FRAMERATE)

pg.quit()
sys.exit()