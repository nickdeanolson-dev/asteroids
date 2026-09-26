import pygame
from constants import *
from logger import log_state
from player import *
from asteroid import *
from logger import log_event
from shot import *
from starfield import Starfield


def show_title_screen(screen, starfield, clock, title_font, option_font):
    selected_option = 0
    dt = 0.0
    options = ("Start Game", "Quit")
    option_surfaces = [option_font.render(option, True, "white") for option in options]
    text_left = (SCREEN_WIDTH - max(surface.get_width() for surface in option_surfaces)) // 2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return selected_option == 0

        screen.fill("black")
        starfield.update(dt)
        starfield.draw(screen)

        title_surface = title_font.render("ASTEROIDS", True, "white")
        title_rect = title_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 110)
        )
        screen.blit(title_surface, title_rect)

        option_y_positions = (SCREEN_HEIGHT // 2 - 16, SCREEN_HEIGHT // 2 + 48)
        for index, (surface, y_position) in enumerate(
            zip(option_surfaces, option_y_positions)
        ):
            option_rect = surface.get_rect(midleft=(text_left, y_position))
            screen.blit(surface, option_rect)
            if index == selected_option:
                tip_x = option_rect.left - 20
                triangle = (
                    (tip_x, y_position),
                    (tip_x - 18, y_position - 12),
                    (tip_x - 18, y_position + 12),
                )
                pygame.draw.polygon(screen, "white", triangle, LINE_WIDTH)

        dt = clock.tick(60) / 1000
        pygame.display.flip()


def run_game(screen, starfield, clock, font):
    dt = 0.0
    score = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    # Player is the name of the class, not an instance of it
    # This must be done before any Player objects are created
    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = (updatable)
    Asteroid.containers = (asteroids, updatable, drawable)
    asteroidfield = AsteroidField()

    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        screen.fill("black")
        starfield.update(dt)
        starfield.draw(screen)
        
        updatable.update(dt)

        for ast in asteroids:
            for shot in shots:
                if ast.collides_with(shot):
                    log_event("asteroid_shot")
                    if ast.radius == ASTEROID_MAX_RADIUS:
                        score += 50
                    elif ast.radius == ASTEROID_MAX_RADIUS - ASTEROID_MIN_RADIUS:
                        score += 100
                    else:
                        score += 200
                    ast.split()
                    shot.kill()
            if ast.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                return True

        sorted_asteroids = sorted(
            asteroids, key=lambda asteroid: asteroid.radius, reverse=True
        )
        for asteroid in sorted_asteroids:
            asteroid.draw(screen)
            asteroid.draw_outline(screen)
        for item in drawable:
            if not isinstance(item, Asteroid):
                item.draw(screen)

        score_surface = font.render(f"Score: {score}", True, "white")
        score_position = (
            SCREEN_WIDTH - score_surface.get_width() - 20,
            20,
        )
        screen.blit(score_surface, score_position)
        
        dt = clock.tick(60)/1000
        pygame.display.flip()


def main():
    print("Hello from asteroids!")
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    starfield = Starfield()
    title_font = pygame.font.Font(None, 64)
    option_font = pygame.font.Font(None, 42)
    score_font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    while True:
        if not show_title_screen(
            screen, starfield, clock, title_font, option_font
        ):
            return
        if not run_game(screen, starfield, clock, score_font):
            return


if __name__ == "__main__":
    main()
