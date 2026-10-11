# nbody

N-body gravity simulation built with Pygame. Particles attract each other
through gravitational force, orbit, collide and merge. Click to spawn, drag to launch.

![Python](https://img.shields.io/badge/python-3.10+-blue)
![Pygame](https://img.shields.io/badge/pygame-2.5+-green)

## setup

```bash
git clone https://github.com/OwksCode/nbody.git
cd nbody
pip install -r requirements.txt
```

## run

```bash
python main.py
```

## controls

| key / mouse | action |
|---|---|
| left click + drag | launch a particle (slingshot) |
| right click | spawn a heavy particle |
| space | pause / resume |
| T | toggle trails |
| C | toggle color by speed (blue=slow, red=fast) |
| + / - | speed up / slow down time |
| 1 | preset: solar system |
| 2 | preset: binary star system |
| 3 | preset: chaos (30 random particles) |
| 4 | preset: ring orbiting a star |
| esc | quit |

## how it works

Each frame the simulation:
1. computes gravitational force between every pair of particles (F = G·m1·m2 / r²)
2. updates velocities using Newton's second law (a = F/m)
3. updates positions (Euler integration) with screen wrapping
4. merges colliding particles (conserving momentum)

All physics are computed from scratch — no physics engine, just basic vector math.

## project structure

```
nbody/
├── main.py             # game loop, events, presets, pygame setup
├── particle.py         # Particle class (position, velocity, mass, trail)
├── physics.py          # gravity, integration, collision handling
├── renderer.py         # drawing particles, trails, UI overlay
├── config.py           # tunable constants (G, window size, colors)
└── tests/
    └── test_physics.py
```

## license

MIT