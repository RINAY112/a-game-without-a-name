import pygame as pg

pg.init()


class Block(pg.sprite.Sprite):
    def __init__(self, x, y, *groups, w=64, h=64):
        super().__init__(*groups)
        self.image = type(self).image
        self.rect = pg.Rect(x, y, w, h)


class Ceiling(Block):
    image = pg.image.load(r'data\ceiling.png').convert_alpha()


class Floor(Block):
    image = pg.image.load(r'data\floor.png').convert_alpha()


class Wall(Block):
    image = pg.Surface([64, 64])
    image.fill('#0f141f')


class LeftWall(Block):
    image = pg.image.load(r'data\left_wall.png').convert_alpha()


class RightWall(Block):
    image = pg.transform.flip(LeftWall.image, True, False)


class FloorThorn(Block):
    image = pg.image.load(r'data\thorn.png').convert_alpha()


class CeilingThorn(Block):
    image = pg.transform.flip(FloorThorn.image, False, True)


class RightThorn(Block):
    image = pg.transform.rotate(FloorThorn.image, 90)


class LeftThorn(Block):
    image = pg.transform.flip(pg.transform.rotate(FloorThorn.image, 90), True, False)


class UpperLeftCorner(Block):
    image = pg.image.load(r'data\upper_left_corner.png').convert_alpha()


class UpperRightCorner(Block):
    image = pg.transform.flip(UpperLeftCorner.image, True, False)


class LowerRightCorner(Block):
    image = pg.transform.flip(UpperRightCorner.image, False, True)


class LowerLeftCorner(Block):
    image = pg.transform.flip(LowerRightCorner.image, True, False)


class Teleport(Block):
    image = pg.image.load(r'data\teleport.png')

    def __init__(self, x, y, *groups):
        rect = Teleport.image.get_rect()

        super().__init__(x, y - rect.h + 64, w=rect.w, h=rect.h, *groups)