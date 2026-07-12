import pygame
import sys
from constants import *
from logger import log_state
from player import *
from asteroid import *
from logger import log_event
from shot import *

def main():
    print("Hello from asteroids!")
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0.0
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
        
        updatable.update(dt)

        for ast in asteroids:
            for shot in shots:
                if ast.collides_with(shot):
                    log_event("asteroid_shot")
                    ast.kill()
                    shot.kill()
            if ast.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

        for item in drawable:
            item.draw(screen)
        
        dt = clock.tick(60)/1000
        pygame.display.flip()


if __name__ == "__main__":
    main()
