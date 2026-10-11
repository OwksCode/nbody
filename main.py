"""
nbody — main game loop.

Run with: python main.py
"""

import pygame
import sys
from particle import Particle
from physics import step
from renderer import draw_particles, draw_trails, draw_ui, draw_drag_line
from config import WIDTH, HEIGHT, FPS, BG_COLOR, DT, DEFAULT_MASS, HEAVY_MASS


def create_demo_particles() -> list[Particle]:
    """spawn a few particles to start with so the screen isn't empty"""
    sun = Particle(WIDTH // 2, HEIGHT // 2, 0, 0, mass=800)
    sun.color = (255, 220, 80)

    p1 = Particle(WIDTH // 2 + 150, HEIGHT // 2, 0, -3, mass=30)
    p2 = Particle(WIDTH // 2 - 200, HEIGHT // 2, 0, 2.5, mass=50)
    p3 = Particle(WIDTH // 2, HEIGHT // 2 - 180, 2.8, 0, mass=20)

    return [sun, p1, p2, p3]


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("nbody")
    clock = pygame.time.Clock()

    particles = create_demo_particles()
    paused = False
    show_trails = True
    time_scale = 1.0
    dragging = False
    drag_start = (0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    particles = create_demo_particles()
                elif event.key == pygame.K_t:
                    show_trails = not show_trails
                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                    time_scale = min(5.0, time_scale + 0.25)
                elif event.key == pygame.K_MINUS:
                    time_scale = max(0.25, time_scale - 0.25)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragging = True
                    drag_start = event.pos
                elif event.button == 3:
                    particles.append(Particle(event.pos[0], event.pos[1], 0, 0, HEAVY_MASS))
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and dragging:
                    mouse_pos = event.pos
                    vx = (drag_start[0] - mouse_pos[0]) * 0.05
                    vy = (drag_start[1] - mouse_pos[1]) * 0.05
                    particles.append(Particle(drag_start[0], drag_start[1], vx, vy, DEFAULT_MASS))
                    dragging = False

        if not paused:
            particles = step(particles, DT * time_scale)

        screen.fill(BG_COLOR)
        if show_trails:
            draw_trails(screen, particles)
        draw_particles(screen, particles)
        if dragging:
            draw_drag_line(screen, drag_start, pygame.mouse.get_pos())
        draw_ui(screen, len(particles), paused, time_scale)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()