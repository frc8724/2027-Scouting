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
    if 'ANDROID_ARGUMENT' in os.environ:
        # workaround that (should) get rid of the title bar.
        screen = pygame.display.set_mode((x2, y2), pygame.FULLSCREEN)
    else:
        # for windows/linux, causes a borderless fullscreen effect.
        screen = pygame.display.set_mode((x2, y2))

#pygame setup for windows, android takes whatever is in buildozer.spec for captions
clock = pygame.time.Clock()
pygame.display.set_caption("Scouting App")

# initial setup so initDrops<menu>() functions don't fail. 
global event2
for event in pygame.event.get():
    event2 = event

# font sizes/image loads
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
# 3 = tele-op

#also call at beginning of GUI code to get the dir to write to!!
def getWriteDir():
    #directory for android/Windows
    global writeDir
    global configFile
    if 'ANDROID_ARGUMENT' in os.environ:
        # Android, writes to /storage/emulated/0/Documents/FRC_Scouting_Output on most devics.
        writeDir = Path(os.environ['EXTERNAL_STORAGE']) / 'Documents' / 'FRC_Scouting_Output'
        #setup config file
        configFile = Path("/data/data/org.frc8724.scouting/files/app/config.txt")
    else:
        # Desktop, writes to C:/Users/<your name>/FRC_Scouting_Output on Windows and ~/FRC_Scouting_Output on Linux.
        writeDir = Path.home() / 'FRC_Scouting_Output'
        configFile = Path.home() / 'FRC_Scouting_Output' / 'config.txt'

    if configFile.is_file():
        theme = int(configFile.read_text().strip())
    else:
        # usually first run
        with open(configFile, "w") as f:
            f.write("1")
        theme = int(configFile.read_text().strip())

    writeDir.mkdir(parents=True, exist_ok=True)

#yes, the dropdown system relies on dictionaries (in dictionaries). however, it is quite optimized!
global dropRect
dropRect = {}
global rect
rect = {}
global fonts
fonts = {}
global checks
# checkbox states are stored in a dictionary for ease-of-access
checks = {}
global themes
themes = {}

#default values for saving, required to not crash when saving before selecting values and display "buttons".
matchNumber2 = "none"
teamNumber = "none"
robotPosition = "none"
scoutName = "John Doe"
global autoFuelCount
autoFuelCount = 0
global autoSwipesCount
autoSwipesCount = 0
towerLevel = 0
robotPos = 'none'
autoWinner = 'none'

# define colors *once* for ease-of-use in adding new elements. also the default theme
global BLACK
global WHITE
global RED
global BLUE
global DARKRED
global GREEN
global DARKGREEN
global DARKERGREEN
global GRAY
BLACK = (0, 0, 0)
WHITE  = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (100, 100, 255)
DARKRED = (170, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 170, 0)
DARKERGREEN = (0, 150, 0)
GRAY = (100, 100, 100)

