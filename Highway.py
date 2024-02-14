import pygame
import random
import sys
import time

pygame.init()
pygame.display.set_caption("Highway")
pygame.display.set_icon(pygame.image.load('Textures\icon.ico'))
displayInfo = pygame.display.Info()
display = pygame.display.set_mode((displayInfo.current_w, displayInfo.current_h), pygame.FULLSCREEN)
windowWidth, windowHeight = display.get_size()
clock = pygame.time.Clock()

GAMESPEED = 5
FPS = 60

carWidth = windowWidth / 12
carHeight = windowHeight / 4
coinSize = windowWidth / 32
centerWidth = windowWidth / 64
centerHeight = windowHeight / 16
centerDistance = windowHeight / 8

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

road = pygame.image.load('Textures\car_surface.png')
road = pygame.transform.scale(road, (displayInfo.current_w, displayInfo.current_h))
coin = pygame.image.load('Textures\coin.png')
coin = pygame.transform.scale(coin, (coinSize, coinSize))
car = pygame.image.load('Textures\car.png')
car = pygame.transform.scale(car, (carWidth, carHeight))
inc = pygame.image.load('Textures\inc.png')
inc = pygame.transform.scale(inc, (carWidth, carHeight))
menu_background = pygame.image.load('Textures\menu_background.png')
menu_background = pygame.transform.scale(menu_background, (displayInfo.current_w, displayInfo.current_h))
help_background = pygame.image.load('Textures\help_background.png')
help_background = pygame.transform.scale(help_background, (displayInfo.current_w, displayInfo.current_h))

point_sound = pygame.mixer.Sound('Sounds\point.ogg')
crash_sound = pygame.mixer.Sound('Sounds\crash.ogg')

smallFont = pygame.font.Font(None, 56)
titleFont = pygame.font.Font(None, 300)
menuFont = pygame.font.Font(None, 96)
crashFont = pygame.font.Font(None, 120)

def startloop():
    musicloop()
    gameloop()

def musicloop():
    pygame.mixer.music.load('Sounds\menu_sound.wav')
    pygame.mixer.music.play(-1)

musicloop()

