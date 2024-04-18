# Default res at launch
SCREEN_X = 1080 # 1080 2560
SCREEN_Y = 720 # 720 1440
# Resolution for backend gameplay area calculations
PLAY_AREA_X = 1440
PLAY_AREA_Y = 1080 
FRAMERATE = 90
# 0 = All players respawn when one die | 1 = Only dead player respawns
RESPAWN_BEHAVIOUR = 0
# Margin to make game less crowded and fit UI elements
LR_MARGIN = 250 # Left/Right
UD_MARGIN = 50 # Up/Down
# Gravitational Force in pixels per frame
GRAVITY = 0.1
# Thrusting Force
THRUSTFORCE = 0.4
# Safe speed and angle for landing on platforms
SAFELANDING_SPEED = 5
SAFELANDING_ANGLE = 25
# Bullet (Projectile) Speed SHOOT COOLDOWN IN SECONDS
BULLETSPEED = 20
SHOOT_CD = 0.2
# Toggle smoke, Average smoke speed from thrusting, and its lifetime (seconds)
SMOKE = True
SMOKESPEED = 2
SMOKELIFETIME = 0.3

# Turn on/off asteroids | Average Spawnrate (Lower = Faster) | How many bullets to destroy asteroid
ASTEROIDS = True
ASTEROID_SPAWNRATE = 1000
ASTEROID_HP = 1
# Fuel configurations (Droprate, starting fuel and spawnrate)
MAX_FUEL = 100
FUEL_DRAIN = 0.25
REFUEL_RATE = 10

# Points lost / gained for specific events
CRASH_PENALTY = -50
KILL_REWARD = 100