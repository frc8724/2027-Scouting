import pygame
import sys
pygame.init()
# put this at beginning of gui code!!!!!!!
def aspectRatio(x, y):
    global screen
    screen = pygame.display.set_mode((x, y))
#pygame setup
clock = pygame.time.Clock()
pygame.display.set_caption("Scouting App")
pygame.display.set_icon(pygame.image.load("assets/logo.png"))
# font sizes
smallFont = pygame.font.Font("assets/mainFont.ttf", 15)
bigFont = pygame.font.Font("assets/mainFont.ttf", 30)
hugeFont = pygame.font.Font("assets/mainFont.ttf", 50)
boldFont = pygame.font.Font("assets/boldFont.ttf", 30)
menuNumber = 1
# 1 = main menu
# 2 = auto period
class Button:
    def __init__(self, text, x, y, width, height, color, function, fontType, rounding):
        #def variables
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.function = function
        self.rounding = rounding

        #initialize font system
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
        #put the button on the screen
        pygame.draw.rect(surface, self.color, self.rect, border_radius=self.rounding)
        surface.blit(self.textRender, self.textRender2)

    def isClicked(self, event):
        #see if it is clicked
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.function()

class Dropdown:
    def __init__(self, text, x, y, width, height, color, function, fontType, dropFont, rounding, dropdownAmount, textList, event):
        #variables
        self.text = text
        self.color = color
        self.function = function
        self.rounding = rounding
        self.amount = dropdownAmount+1
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.font = fontType
        self.dropFont = dropFont
        self.dropped = 0
        self.list = textList
        self.event = event

    def initDropped(self):
        #necessary for my spaghetti code to work
        #call before drawing dropdown
        global dropped
        dropped = 0
        
    def draw(self, surface):
        global z
        global dropRect
        dropRect = {}
        for z in range (0, self.amount):
            global rect
            if self.dropped == 1:
                #draw many buttons
                rect = pygame.Rect(self.x, self.y, self.width, self.height)
                dropRect[self.list[z-1]] = pygame.Rect(self.x, self.y+self.height*z, self.width, self.height)
            else:
                #draw just the one button
                rect = pygame.Rect(self.x, self.y, self.width, self.height)
            #FOOOOOOOOONTSSSS
            if self.font == 1:
                self.textRenderOG = smallFont.render(self.text, True, (0, 0, 0))
            elif self.font == 2:
                self.textRenderOG = bigFont.render(self.text, True, (0, 0, 0))
            elif self.font == 3:
                self.textRenderOG = hugeFont.render(self.text, True, (0, 0, 0))
            elif self.font == 4:
                self.textRenderOG = smallFont.render(self.text, True, (255, 255, 255))
            elif self.font == 5:
                self.textRenderOG = bigFont.render(self.text, True, (255, 255, 255))
            elif self.font == 6:
                self.textRenderOG = hugeFont.render(self.text, True, (255, 255, 255))
            elif self.font == 7:
                self.textRenderOG = boldFont.render(self.text, True, (0, 0, 0))
            elif self.font == 8:
                self.textRenderOG = boldFont.render(self.text, True, (255, 255, 255))
            else:
                self.textRenderOG = bigFont.render(self.text, True, (0, 0, 0))
            if self.dropFont == 1:
                self.textRenderDrop = smallFont.render(self.list[z-1], True, (0, 0, 0))
            elif self.dropFont == 2:
                self.textRenderDrop = bigFont.render(self.list[z-1], True, (0, 0, 0))
            elif self.dropFont == 3:
                self.textRenderDrop = hugeFont.render(self.list[z-1], True, (0, 0, 0))
            elif self.dropFont == 4:
                self.textRenderDrop = smallFont.render(self.list[z-1], True, (255, 255, 255))
            elif self.dropFont == 5:
                self.textRenderDrop = bigFont.render(self.list[z-1], True, (255, 255, 255))
            elif self.dropFont == 6:
                self.textRenderDrop = hugeFont.render(self.list[z-1], True, (255, 255, 255))
            elif self.dropFont == 7:
                self.textRenderDrop = boldFont.render(self.list[z-1], True, (0, 0, 0))
            elif self.dropFont == 8:
                self.textRenderDrop = boldFont.render(self.list[z-1], True, (255, 255, 255))
            else:
                self.textRenderDrop = bigFont.render(self.list[z-1], True, (0, 0, 0))
            #self.render the text and draw the boxes
            self.textRender2 = self.textRenderOG.get_rect(center=rect.center)
            pygame.draw.rect(surface, self.color, rect, border_radius=self.rounding)
            surface.blit(self.textRenderOG, self.textRender2)
            if self.dropped == 1:
                #separate fonts on the dropped vs. undropped boxes
                self.textRender3 = self.textRenderDrop.get_rect(center=dropRect[self.list[z-1]].center)
                pygame.draw.rect(surface, self.color, dropRect[self.list[z-1]], border_radius=self.rounding)
                surface.blit(self.textRenderDrop, self.textRender3)
                if self.event.type == pygame.MOUSEBUTTONDOWN and self.event.button == 1:
                    if dropRect[self.amount].collidepoint(self.event.pos):
                        self.function()

    def isClicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if rect.collidepoint(event.pos):
                #click events
                if self.dropped == 0:
                  self.dropped = 1
                  print('should be dropped down')
                elif self.dropped == 1:
                    self.dropped = 0
                    print('should be dropped up')
            # if dropdown is open, check if a drop item was clicked and call its function
            if self.dropped == 1:
                for z in range(0, self.amount):
                    global dropRect
                    dropRect = {}
                    dropRect[self.list[z-1]] = pygame.Rect(self.x, self.y+self.height*z, self.width, self.height)
                    if dropRect[self.list[z-1]].collidepoint(event.pos):
                        self.function()
                        break

def exitButton():
    #bye
    pygame.quit()
    sys.exit()

def startMatchButton():
    #non functional currently
    print("match started")
    menuNumber = 2

def testDropFunc():
    print(f"text: {' '.join(dropRect)}")

#test code
testDropList = ["mary", "had", "a", "little", "lamb"]
def drawMainMenu(closeX, closeY, closeW, closeH, startX, startY, startW, startH, logoW, logoH):
    #infinite parameters
    global closeButton
    global dropTest
    logo = pygame.image.load("assets/logo.png")
    closeButton = Button(text="Close", x = closeX, y = closeY, width = closeW, height = closeH, color = (255, 0, 0), function = exitButton, fontType = 1, rounding = 15)
    startButton = Button(text="Start Match", x = startX, y = startY, width = startW, height = startH, color = (100, 100, 255), function = startMatchButton, fontType = 3, rounding = 50)
    for event in pygame.event.get():
        global event2
        event2 = event
        closeButton.isClicked(event)
        startButton.isClicked(event)
        dropTest.isClicked(event)
    #draw the things
    screen.fill((100, 100, 100))
    dropTest.draw(screen)
    closeButton.draw(screen)
    startButton.draw(screen)
    screen.blit(pygame.transform.scale(logo, (logoW, logoH)), (0, 0))

def initDrops():
    #dont ask why it's necessary just call it in the GUI code
    global dropTest
    for event in pygame.event.get():
        global event2
        event2 = event
    dropTest = Dropdown(text="Test", x = 100, y = 200, width = 100, height = 50, color = (0, 255, 0), function = testDropFunc, fontType = 2, dropFont = 1, rounding = 5, dropdownAmount = 5, textList = testDropList, event=event2)
    dropTest.initDropped()