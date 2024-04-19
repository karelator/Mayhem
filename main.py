# CODE BY Thomas Lillealter Nygård AND Andreas Karel Eriksen

# FILE FOR MAIN GAME LOOP

# Import pygame with abbreviated alias, and initialize
import pygame as pg
pg.init()
pg.font.init()
# Import config and functions file
import config as cfg, functions as fun, classes as c, assets as asset, levels as lvl
# Used for making sure code is exited fully when game is closed, randomly generate values and framerate independence
import sys, random, time, cProfile

class Game():
    def __init__(self):
        self.SCREEN_X = cfg.SCREEN_X
        self.SCREEN_Y = cfg.SCREEN_Y
        # Initialize screen to default size
        self.screen = pg.display.set_mode((self.SCREEN_X, self.SCREEN_Y), pg.RESIZABLE)
        pg.display.set_caption("Budget Blastoff")

        # Initialize background object and scale to cover screen
        self.background = fun.scale_to_cover(asset.origbg, self.SCREEN_X, self.SCREEN_Y)

        # Initialize game surface to 4:3 aspect ratio 
        self.orig_playarea = pg.Surface((cfg.PLAY_AREA_X, cfg.PLAY_AREA_Y), pg.SRCALPHA)
        self.orig_playarea.fill((0, 0, 0, 0))
        self.playarea = self.orig_playarea
        
        # Module to cap the fps
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

        # Groups for all different sprite types to handle collision and updating
        self.proj_group = pg.sprite.Group()
        self.particle_group = pg.sprite.Group()
        self.asteroid_group = pg.sprite.Group()
        self.wall_group = pg.sprite.Group()
        self.platform_group = pg.sprite.Group()

    def run(self):
        # Load level
        lvl1_walls, lvl1_platforms = lvl.lvl1()
        self.wall_group.add(lvl1_walls)
        self.all_sprites.add(lvl1_walls)
        self.platform_group.add(lvl1_platforms)
        self.all_sprites.add(lvl1_platforms)
        
        running = True

        # Time tracker for framerate independence
        self.last_time = time.time()

        while running:

            # Track time passed since last frame. Multiply by 60 to simulate 60 fps
            self.dt = time.time() - self.last_time
            self.dt *= 60
            self.last_time = time.time()

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
                    self.SCREEN_X, self.SCREEN_Y = event.w, event.h
                    pg.display.set_mode((self.SCREEN_X, self.SCREEN_Y), pg.RESIZABLE)
                    self.background = fun.scale_to_cover(asset.origbg, self.SCREEN_X, self.SCREEN_Y)
                    self.background.convert()
                    self.screen.blit(self.background, (0, 0))
                    self.playarea = fun.scale_to_fit(self.orig_playarea, self.SCREEN_X - cfg.LR_MARGIN, self.SCREEN_Y - cfg.UD_MARGIN)

                elif event.type == pg.KEYDOWN and event.key == pg.K_r:
                    self.hard_restart()

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
                new_smoke = self.Player1.thrust(self.dt)
                if new_smoke:
                    self.particle_group.add(new_smoke)
                    self.all_sprites.add(new_smoke)
            if keys[pg.K_UP]:
                new_smoke = self.Player2.thrust(self.dt)
                if new_smoke:
                    self.particle_group.add(new_smoke)
                    self.all_sprites.add(new_smoke)

            # Update sprites
            self.all_sprites.update(self.dt)

            # Game logic (collisions + events)
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
                            new_smoke = sprite.crashed()
                            for particle in new_smoke:
                                self.all_sprites.add(particle)
                                self.particle_group.add(particle)                            
                            self.respawn([sprite])
                        elif isinstance(hit, c.Player):
                            new_smoke = sprite.crashed()
                            for particle in new_smoke:
                                self.all_sprites.add(particle)
                                self.particle_group.add(particle)                            
                            hit.crashed()
                            self.respawn([sprite, hit])
                        elif isinstance(hit, c.Projectile):
                            # Got shot by projectile
                            new_smoke = sprite.got_shot(hit)
                            for particle in new_smoke:
                                self.all_sprites.add(particle)
                                self.particle_group.add(particle)
                            hit.kill()
                            self.respawn([sprite])
                        elif isinstance(hit, c.Asteroid):
                            new_smoke = sprite.crashed()
                            for particle in new_smoke:
                                self.all_sprites.add(particle)
                                self.particle_group.add(particle)
                            hit.kill()
                            self.respawn([sprite])
                        elif isinstance(hit, c.Platform): # Check if landing conditions are met
                            if abs(sprite.heading.angle_to((0, -1))) <= cfg.SAFELANDING_ANGLE  and sprite.speed.length_squared() < cfg.SAFELANDING_SPEED**2 * self.dt:
                                sprite.acc *= 0
                                sprite.refuel(self.dt)
                                if not sprite.is_thrusting():
                                    sprite.rect.bottom = hit.rect.top
                                    sprite.speed *= 0
                            else:
                                new_smoke = sprite.crashed()
                                for particle in new_smoke:
                                    self.all_sprites.add(particle)
                                    self.particle_group.add(particle)                                
                                self.respawn([sprite])
                                

                    # Bullet collision
                    elif isinstance(sprite, c.Projectile):
                        if isinstance(hit, c.Wall):
                            sprite.kill()
                        if isinstance(hit, c.Asteroid):
                            new_smoke = hit.got_shot(sprite)
                            for particle in new_smoke:
                                self.all_sprites.add(particle)
                                self.particle_group.add(particle)
                            sprite.kill()

                    # Smoke collision
                    elif isinstance(sprite, c.Smoke_Particle):
                        if isinstance(hit, c.Wall):
                            sprite.kill()

            # Attempt to spawn asteroid
            if cfg.ASTEROIDS:
                if not random.randint(0, int(cfg.ASTEROID_SPAWNRATE)):
                    new_asteroid = c.Asteroid()
                    self.asteroid_group.add(new_asteroid)
                    self.all_sprites.add(new_asteroid)

            self.draw()
            self.clock.tick(cfg.FRAMERATE)

        pg.quit()
        sys.exit()

    # Draw sprites to playarea in correct order and make scaled version
    def draw(self):
            self.asteroid_group.draw(self.orig_playarea)
            self.proj_group.draw(self.orig_playarea)
            self.particle_group.draw(self.orig_playarea)
            self.player_group.draw(self.orig_playarea)
            self.wall_group.draw(self.orig_playarea)
            self.platform_group.draw(self.orig_playarea)
            
            self.playarea = fun.scale_to_fit(self.orig_playarea, self.SCREEN_X - cfg.LR_MARGIN, self.SCREEN_Y - cfg.UD_MARGIN)
            
            # Draw bg and game surface such that centers aligns with display center
            top_left_of_playarea = ((self.SCREEN_X / 2) - (self.playarea.get_width() / 2), (self.SCREEN_Y / 2) - (self.playarea.get_height() / 2))
            self.screen.blit(self.playarea, top_left_of_playarea)
            
            # Scales score image to fit on game border taking up 1/3rd of game screen and uses same measure for fuel
            Score_Img = fun.scale_to_fit(asset.score_img, cfg.LR_MARGIN/2, self.playarea.get_height() / 3)
            UI_width, UI_height = Score_Img.get_size()

            # Draws and scales the p1fuel into surface of fitting size
            P1Fuel = pg.Surface((UI_width, UI_height), pg.SRCALPHA)
            P1Fuel.fill((255, 0, 0))
            fuel_percentage = self.Player1.get_fuel() / cfg.MAX_FUEL
            # Scale the fuel percentage to match the height of the bar
            bar_height = UI_height - int(fuel_percentage * UI_height)  
            pg.draw.polygon(P1Fuel, (0, 255, 0), [(0, bar_height), (UI_width, bar_height), (UI_width, UI_height), (0, UI_height)])

            # Draws, scales the p2fuel into surface of fitting size
            P2Fuel = pg.Surface((UI_width, UI_height), pg.SRCALPHA)
            P2Fuel.fill((255, 0, 0))
            fuel_percentage = self.Player2.get_fuel() / cfg.MAX_FUEL
            # Scale the fuel percentage to match the height of the bar
            bar_height = UI_height - int(fuel_percentage * UI_height)  
            pg.draw.polygon(P2Fuel, (0, 255, 0), [(0, bar_height), (UI_width, bar_height), (UI_width, UI_height), (0, UI_height)])

            # Writes and scales the score onto surfaces of fitting size
            p1_score = asset.score_font.render(str(self.Player1.score), True, (255, 255, 255))
            p1_score = fun.scale_to_fit(p1_score, UI_width, UI_width)
            p2_score = asset.score_font.render(str(self.Player2.score), True, (255, 255, 255))
            p2_score = fun.scale_to_fit(p2_score, UI_width, UI_width)

            # Blits all UI elements onto screen in correct positions
            self.screen.blit(P1Fuel, (top_left_of_playarea[0] - UI_width - 50, top_left_of_playarea[1] + self.playarea.get_height() - UI_height))
            self.screen.blit(P2Fuel, (top_left_of_playarea[0] + self.playarea.get_width() + 50 , top_left_of_playarea[1] + self.playarea.get_height() - UI_height))
            self.screen.blit(Score_Img, (top_left_of_playarea[0] - UI_width - 50, top_left_of_playarea[1]))
            self.screen.blit(Score_Img, (top_left_of_playarea[0] + self.playarea.get_width() + 50, top_left_of_playarea[1]))
            self.screen.blit(p1_score, (top_left_of_playarea[0] - UI_width - 50, top_left_of_playarea[1] + UI_height * 1.3))
            self.screen.blit(p2_score, (top_left_of_playarea[0] + self.playarea.get_width() + 50, top_left_of_playarea[1] + UI_height * 1.3))

            # Update the screen after all events have taken place
            pg.display.update()


    def respawn(self, dead_players):
        if cfg.RESPAWN_BEHAVIOUR == 0:
            start_time = time.time()
            # Death animation
            while time.time() <= start_time + 0.5:
                # Track time passed since last frame. Multiply by 60 to simulate 60 fps
                self.dt = time.time() - self.last_time
                self.dt *= 60
                self.last_time = time.time()
                # Make dead player explode while the rest of the game freezes for half a second
                self.screen.blit(self.background, (0, 0))
                self.orig_playarea.fill((0, 0, 0, 0))
                self.particle_group.update(self.dt)
                pg.sprite.groupcollide(self.particle_group, self.wall_group, 1, 0)
                self.draw()
                self.clock.tick(cfg.FRAMERATE)
            for player in self.player_group:
                player.reset_pos()
        else:
            for player in dead_players:
                player.reset_pos()
        for asteroid in self.asteroid_group:
            asteroid.kill()
        for projectile in self.proj_group:
            projectile.kill()

    def hard_restart(self):
        # Empty sprite list
        self.all_sprites = pg.sprite.Group()

        # Initialize the two players
        self.Player1 = c.Player(100, 800)
        self.Player2 = c.Player(1340, 800)

        # Make group for player sprites, then add to all sprite group
        self.player_group = pg.sprite.Group(self.Player1, self.Player2)
        for player in self.player_group:
            self.all_sprites.add(player)

        # Empty other sprite lists
        self.proj_group = pg.sprite.Group()
        self.particle_group = pg.sprite.Group()
        self.asteroid_group = pg.sprite.Group()
        self.wall_group = pg.sprite.Group()
        self.platform_group = pg.sprite.Group()
        self.run()

if __name__ == "__main__":
    Game1 = Game()
    cProfile.run("Game1.run()")
    pass