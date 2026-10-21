#Made by Derek
#Ram usage: 52.7MB once fonts are loaded.
import globalButtons as main
main.getWriteDir()
main.aspectRatio(1070, 600)
main.initDropsMainMenu(0, 50, 150, 50, 2)
main.initDropsMainMenu2(725, 50, 150, 50, 2, 360, 50, 150, 50, 2, 920, 50, 150, 50, 2)
while True:  

    if main.menuNumber == 1:
        main.drawMainMenu(1020, 0, 50, 25, 185, 475, 500, 100, 45, 45)

    elif main.menuNumber == 2:
        main.drawAutoMenu(200, 200, 50, 50, 2)

    print(main.menuNumber)
    main.pygame.display.flip()
    main.clock.tick(60)
