#Made by Derek
#Ram usage: 52.7MB once fonts are loaded.
from globalButtons import *
getWriteDir()
aspectRatio(1070, 600)
initDropsMainMenu(0, 50, 150, 50, 1)
initDropsMainMenu2(725, 50, 150, 50, 1, 360, 50, 150, 50, 1, 920, 50, 150, 50, 1)
while True:
    if menuNumber == 1:
        drawMainMenu(1020, 0, 50, 25, 185, 475, 500, 100, 45, 45)
        updateDynamicDrops()
    pygame.display.flip()
    clock.tick(60)