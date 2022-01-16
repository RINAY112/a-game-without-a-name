import pygame as pg

pg.init()


class Character(pg.sprite.Sprite):
    GRAVITY = .981

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

    def update(self, thorn_group, horizontal_blocks, vertical_blocks, teleport_center, time, right, left, jump):
        if pg.sprite.spritecollideany(self, thorn_group):
            return f'kill {self.type}'
        elif self.rect.collidepoint(teleport_center):
            return f'tp {self.type}'

        if jump:
            if self.on_ground:
                self.on_ground = False
                self.vy -= 20

        self.x += self.vx * time * right
        self.x -= self.vx * time * left

        if not self.on_ground:
            self.vy += Character.GRAVITY * time
        self.y += self.vy * time

        self.rect.x, self.rect.y = self.x, self.y

        if right ^ left and (block := pg.sprite.spritecollideany(self, vertical_blocks)):
            if self.vx > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right
            self.vx = 0

        if block := pg.sprite.spritecollideany(self, horizontal_blocks):
            if self.vy < 0:
                self.rect.left = block.rect.right
                self.vy = 0
            elif self.rect.bottom >= block.rect.top + 8:
                self.rect.bottom = block.rect.top - 8
                self.vy = 0
                self.on_ground = True
        else:
            self.on_ground = False


class Hero(Character):
    def __init__(self, x: int, y: int, *groups):
        super().__init__(x, y, .02, 'hero.png', *groups)


class Enemy(Character):
    def __init__(self, x: int, y: int, *groups):
        super().__init__(x, y, -.02, 'enemy.png', *groups)