def fontDef(fontVar, fontType, passedText="well that's not great"):
    #necessary for optimization; makes it so the fonts (at least for buttons and checkboxes) are only defined on startup and not every frame.
    if fontType == 1:
        variable = smallFont.render(passedText, True, BLACK)
    elif fontType == 2:
        variable = bigFont.render(passedText, True, BLACK)
    elif fontType == 3:
        variable = hugeFont.render(passedText, True, BLACK)
    elif fontType == 4:
        variable = smallFont.render(passedText, True, WHITE)
    elif fontType == 5:
        variable = bigFont.render(passedText, True, WHITE)
    elif fontType == 6:
        variable = hugeFont.render(passedText, True, WHITE)
    elif fontType == 7:
        variable = boldFont.render(passedText, True, BLACK)
    elif fontType == 8:
        variable = boldFont.render(passedText, True, WHITE)
    else:
        variable = bigFont.render(passedText, True, BLACK)
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
                rect[self.text] = pygame.Rect(self.x, self.y, self.width, self.height)
                dropRect[self.text][self.list[z-1]] = pygame.Rect(self.x, self.y+self.height*z, self.width, self.height)
            else:
                #draw just the one button
                rect[self.text] = pygame.Rect(self.x, self.y, self.width, self.height)
            #FOOOOOOOOONTSSSS
            if self.font == 1:
                self.textRenderOG = smallFont.render(self.text, True, BLACK)
            elif self.font == 2:
                self.textRenderOG = bigFont.render(self.text, True, BLACK)
            elif self.font == 3:
                self.textRenderOG = hugeFont.render(self.text, True, BLACK)
            elif self.font == 4:
                self.textRenderOG = smallFont.render(self.text, True, WHITE)
            elif self.font == 5:
                self.textRenderOG = bigFont.render(self.text, True, WHITE)
            elif self.font == 6:
                self.textRenderOG = hugeFont.render(self.text, True, WHITE)
            elif self.font == 7:
                self.textRenderOG = boldFont.render(self.text, True, BLACK)
            elif self.font == 8:
                self.textRenderOG = boldFont.render(self.text, True, WHITE)
            else:
                self.textRenderOG = bigFont.render(self.text, True, BLACK)
            if self.dropFont == 1:
                self.textRenderDrop = smallFont.render(self.list[z-1], True, BLACK)
            elif self.dropFont == 2:
                self.textRenderDrop = bigFont.render(self.list[z-1], True, BLACK)
            elif self.dropFont == 3:
                self.textRenderDrop = hugeFont.render(self.list[z-1], True, BLACK)
            elif self.dropFont == 4:
                self.textRenderDrop = smallFont.render(self.list[z-1], True, WHITE)
            elif self.dropFont == 5:
                self.textRenderDrop = bigFont.render(self.list[z-1], True, WHITE)
            elif self.dropFont == 6:
                self.textRenderDrop = hugeFont.render(self.list[z-1], True, WHITE)
            elif self.dropFont == 7:
                self.textRenderDrop = boldFont.render(self.list[z-1], True, BLACK)
            elif self.dropFont == 8:
                self.textRenderDrop = boldFont.render(self.list[z-1], True, WHITE)
            else:
                self.textRenderDrop = bigFont.render(self.list[z-1], True, BLACK)
            #self.render the text and draw the boxes
            self.textRender2 = self.textRenderOG.get_rect(center=rect[self.text].center)
            pygame.draw.rect(surface, self.color, rect[self.text], border_radius=self.rounding)
            surface.blit(self.textRenderOG, self.textRender2)
            if self.dropped == 1:
                #separate fonts on the dropped vs. undropped boxes
                self.textRender3 = self.textRenderDrop.get_rect(center=dropRect[self.text][self.list[z-1]].center)
                pygame.draw.rect(surface, self.color, dropRect[self.text][self.list[z-1]], border_radius=self.rounding)
                surface.blit(self.textRenderDrop, self.textRender3)
                if self.event.type == pygame.MOUSEBUTTONDOWN and self.event.button == 1:
                    #check click events for the dropped boxes
                    if dropRect[self.text][self.amount].collidepoint(self.event.pos):
                        self.function()

    def isClicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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

class Checkbox:
    def __init__(self, x, y, width, height, color, clickedColor, dictId, rounding, text, fontType):
        # get vars
        self.color = color
        self.color2 = clickedColor
        self.id = dictId
        checks[self.id] = 0
        self.rect = pygame.Rect(x, y, width, height)
        self.rounding = rounding
        self.text = text
        # absolutely the silliest piece of code in this project.
        # it fakes a rect object that is never drawn to get the correct text positioning on the label.
        self.fakeRect = pygame.Rect(math.trunc(x+(width*2)), y, width, height)

        fontDef(f'{dictId}Box', fontType, self.text)
        self.textRender = fonts[f'{dictId}Box'].get_rect(center=self.fakeRect.center)

    def draw(self, surface):
        if checks[self.id] == 0:
            # not checked
            pygame.draw.rect(surface, self.color, self.rect, border_radius=self.rounding)
        elif checks[self.id] == 1:
            # checked
            pygame.draw.rect(surface, self.color2, self.rect, border_radius=self.rounding)
        surface.blit(fonts[f'{self.id}Box'], self.textRender)

    def isClicked(self, event):
        #see if it is clicked
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                # flip state of checkbox
                if checks[self.id] == 0:
                    checks[self.id] = 1
                elif checks[self.id] == 1:
                    checks[self.id] = 0


