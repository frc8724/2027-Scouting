import pygame
import sys
import csv
import os
import math
from pathlib import Path
pygame.init()
# put this at beginning of gui code!!!!!!!
def aspectRatio(x, y):
    #dynamic scaling
    global xMult
    global yMult
    x2 = pygame.display.Info().current_w
    y2 = pygame.display.Info().current_h
    xMult = x2/x
    yMult = y2/y
    #screen setup
    global screen
    screen = pygame.display.set_mode((x2, y2))

#pygame setup for windows, android takes whatever is in buildozer.spec
clock = pygame.time.Clock()
pygame.display.set_caption("Scouting App")

#this part is so initDrops doesn't fail immediatly
global event2
for event in pygame.event.get():
    event2 = event

# font sizes
if 'ANDROID_ARGUMENT' in os.environ:
    #android workaround because the working directory on android is system root not where the code is executing from, so assets need to be loaded with the full path
    smallFont = pygame.font.Font("/data/data/org.frc8724.scouting/files/app/assets/mainFont.ttf", 15)
    bigFont = pygame.font.Font("/data/data/org.frc8724.scouting/files/app/assets/mainFont.ttf", 30)
    hugeFont = pygame.font.Font("/data/data/org.frc8724.scouting/files/app/assets/mainFont.ttf", 50)
    boldFont = pygame.font.Font("/data/data/org.frc8724.scouting/files/app/assets/boldFont.ttf", 30)
    logo = pygame.image.load("/data/data/org.frc8724.scouting/files/app/assets/logo.png")
    pygame.display.set_icon(pygame.image.load("/data/data/org.frc8724.scouting/files/app/assets/logo.png"))
else:
    #normal windows/linux setup where the working dir is actually where the code is executing from, so assets load relative to the .exe/.bin
    smallFont = pygame.font.Font("assets/mainFont.ttf", 15)
    bigFont = pygame.font.Font("assets/mainFont.ttf", 30)
    hugeFont = pygame.font.Font("assets/mainFont.ttf", 50)
    boldFont = pygame.font.Font("assets/boldFont.ttf", 30)
    logo = pygame.image.load("assets/logo.png")
    pygame.display.set_icon(pygame.image.load("assets/logo.png"))

global menuNumber
menuNumber = 1
# 1 = main menu
# 2 = auto period

#also call at beginning of GUI code to get the dir to write to!!
def getWriteDir():
    #directory for android/Windows
    global writeDir
    if 'ANDROID_ARGUMENT' in os.environ:
        # Android
        writeDir = Path(os.environ['EXTERNAL_STORAGE']) / 'Documents' / 'FRC_Scouting_Output'
    else:
        # Windows
        writeDir = Path.home() / 'FRC_Scouting_Output'
    writeDir.mkdir(parents=True, exist_ok=True)

#yes, the dropdown system relies on dictionaries (in dictionaries). however, it is quite optimized!
global dropRect
dropRect = {}
global rect
rect = {}
global fonts
fonts = {}

#default values for saving, required to not crash when saving before selecting values
matchNumber2 = "-1"
teamNumber = "-1"
robotPosition = "none (did not save)"
scoutName = "John Doe"
global autoFuelCount
autoFuelCount = 0

def fontDef(fontVar, fontType, passedText="well that's not great"):
    #necessary for optimization; makes it so the fonts (at least for buttons) are only defined on startup and not every frame.
    if fontType == 1:
        variable = smallFont.render(passedText, True, (0, 0, 0))
    elif fontType == 2:
        variable = bigFont.render(passedText, True, (0, 0, 0))
    elif fontType == 3:
        variable = hugeFont.render(passedText, True, (0, 0, 0))
    elif fontType == 4:
        variable = smallFont.render(passedText, True, (255, 255, 255))
    elif fontType == 5:
        variable = bigFont.render(passedText, True, (255, 255, 255))
    elif fontType == 6:
        variable = hugeFont.render(passedText, True, (255, 255, 255))
    elif fontType == 7:
        variable = boldFont.render(passedText, True, (0, 0, 0))
    elif fontType == 8:
        variable = boldFont.render(passedText, True, (255, 255, 255))
    else:
        variable = bigFont.render(passedText, True, (0, 0, 0))
    fonts[fontVar] = variable

