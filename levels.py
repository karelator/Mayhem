import classes as c, config as cfg

# Function to only generate a border
def border():
    border_width = 10
    walls = []
    walls.append(c.Wall(0, cfg.SCREEN_X, 0, border_width ))                                # Top border
    walls.append(c.Wall(0, cfg.SCREEN_X, cfg.SCREEN_Y - border_width, cfg.SCREEN_Y)) # Bottom border
    walls.append(c.Wall(0, border_width, 0, cfg.SCREEN_Y))                                 # Left border
    walls.append(c.Wall(cfg.SCREEN_X - border_width, cfg.SCREEN_X, 0, cfg.SCREEN_Y)) # Right border
    return walls

def lvl1():
    walls = border()
    return walls