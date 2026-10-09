"""
Particle class — holds position, velocity, mass, and trail history.
"""

import random
import math
from config import COLORS, DEFAULT_RADIUS, TRAIL_LENGTH


class Particle:
    def __init__(self, x: float, y: float, vx: float = 0, vy: float = 0, mass: float = 50):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.color = random.choice(COLORS)
        self.trail = []  # list of (x, y) past positions

    @property
    def radius(self) -> float:
        """radius scales with the cube root of mass so big particles aren't absurdly huge"""
        return max(DEFAULT_RADIUS, DEFAULT_RADIUS * (self.mass / 50) ** (1/3))

    def update_trail(self):
        """save current position to trail history"""
        self.trail.append((self.x, self.y))
        if len(self.trail) > TRAIL_LENGTH:
            self.trail.pop(0)

    def distance_to(self, other: "Particle") -> float:
        return math.hypot(self.x - other.x, self.y - other.y)

    def merge_with(self, other: "Particle") -> "Particle":
        total_mass = self.mass + other.mass
        new_x = (self.x * self.mass + other.x * other.mass) / total_mass
        new_y = (self.y * self.mass + other.y * other.mass) / total_mass
        new_vx = (self.vx * self.mass + other.vx * other.mass) / total_mass
        new_vy = (self.vy * self.mass + other.vy * other.mass) / total_mass
        p = Particle(new_x, new_y, new_vx, new_vy, total_mass)
        p.color = self.color if self.mass >= other.mass else other.color
        return p