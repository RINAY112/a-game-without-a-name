import pygame as pg
from personages import Hero, Enemy

pg.init()
SCREEN_SIZE = 1920, 1080
screen = pg.display.set_mode(SCREEN_SIZE)

# bg_image = pg.image.load(r'data\bg_image.png')


def terminate():
    pg.quit()
    exit()


def load_level(name, thorn_group, vertical_blocks, horizontal_blocks, hero_group, enemy_group):
    with open(rf'data\{name}') as level:
        for line in level:
            for cell in line.strip('\n'):
                ...


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


def level0():
    ...


menu()


pg.quit()