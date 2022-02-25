import pygame as pg

pg.init()
pg.display.set_mode((1920, 1080))


class Block(pg.sprite.Sprite):
    def __init__(self, x, y, *groups, w=64, h=64):
        super().__init__(*groups)
        self.image = type(self).image
        self.rect = pg.Rect(x, y, w, h)


class Ceiling(Block):
    image = pg.image.load(r'data\ceiling.png').convert_alpha()


class Floor(Block):
    images = tuple(pg.image.load(rf'data\floor{i}.png').convert_alpha() for i in range(1, 4))
    image = None

    def __init__(self, i, x, y, *groups):
        super().__init__(x, y, *groups)
        self.image = Floor.images[i]


class Wall(Block):
    image = pg.image.load(r'data\wall.png').convert_alpha()


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


class LeftOuterUpperCorner(Block):
    image = pg.image.load(r'data\left_outer_upper_corner.png').convert_alpha()


class RightOuterUpperCorner(Block):
    image = pg.transform.flip(LeftOuterUpperCorner.image, True, False)


class RightOuterLowerCorner(Block):
    image = pg.transform.flip(RightOuterUpperCorner.image, False, True)


class LeftOuterLowerCorner(Block):
    image = pg.transform.flip(RightOuterLowerCorner.image, True, False)


class LeftInnerUpperCorner(Block):
    image = pg.image.load(r'data\left_inner_upper_corner.png').convert_alpha()


class RightInnerUpperCorner(Block):
    image = pg.transform.flip(LeftInnerUpperCorner.image, True, False)


class LeftInnerLowerCorner(Block):
    image = pg.image.load(r'data\left_inner_lower_corner.png')


class RightInnerLowerCorner(Block):
    image = pg.transform.flip(LeftInnerLowerCorner.image, True, False)


class Teleport(Block):
    image = pg.image.load(r'data\teleport.png').convert_alpha()

    def __init__(self, x, y, *groups):
        rect = Teleport.image.get_rect()
        super().__init__(x, y - rect.h + 64, w=rect.w, h=rect.h, *groups)


class Button(Block):
    image = None
    sheet = pg.image.load(r'data\button.png').convert_alpha()

    def __init__(self, x, y, *groups):
        self.frames, w, h = Button.cut_sheet()
        self.current_frame = 0
        self.frame_change_time = 50
        self.frame_time = 0
        super().__init__(x, y + 64 - h, w=w, h=h, *groups)

    @staticmethod
    def cut_sheet():
        rect = Button.sheet.get_rect()
        w, h = rect.w // 3, rect.h
        return tuple(Button.sheet.subsurface((i * w, 0, w, h)) for i in range(3)), w, h

    def update(self, switch_on, time):
        if switch_on and self.current_frame != 2:
            self.frame_time += time
            if self.frame_time >= self.frame_change_time:
                self.current_frame += 1
                self.frame_time -= self.frame_change_time
        elif not switch_on and self.current_frame != 0:
            self.frame_time += time
            if self.frame_time >= self.frame_change_time:
                self.current_frame -= 1
                self.frame_time -= self.frame_change_time
        elif self.frame_time:
            self.frame_time = 0

        self.image = self.frames[self.current_frame]

    def set_start_frame(self):
        self.current_frame, self.frame_time = 0, 0
        self.image = self.frames[self.current_frame]


class Door(Block):
    image = pg.image.load(r'data\door.png')
    YSPEED = .7

    def __init__(self, x, y, *groups):
        super().__init__(x, y, h=Door.image.get_height(), *groups)
        self.start_y = y
        self.max_y = y + self.rect.h + 8
        self.y = y

    def update(self, hide, time):
        if hide and self.y < self.max_y:
            self.y += Door.YSPEED * time
        elif not hide and self.y > self.start_y:
            self.y -= Door.YSPEED * time

        if self.y > self.max_y:
            self.y = self.max_y
        elif self.y < self.start_y:
            self.y = self.start_y
        self.rect.y = self.y

    def move_to_start_pos(self):
        self.y, self.rect.y = self.start_y, self.start_y