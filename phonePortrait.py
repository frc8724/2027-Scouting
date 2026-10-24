#Made by Derek
import globalButtons as main
main.getWriteDir()
main.aspectRatio(460, 1000)
main.initDropsMainMenu(0, 35, 90, 50, 2)
main.initDropsMainMenu2(370, 35, 90, 50, 2, 115, 445, 90, 50, 2, 225, 445, 130, 50, 2)
main.initDropsAutoMenu(260, 50, 200, 100, 3)
while True:

    if main.menuNumber == 1:
        main.drawMainMenu(410, 0, 50, 25, 30, 925, 400, 50, 30, 30, 0, 850, 96.25, 50)

    elif main.menuNumber == 2:
        main.drawAutoMenu(100, 50, 50, 75, 2)

    main.pygame.display.flip()
    main.clock.tick(60)