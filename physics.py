"""
Physics engine — gravity, integration, collisions.
This is where the actual simulation happens.
"""

import math
from particle import Particle
from config import G, DT, SOFTENING, MIN_MERGE_DIST


def compute_gravity(p1: Particle, p2: Particle) -> tuple[float, float]:
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    dist_sq = dx * dx + dy * dy + SOFTENING ** 2
    dist = math.sqrt(dist_sq)
    force = G * p1.mass * p2.mass / dist_sq
    fx = force * dx / dist
    fy = force * dy / dist
    return (fx, fy)


def update_velocities(particles: list[Particle], dt: float = DT) -> None:
    for p in particles:
        total_fx, total_fy = 0, 0
        for q in particles:
            if p != q:
                fx, fy = compute_gravity(p, q)
                total_fx += fx
                total_fy += fy
        p.vx += (total_fx / p.mass) * dt
        p.vy += (total_fy / p.mass) * dt


def update_positions(particles: list[Particle], dt: float = DT) -> None:
    for p in particles:
        p.x += p.vx * dt
        p.y += p.vy * dt
        p.update_trail()


def handle_collisions(particles: list[Particle]) -> list[Particle]:
    merged = []
    skip = set()
    for i in range(len(particles)):
        if i in skip:
            continue
        current = particles[i]
        for j in range(i + 1, len(particles)):
            if j in skip:
                continue
            if current.distance_to(particles[j]) < current.radius + particles[j].radius:
                current = current.merge_with(particles[j])
                skip.add(j)
        merged.append(current)
    return merged


def step(particles: list[Particle], dt: float = DT) -> list[Particle]:
    update_velocities(particles, dt)
    update_positions(particles, dt)
    return handle_collisions(particles)