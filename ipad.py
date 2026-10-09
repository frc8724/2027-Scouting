#Made by Derek
from globalButtons import *
aspectRatio(600, 800)
initDropsMainMenu(50, 75, 100, 50, 1)
initDropsMainMenu2(450, 75, 100, 50, 1)
while True:
    if menuNumber == 1:
        drawMainMenu(550, 0, 50, 25, 50, 675, 500, 100, 50, 50)
        updateDynamicDrops()
    pygame.display.flip()
    clock.tick(60)