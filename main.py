# Import pygame with abbreviated alias, and initialize
import pygame as pg
import cProfile
pg.init()
# Import config and functions file
import config as cfg
import functions as fun
import classes as c
import assets as asset
import levels as lvl
# Used for making sure code is exited fully when game is closed
import sys
import random 

class Game():
    def __init__(self):

        # Object for monitor size
        self.infoObject = pg.display.Info() 
        # File directories and screen size
        self.FULLSCREEN = False
        self.SCREEN_X = cfg.SCREEN_X
        self.SCREEN_Y = cfg.SCREEN_Y


        # Initialize screen depending on launched with fullscreen or not
        self.screen = pg.display.set_mode((self.SCREEN_X, self.SCREEN_Y), pg.RESIZABLE)
        pg.display.set_caption("Budget Blastoff")

        # Initialize background object and scale to cover screen

        self.background = fun.scale_to_cover(asset.origbg, self.SCREEN_X, self.SCREEN_Y)


        # Initialize game surface to 4:3 aspect ratio 
        self.orig_playarea = pg.Surface((cfg.PLAY_AREA_X, cfg.PLAY_AREA_Y), pg.SRCALPHA)
        self.orig_playarea.fill((0, 0, 0, 0))
        self.playarea = self.orig_playarea
        

        self.clock = pg.time.Clock()

        # Make group for all sprites
        self.all_sprites = pg.sprite.Group()

        # Initialize the two players
        self.Player1 = c.Player(100, 800)
        self.Player2 = c.Player(1340, 800)

        # Make group for player sprites, then add to all sprite group
        self.player_group = pg.sprite.Group(self.Player1, self.Player2)
        for player in self.player_group:
            self.all_sprites.add(player)

        # TODO: Make groups for other sprite types
        self.proj_group = pg.sprite.Group()
        self.particle_group = pg.sprite.Group()
        self.asteroid_group = pg.sprite.Group()
        self.wall_group = pg.sprite.Group()
        self.platform_group = pg.sprite.Group()

    def run(self):

        lvl1_walls, lvl1_platforms = lvl.lvl1()
        self.wall_group.add(lvl1_walls)
        self.all_sprites.add(lvl1_walls)
        self.platform_group.add(lvl1_platforms)
        self.all_sprites.add(lvl1_platforms)
        

        running = True
        while running:

            # Reset playarea
            self.screen.blit(self.background, (0, 0))
            self.orig_playarea.fill((0, 0, 0, 0))

            # Accept user input
            for event in pg.event.get():
                # Exit application if player pressed quit button or escape
                if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    running = False
                # Resize window properly
                elif event.type == pg.VIDEORESIZE:
                    if not self.FULLSCREEN:
                        self.SCREEN_X, self.SCREEN_Y = event.w, event.h
                        pg.display.set_mode((self.SCREEN_X, self.SCREEN_Y), pg.RESIZABLE)
                        self.background = fun.scale_to_cover(asset.origbg, self.SCREEN_X, self.SCREEN_Y)
                        self.background.convert()
                        self.screen.blit(self.background, (0, 0))
                        self.playarea = fun.scale_to_fit(self.orig_playarea, self.SCREEN_X - cfg.LR_MARGIN, self.SCREEN_Y - cfg.UD_MARGIN)


                # Toggle between Fullscreen and Windowed
                elif event.type == pg.KEYDOWN and event.key == pg.K_F11:
                    # Toggle Fullscreen bool
                    self.FULLSCREEN = not self.FULLSCREEN
                    self.SCREEN_X = self.infoObject.current_w if self.FULLSCREEN else cfg.SCREEN_X
                    self.SCREEN_Y = self.infoObject.current_h if self.FULLSCREEN else cfg.SCREEN_Y
                    self.screen = pg.display.set_mode((self.SCREEN_X, self.SCREEN_Y), pg.FULLSCREEN if self.FULLSCREEN else pg.RESIZABLE)
                    self.background = fun.scale_to_cover(asset.origbg, self.SCREEN_X, self.SCREEN_Y)
                    self.background.convert()
                    self.playarea = fun.scale_to_fit(self.orig_playarea, self.SCREEN_X - cfg.LR_MARGIN, self.SCREEN_Y - cfg.UD_MARGIN)


            # Parse player input to rockets
            keys = pg.key.get_pressed()
            # [Thrust 0/1, Shoot 0/1, Rotate -1/0/1]
            self.P1_input = [keys[pg.K_w], keys[pg.K_d] - keys[pg.K_a]]
            self.P2_input = [keys[pg.K_UP], keys[pg.K_RIGHT] - keys[pg.K_LEFT]]
            # Store inputs in input field so it is accessable in update
            self.Player1.set_inputs(self.P1_input)
            self.Player2.set_inputs(self.P2_input)
            # Handle shooting, shoot functions return projectile object if it shot
            if keys[pg.K_LSHIFT] or keys[pg.K_s]:
                new_proj = self.Player1.shoot()
                if new_proj:
                    self.proj_group.add(new_proj)
                    self.all_sprites.add(new_proj)
            if keys[pg.K_SPACE] or keys[pg.K_DOWN]:
                new_proj = self.Player2.shoot()
                if new_proj:
                    self.proj_group.add(new_proj)
                    self.all_sprites.add(new_proj)
            # Handle thrusting, thrust function returns smoke particle objects
            if keys[pg.K_w]:
                new_smoke = self.Player1.thrust()
                if new_smoke:
                    self.particle_group.add(new_smoke)
                    self.all_sprites.add(new_smoke)
            if keys[pg.K_UP]:
                new_smoke = self.Player2.thrust()
                if new_smoke:
                    self.particle_group.add(new_smoke)
                    self.all_sprites.add(new_smoke)


            # Update sprites
            self.all_sprites.update()

            # Game collision logic

            for sprite in self.all_sprites:
                collisions = pg.sprite.spritecollide(sprite, self.all_sprites, False)
                for hit in collisions:
                    if hit == sprite:
                        continue
                    # Player collisions
                    if isinstance(sprite, c.Player):
                        # Update masks before check
                        sprite.mask = pg.mask.from_surface(sprite.image)
                        hit.mask = pg.mask.from_surface(hit.image)
                        if not pg.sprite.collide_mask(sprite, hit):
                            continue
                        # Differentiate between events
                        if isinstance(hit, c.Wall):
                            sprite.kill()
                        elif isinstance(hit, c.Player):
                            sprite.kill()
                            hit.kill()
                        elif isinstance(hit, c.Projectile):
                            sprite.kill()
                            hit.kill()
                        elif isinstance(hit, c.Asteroid):
                            sprite.kill()
                        elif isinstance(hit, c.Platform): # Check if landing conditions are met
                            if abs(sprite.heading.angle_to((0, -1))) > cfg.SAFELANDING_ANGLE  or sprite.speed.length_squared() > cfg.SAFELANDING_SPEED**2:
                                sprite.kill()
                            sprite.acc *= 0
                            if sprite.is_thrusting():
                                sprite.thrust
                            else: 
                                sprite.rect.bottom = hit.rect.top
                                sprite.speed *= 0
                                

                    # Bullet collision
                    if isinstance(sprite, c.Projectile):
                        if isinstance(hit, c.Wall):
                            sprite.kill()


                        
            

            # Other game event logic 

            # Attempt to spawn asteroid
            if cfg.ASTEROIDS:
                if not random.randint(0, cfg.ASTEROID_SPAWNRATE):
                    new_asteroid = c.Asteroid()
                    self.asteroid_group.add(new_asteroid)
                    self.all_sprites.add(new_asteroid)

            # Draw sprites to playarea in correct order and make scaled version
            self.asteroid_group.draw(self.orig_playarea)
            self.proj_group.draw(self.orig_playarea)
            self.particle_group.draw(self.orig_playarea)
            self.player_group.draw(self.orig_playarea)
            self.wall_group.draw(self.orig_playarea)
            self.platform_group.draw(self.orig_playarea)
            
            self.playarea = fun.scale_to_fit(self.orig_playarea, self.SCREEN_X - cfg.LR_MARGIN, self.SCREEN_Y - cfg.UD_MARGIN)
            
            # Draw bg and game surface such that centers aligns with display center
            self.screen.blit(self.playarea, ((self.SCREEN_X / 2) - (self.playarea.get_width() / 2), (self.SCREEN_Y / 2) - (self.playarea.get_height() / 2)))

            # Update the screen after all events have taken place
            pg.display.update()
            self.clock.tick(cfg.FRAMERATE)

        pg.quit()
        sys.exit()

Game1 = Game()

if __name__ == "__main__":
    cProfile.run("Game1.run()")
    