def gameloop():
    startmenu()

    centerX_1, centerY = windowWidth / 3.03, 0
    centerX_2, centerY = windowWidth / 2.03, 0
    centerX_3, centerY = windowWidth / 1.53, 0
    carX, carY = windowWidth / 2, windowHeight / 2.25 + carHeight
    coinX, coinY = random.uniform(0.2 * windowWidth, 0.7 * windowWidth), windowHeight * -0.5
    incX, incY = random.uniform(0.2 * windowWidth, 0.7 * windowWidth), windowHeight * -0.5

    points = 0
    points_counter = 0
    direction = 0

    while True:

        display.fill(white)
        display.blit(road, (0, 0))

        for event in pygame.event.get():
            pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif pressed[pygame.K_LEFT]:
                        direction = -1
            elif pressed[pygame.K_RIGHT]:
                        direction = 1
            else:
                direction = 0

        if direction == -1:
            carX -= GAMESPEED
        elif direction == 1:
            carX += GAMESPEED

        if (check_coin(carX, carY, coinX, coinY)):
            coinX, coinY = random.uniform(0.2 * windowWidth, 0.7 * windowWidth), 0
            points += 1
            points_counter += 1

        if points <= 9:
            GAMESPEED = 5
        elif points <= 19:
            GAMESPEED = 6
        elif points <= 29:
            GAMESPEED = 7
        elif points <= 39:
            GAMESPEED = 8
        elif points <= 49:
            GAMESPEED = 9
        else:
            GAMESPEED = 10

        centerY += GAMESPEED
        centerY = centerY % centerDistance
        coinY += GAMESPEED
        incY += 2 * GAMESPEED

        if coinY >= windowHeight:
            coinX, coinY = random.uniform(0.2 * windowWidth, 0.7 * windowWidth), windowHeight * -0.5
        if incY >= windowHeight:
            incX, incY = random.uniform(0.2 * windowWidth, 0.7 * windowWidth), windowHeight * -0.5

        for i in range(-1, 8):
            pygame.draw.rect(display, white, [centerX_1, centerY + i * centerDistance, centerWidth, centerHeight])
            pygame.draw.rect(display, white, [centerX_2, centerY + i * centerDistance, centerWidth, centerHeight])
            pygame.draw.rect(display, white, [centerX_3, centerY + i * centerDistance, centerWidth, centerHeight])
        display.blit(coin, (coinX, coinY))
        display.blit(car, (carX, carY))
        display.blit(inc, (incX, incY))

        text = smallFont.render('Score: ' + str(points), True, black)
        display.blit(text, (0, 0))

        car_crash(carX, carY, incX, incY)
        if check_GAMESPEED_out(carX):
            if carX < 0.15 * windowWidth:
                for i in range(0, 20):
                    display.fill(white)
                    display.blit(road, (0, 0))
                    if (check_coin(carX, carY, coinX, coinY)):
                        coinX, coinY = random.uniform(0.2 * windowWidth, 0.7 * windowWidth), 0
                        points += 1
                        points_counter += 1

                    centerY += GAMESPEED
                    centerY = centerY % centerDistance
                    coinY += GAMESPEED
                    incY += 2 * GAMESPEED
                    carX -= GAMESPEED
                    carY -= GAMESPEED

                    if coinY >= windowHeight:
                        coinX, coinY = random.uniform(0.2 * windowWidth, 0.7 * windowWidth), windowHeight * -0.5
                    if incY >= windowHeight:
                        incX, incY = random.uniform(0.2 * windowWidth, 0.7 * windowWidth), windowHeight * -0.5

                    new_car = pygame.transform.rotate(car, 10 + 3 * i)

                    for i in range(-1, 8):
                        pygame.draw.rect(display, white, [centerX_1, centerY + i * centerDistance, centerWidth, centerHeight])
                        pygame.draw.rect(display, white, [centerX_2, centerY + i * centerDistance, centerWidth, centerHeight])
                        pygame.draw.rect(display, white, [centerX_3, centerY + i * centerDistance, centerWidth, centerHeight])
                    display.blit(coin, (coinX, coinY))
                    display.blit(new_car, (carX, carY))
                    display.blit(inc, (incX, incY))

                    text = smallFont.render('Score: ' + str(points), True, black)
                    display.blit(text, (0, 0))
                    clock.tick(FPS)
                    pygame.display.update()
            if carX > 0.75 * windowWidth:
                for i in range(0, 20):
                    display.fill(white)
                    display.blit(road, (0, 0))
                    if (check_coin(carX, carY, coinX, coinY)):
                        coinX, coinY = random.uniform(0.2 * windowWidth, 0.7 * windowWidth), 0
                        points += 1
                        points_counter += 1

                    centerY += GAMESPEED
                    centerY = centerY % centerDistance
                    coinY += GAMESPEED
                    incY += 2 * GAMESPEED
                    carX += GAMESPEED
                    carY -= GAMESPEED

                    if coinY >= windowHeight:
                        coinX, coinY = random.uniform(0.2 * windowWidth, 0.7 * windowWidth), windowHeight * -0.5
                    if incY >= windowHeight:
                        incX, incY = random.uniform(0.2 * windowWidth, 0.7 * windowWidth), windowHeight * -0.5

                    new_car = pygame.transform.rotate(car, -(10 + 3 * i))

                    for i in range(-1, 8):
                        pygame.draw.rect(display, white, [centerX_1, centerY + i * centerDistance, centerWidth, centerHeight])
                        pygame.draw.rect(display, white, [centerX_2, centerY + i * centerDistance, centerWidth, centerHeight])
                        pygame.draw.rect(display, white, [centerX_3, centerY + i * centerDistance, centerWidth, centerHeight])
                    display.blit(coin, (coinX, coinY))
                    display.blit(new_car, (carX, carY))
                    display.blit(inc, (incX, incY))

                    text = smallFont.render('Score: ' + str(points), True, black)
                    display.blit(text, (0, 0))
                    clock.tick(FPS)
                    pygame.display.update()
            game_over()

        clock.tick(FPS)
        pygame.display.update()

def check_coin(carX, carY, coinX, coinY):
    if (carX - coinX) <= coinSize and (coinX - carX) <= carWidth:
        if (carY - coinY) <= coinSize and (coinY - carY) <= carHeight:
            point_sound.play()
            return True

def car_crash(carX, carY, incX, incY):
    if (carX - incX) <= carWidth and (incX - carX) <= carWidth:
        if (carY - incY) <= carHeight and (incY - carY) <= carHeight:
            crash_sound.play()
            game_over()

