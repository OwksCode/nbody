import pygame, math
from particle import Particle
from config import WIDTH, HEIGHT, BG_COLOR, TRAIL_ALPHA

SLOW_COLOR = (50, 100, 255)
FAST_COLOR = (255, 50, 50)


def draw_particles(screen: pygame.Surface, particles: list[Particle], color_by_speed: bool = False) -> None:
    for p in particles:
        if color_by_speed:
            ratio = min(1.0, math.hypot(p.vx, p.vy) / 10)
            color = (
                int(SLOW_COLOR[0] + (FAST_COLOR[0] - SLOW_COLOR[0]) * ratio),
                int(SLOW_COLOR[1] + (FAST_COLOR[1] - SLOW_COLOR[1]) * ratio),
                int(SLOW_COLOR[2] + (FAST_COLOR[2] - SLOW_COLOR[2]) * ratio),
            )
        else:
            color = p.color
        pygame.draw.circle(screen, color, (int(p.x), int(p.y)), int(p.radius))


def draw_trails(screen: pygame.Surface, particles: list[Particle]) -> None:
    for p in particles:
        for i, (tx, ty) in enumerate(p.trail):
            brightness = i / len(p.trail) * 0.5
            r = int(p.color[0] * brightness)
            g = int(p.color[1] * brightness)
            b = int(p.color[2] * brightness)
            pygame.draw.circle(screen, (r, g, b), (int(tx), int(ty)), 1)


def draw_ui(screen: pygame.Surface, particle_count: int, paused: bool,
            time_scale: float, preset_name: str, show_trails: bool,
            color_by_speed: bool) -> None:
    font = pygame.font.SysFont("monospace", 14)

    # top-left: status
    lines = [
        f"scene: {preset_name}",
        f"particles: {particle_count}",
        f"speed: {time_scale:.1f}x",
        f"trails: {'on' if show_trails else 'off'}  |  color: {'speed' if color_by_speed else 'default'}",
        "PAUSED" if paused else "running",
    ]
    for i, line in enumerate(lines):
        surface = font.render(line, True, (180, 180, 180))
        screen.blit(surface, (10, 10 + i * 18))

    # bottom-left: controls help
    help_lines = [
        "drag: launch  |  right-click: heavy  |  space: pause",
        "1-4: presets  |  T: trails  |  C: colors  |  +/-: speed",
    ]
    for i, line in enumerate(help_lines):
        surface = font.render(line, True, (100, 100, 100))
        screen.blit(surface, (10, HEIGHT - 40 + i * 18))


def draw_drag_line(screen: pygame.Surface, start: tuple, end: tuple) -> None:
    pygame.draw.line(screen, (255, 255, 255), start, end, 1)