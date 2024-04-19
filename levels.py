# CODE BY Thomas Lillealter Nygård AND Andreas Karel Eriksen

#FILE FOR LEVEL DESIGN
import classes as c, config as cfg

# Function to only generate a border
def border():
    border_width = 10
    walls = []
    walls.append(c.Wall(0, cfg.PLAY_AREA_X, 0, border_width ))                                  # Top border
    walls.append(c.Wall(0, cfg.PLAY_AREA_X, cfg.PLAY_AREA_Y - border_width, cfg.PLAY_AREA_Y))   # Bottom border
    walls.append(c.Wall(0, border_width, 0, cfg.PLAY_AREA_Y))                                   # Left border
    walls.append(c.Wall(cfg.PLAY_AREA_X - border_width, cfg.PLAY_AREA_X, 0, cfg.PLAY_AREA_Y))   # Right border
    return walls

def lvl1():
    walls = border()
    walls.append(c.Wall(500, cfg.PLAY_AREA_X - 500, 520, cfg.PLAY_AREA_Y - 520))                # Middle box
    walls.append(c.Wall(700, cfg.PLAY_AREA_X - 700, 700, cfg.PLAY_AREA_Y - 200))                # Lower middle box
    walls.append(c.Wall(0, 250, cfg.PLAY_AREA_Y - 240, cfg.PLAY_AREA_Y - 200))                  # Lower left
    walls.append(c.Wall(cfg.PLAY_AREA_X - 250, cfg.PLAY_AREA_X, cfg.PLAY_AREA_Y - 240, cfg.PLAY_AREA_Y - 200))    # Lower Right
    platforms = [c.Platform(100, cfg.PLAY_AREA_Y - 240), c.Platform(1340, cfg.PLAY_AREA_Y - 240), c.Platform(cfg.PLAY_AREA_X / 2, 520)]

    return (walls, platforms)