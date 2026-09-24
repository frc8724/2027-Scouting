#Made by Derek
from globalButtons import *
aspectRatio(1070, 600)
initDrops()
while True:
    if menuNumber == 1:
        drawMainMenu(1020, 0, 50, 25, 285, 475, 500, 100, 75, 75)

    pygame.display.flip()
    clock.tick(60)