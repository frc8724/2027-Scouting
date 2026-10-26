#Made by Derek
#Ram usage: 60.9MB once fonts are loaded. (10.1MB when compiled to an .exe)
import globalButtons as main
main.getWriteDir()
main.aspectRatio(1070, 600)
main.initDropsMainMenu(0, 50, 150, 50, 2)
main.initDropsMainMenu2(725, 50, 150, 50, 2, 360, 50, 150, 50, 2, 920, 50, 150, 50, 2)
main.initDropsAutoMenu(400, 100, 200, 100, 3, 750, 50, 200, 50, 3, 100, 275, 250, 50, 3)
main.initDropsTeleMenu(125, 25, 50, 50, 375, 75, 75, 50)
while True:  

    if main.menuNumber == 1:
        main.drawMainMenu(1020, 0, 50, 25, 185, 475, 500, 100, 45, 45, 100, 0, 200, 45)

    elif main.menuNumber == 2:
        main.drawAutoMenu(200, 100, 50, 50, 2, 70, 0, 250, 45, 650, 375, 400, 200)

    elif main.menuNumber == 3:
        main.drawTeleopMenu(200, 100, 50, 50, 2, 70, 0, 250, 45, 650, 375, 400, 200)

    print(main.menuNumber)
    main.pygame.display.flip()
    main.clock.tick(60)
