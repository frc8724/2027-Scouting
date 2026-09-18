import pygame
import sys
pygame.init()
# put this at beginning of gui code!!!!!!!
def aspectRatio(x, y):
    global screen
    screen = pygame.display.set_mode((x, y))
clock = pygame.time.Clock()
pygame.display.set_caption("Scouting App")
pygame.display.set_icon(pygame.image.load("assets/logo.png"))
smallFont = pygame.font.Font("assets/mainFont.ttf", 15)
bigFont = pygame.font.Font("assets/mainFont.ttf", 30)
hugeFont = pygame.font.Font("assets/mainFont.ttf", 50)
boldFont = pygame.font.Font("assets/boldFont.ttf", 30)
menuNumber = 1
# 1 = main menu
# 2 = auto period
class Button:
    def __init__(self, text, x, y, width, height, color, function, fontType, rounding):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.function = function
        self.rounding = rounding

        if fontType == 1:
            self.textRender = smallFont.render(text, True, (0, 0, 0))
        elif fontType == 2:
            self.textRender = bigFont.render(text, True, (0, 0, 0))
        elif fontType == 3:
            self.textRender = hugeFont.render(text, True, (0, 0, 0))
        elif fontType == 4:
            self.textRender = smallFont.render(text, True, (255, 255, 255))
        elif fontType == 5:
            self.textRender = bigFont.render(text, True, (255, 255, 255))
        elif fontType == 6:
            self.textRender = hugeFont.render(text, True, (255, 255, 255))
        elif fontType == 7:
            self.textRender = boldFont.render(text, True, (0, 0, 0))
        elif fontType == 8:
            self.textRender = boldFont.render(text, True, (255, 255, 255))
        else:
            self.textRender = bigFont.render(text, True, (0, 0, 0))
        self.textRender2 = self.textRender.get_rect(center=self.rect.center)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=self.rounding)
        surface.blit(self.textRender, self.textRender2)

    def isClicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.function()

def exitButton():
    pygame.quit()
    sys.exit()

def startMatchButton():
    print("match started")
    menuNumber = 2

def drawMainMenu(closeX, closeY, closeW, closeH, startX, startY, startW, startH, logoW, logoH):
    global closeButton
    logo = pygame.image.load("assets/logo.png")
    closeButton = Button(text="Close", x = closeX, y = closeY, width = closeW, height = closeH, color = (255, 0, 0), function = exitButton, fontType = 4, rounding = 15)
    startButton = Button(text="Start Match", x = startX, y = startY, width = startW, height = startH, color = (100, 100, 255), function = startMatchButton, fontType = 3, rounding = 50)
    for event in pygame.event.get():
        closeButton.isClicked(event)
        startButton.isClicked(event)

    screen.fill((100, 100, 100))
    closeButton.draw(screen)
    startButton.draw(screen)
    screen.blit(pygame.transform.scale(logo, (logoW, logoH)), (0, 0))