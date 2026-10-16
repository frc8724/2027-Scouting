#Made by Derek
from globalButtons import *
getWriteDir()
aspectRatio(460, 1000)
initDropsMainMenu(0, 35, 90, 50, 2)
initDropsMainMenu2(370, 35, 90, 50, 2, 115, 445, 90, 50, 2, 225, 445, 130, 50, 2)
while True:
    if menuNumber == 1:
        drawMainMenu(410, 0, 50, 25, 30, 925, 400, 50, 30, 30)
        updateDynamicDrops()
    pygame.display.flip()
    clock.tick(60)