import pygame as pg
from personages import Hero, Enemy
from blocks import (Floor, Ceiling, Wall, RightWall, LeftWall, FloorThorn, CeilingThorn, RightThorn, LeftThorn,
                    Teleport, UpperLeftCorner, UpperRightCorner, LowerLeftCorner, LowerRightCorner, Button, Door)
from particles import Blood

pg.init()
SCREEN_SIZE = 1920, 1080
screen = pg.display.set_mode(SCREEN_SIZE)
clock = pg.time.Clock()

bg_image = pg.image.load(r'data\background.png').convert_alpha()

darkness_visibility, restart_level, pass_level = 0, False, False
RISE_VISIBILITY = pg.USEREVENT + 1


def terminate():
    pg.quit()
    exit()


def obscuration(screen, visibility):
    image = pg.surface.Surface([1920, 1080], flags=pg.SRCALPHA)
    image.fill(pg.Color(0, 0, 0, visibility))
    screen.blit(image, (0, 0))


def load_level(name, thorns, vertical_blocks, horizontal_blocks, characters, all_sprites):
    floor_counter = 0
    thorns.empty(), vertical_blocks.empty(), horizontal_blocks.empty(), characters.empty(), all_sprites.empty()
    button, door = None, None
    with open(rf'data\{name}', encoding='utf-8') as level:
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
                    Floor(floor_counter, j * 64, i * 64, all_sprites, horizontal_blocks)
                    floor_counter = (floor_counter + 1) % 3
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
                    teleport = Teleport(j * 64, i * 64 + 8, all_sprites)
                elif cell == '@':
                    hero = Hero(j * 64, i * 64, characters)
                elif cell == '0':
                    enemy = Enemy(j * 64, i * 64, characters)
                elif cell == '_':
                    button = Button(j * 64, i * 64, all_sprites)
                elif cell == '|':
                    door = Door(j * 64, i * 64, all_sprites, vertical_blocks)
    return teleport.rect.center, hero, enemy, button, door


def menu():
    menu_image = pg.image.load(r'data\menu.jpg').convert()
    menu_font = pg.font.Font(r'data\menu_font.ttf', 150)

    pg.mixer.music.load(r'data\menu.mp3')
    pg.mixer.music.play(-1)

    screen.blit(menu_image, (0, 0))

    text1 = menu_font.render('PLAY', True, (201, 183, 122))
    text2 = menu_font.render('QUIT', True, (201, 183, 122))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            if event.type == pg.MOUSEMOTION:
                x, y = event.pos
                if 1454 <= x <= 1706 and 701 <= y <= 795:
                    text1 = menu_font.render('PLAY', True, (255, 51, 51))
                else:
                    text1 = menu_font.render('PLAY', True, (201, 183, 122))
                if 1451 <= x <= 1695 and 878 <= y <= 986:
                    text2 = menu_font.render('QUIT', True, (255, 51, 51))
                else:
                    text2 = menu_font.render('QUIT', True, (201, 183, 122))
            elif event.type == pg.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 1454 <= x <= 1706 and 701 <= y <= 795:
                    return
                elif 1451 <= x <= 1695 and 878 <= y <= 986:
                    terminate()

        screen.blit(text1, (1453, 685))
        screen.blit(text2, (1450, 871))

        pg.display.flip()


all_groups = thorns, vertical_blocks, horizontal_blocks, characters, all_sprites = tuple([pg.sprite.Group() for _ in range(5)])


