import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float, radius: float) -> None:
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()

        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen: pygame.Surface) -> None:
        # must override
        pass

    def update(self, dt: float) -> None:
        # must override
        pass

    def wrap_position(self) -> None:
        self.position.x %= SCREEN_WIDTH
        self.position.y %= SCREEN_HEIGHT

    def collides_with(self, other):
        distance = self.position.distance_to(other.position)
        #print(distance)
        hitrange = self.radius+other.radius
        #print(self.radius)
        #print(other.radius)
        #print(hitrange)
        if hitrange > distance:
            return True
        return False