class Button:
    def __init__(self, text, x, y, width, height, color, function, fontType, rounding):
        #def variables
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.function = function
        self.rounding = rounding
        self.textRender = text

        #initialize font system
        fontDef(self.textRender, fontType, self.text)
        self.textRender2 = fonts[self.textRender].get_rect(center=self.rect.center)

    def draw(self, surface):
        #put the button on the screen
        pygame.draw.rect(surface, self.color, self.rect, border_radius=self.rounding)
        surface.blit(fonts[self.textRender], self.textRender2)

    def isClicked(self, event):
        #see if it is clicked
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 or event.type == pygame.FINGERDOWN:
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
                rect[self.text] = pygame.Rect(self.x, self.y, self.width, self.height)
                dropRect[self.text][self.list[z-1]] = pygame.Rect(self.x, self.y+self.height*z, self.width, self.height)
            else:
                #draw just the one button
                rect[self.text] = pygame.Rect(self.x, self.y, self.width, self.height)
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
            self.textRender2 = self.textRenderOG.get_rect(center=rect[self.text].center)
            pygame.draw.rect(surface, self.color, rect[self.text], border_radius=self.rounding)
            surface.blit(self.textRenderOG, self.textRender2)
            if self.dropped == 1:
                #separate fonts on the dropped vs. undropped boxes
                self.textRender3 = self.textRenderDrop.get_rect(center=dropRect[self.text][self.list[z-1]].center)
                pygame.draw.rect(surface, self.color, dropRect[self.text][self.list[z-1]], border_radius=self.rounding)
                surface.blit(self.textRenderDrop, self.textRender3)
                if self.event.type == pygame.MOUSEBUTTONDOWN and self.event.button == 1 or self.event.type == pygame.FINGERDOWN:
                    #check click events for the dropped boxes
                    if dropRect[self.text][self.amount].collidepoint(self.event.pos):
                        self.function()

    def isClicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 or event.type == pygame.FINGERDOWN:
            if rect[self.text].collidepoint(event.pos):
                #click events (only for the main button, not the dropped ones)
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
                    #global it yet again and redefine it so both pieces of code can work
                    dropRect[self.text] = {}
                    dropRect[self.text][self.list[z-1]] = pygame.Rect(self.x, self.y+self.height*z, self.width, self.height)
                    if dropRect[self.text][self.list[z-1]].collidepoint(event.pos):
                        self.function()
                        #requires break to not repeatedly call the function on hold
                        break

def exitButton():
    #bye
    pygame.quit()
    sys.exit()

def startMatchButton():
    #non functional currently
    print("match started")
    menuNumber = 2
    print(menuNumber)

def matchSelector():
    global matchNumber2
    if ' '.join(dropRect["Match"]) == 'placeholder':
        pass
    else:
        matchNumber2 = ' '.join(dropRect["Match"])
        matchSelectDrop.dropped = 0

def matchBatchSelector():
    global selectedBatch
    # updates batch of matches shown on the dropdown
    if ' '.join(dropRect["Match Chunk"]) == 'do not select':
        #required to work
        pass
    else:
        # updates the batch
        selectedBatch = int(' '.join(dropRect["Match Chunk"]))
        matchBatch.dropped = 0

def teamSelector():
    global teamNumber
    if ' '.join(dropRect["Team"]) == 'placeholder':
        pass
    else:
        teamNumber = ' '.join(dropRect["Team"])
        teamSelectDrop.dropped = 0

def teamBatchSelector():
    global selectedBatch2
    # updates batch of teams shown on the dropdown
    if ' '.join(dropRect["Team Chunk"]) == 'do not select':
        #required to work
        pass
    else:
        # updates the batch
        selectedBatch2 = int(' '.join(dropRect["Team Chunk"]))
        teamBatch.dropped = 0

def positionSelector():
    global robotPosition
    if ' '.join(dropRect["Position"]) == 'placeholder':
        pass
    else:
        robotPosition = ' '.join(dropRect["Position"])
        positionSelect.dropped = 0

def scoutSelector():
    global scoutName
    if ' '.join(dropRect["Scout"]) == 'placeholder':
        pass
    else:
        scoutName = ' '.join(dropRect["Scout"])
        scoutSelect.dropped = 0

def autoFuelPlus1Button():
    global autoFuelCount
    autoFuelCount += 1

