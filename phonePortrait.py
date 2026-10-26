#Made by Derek
import globalButtons as main
main.getWriteDir()
main.aspectRatio(460, 1000)
main.initDropsMainMenu(0, 35, 90, 50, 2)
main.initDropsMainMenu2(370, 35, 90, 50, 2, 115, 445, 90, 50, 2, 225, 445, 130, 50, 2)
main.initDropsAutoMenu(200, 100, 125, 100, 2, 330, 100, 125, 100, 2, 25, 375, 150, 100, 2)
main.initDropsTeleMenu(25, 15, 50, 50, 225, 75, 75, 50)
while True:

    if main.menuNumber == 1:
        main.drawMainMenu(410, 0, 50, 25, 30, 925, 400, 50, 30, 30, 0, 850, 96.25, 50)

    elif main.menuNumber == 2:
        main.drawAutoMenu(75, 100, 50, 75, 3, 0, 850, 135, 50, 30, 925, 400, 50)

    elif main.menuNumber == 3:
        main.drawTeleopMenu(75, 100, 50, 75, 3, 0, 850, 135, 50, 30, 925, 400, 50)

    main.pygame.display.flip()
    main.clock.tick(60)