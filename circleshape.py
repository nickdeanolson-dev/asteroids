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
        if self.position.x < -self.radius and self.velocity.x < 0:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius and self.velocity.x > 0:
            self.position.x = -self.radius

        if self.position.y < -self.radius and self.velocity.y < 0:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius and self.velocity.y > 0:
            self.position.y = -self.radius

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
