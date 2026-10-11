import pygame
from particle import Particle
from config import WIDTH, HEIGHT, BG_COLOR, TRAIL_ALPHA


def draw_particles(screen: pygame.Surface, particles: list[Particle]) -> None:
    for p in particles:
        pygame.draw.circle(screen, p.color, (int(p.x), int(p.y)), int(p.radius))


def draw_trails(screen: pygame.Surface, particles: list[Particle]) -> None:
    for p in particles:
        for i, (tx, ty) in enumerate(p.trail):
            brightness = i / len(p.trail) * 0.5
            r = int(p.color[0] * brightness)
            g = int(p.color[1] * brightness)
            b = int(p.color[2] * brightness)
            pygame.draw.circle(screen, (r, g, b), (int(tx), int(ty)), 1)


def draw_ui(screen: pygame.Surface, particle_count: int, paused: bool, time_scale: float) -> None:
    font = pygame.font.SysFont("monospace", 14)
    lines = [
        f"particles: {particle_count}",
        f"speed: {time_scale:.1f}x",
        "PAUSED" if paused else "running",
    ]
    for i, line in enumerate(lines):
        surface = font.render(line, True, (180, 180, 180))
        screen.blit(surface, (10, 10 + i * 18))


def draw_drag_line(screen: pygame.Surface, start: tuple, end: tuple) -> None:
    pygame.draw.line(screen, (255, 255, 255), start, end, 1)