def startmenu():
    while True:
        display.fill(white)
        display.blit(menu_background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # START BUTTON
                if windowWidth / 10 <= mousePos[0] <= windowWidth / 10 + 320 and windowHeight / 10 <= mousePos[1] <= windowHeight / 10 + 60:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    return True
                # HELP BUTTON
                if windowWidth / 10 <= mousePos[0] <= windowWidth / 10 + 320 and 2 * windowHeight / 10 <= mousePos[1] <= 2 * windowHeight / 10 + 60:
                    helpmenu()
                # QUIT BUTTON
                if windowWidth / 10 <= mousePos[0] <= windowWidth / 10 + 320 and 3 * windowHeight / 10 <= mousePos[1] <= 3 * windowHeight / 10 + 60:
                    pygame.quit()
                    sys.exit()

        mousePos = pygame.mouse.get_pos()

        # MENU BOX
        if windowWidth / 10 <= mousePos[0] <= windowWidth / 10 + 320 and 2 * windowHeight / 10 <= mousePos[1] <= 3 * windowHeight / 10 + 60:
            pygame.draw.rect(display, (black), [windowWidth / 12.5, windowHeight / 25, 400, 400])
        else:
            pygame.draw.rect(display, (black), [windowWidth / 12.5, windowHeight / 25, 400, 400])

        # START BUTTON
        if windowWidth / 10 <= mousePos[0] <= windowWidth / 10 + 320 and windowHeight / 10 <= mousePos[1] <= windowHeight / 10 + 60:
            pygame.draw.rect(display, (white), [windowWidth / 10, windowHeight / 10, 320, 60])
            startText = menuFont.render("START", True, red)
        else:
            pygame.draw.rect(display, (white), [windowWidth / 10, windowHeight / 10, 320, 60])
            startText = menuFont.render("START", True, black)

        # HELP BUTTON
        if windowWidth / 10 <= mousePos[0] <= windowWidth / 10 + 320 and 2 * windowHeight / 10 <= mousePos[1] <= 2 * windowHeight / 10 + 60:
            pygame.draw.rect(display, (white), [windowWidth / 10, 2 * windowHeight / 10, 320, 60])
            helpText = menuFont.render("HELP", True, red)
        else:
            pygame.draw.rect(display, (white), [windowWidth / 10, 2 * windowHeight / 10, 320, 60])
            helpText = menuFont.render("HELP", True, black)

        # QUIT BUTTON
        if windowWidth / 10 <= mousePos[0] <= windowWidth / 10 + 320 and 3 * windowHeight / 10 <= mousePos[1] <= 3 * windowHeight / 10 + 60:
            pygame.draw.rect(display, (white), [windowWidth / 10, 3 * windowHeight / 10, 320, 60])
            quitText = menuFont.render("QUIT", True, red)
        else:
            pygame.draw.rect(display, (white), [windowWidth / 10, 3 * windowHeight / 10, 320, 60])
            quitText = menuFont.render("QUIT", True, black)

        # START BUTTON
        display.blit(startText, (windowWidth / 10 + 40, windowHeight / 10))
        # HELP BUTTON
        display.blit(helpText, (windowWidth / 10 + 40, 2 * windowHeight / 10))
        # QUIT BUTTON
        display.blit(quitText, (windowWidth / 10 + 40, 3 * windowHeight / 10))

        # GAME TITLE
        titleText = titleFont.render("HIGHWAY", True, black)
        display.blit(titleText, (windowWidth / 10 + 580, 1.5 * windowHeight / 10))

        pygame.display.update()

def helpmenu():
    while True:
        display.fill(white)
        display.blit(help_background, (0, 0))
        title = menuFont.render('HELP:', True, black)
        help_1 = menuFont.render('Try to collect as many coins as you can while', True, black)
        help_2 = menuFont.render('avoiding the vehicles driving towards you.', True, black)
        help_3 = menuFont.render('You will get faster every 10 points up to 50 points.', True, black)
        control_1 = menuFont.render('CONTROLS:', True, black)
        control_2 = menuFont.render('Right Arrow: Hold to move car right.', True, black)
        control_3 = menuFont.render('Left Arrow: Hold to move car left.', True, black)
        display.blit(title, (windowWidth / 10, windowHeight / 10))
        display.blit(help_1, (windowWidth / 10, 2 * windowHeight / 10))
        display.blit(help_2, (windowWidth / 10, 3 * windowHeight / 10))
        display.blit(help_3, (windowWidth / 10, 4 * windowHeight / 10))
        display.blit(control_1, (windowWidth / 10, 5 * windowHeight / 10))
        display.blit(control_2, (windowWidth / 10, 6 * windowHeight / 10))
        display.blit(control_3, (windowWidth / 10, 7 * windowHeight / 10))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if windowWidth / 10 <= mousePos[0] <= windowWidth / 10 + 270 and 9 * windowHeight / 10 <= mousePos[1] <= 9 * windowHeight / 10 + 60:
                    gameloop()

        mousePos = pygame.mouse.get_pos()

        if windowWidth / 10 <= mousePos[0] <= windowWidth / 10 + 270 and 9 * windowHeight / 10 <= mousePos[1] <= 9 * windowHeight / 10 + 60:
            pygame.draw.rect(display, (white), [windowWidth / 10, 9 * windowHeight / 10, 270, 60])
            backText = menuFont.render("BACK", True, red)
        else:
            pygame.draw.rect(display, (white), [windowWidth / 10, 9 * windowHeight / 10, 270, 60])
            backText = menuFont.render("BACK", True, black)

        display.blit(backText, (windowWidth / 10 + 40, 9 * windowHeight / 10))

        pygame.display.update()

def game_over():
    display.fill(red)
    crashed = crashFont.render('YOU CRASHED', True, white)
    gameover = crashFont.render('GAME OVER', True, white)
    display.blit(crashed, (windowWidth / 3, windowHeight / 2.75))
    display.blit(gameover, (windowWidth / 2.75, windowHeight / 2.25))
    pygame.display.update()
    time.sleep(4)
    startloop()

def check_GAMESPEED_out(carX):
    if carX < 0.15 * windowWidth or carX > 0.75 * windowWidth:
        crash_sound.play()
        return True
    return False

gameloop()