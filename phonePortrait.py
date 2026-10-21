#Made by Derek
import globalButtons as main
main.getWriteDir()
main.aspectRatio(460, 1000)
main.initDropsMainMenu(0, 35, 90, 50, 2)
main.  initDropsMainMenu2(370, 35, 90, 50, 2, 115, 445, 90, 50, 2, 225, 445, 130, 50, 2)
while True:

    if main.menuNumber == 1:
        main.drawMainMenu(410, 0, 50, 25, 30, 925, 400, 50, 30, 30)
    elif main.menuNumber == 2:
        main.drawAutoMenu(200, 200, 50, 50, 2) #placeholder values until menuNumber actually updates

    main.pygame.display.flip()
    main.clock.tick(60)