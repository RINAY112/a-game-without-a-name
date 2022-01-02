import pygame as pg

pg.init()
SCREEN_SIZE = 1920, 1080
screen = pg.display.set_mode(SCREEN_SIZE)

menu_image = pg.image.load(r'data\menu_image.jpg')
menu_font = pg.font.Font(r'data\menu_font.ttf', 150)

screen.blit(menu_image, (0, 0))

running = True
status = 'menu'

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEMOTION:
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
                status = 'game'
            elif 1451 <= x <= 1695 and 878 <= 986:
                running = False

    pg.display.flip()
pg.quit()