def autoFuelMinus1Button():
    global autoFuelCount
    autoFuelCount -= 1

#define allllllllllllll the lists
matchList = [0, 0, 0, 0, 0, 0, 0]
matchList[0] = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'placeholder']
matchList[1] = ['11', '12', '13', '14', '15', '16', '17', '18', '19', '20', 'placeholder']
matchList[2] = ['21', '22', '23', '24', '25', '26', '27', '28', '29', '30', 'placeholder']
matchList[3] = ['31', '32', '33', '34', '35', '36', '37', '38', '39', '40', 'placeholder']
matchList[4] = ['41', '42', '43', '44', '45', '46', '47', '48', '49', '50', 'placeholder']
matchList[5] = ['51', '52', '53', '54', '55', '56', '57', '58', '59', '60', 'placeholder']
matchList[6] = ['61', '62', '63', '64', '65', '66', '67', '68', '69', '70', 'placeholder']
batchList = ['1', '2', '3', '4', '5', '6', '7', 'do not select']
teamList = [0, 0, 0, 0, 0, 0, 0]
#replace these with actual team lists before compile
teamList[0] = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'placeholder']
teamList[1] = ['11', '12', '13', '14', '15', '16', '17', '18', '19', '20', 'placeholder']
teamList[2] = ['21', '22', '23', '24', '25', '26', '27', '28', '29', '30', 'placeholder']
teamList[3] = ['31', '32', '33', '34', '35', '36', '37', '38', '39', '40', 'placeholder']
teamList[4] = ['41', '42', '43', '44', '45', '46', '47', '48', '49', '50', 'placeholder']
teamList[5] = ['51', '52', '53', '54', '55', '56', '57', '58', '59', '60', 'placeholder']
teamList[6] = ['61', '62', '63', '64', '65', '66', '67', '68', '69', '70', 'placeholder']
batchList2 = ['1', '2', '3', '4', '5', '6', '7', 'do not select']
positionList = ["Red 1", "Red 2", "Red 3", "Blue 1", "Blue 2", "Blue 3", "placeholder"]
scoutList = ["Default Scout", "New Scout", "Scouts Go", "Here In", "Production Please", "Thank You", "placeholder"]

