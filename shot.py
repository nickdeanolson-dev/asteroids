from circleshape import *
from constants import *

#github upload test

class Shot(CircleShape):
    def __init__(self,x,y):
        super().__init__(x,y,SHOT_RADIUS)
        self.lifetime = 0.0

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity*dt
        self.wrap_position()
        self.lifetime += dt
        if self.lifetime >= SHOT_LIFETIME_SECONDS:
            self.kill()
