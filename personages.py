import pygame as pg
from particles import Dirt

pg.init()
pg.display.set_mode((1920, 1080))


class Character(pg.sprite.Sprite):
    GRAVITY = .009
    XSPEED = 1.2
    sheet = None

    def __init__(self, x: int, y: int, direction: int, *groups):
        super().__init__(*groups)
        self.start_x, self.start_y = x, y
        self.vx, self.vy = 0, 0
        self.rect = pg.Rect(x, y, 64, 64)
        self.x, self.y = x, y
        self.type = None
        self.on_ground = True
        self.direction = direction
        self.action, self.current_frame, self.frame_time = 0, 0, 0
        self.reverse, self.frame_change_times = None, (0, 0, 0)
        self.frames = tuple()
        self.is_leave = True

    def update(self, thorns, horizontal_blocks, vertical_blocks, teleport_center, time, right, left, jump, button,
               door, particles):
        if not self.is_leave:
            return
        if pg.sprite.spritecollideany(self, thorns):
            self.is_leave = False
            return f'kill {type(self).__name__}'
        elif self.rect.collidepoint(teleport_center):
            self.image = self.frames[3][0]
            return f'tp {type(self).__name__}'

        if jump:
            if self.on_ground:
                self.on_ground = False
                self.vy = -2.1

        if left and right:
            self.vx = 0
        elif right:
            self.vx = Character.XSPEED * self.direction
        elif left:
            self.vx = -Character.XSPEED * self.direction
        else:
            self.vx = 0

        if not self.on_ground:
            self.vy += Character.GRAVITY * time

        self.y += self.vy * time
        self.rect.y = self.y

        if block := pg.sprite.spritecollideany(self, horizontal_blocks):
            if self.vy < 0:
                self.rect.top = block.rect.bottom + 8
                self.vy = 0
                self.y = self.rect.y
            elif not self.on_ground and self.rect.bottom >= block.rect.top + 8:
                self.rect.bottom = block.rect.top + 8
                self.vy = 0
                self.on_ground = True
                self.y = self.rect.y
                Dirt.create_particles(self.rect.center[0], self.rect.bottom, particles)
        else:
            self.on_ground = False

        self.x += self.vx * time
        self.rect.x = self.x

        if self.vx and (block := pg.sprite.spritecollideany(self, vertical_blocks)):
            if self.vx > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right
            self.vx = 0
            self.x = self.rect.x

        if self.vy > 0 and self.action:
            self.action, self.current_frame, self.frame_time = 1, 0, 0
        elif self.vy < 0 and self.action:
            self.action, self.current_frame, self.frame_time = 1, 1, 0
        elif self.vx == 0 and self.action != 0:
            self.action, self.current_frame = 0, 0
        elif self.vx > 0:
            self.action, self.reverse = 2, False
        elif self.vx < 0:
            self.action, self.reverse = 2, True

        if self.action == 0 or self.action == 2:
            self.frame_time += time
            if self.frame_time >= (frame_change_time := self.frame_change_times[self.action]):
                self.frame_time -= frame_change_time
                self.current_frame = (self.current_frame + 1) % len(self.frames[self.action])

        self.image = pg.transform.flip(self.frames[self.action][self.current_frame], self.reverse, False)

    def move_to_start_pos(self):
        self.x, self.rect.x = self.start_x, self.start_x
        self.y, self.rect.y = self.start_y, self.start_y
        self.is_leave = True

    @classmethod
    def cut_sheet(cls, *cols):
        return tuple(tuple(cls.sheet.subsurface((i * 64, j * 64, 64, 64)) for i in range(cols_count)) for j, cols_count in enumerate(cols))


class Hero(Character):
    sheet = pg.image.load(r'data\hero.png').convert_alpha()

    def __init__(self, x: int, y: int, *groups):
        super().__init__(x, y, 1, *groups)
        self.frames = Hero.cut_sheet(2, 2, 8, 1)
        self.frame_change_times = (400, 0, 100)
        self.reverse = False


class Enemy(Character):
    sheet = pg.image.load(r'data\enemy.png').convert_alpha()

    def __init__(self, x: int, y: int, *groups):
        super().__init__(x, y, -1, *groups)
        self.frames = Enemy.cut_sheet(2, 2, 2, 1)
        self.frame_change_times = (400, 0, 100)
        self.reverse = True