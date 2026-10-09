#Made by Derek
from globalButtons import *
aspectRatio(460, 1000)
initDropsMainMenu(0, 75, 90, 50, 1)
initDropsMainMenu2(370, 75, 90, 50, 1)
while True:
    if menuNumber == 1:
        drawMainMenu(410, 0, 50, 25, 30, 875, 400, 100, 50, 50)
        updateDynamicDrops()
    pygame.display.flip()
    clock.tick(60)