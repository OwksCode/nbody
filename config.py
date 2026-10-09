# window
WIDTH = 1000
HEIGHT = 700
FPS = 60

# physics
G = 500             # gravitational constant — tweak this to change how strong gravity is
DT = 0.016          # time step per frame (~1/60)
SOFTENING = 10      # prevents division by zero when particles are very close
MIN_MERGE_DIST = 8  # particles closer than this merge into one

# particles
DEFAULT_MASS = 50
HEAVY_MASS = 500
DEFAULT_RADIUS = 4  # base radius, scales with mass

# trails
TRAIL_LENGTH = 80   # how many past positions to remember
TRAIL_ALPHA = 60    # transparency of trail dots (0-255)

# colors
BG_COLOR = (10, 10, 20)
COLORS = [
    (255, 100, 100),  # red
    (100, 200, 255),  # blue
    (100, 255, 150),  # green
    (255, 220, 100),  # yellow
    (200, 130, 255),  # purple
    (255, 170, 100),  # orange
]