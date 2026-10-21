#Made by Derek
#Ram usage: 52.7MB once fonts are loaded.
from globalButtons import *
getWriteDir()
aspectRatio(1070, 600)
initDropsMainMenu(0, 50, 150, 50, 2)
initDropsMainMenu2(725, 50, 150, 50, 2, 360, 50, 150, 50, 2, 920, 50, 150, 50, 2)
while True:  

    if menuNumber == 1:
        drawMainMenu(1020, 0, 50, 25, 185, 475, 500, 100, 45, 45)

    elif menuNumber == 2:
        drawAutoMenu(200, 200, 50, 50, 2)

    print(menuNumber)
    pygame.display.flip()
    clock.tick(60)
