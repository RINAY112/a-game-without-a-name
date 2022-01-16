import pygame as pg
from personages import Hero, Enemy
from blocks import (Floor, Ceiling, Wall, RightWall, LeftWall, FloorThorn, CeilingThorn, RightThorn, LeftThorn,
                    Teleport, UpperLeftCorner, UpperRightCorner, LowerLeftCorner, LowerRightCorner)

pg.init()
SCREEN_SIZE = 1920, 1080
screen = pg.display.set_mode(SCREEN_SIZE)

bg_image = pg.image.load(r'data\bg_image.png').convert_alpha()


def terminate():
    pg.quit()
    exit()


def load_level(name, thorns, vertical_blocks, horizontal_blocks, characters, all_sprites):
    thorns.clear(), vertical_blocks.clear(), horizontal_blocks.clear(), characters.clear(), all_sprites.clear()
    wall_image = pg.Surface([64, 64])
    wall_image.fill('#0f141f')
    with open(rf'data\{name}') as level:
        for i, line in enumerate(level):
            for j, cell in enumerate(line.strip('\n')):
                if cell == '▢':
                    Wall(j * 64, i * 64, all_sprites)
                elif cell == '↦':
                    LeftThorn(j * 64, i * 64, all_sprites, thorns)
                elif cell == '↤':
                    RightThorn(j * 64, i * 64, all_sprites, thorns)
                elif cell == '↧':
                    CeilingThorn(j * 64, i * 64, all_sprites, thorns)
                elif cell == '↥':
                    FloorThorn(j * 64, i * 64, all_sprites, thorns)
                elif cell == '→':
                    LeftWall(j * 64, i * 64, all_sprites, vertical_blocks)
                elif cell == '←':
                    RightWall(j * 64, i * 64, all_sprites, vertical_blocks)
                elif cell == '↑':
                    Floor(j * 64, i * 64, all_sprites, horizontal_blocks)
                elif cell == '↓':
                    Ceiling(j * 64, i * 64, all_sprites, horizontal_blocks)
                elif cell == '↘':
                    UpperLeftCorner(j * 64, i * 64, all_sprites, vertical_blocks, horizontal_blocks)
                elif cell == '↙':
                    UpperRightCorner(j * 64, i * 64, all_sprites, vertical_blocks, horizontal_blocks)
                elif cell == '↖':
                    LowerRightCorner(j * 64, i * 64, all_sprites, vertical_blocks, horizontal_blocks)
                elif cell == '↗':
                    LowerLeftCorner(j * 64, i * 64, all_sprites, vertical_blocks, horizontal_blocks)
                elif cell == '▮':
                    teleport = Teleport(j * 64, i * 64, all_sprites)
                elif cell == '@':
                    Hero(j * 64, i * 64, all_sprites, characters)
                elif cell == '0':
                    Enemy(j * 64, i * 64, all_sprites, characters)
                ...
    return teleport.rect.center


def menu():
    menu_image = pg.image.load(r'data\menu_image.jpg').convert()
    menu_font = pg.font.Font(r'data\menu_font.ttf', 150)

    pg.mixer.music.load(r'data\menu.mp3')
    pg.mixer.music.play(-1)

    screen.blit(menu_image, (0, 0))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            if event.type == pg.MOUSEMOTION:
                x, y = event.pos
                if 1454 <= x <= 1706 and 701 <= y <= 795:
                    screen.blit(menu_font.render('PLAY', True, (255, 51, 51)), (1453, 685))
                else:
                    screen.blit(menu_font.render('PLAY', True, (201, 183, 122)), (1453, 685))
                if 1451 <= x <= 1695 and 878 <= y <= 986:
                    screen.blit(menu_font.render('QUIT', True, (255, 51, 51)), (1450, 871))
                else:
                    screen.blit(menu_font.render('QUIT', True, (201, 183, 122)), (1450, 871))
            elif event.type == pg.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 1454 <= x <= 1706 and 701 <= y <= 795:
                    return
                elif 1451 <= x <= 1695 and 878 <= 986:
                    terminate()
        pg.display.flip()


all_groups = thorns, vertical_blocks, horizontal_blocks, characters, all_sprites = tuple(
    [pg.sprite.Group() for _ in range(5)]
)


def level0():
    load_level('level0.txt', *all_groups)


menu()

pg.quit()