def exitButton():
    #bye
    pygame.quit()
    sys.exit()

def startMatchButton():
    # functional currently
    print("match started")
    global menuNumber
    if matchNumber2 != "none" and teamNumber != "none" and robotPosition != "none" and scoutName != "John Doe":
        #make sure to select the values!!
        menuNumber = 2
    else:
        # yes, it's only visible in the terminal.
        print("Select all values first.")

def matchSelector():
    global matchNumber2
    # this bypass only works because the function is called mid-draw by the dropdown, specifically the sub-frame that has the button that was clicked as the latest thing drawn.
    # this is required because the dropdown object's draw() function is destructive to the data that's not being currently rendered.
    # ' '.join() is to strip the dictionary label off.
    if ' '.join(dropRect["Match"]) == 'placeholder':
        pass
    else:
        matchNumber2 = ' '.join(dropRect["Match"])
        matchSelectDrop.dropped = 0
        displayMatch.text = f'Match {matchNumber2}'

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
    if autoFuelCount >= 1:
        # check so that the counter can't go below 0
        autoFuelCount -= 1
    else:
        pass

def autoSwipesPlus1Button():
    global autoSwipesCount
    autoSwipesCount += 1

def autoSwipesMinus1Button():
    global autoSwipesCount
    if autoSwipesCount >= 1:
        # check so that the counter can't go below 0
        autoSwipesCount -= 1
    else:
        pass

def towerLevelSelect():
    # pretty self-explanitory code
    global towerLevel
    if ' '.join(dropRect["Tower Level"]) == 'placeholder':
        pass
    else:
        try:
            towerLevel = int(' '.join(dropRect["Tower Level"]))
            towerSelect.dropped = 0
        except Exception as e:
            pass

def robotPosSelect():
    global robotPos
    if ' '.join(dropRect["Start Position"]) == 'placeholder':
        pass
    else:
        robotPos = ' '.join(dropRect["Start Position"])
        robotStart.dropped = 0

def autoWinnerSelect():
    global autoWinner
    if ' '.join(dropRect["Winning Alliance"]) == 'placeholder':
        pass
    else:
        autoWinner = ' '.join(dropRect["Winning Alliance"])
        autoWinnerSelect.dropped = 0

def startTeleopButton():
    print("teleop started")
    global menuNumber
    if robotPos != "none" and autoWinner != "none":
        #make sure to select the values!!
        menuNumber = 3
    else:
        # yes, it's only visible in the terminal.
        print("Select all values first.")

def empty():
    #for static "display" buttons that need to have a function assigned to them, but shouldn't do anything when clicked.
    pass

#define allllllllllllll the lists
# 'placeholder' values at the end are there for checking if the click was to drop it down or actually clicking a dropdown object.
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
towerList = ['1', '2', '3', 'placeholder']
startPositions = ['Left Trench', 'Left Bump', "Hub", 'Right Bump', 'Right Trench', 'placeholder']
winnerList = ['Red', 'Blue', 'Tie', "placeholder"]

