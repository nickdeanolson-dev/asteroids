from constants import *
from circleshape import *
from shot import *


class Player(CircleShape):
    def __init__(self,x,y):
        super().__init__(x,y, PLAYER_RADIUS)
        self.rotation = 0
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
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

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
            self.move(dt)
            self.driftpercent = 1.0
        if keys[pygame.K_s]:
            self.move(dt*-1)
            self.driftpercent = 1.0
        if keys[pygame.K_SPACE]:
            if self.shot_cooldown <= 0.0:
                self.shoot()
                self.shot_cooldown = PLAYER_SHOT_COOLDOWN_SECONDS
        if self.shot_cooldown > 0.0:
            self.shot_cooldown -= dt
        else:
            self.shot_cooldown = 0.0
        
        #print (self.driftpercent)
        #if self.driftpercent > 0.0 and not keys[pygame.K_s] and not keys[pygame.K_w]:
            #self.driftpercent -= PLAYER_DRIFT_DECAY
            #if self.driftpercent < 0.0:
                #self.driftpercent = 0.0
            #self.move(dt*self.driftpercent)


    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector