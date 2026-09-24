#Made by Derek
from globalButtons import *
aspectRatio(600, 800)
initDrops()
while True:
    if menuNumber == 1:
        drawMainMenu(550, 0, 50, 25, 50, 675, 500, 100, 50, 50)

    pygame.display.flip()
    clock.tick(60)