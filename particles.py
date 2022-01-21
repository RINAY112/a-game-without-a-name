import pygame as pg
from random import randint, choice

SCREEN_RECT = pg.Rect(0, 0, 1920, 1080)
pg.display.set_mode((1920, 1080))


class Particle(pg.sprite.Sprite):
    GRAVITY = .005
    images = tuple()

    def __init__(self, x, y, *groups):
        super().__init__(*groups)

        scale = randint(7, 12)
        self.rect = pg.Rect(x, y, scale, scale)
        self.x, self.y = x, y
        self.vx, self.vy = randint(-50, 50) / 100, randint(-60, 60) / 100

        self.image = pg.transform.scale(choice(type(self).images), (scale, scale))

    def update(self, time):
        self.vy += Particle.GRAVITY * time

        self.y += self.vy * time
        self.x += self.vx * time

        self.rect.x, self.rect.y = self.x, self.y

        if not self.rect.colliderect(SCREEN_RECT):
            self.kill()

    @classmethod
    def create_particles(cls, x, y, *groups):
        for _ in range(12, 17):
            cls(x, y, *groups)


class Blood(Particle):
    images = (pg.Surface([1, 1]),)
    images[0].fill(pg.color.Color(132, 31, 45))


class Dirt(Particle):
    images = tuple(pg.Surface([1, 1], flags=pg.SRCALPHA) for _ in range(5))
    for i, color in enumerate(((75, 87, 68), (72, 135, 67), (72, 62, 60), (81, 94, 72), (88, 180, 100))):
        images[i].fill(pg.Color(*color, randint(150, 255)))