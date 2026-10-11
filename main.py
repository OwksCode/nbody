import pygame, random, math, sys
from particle import Particle
from physics import step
from renderer import draw_particles, draw_trails, draw_ui, draw_drag_line
from config import WIDTH, HEIGHT, FPS, BG_COLOR, DT, DEFAULT_MASS, HEAVY_MASS


def solar_system() -> list[Particle]:
    sun = Particle(WIDTH // 2, HEIGHT // 2, 0, 0, mass=800)
    sun.color = (255, 220, 80)
    p1 = Particle(WIDTH // 2 + 150, HEIGHT // 2, 0, -3, mass=30)
    p2 = Particle(WIDTH // 2 - 200, HEIGHT // 2, 0, 2.5, mass=50)
    p3 = Particle(WIDTH // 2, HEIGHT // 2 - 180, 2.8, 0, mass=20)
    return [sun, p1, p2, p3]


def binary_system() -> list[Particle]:
    s1 = Particle(400, 350, 0, -1.5, mass=400)
    s2 = Particle(600, 350, 0, 1.5, mass=400)
    s1.color = (255, 50, 50)
    s2.color = (50, 50, 255)
    p1 = Particle(WIDTH // 2 + 150, HEIGHT // 2, 0, -3, mass=30)
    p2 = Particle(WIDTH // 2 - 200, HEIGHT // 2, 0, 2.5, mass=50)
    return [s1, s2, p1, p2]


def chaos_system() -> list[Particle]:
    particles = []
    for _ in range(30):
        p = Particle(
            random.uniform(0, WIDTH),
            random.uniform(0, HEIGHT),
            random.uniform(-1, 1),
            random.uniform(-1, 1),
            random.uniform(20, 100)
        )
        particles.append(p)
    return particles


def ring_system() -> list[Particle]:
    sun = Particle(WIDTH // 2, HEIGHT // 2, 0, 0, mass=800)
    sun.color = (255, 220, 80)
    cx, cy = WIDTH // 2, HEIGHT // 2
    radius = 200
    speed = 2.5
    count = 25

    particles = [sun]
    for i in range(count):
        angle = i * (2 * math.pi / count)
        px = cx + radius * math.cos(angle)
        py = cy + radius * math.sin(angle)
        vx = -math.sin(angle) * speed
        vy = math.cos(angle) * speed
        particles.append(Particle(px, py, vx, vy, random.uniform(15, 40)))
    return particles


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("nbody")
    clock = pygame.time.Clock()

    particles = solar_system()
    preset_name = "solar system"
    paused = False
    show_trails = True
    color_by_speed = False
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
                elif event.key == pygame.K_t:
                    show_trails = not show_trails
                elif event.key == pygame.K_c:
                    color_by_speed = not color_by_speed
                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                    time_scale = min(5.0, time_scale + 0.25)
                elif event.key == pygame.K_MINUS:
                    time_scale = max(0.25, time_scale - 0.25)
                elif event.key == pygame.K_1:
                    particles = solar_system()
                    preset_name = "solar system"
                elif event.key == pygame.K_2:
                    particles = binary_system()
                    preset_name = "binary stars"
                elif event.key == pygame.K_3:
                    particles = chaos_system()
                    preset_name = "chaos"
                elif event.key == pygame.K_4:
                    particles = ring_system()
                    preset_name = "ring"
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
        draw_particles(screen, particles, color_by_speed)
        if dragging:
            draw_drag_line(screen, drag_start, pygame.mouse.get_pos())
        draw_ui(screen, len(particles), paused, time_scale, preset_name, show_trails, color_by_speed)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()