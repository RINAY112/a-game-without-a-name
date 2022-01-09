import pygame as pg

pg.init()


class Block(pg.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.rect = pg.Rect(x, y, 64, 64)
        self.bottom, self.top, self.right, self.left = self.rect.bottom, self.rect.top, self.rect.right, self.rect.left


class Ceiling(Block):
    image = pg.image.load(r'data\ceiling.png').convert_alpha()

    def __init__(self, x, y, *groups):
        super().__init__(x, y, *groups)
        self.image = Ceiling.image


class Floor(Block):
    image = pg.image.load(r'data\floor.png').convert_alpha()

    def __init__(self, x, y, *groups):
        super().__init__(x, y, *groups)
        self.image = Floor.image
        self.top -= 1


class LeftWall(Block):
    image = pg.image.load(r'data\wall.png').convert_alpha()

    def __init__(self, x, y, *groups):
        super().__init__(x, y, *groups)
        self.image = LeftWall.image


class RightWall(Block):
    image = pg.transform.flip(pg.image.load(r'data\wall.png').convert_alpha(), True, False)

    def __init__(self, x, y, *groups):
        super().__init__(x, y, *groups)
        self.image = RightWall.image


class Thorn(pg.sprite.Sprite):
    image = pg.image.load(r'data\thorn.png').convert_alpha()

    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.rect = pg.Rect(x, y, 64, 64)


class FloorThorn(Thorn):
    image = Thorn.image

    def __init__(self, x, y, *groups):
        super().__init__(x, y, *groups)
        self.image = FloorThorn.image


class CeilingThorn(Thorn):
    image = pg.transform.flip(Thorn.image, False, True)

    def __init__(self, x, y, *groups):
        super().__init__(x, y, *groups)
        self.image = CeilingThorn.image


class RightThorn(Thorn):
    image = pg.transform.rotate(Thorn.image, 90)

    def __init__(self, x, y, *groups):
        super().__init__(x, y, *groups)
        self.image = RightThorn.image


class LeftThorn(Thorn):
    image = pg.transform.flip(pg.transform.rotate(Thorn.image, 90), True, False)

    def __image__(self, x, y, *groups):
        super().__init__(x, y, *groups)
        self.image = LeftImage