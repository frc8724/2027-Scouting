#Made by Derek
from globalButtons import *
aspectRatio(460, 1000)
while True:
    if menuNumber == 1:
        drawMainMenu(410, 0, 50, 25, 30, 875, 400, 100, 50, 50)

    pygame.display.flip()
    clock.tick(60)