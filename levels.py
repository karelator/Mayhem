import classes as c, config as cfg

# Function to only generate a border
def border():
    border_width = 10
    walls = []
    walls.append(c.Wall(0, cfg.PLAY_AREA_X, 0, border_width ))                                # Top border
    walls.append(c.Wall(0, cfg.PLAY_AREA_X, cfg.PLAY_AREA_Y - border_width, cfg.PLAY_AREA_Y)) # Bottom border
    walls.append(c.Wall(0, border_width, 0, cfg.PLAY_AREA_Y))                                 # Left border
    walls.append(c.Wall(cfg.PLAY_AREA_X - border_width, cfg.PLAY_AREA_X, 0, cfg.PLAY_AREA_Y)) # Right border
    return walls

def lvl1():
    walls = border()
    return walls