def level0():
    global darkness_visibility, restart_level, pass_level
    right, left, jump = False, False, False
    particles = pg.sprite.Group()
    pg.mixer.music.play(-1)

    tp_center, hero, enemy, button, door = load_level('level0.txt', *all_groups)
    all_sprites.add(hero), all_sprites.add(enemy)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_d:
                    right = True
                elif event.key == pg.K_a:
                    left = True
                elif event.key == pg.K_SPACE:
                    jump = True
                elif event.key == pg.K_ESCAPE:
                    return 0
                elif event.key == pg.K_r:
                    restart_level = True
                    pg.time.set_timer(RISE_VISIBILITY, 2)
            elif event.type == pg.KEYUP:
                if event.key == pg.K_d:
                    right = False
                elif event.key == pg.K_a:
                    left = False
                elif event.key == pg.K_SPACE:
                    jump = False
                elif event.key == pg.K_r and restart_level:
                    restart_level = False
                    pg.time.set_timer(RISE_VISIBILITY, 0)
                    darkness_visibility = 0
            elif event.type == RISE_VISIBILITY:
                if darkness_visibility == 250 and restart_level:
                    pg.time.set_timer(RISE_VISIBILITY, 0)
                    restart_level, darkness_visibility = False, 0
                    all_sprites.add(hero), all_sprites.add(enemy)
                    hero.move_to_start_pos(), enemy.move_to_start_pos()
                    if button is not None:
                        button.set_start_frame(), door.move_to_start_pos()
                elif darkness_visibility == 250 and pass_level:
                    pg.time.set_timer(RISE_VISIBILITY, 0)
                    darkness_visibility, pass_level = 0, False
                    return
                else:
                    darkness_visibility += 1

        time = clock.tick(200)

        screen.blit(bg_image, (0, 0))

        res = {hero.update(thorns, horizontal_blocks, vertical_blocks, tp_center, time, right, left, jump, button, door, particles),
                enemy.update(thorns, horizontal_blocks, vertical_blocks, tp_center, time, right, left, jump, button, door, particles)}

        if 'kill Hero' in res or pg.sprite.collide_rect(enemy, hero) and hero.is_leave:
            Blood.create_particles(*hero.rect.center, particles)
            restart_level = True
            pg.time.set_timer(RISE_VISIBILITY, 2)
            all_sprites.remove(hero)
        elif 'tp Enemy' in res:
            restart_level = True
            pg.time.set_timer(RISE_VISIBILITY, 2)
        elif 'tp Hero' in res:
            pass_level = True
            pg.time.set_timer(RISE_VISIBILITY, 2)
        elif 'kill Enemy' in res:
            all_sprites.remove(enemy)
            Blood.create_particles(*enemy.rect.center, particles)

        if button is not None:
            if (personage := pg.sprite.spritecollideany(button, characters)) and personage.is_leave:
                button.update(True, time)
                door.update(True, time)
            else:
                button.update(False, time)
                door.update(False, time)

        font = pg.font.Font(None, 70)
        text1 = font.render('[A], [D] - move', True, (255, 255, 255))
        text2 = font.render('[SPACE] - jump', True, (255, 255, 255))
        text3 = font.render('[R] - restart level', True, (255, 255, 255))
        text4 = font.render('[ESC] - main menu', True, (255, 255, 255))

        all_sprites.draw(screen)

        screen.blit(text1, (450, 40))
        screen.blit(text2, (450, 150))
        screen.blit(text3, (1000, 40))
        screen.blit(text4, (1000, 150))

        particles.update(time)
        particles.draw(screen)

        obscuration(screen, darkness_visibility)
        pg.display.flip()


def level1():
    global darkness_visibility, restart_level, pass_level
    right, left, jump = False, False, False
    particles = pg.sprite.Group()
    pg.mixer.music.play(-1)

    tp_center, hero, enemy, button, door = load_level('level1.txt', *all_groups)
    all_sprites.add(hero), all_sprites.add(enemy)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_d:
                    right = True
                elif event.key == pg.K_a:
                    left = True
                elif event.key == pg.K_SPACE:
                    jump = True
                elif event.key == pg.K_ESCAPE:
                    return 0
                elif event.key == pg.K_r:
                    restart_level = True
                    pg.time.set_timer(RISE_VISIBILITY, 2)
            elif event.type == pg.KEYUP:
                if event.key == pg.K_d:
                    right = False
                elif event.key == pg.K_a:
                    left = False
                elif event.key == pg.K_SPACE:
                    jump = False
                elif event.key == pg.K_r and restart_level:
                    restart_level = False
                    pg.time.set_timer(RISE_VISIBILITY, 0)
                    darkness_visibility = 0
            elif event.type == RISE_VISIBILITY:
                if darkness_visibility == 250 and restart_level:
                    pg.time.set_timer(RISE_VISIBILITY, 0)
                    restart_level, darkness_visibility = False, 0
                    all_sprites.add(hero), all_sprites.add(enemy)
                    hero.move_to_start_pos(), enemy.move_to_start_pos()
                    if button is not None:
                        button.set_start_frame(), door.move_to_start_pos()
                elif darkness_visibility == 250 and pass_level:
                    pg.time.set_timer(RISE_VISIBILITY, 0)
                    darkness_visibility, pass_level = 0, False
                    return
                else:
                    darkness_visibility += 1

        time = clock.tick(200)

        screen.blit(bg_image, (0, 0))

        res = {hero.update(thorns, horizontal_blocks, vertical_blocks, tp_center, time, right, left, jump, button, door, particles),
                enemy.update(thorns, horizontal_blocks, vertical_blocks, tp_center, time, right, left, jump, button, door, particles)}

        if 'kill Hero' in res or pg.sprite.collide_rect(enemy, hero):
            Blood.create_particles(*hero.rect.center, particles)
            restart_level = True
            pg.time.set_timer(RISE_VISIBILITY, 2)
            all_sprites.remove(hero)
        elif 'tp Enemy' in res:
            restart_level = True
            pg.time.set_timer(RISE_VISIBILITY, 2)
        elif 'tp Hero' in res:
            pass_level = True
            pg.time.set_timer(RISE_VISIBILITY, 2)
        elif 'kill Enemy' in res:
            Blood.create_particles(*enemy.rect.center, particles)
            all_sprites.remove(enemy)

        if button is not None:
            if (personage := pg.sprite.spritecollideany(button, characters)) and personage.is_leave:
                button.update(True, time)
                door.update(True, time)
            else:
                button.update(False, time)
                door.update(False, time)

        all_sprites.draw(screen)

        particles.update(time)
        particles.draw(screen)

        obscuration(screen, darkness_visibility)
        pg.display.flip()


def game():
    pg.mixer.music.load(r'data\game.mp3')
    pg.mixer.music.play(-1)

    clock.tick()
    if level0() == 0:
        return
    clock.tick()
    if level1() == 0:
        return
    terminate()


while True:
    menu()
    game()