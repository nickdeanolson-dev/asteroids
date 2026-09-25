import pygame
import sys
from constants import *
from logger import log_state
from player import *
from asteroid import *
from logger import log_event
from shot import *
from starfield import Starfield

def main():
    print("Hello from asteroids!")
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    starfield = Starfield()
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
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
                return
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
                sys.exit()

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


if __name__ == "__main__":
    main()