def testTheValues():
    with open(writeDir / f'{matchNumber2}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([matchNumber2, teamNumber, robotPosition, scoutName])

def drawMainMenu(closeX, closeY, closeW, closeH, startX, startY, startW, startH, logoW, logoH):
    #infinite parameters
    global closeButton
    global matchSelectDrop
    global teamSelectDrop
    closeButton = Button(text="Close", x = closeX*xMult, y = closeY*yMult, width = closeW*xMult, height = closeH*yMult, color = (255, 0, 0), function = exitButton, fontType = 2, rounding = math.trunc(15*xMult))
    startButton = Button(text="Start Match", x = startX*xMult, y = startY*yMult, width = startW*xMult, height = startH*yMult, color = (100, 100, 255), function = startMatchButton, fontType = 3, rounding = math.trunc(50*xMult))
    #check if clicked
    for event in pygame.event.get():
        event2 = event
        closeButton.isClicked(event2)
        startButton.isClicked(event2)
        matchSelectDrop.isClicked(event2)
        matchBatch.isClicked(event2)
        teamSelectDrop.isClicked(event2)
        teamBatch.isClicked(event2)
        positionSelect.isClicked(event2)
        scoutSelect.isClicked(event2)
    #draw the things
    screen.fill((100, 100, 100))
    matchSelectDrop.draw(screen)
    matchBatch.draw(screen)
    teamSelectDrop.draw(screen)
    teamBatch.draw(screen)
    closeButton.draw(screen)
    startButton.draw(screen)
    positionSelect.draw(screen)
    scoutSelect.draw(screen)
    screen.blit(pygame.transform.scale(logo, (logoW*xMult, logoH*yMult)), (0, 0))
    matchSelectDrop.list = matchList[selectedBatch-1]
    teamSelectDrop.list = teamList[selectedBatch2-1]

def initDropsMainMenu(matchX, matchY, matchW, matchH, matchFont):
    #separate function to define dropdowns so you can actually read data from them
    global matchSelectDrop
    global matchBatch
    global selectedBatch
    selectedBatch = 1
    matchSelectDrop = Dropdown(text="Match", x = matchX*xMult, y = matchY*yMult, width = matchW*xMult, height = matchH*yMult, color = (0, 255, 0), function = matchSelector, fontType = matchFont, dropFont = 2, rounding = math.trunc(5*xMult), dropdownAmount = len(matchList[selectedBatch-1])-1, textList = matchList[selectedBatch-1], event=event2)
    matchBatch = Dropdown(text="Match Chunk", x = (matchX+matchW+25)*xMult, y = matchY*yMult, width = matchW*xMult, height = matchH*yMult, color = (0, 255, 0), function = matchBatchSelector, fontType = matchFont, dropFont = 2, rounding = math.trunc(5*xMult), dropdownAmount = len(batchList)-1, textList = batchList, event=event2)
    matchSelectDrop.initDropped()
    matchBatch.initDropped()

def initDropsMainMenu2(teamX, teamY, teamW, teamH, teamFont, positionX, positionY, positionW, positionH, positionFont, scoutX, scoutY, scoutW, scoutH, scoutFont):
    #here to clean up functions
    global selectedBatch2
    global teamBatch
    global positionSelect
    global scoutSelect
    global teamSelectDrop
    event3 = event2
    selectedBatch2 = 1
    teamSelectDrop = Dropdown(text="Team", x = teamX*xMult, y = teamY*yMult, width = teamW*xMult, height = teamH*yMult, color = (0, 255, 0), function = teamSelector, fontType = teamFont, dropFont = 2, rounding = math.trunc(5*xMult), dropdownAmount = len(teamList[selectedBatch2-1])-1, textList = teamList[selectedBatch2-1], event=event2)
    teamBatch = Dropdown(text="Team Chunk", x = (teamX-teamW-25)*xMult, y = teamY*yMult, width = teamW*xMult, height = teamH*yMult, color = (0, 255, 0), function = teamBatchSelector, fontType = teamFont, dropFont = 2, rounding = math.trunc(5*xMult), dropdownAmount = len(batchList2)-1, textList = batchList2, event=event2)
    positionSelect = Dropdown(text="Position", x = positionX*xMult, y = positionY*yMult, width = positionW*xMult, height = positionH*yMult, color = (0, 255, 0), function = positionSelector, fontType = positionFont, dropFont = 2, rounding = math.trunc(5*xMult), dropdownAmount = 6, textList = positionList, event=event2)
    scoutSelect = Dropdown(text="Scout", x = scoutX*xMult, y = scoutY*yMult, width = scoutW*xMult, height = scoutH*yMult, color = (0, 255, 0), function = scoutSelector, fontType = scoutFont, dropFont = 2, rounding = math.trunc(5*xMult), dropdownAmount = len(scoutList)-1, textList = scoutList, event=event2)
    teamSelectDrop.initDropped()
    teamBatch.initDropped()
    positionSelect.initDropped()
    scoutSelect.initDropped()

def drawAutoMenu(fuelX, fuelY, fuelW, fuelH, fuelFont):
    #infinite parameters v2
    global autoFuelPlus1
    global autofuelMinus1
    autoFuelPlus1 = Button(text="+1", x = (fuelX+fuelW+25)*xMult, y = fuelY*yMult, width = fuelW*xMult, height = fuelH*yMult, color = (0, 170, 0), function = autoFuelPlus1Button, fontType = fuelFont, rounding = math.trunc(15*xMult))
    autoFuelMinus1 = Button(text="-1", x = (fuelX-fuelW-25)*xMult, y = fuelY*yMult, width = fuelW*xMult, height = fuelH*yMult, color = (170, 0, 0), function = autoFuelMinus1Button, fontType = fuelFont, rounding = math.trunc(15*xMult))
    #check if clicked v2
    for event in pygame.event.get():
        event2 = event
        autoFuelPlus1.isClicked(event2)
        autoFuelMinus1.isClicked(event2)
    screen.fill((100, 100, 100))
    autoFuelPlus1.draw(screen)
    autoFuelMinus1.draw(screen)
    screen.blit(hugeFont.render(str(autoFuelCount), True, (0, 0, 0)), ((fuelX+(fuelW/3))*xMult, (fuelY+(fuelH/3))*yMult))
    screen.blit(boldFont.render("Auto Fuel Count", True, (0, 0, 0)), ((fuelX-fuelW)*xMult, (fuelY-(fuelH/1.5))*yMult))