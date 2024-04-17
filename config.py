# Default res at launch
SCREEN_X = 1080 # 1080 2560
SCREEN_Y = 720 # 720 1440
# Resolution for backend gameplay area calculations
PLAY_AREA_X = 1440
PLAY_AREA_Y = 1080 
FRAMERATE = 120
# 0 = All players respawn when one die | 1 = Only dead player respawns
RESPAWN_BEHAVIOUR = 0
# Margin to make game less crowded
LR_MARGIN = 50 # Left/Right
UD_MARGIN = 50 # Up/Down
# Gravitational Force in pixels per frame
GRAVITY = 0.1
# Thrusting Force
THRUSTFORCE = 0.4
# Safe speed and angle for landing on platforms
SAFELANDING_SPEED = 3
SAFELANDING_ANGLE = 25
# Bullet (Projectile) Speed SHOOT COOLDOWN IN SECONDS
BULLETSPEED = 20
SHOOT_CD = 0.2
# Toggle smoke, Average smoke speed from thrusting, and its lifetime
SMOKE = True
SMOKESPEED = 2
SMOKELIFETIME = 0.3

# Turn on/off asteroids | Spawnrate in average frames between each spawn | How many bullets to break apart asteroid
ASTEROIDS = True
ASTEROID_SPAWNRATE = 200
ASTEROID_HP = 1
# Fuel configurations (Droprate, starting fuel and spawnrate)
FUEL_DRATE = 0.25
START_FUEL = 1000
FUEL_SPAWNRATE = 250

# Points lost / gained for specific events
CRASH_PENALTY = -50
KILL_REWARD = 100