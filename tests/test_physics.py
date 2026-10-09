"""tests for the physics engine"""

import math
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from particle import Particle
from physics import compute_gravity, update_velocities, update_positions, handle_collisions, step


class TestComputeGravity:
    def test_force_points_toward_other(self):
        """if p2 is to the right of p1, force on p1 should point right (positive fx)"""
        p1 = Particle(0, 0, mass=100)
        p2 = Particle(100, 0, mass=100)
        fx, fy = compute_gravity(p1, p2)
        assert fx > 0
        assert abs(fy) < 0.01  # should be ~0 since they're on the same horizontal line

    def test_force_is_symmetric(self):
        """force of p2 on p1 should be equal and opposite to force of p1 on p2"""
        p1 = Particle(0, 0, mass=50)
        p2 = Particle(80, 60, mass=120)
        fx1, fy1 = compute_gravity(p1, p2)
        fx2, fy2 = compute_gravity(p2, p1)
        assert abs(fx1 + fx2) < 0.01
        assert abs(fy1 + fy2) < 0.01

    def test_heavier_mass_stronger_force(self):
        p1 = Particle(0, 0, mass=100)
        light = Particle(100, 0, mass=10)
        heavy = Particle(100, 0, mass=1000)
        fx_light, _ = compute_gravity(p1, light)
        fx_heavy, _ = compute_gravity(p1, heavy)
        assert fx_heavy > fx_light

    def test_closer_means_stronger(self):
        p1 = Particle(0, 0, mass=100)
        close = Particle(50, 0, mass=100)
        far = Particle(200, 0, mass=100)
        fx_close, _ = compute_gravity(p1, close)
        fx_far, _ = compute_gravity(p1, far)
        assert fx_close > fx_far


class TestUpdateVelocities:
    def test_particles_accelerate_toward_each_other(self):
        p1 = Particle(0, 0, mass=100)
        p2 = Particle(200, 0, mass=100)
        old_vx1 = p1.vx
        old_vx2 = p2.vx
        update_velocities([p1, p2])
        # p1 should accelerate right (toward p2)
        assert p1.vx > old_vx1
        # p2 should accelerate left (toward p1)
        assert p2.vx < old_vx2

    def test_single_particle_no_change(self):
        p = Particle(100, 100, vx=5, vy=3, mass=50)
        update_velocities([p])
        assert p.vx == 5
        assert p.vy == 3


class TestUpdatePositions:
    def test_moves_in_velocity_direction(self):
        p = Particle(100, 100, vx=10, vy=-5, mass=50)
        update_positions([p], dt=1.0)
        assert p.x == 110
        assert p.y == 95

    def test_trail_grows(self):
        p = Particle(100, 100, vx=1, vy=0, mass=50)
        for _ in range(5):
            update_positions([p], dt=1.0)
        assert len(p.trail) == 5


class TestHandleCollisions:
    def test_overlapping_particles_merge(self):
        p1 = Particle(100, 100, mass=50)
        p2 = Particle(102, 100, mass=50)  # very close
        result = handle_collisions([p1, p2])
        assert len(result) == 1
        assert result[0].mass == 100  # masses add up

    def test_far_particles_dont_merge(self):
        p1 = Particle(0, 0, mass=50)
        p2 = Particle(500, 500, mass=50)
        result = handle_collisions([p1, p2])
        assert len(result) == 2

    def test_momentum_conserved(self):
        p1 = Particle(100, 100, vx=10, vy=0, mass=50)
        p2 = Particle(102, 100, vx=-10, vy=0, mass=50)
        result = handle_collisions([p1, p2])
        merged = result[0]
        # total momentum before: 50*10 + 50*(-10) = 0
        assert abs(merged.vx) < 0.01
        assert abs(merged.vy) < 0.01


class TestStep:
    def test_returns_list(self):
        particles = [Particle(100, 100, mass=50), Particle(300, 300, mass=50)]
        result = step(particles)
        assert isinstance(result, list)

    def test_particles_move(self):
        p = Particle(100, 100, vx=50, vy=0, mass=50)
        old_x = p.x
        step([p])
        assert p.x != old_x