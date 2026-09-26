from constants import *
from circleshape import *
from shot import *

import os


class Player(CircleShape):
    def __init__(self,x,y):
        super().__init__(x,y, PLAYER_RADIUS)
        self.rotation = 180
        image_path = os.path.join(os.path.dirname(__file__), "assets", "usstriangle.png")
        image = pygame.image.load(image_path).convert_alpha()
        image_size = (int(self.radius * 2 / 1.5), int(self.radius * 2))
        self.image = pygame.transform.smoothscale(image, image_size)
        #self.driftpercent = 0.0
        self.shot_cooldown = 0.0


    # in the Player class
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, 180 - self.rotation)
        image_rect = rotated_image.get_rect(center=self.position)
        screen.blit(rotated_image, image_rect)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def shoot(self):
        shot = Shot(self.position, self.rotation)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOT_SPEED

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(dt*-1)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            self.velocity += forward * PLAYER_ACCELLERATION
            if self.velocity.length() > PLAYER_SPEED:
                self.velocity.scale_to_length(PLAYER_SPEED)
        if keys[pygame.K_SPACE]:
            if self.shot_cooldown <= 0.0:
                self.shoot()
                self.shot_cooldown = PLAYER_SHOT_COOLDOWN_SECONDS
        if self.shot_cooldown > 0.0:
            self.shot_cooldown -= dt
        else:
            self.shot_cooldown = 0.0
        self.move(dt)
        #print (self.driftpercent)
        #if self.driftpercent > 0.0 and not keys[pygame.K_s] and not keys[pygame.K_w]:
            #self.driftpercent -= PLAYER_DRIFT_DECAY
            #if self.driftpercent < 0.0:
                #self.driftpercent = 0.0
            #self.move(dt*self.driftpercent)


    def move(self, dt):
        self.position += self.velocity * dt
        self.wrap_position()