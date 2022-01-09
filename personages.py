import pygame as pg


class Character(pg.sprite.Sprite):
    GRAVITY = 9.81 * 64

    def __init__(self, x: int, y: int, vx: float, image: str, *groups):
        super().__init__(*groups)
        self.start_x, self.start_y = x, y
        self.vx, self.vy = vx, 0
        self.image = pg.image.load(rf'data\{image}').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.x, self.y = x, y
        self.type = None
        self.on_ground = True

    def update(self, thorn_group, vertical_blocks, horizontal_blocks, teleport_center, time, right, left, up):
        if pg.sprite.spritecollideany(self, thorn_group):
            return f'kill {self.type}'
        elif self.rect.collidepoint(teleport_center):
            return f'tp {self.type}'

        if up:
            if self.on_ground:
                self.vy -= 10
            up = False

        if not self.on_ground:
            self.vy += Character.GRAVITY * time

        if block := pg.sprite.spritecollideany(self, vertical_blocks):
            if self.vx > 0:
                self.rect.right = block.left
            else:
                self.rect.left = block.right
            self.vx = 0
        elif block := pg.sprite.spritecollideany(self, horizontal_blocks):
            if self.vy > 0:
                self.rect.bottom = block.top
                self.on_ground = True
            else:
                self.rect.top = block.bottom
            self.vy = 0

        self.x += self.vx * time * right
        self.x -= self.vx * time * left
        self.y += self.vy * time

        self.rect.x, self.rect.y = self.x, self.y


class Hero(Character):
    def __init__(self, x: int, y: int, *groups):
        super().__init__(x, y, 50, 'hero.png', *groups)


class Enemy(Character):
    def __init__(self, x: int, y: int, *groups):
        super().__init__(x, y, -50, 'enemy.png', *groups)