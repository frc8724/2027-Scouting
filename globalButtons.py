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
global dropRect
dropRect = {}
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
        self.list = textList
        self.event = event

    def initDropped(self):
        #necessary for my spaghetti code to work
        #call before drawing dropdown
        self.dropped = 0
        
    def draw(self, surface):
        global z
        dropRect[self.text] = {}
        for z in range (0, self.amount):
            global rect
            if self.dropped == 1:
                #draw many buttons
                rect = pygame.Rect(self.x, self.y, self.width, self.height)
                dropRect[self.text][self.list[z-1]] = pygame.Rect(self.x, self.y+self.height*z, self.width, self.height)
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
                self.textRender3 = self.textRenderDrop.get_rect(center=dropRect[self.text][self.list[z-1]].center)
                pygame.draw.rect(surface, self.color, dropRect[self.text][self.list[z-1]], border_radius=self.rounding)
                surface.blit(self.textRenderDrop, self.textRender3)
                if self.event.type == pygame.MOUSEBUTTONDOWN and self.event.button == 1:
                    if dropRect[self.text][self.amount].collidepoint(self.event.pos):
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
                    dropRect[self.text] = {}
                    dropRect[self.text][self.list[z-1]] = pygame.Rect(self.x, self.y+self.height*z, self.width, self.height)
                    if dropRect[self.text][self.list[z-1]].collidepoint(event.pos):
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

def matchSelector():
    print(dropRect)
    print(f"text: {' '.join(dropRect["Match"])}")

def matchBatchSelector():
    global selectedBatch
    if ' '.join(dropRect["Match Chunk"]) == 'do not select':
        pass
    else:
        selectedBatch = int(' '.join(dropRect["Match Chunk"]))
        print(selectedBatch)

def teamSelector():
    print(dropRect)
    print(f"text: {' '.join(dropRect["Team"])}")

def teamBatchSelector():
    global selectedBatch2
    if ' '.join(dropRect["Team Chunk"]) == 'do not select':
        pass
    else:
        selectedBatch2 = int(' '.join(dropRect["Team Chunk"]))
        print(selectedBatch2)

#test code
matchList = [0, 0, 0, 0, 0, 0, 0]
matchList[0] = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
matchList[1] = ['11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
matchList[2] = ['21', '22', '23', '24', '25', '26', '27', '28', '29', '30']
matchList[3] = ['31', '32', '33', '34', '35', '36', '37', '38', '39', '40']
matchList[4] = ['41', '42', '43', '44', '45', '46', '47', '48', '49', '50']
matchList[5] = ['51', '52', '53', '54', '55', '56', '57', '58', '59', '60']
matchList[6] = ['61', '62', '63', '64', '65', '66', '67', '68', '69', '70']
batchList = ['1', '2', '3', '4', '5', '6', '7', 'do not select']
teamList = [0, 0, 0, 0, 0, 0, 0]
teamList[0] = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
teamList[1] = ['11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
teamList[2] = ['21', '22', '23', '24', '25', '26', '27', '28', '29', '30']
teamList[3] = ['31', '32', '33', '34', '35', '36', '37', '38', '39', '40']
teamList[4] = ['41', '42', '43', '44', '45', '46', '47', '48', '49', '50']
teamList[5] = ['51', '52', '53', '54', '55', '56', '57', '58', '59', '60']
teamList[6] = ['61', '62', '63', '64', '65', '66', '67', '68', '69', '70']
batchList2 = ['1', '2', '3', '4', '5', '6', '7', 'do not select']

def drawMainMenu(closeX, closeY, closeW, closeH, startX, startY, startW, startH, logoW, logoH):
    #infinite parameters
    global closeButton
    global matchSelectDrop
    global teamSelectDrop
    logo = pygame.image.load("assets/logo.png")
    closeButton = Button(text="Close", x = closeX, y = closeY, width = closeW, height = closeH, color = (255, 0, 0), function = exitButton, fontType = 1, rounding = 15)
    startButton = Button(text="Start Match", x = startX, y = startY, width = startW, height = startH, color = (100, 100, 255), function = startMatchButton, fontType = 3, rounding = 50)
    for event in pygame.event.get():
        global event2
        event2 = event
        closeButton.isClicked(event)
        startButton.isClicked(event)
        matchSelectDrop.isClicked(event)
        matchBatch.isClicked(event)
        teamSelectDrop.isClicked(event)
        teamBatch.isClicked(event)
    #draw the things
    screen.fill((100, 100, 100))
    matchSelectDrop.draw(screen)
    matchBatch.draw(screen)
    teamSelectDrop.draw(screen)
    teamBatch.draw(screen)
    closeButton.draw(screen)
    startButton.draw(screen)
    screen.blit(pygame.transform.scale(logo, (logoW, logoH)), (0, 0))

def initDrops(matchX, matchY, matchW, matchH, matchFont, teamX, teamY, teamW, teamH, teamFont):
    #separate function to define dropdowns so you can actually read data from them
    global matchSelectDrop
    global matchBatch
    global selectedBatch
    global selectedBatch2
    global teamSelectDrop
    global teamBatch
    for event in pygame.event.get():
        global event2
        event2 = event
    selectedBatch = 1
    selectedBatch2 = 1
    matchSelectDrop = Dropdown(text="Match", x = matchX, y = matchY, width = matchW, height = matchH, color = (0, 255, 0), function = matchSelector, fontType = matchFont, dropFont = 1, rounding = 5, dropdownAmount = 10, textList = matchList[selectedBatch-1], event=event2)
    matchBatch = Dropdown(text="Match Chunk", x = matchX+matchW+25, y = matchY, width = matchW, height = matchH, color = (0, 255, 0), function = matchBatchSelector, fontType = matchFont, dropFont = 1, rounding = 5, dropdownAmount = 7, textList = batchList, event=event2)
    matchSelectDrop.initDropped()
    matchBatch.initDropped()
    teamSelectDrop = Dropdown(text="Team", x = teamX, y = teamY, width = teamW, height = teamH, color = (0, 255, 0), function = teamSelector, fontType = teamFont, dropFont = 1, rounding = 5, dropdownAmount = 10, textList = teamList[selectedBatch2-1], event=event2)
    teamBatch = Dropdown(text="Team Chunk", x = teamX-teamW-25, y = teamY, width = teamW, height = teamH, color = (0, 255, 0), function = teamBatchSelector, fontType = teamFont, dropFont = 1, rounding = 5, dropdownAmount = 7, textList = batchList2, event=event2)
    teamSelectDrop.initDropped()
    teamBatch.initDropped()

def updateDynamicDrops():
    global matchSelectDrop
    global teamSelectDrop
    for event in pygame.event.get():
        global event2
        event2 = event
    matchSelectDrop.list = matchList[selectedBatch-1]
    teamSelectDrop.list = matchList[selectedBatch2-1]