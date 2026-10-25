#Made by Derek
import globalButtons as main
main.getWriteDir()
main.aspectRatio(600, 800)
main.initDropsMainMenu(10, 60, 75, 50, 2)
main.initDropsMainMenu2(400, 60, 75, 50, 2, 200, 60, 75, 50, 2, 500, 60, 100, 50, 2)
main.initDropsAutoMenu(350, 100, 100, 100, 2, 475, 100, 100, 100, 2, 25, 275, 200, 50, 2)
while True:
    if main.menuNumber == 1:
        main.drawMainMenu(550, 0, 50, 25, 50, 700, 500, 75, 50, 50, 12.5, 625, 125, 50)

    if main.menuNumber == 2:
        main.drawAutoMenu(100, 100, 50, 50, 2, 12.5, 625, 125, 50)
    main.pygame.display.flip()
    main.clock.tick(60)