def testTheValues():
    with open(writeDir / f'{matchNumber2}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([matchNumber2, teamNumber, robotPosition, scoutName])

def drawMainMenu(closeX, closeY, closeW, closeH, startX, startY, startW, startH, logoW, logoH, displayX, displayY, displayW, displayH):
    #infinite parameters
    global closeButton
    global matchSelectDrop
    global teamSelectDrop
    global displayMatch
    global displayTeam
    global displayScout
    global displayPosition
    closeButton = Button(text="Close", x = closeX*xMult, y = closeY*yMult, width = closeW*xMult, height = closeH*yMult, color = RED, function = exitButton, fontType = 2, rounding = math.trunc(15*xMult))
    startButton = Button(text="Start Match", x = startX*xMult, y = startY*yMult, width = startW*xMult, height = startH*yMult, color = BLUE, function = startMatchButton, fontType = 3, rounding = math.trunc(50*xMult))
    # "display" buttons that do nothing because the dropdowns can update any text on-screen *except* its own
    displayMatch = Button(text=f'Match: {matchNumber2}', x = displayX*xMult, y = displayY*yMult, width = displayW*xMult, height = displayH*yMult, color = DARKERGREEN, function = empty, fontType = 2, rounding = math.trunc(15*xMult))
    displayTeam = Button(text=f'Team #: {teamNumber}', x = (displayX+(displayW*2)+50)*xMult, y = displayY*yMult, width = displayW*xMult, height = displayH*yMult, color = DARKERGREEN, function = empty, fontType = 2, rounding = math.trunc(15*xMult))
    displayScout = Button(text=f'Scout: {scoutName}', x = (displayX+(displayW*3)+75)*xMult, y = displayY*yMult, width = displayW*xMult, height = displayH*yMult, color = DARKERGREEN, function = empty, fontType = 2, rounding = math.trunc(15*xMult))
    displayPosition = Button(text=f'Position: {robotPosition}', x = (displayX+displayW+25)*xMult, y = displayY*yMult, width = displayW*xMult, height = displayH*yMult, color = DARKERGREEN, function = empty, fontType = 2, rounding = math.trunc(15*xMult))
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
    screen.fill(GRAY)
    matchSelectDrop.draw(screen)
    matchBatch.draw(screen)
    teamSelectDrop.draw(screen)
    teamBatch.draw(screen)
    closeButton.draw(screen)
    startButton.draw(screen)
    positionSelect.draw(screen)
    scoutSelect.draw(screen)
    displayMatch.draw(screen)
    displayTeam.draw(screen)
    displayScout.draw(screen)
    displayPosition.draw(screen)
    screen.blit(pygame.transform.scale(logo, (logoW*xMult, logoH*yMult)), (0, 0))
    matchSelectDrop.list = matchList[selectedBatch-1]
    teamSelectDrop.list = teamList[selectedBatch2-1]

def initDropsMainMenu(matchX, matchY, matchW, matchH, matchFont):
    #separate function to define dropdowns so you can actually read data from them
    global matchSelectDrop
    global matchBatch
    global selectedBatch
    selectedBatch = 1
    matchSelectDrop = Dropdown(text="Match", x = matchX*xMult, y = matchY*yMult, width = matchW*xMult, height = matchH*yMult, color = GREEN, function = matchSelector, fontType = matchFont, dropFont = 2, rounding = math.trunc(5*xMult), dropdownAmount = len(matchList[selectedBatch-1])-1, textList = matchList[selectedBatch-1], event=event2)
    matchBatch = Dropdown(text="Match Chunk", x = (matchX+matchW+25)*xMult, y = matchY*yMult, width = matchW*xMult, height = matchH*yMult, color = GREEN, function = matchBatchSelector, fontType = matchFont, dropFont = 2, rounding = math.trunc(5*xMult), dropdownAmount = len(batchList)-1, textList = batchList, event=event2)
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
    teamSelectDrop = Dropdown(text="Team", x = teamX*xMult, y = teamY*yMult, width = teamW*xMult, height = teamH*yMult, color = GREEN, function = teamSelector, fontType = teamFont, dropFont = 2, rounding = math.trunc(5*xMult), dropdownAmount = len(teamList[selectedBatch2-1])-1, textList = teamList[selectedBatch2-1], event=event2)
    teamBatch = Dropdown(text="Team Chunk", x = (teamX-teamW-25)*xMult, y = teamY*yMult, width = teamW*xMult, height = teamH*yMult, color = GREEN, function = teamBatchSelector, fontType = teamFont, dropFont = 2, rounding = math.trunc(5*xMult), dropdownAmount = len(batchList2)-1, textList = batchList2, event=event2)
    positionSelect = Dropdown(text="Position", x = positionX*xMult, y = positionY*yMult, width = positionW*xMult, height = positionH*yMult, color = GREEN, function = positionSelector, fontType = positionFont, dropFont = 2, rounding = math.trunc(5*xMult), dropdownAmount = 6, textList = positionList, event=event2)
    scoutSelect = Dropdown(text="Scout", x = scoutX*xMult, y = scoutY*yMult, width = scoutW*xMult, height = scoutH*yMult, color = GREEN, function = scoutSelector, fontType = scoutFont, dropFont = 2, rounding = math.trunc(5*xMult), dropdownAmount = len(scoutList)-1, textList = scoutList, event=event2)
    teamSelectDrop.initDropped()
    teamBatch.initDropped()
    positionSelect.initDropped()
    scoutSelect.initDropped()

def initDropsAutoMenu(towerX, towerY, towerW, towerH, towerFont, startX, startY, startW, startH, startFont, winnerX, winnerY, winnerW, winnerH, winnerFont):
    global towerSelect
    global towerCheck
    global robotStart
    global autoWinnerSelect
    robotStart = Dropdown(text="Start Position", x = startX*xMult, y = startY*yMult, width = startW*xMult, height = startH*yMult, color = GREEN, function = robotPosSelect, fontType = startFont, dropFont = startFont, rounding = math.trunc(5*xMult), dropdownAmount = 5, textList = startPositions, event=event2)
    towerCheck = Checkbox(x=towerX*xMult, y=(towerY-(towerH/2))*yMult, width=(towerW/3)*xMult, height=(towerH/3)*yMult, color=WHITE, clickedColor=BLACK, dictId='tower', rounding=15, text='Climber?', fontType=3)
    towerSelect = Dropdown(text="Tower Level", x = towerX*xMult, y = towerY*yMult, width = towerW*xMult, height = towerH*yMult, color = GREEN, function = towerLevelSelect, fontType = towerFont, dropFont = 3, rounding = math.trunc(5*xMult), dropdownAmount = len(towerList)-1, textList = towerList, event=event2)
    autoWinnerSelect = Dropdown(text="Winning Alliance", x = winnerX*xMult, y = winnerY*yMult, width = winnerW*xMult, height = winnerH*yMult, color = GREEN, function = autoWinnerSelect, fontType = winnerFont, dropFont = 3, rounding = math.trunc(5*xMult), dropdownAmount = 3, textList = winnerList, event=event2)
    towerSelect.initDropped()
    robotStart.initDropped()
    autoWinnerSelect.initDropped()

def drawAutoMenu(fuelX, fuelY, fuelW, fuelH, fuelFont, displayX, displayY, displayW, displayH, nextX, nextY, nextW, nextH):
    #infinite parameters v2
    global autoFuelPlus1
    global autofuelMinus1
    global displayStart
    global displayLevel
    autoFuelPlus1 = Button(text="+1", x = (fuelX+fuelW+25)*xMult, y = fuelY*yMult, width = fuelW*xMult, height = fuelH*yMult, color = DARKGREEN, function = autoFuelPlus1Button, fontType = fuelFont, rounding = math.trunc(15*xMult))
    autoFuelMinus1 = Button(text="-1", x = (fuelX-fuelW-25)*xMult, y = fuelY*yMult, width = fuelW*xMult, height = fuelH*yMult, color = DARKRED, function = autoFuelMinus1Button, fontType = fuelFont, rounding = math.trunc(15*xMult))
    autoSwipesPlus1 = Button(text="+1", x = (fuelX+fuelW+25)*xMult, y = (fuelY+fuelH+50)*yMult, width = fuelW*xMult, height = fuelH*yMult, color = DARKGREEN, function = autoSwipesPlus1Button, fontType = fuelFont, rounding = math.trunc(15*xMult))
    autoSwipesMinus1 = Button(text="-1", x = (fuelX-fuelW-25)*xMult, y = (fuelY+fuelH+50)*yMult, width = fuelW*xMult, height = fuelH*yMult, color = DARKRED, function = autoSwipesMinus1Button, fontType = fuelFont, rounding = math.trunc(15*xMult))
    displayLevel = Button(text=f'Tower Level: {towerLevel}', x = displayX*xMult, y = displayY*yMult, width = displayW*xMult, height = displayH*yMult, color = DARKERGREEN, function = empty, fontType = 2, rounding = math.trunc(15*xMult))
    displayStart = Button(text=f'Starting Position: {robotPos}', x = (displayX+(displayW)+25)*xMult, y = displayY*yMult, width = displayW*xMult, height = displayH*yMult, color = DARKERGREEN, function = empty, fontType = 2, rounding = math.trunc(15*xMult))
    displayWinner = Button(text=f'Winning Alliance: {autoWinner}', x = (displayX+(displayW*2)+50)*xMult, y = displayY*yMult, width = displayW*xMult, height = displayH*yMult, color = DARKERGREEN, function = empty, fontType = 2, rounding = math.trunc(15*xMult))
    startTeleop = Button(text="Start tele-op", x = nextX*xMult, y = nextY*yMult, width = nextW*xMult, height = nextH*yMult, color = BLUE, function = startTeleopButton, fontType = 3, rounding = math.trunc(50*xMult))
   
    #check if clicked v2
    for event in pygame.event.get():
        event2 = event
        autoFuelPlus1.isClicked(event2)
        autoFuelMinus1.isClicked(event2)
        autoSwipesPlus1.isClicked(event2)
        autoSwipesMinus1.isClicked(event2)
        towerSelect.isClicked(event2)
        closeButton.isClicked(event2)
        towerCheck.isClicked(event2)
        robotStart.isClicked(event2)
        autoWinnerSelect.isClicked(event2)
        startTeleop.isClicked(event2)

    screen.fill(GRAY)
    autoFuelPlus1.draw(screen)
    autoFuelMinus1.draw(screen)
    autoSwipesPlus1.draw(screen)
    autoSwipesMinus1.draw(screen)
    towerSelect.draw(screen)
    closeButton.draw(screen)
    towerCheck.draw(screen)
    robotStart.draw(screen)
    displayLevel.draw(screen)
    displayStart.draw(screen)
    autoWinnerSelect.draw(screen)
    displayWinner.draw(screen)
    startTeleop.draw(screen)
    screen.blit(hugeFont.render(str(autoFuelCount), True, BLACK), ((fuelX+(fuelW/3))*xMult, (fuelY+(fuelH/3))*yMult))
    screen.blit(boldFont.render("Auto Fuel Count", True, BLACK), ((fuelX-(fuelW/2))*xMult, (fuelY-fuelH/2)*yMult))
    screen.blit(hugeFont.render(str(autoSwipesCount), True, BLACK), ((fuelX+(fuelW/3))*xMult, ((fuelY+(fuelH/3))+fuelH+50)*yMult))
    screen.blit(boldFont.render("Auto Cycles Count", True, BLACK), ((fuelX-(fuelW/1.75))*xMult, ((fuelY-fuelH/2)+fuelH+50)*yMult))

def drawTeleopMenu(fuelX, fuelY, fuelW, fuelH, fuelFont, displayX, displayY, displayW, displayH, nextX, nextY, nextW, nextH):
    #infinite parameters v3
    global autoFuelPlus1
    global autofuelMinus1
    teleFuelPlus1 = Button(text="+1", x = (fuelX+fuelW+25)*xMult, y = fuelY*yMult, width = fuelW*xMult, height = fuelH*yMult, color = DARKGREEN, function = teleFuelPlus1Button, fontType = fuelFont, rounding = math.trunc(15*xMult))
    teleFuelMinus1 = Button(text="-1", x = (fuelX-fuelW-25)*xMult, y = fuelY*yMult, width = fuelW*xMult, height = fuelH*yMult, color = DARKRED, function = teleFuelMinus1Button, fontType = fuelFont, rounding = math.trunc(15*xMult))
    
    # check if clicked v3
    for event in pygame.event.get():
        event2 = event
        teleFuelPlus1.isClicked(event2)
        teleFuelMinus1.isClicked(event2)

    screen.fill(GRAY)
    teleFuelPlus1.draw(screen)
    teleFuelMinus1.draw(screen)
    screen.blit(hugeFont.render(str(autoFuelCount), True, BLACK), ((fuelX+(fuelW/3))*xMult, (fuelY+(fuelH/3))*yMult))
    screen.blit(boldFont.render("Auto Fuel Count", True, BLACK), ((fuelX-(fuelW/2))*xMult, (fuelY-fuelH/2)*yMult))