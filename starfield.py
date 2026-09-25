import random

import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH


class Starfield:
    STAR_COUNT = 150
    TWINKLE_INTERVAL_SECONDS = 60.0
    TWINKLE_DURATION_SECONDS = 0.25
    TWINKLE_BRIGHTNESS_INCREASE = round(255 * 0.2)

    def __init__(self) -> None:
        layout_random = random.Random(0)
        twinkle_random = random.Random()
        self.elapsed = 0.0
        self.stars: list[tuple[int, int, int, int, float]] = []

        for _ in range(self.STAR_COUNT):
            size = layout_random.randint(1, 3)
            x = layout_random.randrange(SCREEN_WIDTH - size + 1)
            y = layout_random.randrange(SCREEN_HEIGHT - size + 1)
            brightness = round(layout_random.uniform(0.1, 0.6) * 255)
            twinkle_phase = twinkle_random.uniform(
                0.0, self.TWINKLE_INTERVAL_SECONDS
            )
            self.stars.append((x, y, size, brightness, twinkle_phase))

    def update(self, dt: float) -> None:
        self.elapsed += dt

    def draw(self, screen: pygame.Surface) -> None:
        for x, y, size, brightness, twinkle_phase in self.stars:
            time_in_cycle = (
                self.elapsed - twinkle_phase
            ) % self.TWINKLE_INTERVAL_SECONDS
            if time_in_cycle < self.TWINKLE_DURATION_SECONDS:
                brightness += self.TWINKLE_BRIGHTNESS_INCREASE
            color = (brightness, brightness, brightness)
            pygame.draw.rect(screen, color, (x, y, size, size))