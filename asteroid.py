from circleshape import *
from logger import log_event

import random
from collections.abc import Callable

import pygame
from constants import *

class Asteroid(CircleShape):
    def __init__(self,x,y,radius):
        super().__init__(x,y,radius)
        vertex_count = ASTEROID_VERTEX_COUNT
        min_radius_factor = ASTEROID_MIN_RADIUS_FACTOR
        max_radius_factor = ASTEROID_MAX_RADIUS_FACTOR
        max_adjacent_change = ASTEROID_MAX_ADJACENT_RADIUS_CHANGE
        raw_radius_factors = [
            random.uniform(min_radius_factor, max_radius_factor)
            for _ in range(vertex_count)
        ]
        min_index = random.randrange(vertex_count)
        max_candidates = [
            index
            for index in range(vertex_count)
            if min(abs(index - min_index), vertex_count - abs(index - min_index))
            >= ASTEROID_MIN_PEAK_SEPARATION
        ]
        max_index = random.choice(max_candidates)
        raw_radius_factors[min_index] = min_radius_factor
        raw_radius_factors[max_index] = max_radius_factor
        for distance, lower_factor in (
            (1, ASTEROID_PEAK_ADJACENT_RADIUS_FACTOR),
            (2, ASTEROID_PEAK_NEXT_RADIUS_FACTOR),
        ):
            for offset in (-distance, distance):
                index = (max_index + offset) % vertex_count
                raw_radius_factors[index] = random.uniform(
                    lower_factor, max_radius_factor
                )
        radius_factors = [
            min(
                raw_radius_factors[source_index]
                + max_adjacent_change
                * min(
                    abs(index - source_index),
                    vertex_count - abs(index - source_index),
                )
                for source_index in range(vertex_count)
            )
            for index in range(vertex_count)
        ]
        self.vertices = [
            pygame.Vector2(radius * factor, 0).rotate(index * 360 / len(radius_factors))
            for index, factor in enumerate(radius_factors)
        ]
        if radius >= ASTEROID_MAX_RADIUS:
            max_rotation_speed = ASTEROID_ROTATION_SPEEDS[0]
        elif radius > ASTEROID_MIN_RADIUS:
            max_rotation_speed = ASTEROID_ROTATION_SPEEDS[1]
        else:
            max_rotation_speed = ASTEROID_ROTATION_SPEEDS[2]
        self.rotation_speed = random.uniform(-max_rotation_speed, max_rotation_speed)


    def draw(self, screen):
        points = [self.position + vertex for vertex in self.vertices]
        if self.radius >= ASTEROID_MAX_RADIUS:
            color = ASTEROID_COLORS[0]
        elif self.radius > ASTEROID_MIN_RADIUS:
            color = ASTEROID_COLORS[1]
        else:
            color = ASTEROID_COLORS[2]
        pygame.draw.polygon(screen, color, points)

    def draw_outline(self, screen):
        points = [self.position + vertex for vertex in self.vertices]
        pygame.draw.polygon(screen, "black", points, 1)

    def update(self, dt):
        self.vertices = [
            vertex.rotate(self.rotation_speed * dt) for vertex in self.vertices
        ]
        self.position += self.velocity*dt
        self.wrap_position()

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        split_angle_a = random.uniform(20, 50)
        split_angle_b = random.uniform(20, 50)
        split_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid_split_a = Asteroid(self.position[0], self.position[1], split_radius)
        asteroid_split_a.velocity = self.velocity.rotate(split_angle_a) * 1.2
        asteroid_split_b = Asteroid(self.position[0], self.position[1], split_radius)
        asteroid_split_b.velocity = self.velocity.rotate(-split_angle_b) * 1.2


Edge = tuple[pygame.Vector2, Callable[[float], pygame.Vector2]]

class AsteroidField(pygame.sprite.Sprite):
    containers: pygame.sprite.Group

    edges: list[Edge] = [
        (
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ),
        (
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ),
        (
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ),
        (
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ),
    ]

    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

    def spawn(
        self, radius: float, position: pygame.Vector2, velocity: pygame.Vector2
    ) -> None:
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt: float) -> None:
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE_SECONDS:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            self.spawn(ASTEROID_MAX_RADIUS, position, velocity)
