import pygame
from math import ceil
from time import time
from random import randint
from copy import copy
from dataclasses import dataclass
#from sys import open

# Initialize pygame modules
pygame.init()

#This will be set later
#pygame.display.set_caption('Sorting Algorithm Animation Generator')
pygame.display.set_caption('Animation Generator for Sorting Algorithms')

try:
    f = open("CUSTOM_RES.txt","r")
    v = f.readline().split(",")
    f.close()
    windowSize = (int(v[1]),int(v[0])+740)
except FileNotFoundError:
    windowSize = (900, 1200)

GUI = None
#screen = pygame.display.set_mode(windowSize)

# Font
baseFont = pygame.font.SysFont('Arial', 24)
smallBaseFont = pygame.font.SysFont('Arial', 14)
screen = None
def init():
    global GUI
    global windowSize
    global screen
    screen = pygame.display.set_mode(windowSize)
    GUI = GUI()

# Used Colors
class Colors:
    grey = (100, 100, 100)
    green = (125, 240, 125)
    white = (255, 255, 255)
    red = (255, 50, 50)
    black = (0, 0, 0)
    blue = (50, 50, 255)
    background = copy(white)#(201, 201, 201)
    text = copy(black)


standard = Colors()
animationColors = Colors()

displayLog = []
displayLog_update = False
def printToMainLog(type,addition):
    global displayLog
    global displayLog_update
    displayLog_update = True
    displayLog.append((type, addition))


def createDisplay(showOrHide):
    #global screen
    # Display settings
    windowSize = (900, 800)
    #screen = pygame.display.set_mode(windowSize,flags=showOrHide)

def updateGroups():
    if randint(0,10) == 5:
        for group in GUI.basicGroup.groups:
            group.update(None)

def try_get_width(buttonTextObject) -> int:
    try:
        int(buttonTextObject.get_width())
    except AttributeError:
        if isinstance(buttonTextObject,int):
            return buttonTextObject
        elif isinstance(buttonTextObject, float):
            return int(buttonTextObject)
    return 1

class Box:
    def __init__(self, rect):
        self.isActive = False
        self.rect = pygame.Rect(rect)
        self.name = "superName"
        self.baseWidth = copy(self.rect.w)
        self.myLabel = None
        self.buttonText = None

    def update(self,event=None):
        self.mousePos = pygame.mouse.get_pos()
        self.clicked = pygame.mouse.get_pressed() != (0, 0, 0)
        self.isActive = True if self.rect.collidepoint(self.mousePos) else False



    def setRect(self,rect):
        self.rect = pygame.Rect(rect)


class sampleSortAnimation(Box):
    def __init__(self, rect):
        super().__init__(rect)
        self.isActive = False
        self.myRed = standard.red
        self.myBlue = standard.blue
        self.myGreen = standard.green
        self.myBase = standard.grey

    def update(self,event=None):
        self.draw()
        return None

    def draw(self):
        global numBars
        global displayValuesInOutput
        #Draw bars, but like with different colors
        array = [15,27,34,51,62,72,89]
        redBar1 = 2
        redBar2 = 5
        blueBar1 = 4
        blueBar2 = 1
        prev_numBars = numBars
        prev_displayValuesInOutput = displayValuesInOutput
        displayValuesInOutput = False
        numBars = len(array)
        pygame.draw.rect(screen,animationColors.background,(self.rect.left,self.rect.y,self.rect.w,self.rect.h))
        drawBars(array, redBar1, redBar2, blueBar1, blueBar2, [],displaySize=(self.rect.w,self.rect.h), leftOffset=self.rect.left,topOffset=self.rect.y)
        numBars = prev_numBars
        displayValuesInOutput = prev_displayValuesInOutput
        return None

class Group:
    groups = []

    def __init__(self,rect,outline,title,objectFormatting,item_collisions,if_different_offset,**myObjects):
        self.title = title
        self.item_collisions = item_collisions
        self.items = list(myObjects.values())
        self.rect = pygame.Rect(rect)
        self.upper_line,self.lower_line,self.fullLines = outline
        self.color = standard.grey
        self.groups.append(self)
        self.objectFormatting = objectFormatting
        self.counter = 0
        if not isinstance(if_different_offset,list):
            self.nextRow = [if_different_offset]
        else:
            self.nextRow = if_different_offset

    def find_rightmost(self):
        most_right = 0
        most_right_index = 0
        for index, item in enumerate(self.items):
            if item.rect.x > most_right:
                most_right_index = index
        return most_right_index
    def find_lowest(self):
        most_low = 0
        most_low_index = 0
        for index, item in enumerate(self.items):
            if item.rect.y > most_low:
                most_low_index = index
        return most_low_index
    def checkIfIncludeLabelInLine(self):
        for item in self.items:
            if hasattr(item, "render_text_on_side") and hasattr(item, "myLabel"):
                if item.render_text_on_side:
                    return True
        return False

    def findMaxLengthOfLabelInLine(self):
        currentMax = 0
        for item in self.items:
            # Guard statements
            if not hasattr(item, "render_text_on_side") or not hasattr(item, "myLabel"):
                continue
            if item.myLabel is None or not item.render_text_on_side:
                continue
            # Actually do calc
            if item.myLabel.get_width() > currentMax:
                currentMax = item.myLabel.get_width()
        return currentMax

    def manageSpacing(self):
        self.counter +=1
        if self.objectFormatting == "Horizontal":
            for element in self.items:
                if not hasattr(element, "baseWidth"):
                    printToMainLog(4,"Element lacks object baseWidth")
                    return
                if element.baseWidth is None:
                    printToMainLog(4, "element.baseWidth = None")
                    return
                if not hasattr(element, "myLabel"):
                    printToMainLog(4, "No attr myLabel")
                    return
                if element.myLabel is None:
                    element.myLabel = baseFont.render("", True, self.color)
                if not hasattr(element, "buttonText"):
                    printToMainLog(4, "No button text element in object")
                    return
                if element.buttonText is None:
                    element.buttonText = baseFont.render("", True, self.color)
            # Find how far left so that buttons line up well, and text does not wrap over line
            # get starting top point
            currentLeft = self.rect.left + self.items[0].myLabel.get_width()/2
            for place, element in enumerate(self.items):
                if element in self.nextRow:
                    element.setRect(((windowSize[0]*(20/900)) + self.items[0].myLabel.get_width()/2, self.rect.y+max(k.rect.height for k in self.items)+(windowSize[1]*(10/900)), element.baseWidth,
                                     element.rect.height))
                else:
                    element.setRect((currentLeft, self.rect.y, element.baseWidth + try_get_width(element.buttonText),element.rect.height))
                if element not in self.item_collisions:
                    currentLeft += max(element.rect.width, element.myLabel.get_width()) + (windowSize[0]*(20/900))

        elif self.objectFormatting == "Vertical":
            for element in self.items:
                if not hasattr(element,"baseWidth"):
                    printToMainLog(4, f"{element.name} lacks object baseWidth")
                    return
                if element.baseWidth is None:
                    printToMainLog(4, f"{element.name}.baseWidth = None")
                    return
                if not hasattr(element,"myLabel"):
                    printToMainLog(4, f"{element.name}=No attr myLabel")
                    return
                if element.myLabel is None:
                    element.myLabel = baseFont.render("", True, self.color)
                    return
                if not hasattr(element,"buttonText"):
                    printToMainLog(4, f"No button text element in {element.name}")
                    return
                if element.buttonText is None:
                    element.buttonText = baseFont.render("", True, self.color)
            # Find how far left so that buttons line up well, and text does not wrap over line
            # get starting top point
            maxLabelWidth = max((k.myLabel.get_width()) for k in self.items)
            maxButtonWidth = max((k.buttonText.get_width() for k in self.items))
            currentTop = self.rect.y
            currentLeft = self.rect.left
            if currentLeft - maxLabelWidth < (20/900)*windowSize[0]:
                currentLeft += maxLabelWidth
            if currentLeft + maxLabelWidth > windowSize[0]:
                currentLeft -= maxLabelWidth
            for place, element in enumerate(self.items):
                if element in self.nextRow:
                    element.setRect((currentLeft+(windowSize[0]*(100/900)) + element.myLabel.get_width() + maxButtonWidth, element.rect.y, element.baseWidth + element.buttonText.get_width(), element.rect.height))
                else:
                    element.setRect((currentLeft, currentTop, element.baseWidth + maxButtonWidth, element.rect.height))
                currentTop += element.rect.height + (windowSize[1]*(10/1200))
                # Place all text 10 pix from left, top = 10px + height + 10px
                # Remember to account for any labels
        else:
            printToMainLog(3,f"Some group ({group.items}) had config for group other than Vertical or Horizontal")
            printToMainLog(3, "This may cause incorrect GUI")

    def findItemsAtSimilarHeight(self):
        myItems = [0]
        for group in self.groups:
            for object in group.items:
                if self.rect.top - 10 < object.rect.top < self.rect.top + 10:
                    myItems.append(object.rect.left)
        return myItems

    def draw(self):
        self.manageSpacing()
        # Guard statement, if neither outline or title requested, then just return
        if self.title == "" and not (self.upper_line or self.lower_line):
            return None
        # Now we know that atleast one time, but maybe twice, these calc will be needed
        #Calculate all positions
        left = min(k.rect.x for k in self.items)
        top = min(k.rect.y for k in self.items)
        # To find eg Width: Find the x value for the item that is furthest right,
        # Then, remove the x value for item that is furthest left
        # Now we have width from start of item furthest left to start of item furthest right,
        # So add width of item furthest right, and now we have total width.
        width = max(k.rect.x for k in self.items) - left + self.items[self.find_rightmost()].rect.w
        height = max(k.rect.y for k in self.items) - top + self.items[self.find_lowest()].rect.h
        offset_height_topside = 20
        offset_height_underside = 10
        offset_width = 30
        if self.title != "":
            label = baseFont.render(self.title, True, self.color)
            screen.blit(label, (left + (width - label.get_width()) / 2, top - 32))
        if self.upper_line or self.lower_line:
            #Draw line around rect
            # If width is large enough, just do entire program width
            if self.fullLines:
                width = screen.get_width() - 8 * offset_width
            if self.checkIfIncludeLabelInLine():
                width += self.findMaxLengthOfLabelInLine()
                left -= self.findMaxLengthOfLabelInLine()
                if left < 40:
                    left = left - offset_width
            if self.upper_line:
                pygame.draw.line(screen,self.color,(left-offset_width,top-offset_height_topside),(left+width-offset_width,top-offset_height_topside),3)
            if self.lower_line:
                pygame.draw.line(screen, self.color, (left - offset_width, top + height + offset_height_underside), (left + width - offset_width, top + height + offset_height_underside), 3)

    def update(self,event):
        return


class ColorSampleRectangle(Box):
    def __init__(self, name, rect, color, outlineColor):
        super().__init__(rect)
        self.name = name
        self.currentColor = color
        self.outlineColor = outlineColor

    def draw(self):
        pygame.draw.rect(screen,self.currentColor,(self.rect.x, self.rect.y, self.rect.w-2, self.rect.h-2), 50)
        pygame.draw.rect(screen, self.outlineColor, self.rect, 3)

    def update(self, event):
        super().update(event)
        self.draw()



class InputBox(Box):
    def __init__(self, name, color, rect, **kwargs):
        super().__init__(rect)
        self.name = name
        self.color = color
        self.myLabel = None
        self.buttonText = None
        self.baseWidth = copy(self.rect.width)
        if kwargs.get("side_text"):
            self.render_text_on_side = kwargs.get("side_text")
        else:
            self.render_text_on_side = False

    def draw(self):
        label = baseFont.render(self.name, True, self.color)
        self.myLabel = label
        if self.render_text_on_side:
            screen.blit(label, (self.rect.x - label.get_width()-10, self.rect.y+(self.rect.height/4)))
        else:
            screen.blit(label, (self.rect.x + (self.rect.w - label.get_width()) / 2, self.rect.y - 32))
        pygame.draw.rect(screen, self.color, self.rect, 3)


class ColorPicker(InputBox):
    combinedColor = pygame.Color(0,0,0)
    def __init__(self, name, rect,cube = None):
        super().__init__("",standard.grey,rect)
        self.rect = pygame.Rect(rect)
        self.rad = self.rect.h // 2
        self.start = self.rect.x
        #self.rect.width = self.rect.x + 255
        self.end = self.rect.x + self.rect.width
        self.value = self.start
        self.isActive = True
        self.color = name
        #self.rect.x = self.rect.x + 20
        if cube is None:
            self.draw_cube = False
        else:
            self.draw_cube = cube

    def draw(self):
        #super().draw()
        if "Red" == self.color:
            center = self.rect.left + (self.rad/2) + (self.value-self.rect.x-7), self.rect.centery
            self.combinedColor.r = self.value-self.rect.x
            pygame.draw.circle(screen, (self.combinedColor.r,0,0), center, self.rect.height // 2.5)
            for i in range(0,254):
                pygame.draw.rect(screen,(i,0,0),(self.rect.x+i,self.rect.y+(self.rect.height/2)-5,10,10),1)
        if "Green" == self.color:
            self.combinedColor.g = self.value - self.rect.x
            center = self.rect.left + (self.rad / 2) + (self.value - self.rect.x - 7), self.rect.centery
            pygame.draw.circle(screen, (0,self.combinedColor.g, 0), center, self.rect.height // 2.5)
            for i in range(254):
                pygame.draw.rect(screen,(0,i,0),(self.rect.x+i,self.rect.y+self.rect.height/2-5,10,10),1)
        if "Blue" == self.color:
            center = self.rect.left + (self.rad / 2) + (self.value - self.rect.x - 7), self.rect.centery
            self.combinedColor.b = self.value - self.rect.x
            pygame.draw.circle(screen, (0,0,self.combinedColor.b), center, self.rect.height // 2.5)
            for i in range(254):
                pygame.draw.rect(screen,(0,0,i),(self.rect.x+i,self.rect.y+self.rect.height/2-5,10,10),1)
        if self.draw_cube:
            pygame.draw.rect(screen,self.combinedColor,(self.rect.x-15,self.rect.y-35,30,30),30)

    def update(self, event):
        super().update(event)
        previousStart = self.start
        self.start = self.rect.x
        self.end = self.rect.x + self.rect.w+4
        self.value += self.start - previousStart
        if self.isActive:
            if self.clicked:
                if self.start <= self.mousePos[0] <= self.end:
                    self.value = self.mousePos[0]

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.value = min(self.value + 10, self.end)
                elif event.button == 5:
                    self.value = max(self.value - 10, self.start)
        self.draw()

class justText(Box):
    def __init__(self, text, color,rect,**kwargs):
        super().__init__(rect)
        self.text = text
        self.color = color
        self.myLabel = None
        self.mySize = 0
        self.myAlg = None
        self.myDelay = 0
        self.printedNoteAboutTableSettings = False
        if kwargs.get("side_text"):
            self.side_text = True
        else:
            self.side_text = False
        self.totalFile = []


    def searchInFile(self,size,alg):
        #Check if list was already read
        # Saving list in memory saves much execution time, and the list is not that long (less than 200 lines of maybe 50chars each right now)
        # In the future, more lines can be added to support more predictions.
        # However, as it stands, generating the table takes like 20 min on a fairly fast machine, if it does any decent avg for each result.
        if len(self.totalFile) > 0:
            # Setting output as > 5000 means that program will display (unknown) upon failure
            resulting_number_of_frames = 5002
            lastFactor = 1000
            for line in self.totalFile:
                line_alg = line[0].split("=")[1]
                line_size = int(line[1].split("=")[1])
                line_result = float(line[2].split("=")[1])
                # if guess is close AND right alg AND new guess is closer than last
                if (alg == line_alg) and (size*0.5 <= line_size <= size * 2) and abs(1-(size/line_size)) < lastFactor:
                    resulting_number_of_frames = line_result * (size/line_size)
                    lastFactor = abs(1-(size/line_size))
                    # Don't break because if we find better than we want to take it
            return resulting_number_of_frames
        else:
            # No text in memory, so do all the stuff and then
            f = open(ANIMATION_TABLE_TIME_ESTIMATE, "r")
            for line in (line.split(",") for line in f.readlines()):
                self.totalFile.append(line)
            f.close()
            # Just run myself again
            # Next time, totalfile will be longer than 0 so code above will run.
            # This reduces risk for mistakes because code is not replicated in multiple places
            return self.searchInFile(size,alg)

    def update(self,event):
        if "Estimated playtime for animation" in self.text:
            # Get value for delay, size, format, alg
            # Check how many frames that usually generates
            size = GUI.sizeBox.get_value()
            alg = GUI.algorithmBox.get_active_option()
            if self.mySize == size and self.myAlg == alg and self.myDelay == delay or size < 10:
                return None
            resulting_number_of_frames = self.searchInFile(size,alg)
            self.mySize = size
            self.myAlg = alg
            self.myDelay = delay
            if resulting_number_of_frames > 5000 or size * 1.1 < resulting_number_of_frames < 0.9*size:
                self.text = f"Estimated playtime for animation: (unknown) sec"
                if not self.printedNoteAboutTableSettings:
                    printToMainLog(4, f"----------------------------------------------------------------------")
                    printToMainLog(4,f"Missing data in table for these settings (or animation will be very long)")
                    printToMainLog(4, f"If you are reading this, feel free to run -new_time_table {size} {alg}")
                    self.printedNoteAboutTableSettings = True
            else:
                self.text = f"Estimated playtime for animation: {round(resulting_number_of_frames/(1000/delay),3)} sec"
            self.draw()

    def draw(self):
        if self.side_text:
            label = baseFont.render(self.text, True, self.color)
            self.myLabel = label
            screen.blit(label, (self.rect.x - label.get_width()-10, self.rect.y+(self.rect.height/4)))
        else:
            label = baseFont.render(self.text, True, self.color)
            self.myLabel = label
            screen.blit(label, (self.rect.x + (self.rect.w - label.get_width()) / 2, self.rect.y - 32))


class BoxWithText(Box):
    def __init__(self, name, rect, text1, text2, myFunction,**kwargs):
        super().__init__(rect)
        self.text1 = text1
        self.text2 = text2
        self.text = text1
        self.name = name
        self.myFunction = myFunction
        # Without storing baseWidth, we risk constantly increasing size of buttons everytime we redraw buttons to fit text
        self.baseWidth = copy(self.rect.width)
        self.myLabel = None
        self.buttonText = None
        if kwargs.get("side_text"):
            self.render_text_on_side = kwargs.get("side_text")
        else:
            self.render_text_on_side = False

    def draw(self):
        # Draw button
        label2 = baseFont.render(self.text, True, standard.grey)
        screen.blit(label2, (self.rect.left+self.rect.width/4, self.rect.y+self.rect.height/4))
        self.buttonText = label2
        pygame.draw.rect(screen, standard.grey, self.rect, 3)
        # Draw explanations text for button
        label = baseFont.render(self.name, True, standard.grey)
        self.myLabel = label
        if self.render_text_on_side:
            screen.blit(label, (self.rect.x - label.get_width()-10, self.rect.y+(self.rect.height/4)))
        else:
            screen.blit(label, (self.rect.x - ((label.get_width() + self.rect.width) / 2), self.rect.y - 32))



    def update(self,event=None):
        global someFactor
        global includeSettingsInOutput
        global displayValuesInOutput
        super().update()
        if self.isActive and self.clicked:
            self.myFunction(self)
            #Switch text
            if self.text == self.text1:
                self.text = self.text2
            else:
                self.text = self.text1
            self.draw()

def softint(value):
    try:
        return int(value)
    except ValueError:
        return 0

class TextBox(InputBox):
    def __init__(self, name, color, rect, text='100'):
        super().__init__(name, color, rect)
        self.text = text
        self.buttonText = None
        #self.draw()  # establish the correct width for initial rendering

    def draw(self):
        super().draw()
        if self.text != "":
            displayedText = baseFont.render(self.text, True, self.color)
            self.buttonText = displayedText
            screen.blit(displayedText, (self.rect.x + 10, self.rect.y + 10))

    def update(self, event):
        super().update()
        if self.name == "Loops" and self.text == "0":
            self.text = "Inf"
        else:
            if self.isActive and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.unicode.isdigit() and softint(self.text) < 10000:
                    self.text += event.unicode

    def get_value(self):
        if self.name == "Loops" and self.text == "Inf":
            return 0
        else:
            return softint(self.text)

class SlideBox(InputBox):
    def __init__(self, name, color, rect):
        super().__init__(name, color, rect)
        self.start = self.rect.x + 6
        self.end = self.rect.x + self.rect.w - 6
        self.value = self.start + 100
        self.myLabel = None
        self.myText = None

    def draw(self):
        super().draw()
        pygame.draw.line(screen, self.color, (self.start, self.rect.y + 25), (self.end, self.rect.y + 25), 2)
        pygame.draw.line(screen, self.color, (self.value, self.rect.y + 5), (self.value, self.rect.y + 45), 12)

    def update(self, event):
        global someFactor
        global delay
        previousStart = self.start
        self.start = self.rect.x + 6
        self.end = self.rect.x + self.rect.w - 6
        self.value += self.start - previousStart
        if "Delay" in self.name:
            delay = ((self.value-self.start) * someFactor)+1
            self.name = "Delay:" + str(round((self.value-self.start) * someFactor,5)+1) + "ms"
        super().update()
        if self.isActive:
            if self.clicked:
                if self.start <= self.mousePos[0] <= self.end: self.value = self.mousePos[0]

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.value = min(self.value + 10, self.end)
                elif event.button == 5:
                    self.value = max(self.value - 10, self.start)


class VerticalSliderBox(InputBox):
    def __init__(self, name, color, rect):
        super().__init__(name, color, rect)
        self.start = self.rect.y + 6
        self.end = self.rect.y + self.rect.h
        self.value = self.start
        self.isActive = True

    def draw(self):
        x = self.rect.x
        pygame.draw.line(screen, standard.grey, (x, self.start - 6), (x, self.end), 25)
        pygame.draw.line(screen, standard.white, (x + 5, self.value), (x + 5, self.value + 20), 8)

    def update(self, event):
        super().update()
        previousStart = self.start
        self.start = self.rect.y + 6
        self.end = self.rect.y + self.rect.h
        self.value += self.start - previousStart
        if self.isActive:
            if self.clicked:
                if self.start <= self.mousePos[1] <= self.end: self.value = self.mousePos[1]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.value = min(self.end, self.value + 10)
                elif event.button == 5:
                    self.value = max(self.start, self.value - 10)


class ButtonBox(Box):
    def __init__(self, img_path, rect, myFunction="start_stop_generation"):
        super().__init__(rect)
        self.img = pygame.image.load(img_path)
        self.myFunction = myFunction
        self.baseWidth = copy(self.rect.width)
        self.myLabel = None
        self.buttonText = None

    def draw(self):
        screen.blit(self.img, (self.rect.x, self.rect.y))

    def update(self,event=None):
        global screen
        global show_advanced
        global windowSize
        super().update()
        if True:
            if self.isActive: self.isActive = True if self.clicked else False


class CheckBox(Box):
    checked = False
    image1 = None
    image2 = None
    myText = None

    def __init__(self, img_path, img_path2, option_text, rect):
        super().__init__(rect)
        self.img = pygame.image.load(img_path)
        self.myText = option_text
        self.image1 = img_path  # Save the different pictures for switching later
        self.image2 = img_path2

    def draw(self):
        mySurface = baseFont.render(self.myText, True, standard.grey)
        screen.blit(mySurface, (self.rect.x - 20, self.rect.y - 30))
        if self.checked:
            # Draw checked box
            self.img = pygame.image.load(self.image2)
        else:
            # Draw unchecked box
            self.img = pygame.image.load(self.image1)
        screen.blit(self.img, (self.rect.x, self.rect.y))

    def update(self,event=None):
        super().update()
        if self.isActive: self.isActive = True if self.clicked else False
        if self.isActive:
            self.checked = not self.checked

    # Switch between checked & unchecked image
    def switch(self):
        self.checked = not self.checked
        self.draw()


class DropdownBox(InputBox):

    def __init__(self, name, rect, font, color,side_text):
        super().__init__(name, color, rect, side_text=side_text)
        self.isActive = False
        self.font = font
        self.options_color = standard.white
        self.active_option = -1
        self.options = None
        self.DEFAUTL_OPTION = 0
        self.options_text_obj = [(-1,pygame.Rect(0,0,0,0)) for k in range(100)]
        self.columns = 0
    def setTextLength(self):
        self.options_text_obj.clear()
        maxWidth = 0
        for i,option in enumerate(self.options):
            option_text = baseFont.render(option[:12], 1, standard.grey)
            if option_text.get_width() > maxWidth:
                maxWidth = option_text.get_width()
                self.buttonText = option_text
            self.options_text_obj.append((option_text,pygame.Rect(0,0,0,0)))

    def add_options(self, options):
        self.options = options
        self.setTextLength()
        self.columns = ceil(len(options)/10)


    def get_active_option(self):
        return self.options[self.DEFAUTL_OPTION]

    def draw(self):
        super().draw()
        option_text = self.font.render(self.options[self.DEFAUTL_OPTION], 1, standard.grey)
        screen.blit(option_text, option_text.get_rect(center=self.rect.center))
        if self.isActive:
            column = 0 if self.name == "Output Format" else -0.5
            index = 0
            rect_start = self.rect.y - self.rect.height
            for i in range(self.DEFAUTL_OPTION + 1, len(self.options)):
                rect = self.rect.copy()
                rect.y -= (index + 1) * self.rect.height
                rect.x = self.rect.x + (column * self.rect.width)
                if rect.y <= 10:
                    column += 1
                    index = 0
                    rect.y = rect_start
                index += 1


                options_color = standard.black if i - 1 == self.active_option else standard.grey
                pygame.draw.rect(screen, self.options_color, rect, 0)
                pygame.draw.rect(screen, self.color, rect, 3)  # draw border
                option_text = self.font.render(self.options[i][:12], 1, options_color)
                self.options_text_obj[i] = (option_text,rect)
                screen.blit(option_text, option_text.get_rect(center=rect.center))

    def checkCollision(self,mouse_position):
        for i,(object,rect) in enumerate(self.options_text_obj):
            if rect.collidepoint(mouse_position):
                return True
        return False

    def update(self,event=None):
        mouse_position = pygame.mouse.get_pos()
        column = 0 if self.name == "Output Format" else -0.5
        index = 0
        rect_start = self.rect.y - self.rect.height
        for i in range(len(self.options) - 1):
            rect = self.rect.copy()
            rect.y -= (index + 1) * self.rect.height
            rect.x = self.rect.x + column * self.rect.width
            if rect.y <= 10:
                column += 1
                index = 0
                rect.y = rect_start
            index += 1

            if rect.collidepoint(mouse_position):
                self.active_option = i

        if pygame.mouse.get_pressed() != (0, 0, 0):
            if self.checkCollision(mouse_position):
                self.options[self.DEFAUTL_OPTION], self.options[self.active_option + 1] = \
                    self.options[self.active_option + 1], self.options[self.DEFAUTL_OPTION]
                self.active_option = -1
            self.isActive = self.rect.collidepoint(mouse_position)
        if not self.isActive:
            self.active_option = -1


# Button specific functions
def delayX10BoxFunction(self):
    global someFactor
    if someFactor == 1:
        someFactor = 10
    else:
        someFactor = 1
    GUI.delayBox.update(None)

def includeSettingsInOutputBoxFunction(self):
    global includeSettingsInOutput
    if includeSettingsInOutput:
        includeSettingsInOutput = False
    else:
        includeSettingsInOutput = True

def showValueInBarsBox(self):
    global displayValuesInOutput
    if displayValuesInOutput:
        displayValuesInOutput = False
    else:
        displayValuesInOutput = True


def blueBarsColorBoxFunction(self):
    if self.text == "Set":
        animationColors.blue = copy(GUI.P1_colorPickerBox.combinedColor)
    else:
        animationColors.blue = standard.blue
    GUI.preview_colors.update(None)
    GUI.blueBarsColorSample.currentColor = animationColors.blue

def redBarsColorBoxFunction(self):
    if self.text == "Set":
        animationColors.red = copy(GUI.P1_colorPickerBox.combinedColor)
    else:
        animationColors.red = standard.red
    GUI.preview_colors.update(None)
    GUI.RedBarsColorSample.currentColor = animationColors.red

def greenBarsColorBoxFunction(self):
    if self.text == "Set":
        animationColors.green = copy(GUI.P1_colorPickerBox.combinedColor)
    else:
        animationColors.green = standard.green
    GUI.preview_colors.update(None)
    GUI.greenBarsColorSample.currentColor = animationColors.green

def baseBarsColorBoxFunction(self):
    if self.text == "Set":
        animationColors.grey = copy(GUI.P1_colorPickerBox.combinedColor)
    else:
        animationColors.grey = standard.grey
    GUI.preview_colors.update(None)
    GUI.BaseBarsColorSample.currentColor = animationColors.grey

def backgroundColorBoxFunction(self):
    if self.text == "Set":
        animationColors.background = copy(GUI.P1_colorPickerBox.combinedColor)
    else:
        animationColors.background = standard.background
    GUI.preview_colors.update(None)
    GUI.backBarsColorSample.currentColor = animationColors.background

def textInBarsColorBoxFunction(self):
    if self.text == "Set":
        animationColors.text = copy(GUI.P1_colorPickerBox.combinedColor)
    else:
        animationColors.text = standard.black
    GUI.preview_colors.update(None)
    GUI.textBarsColorSample.currentColor = animationColors.text

# Global Settings - used for animation generation
numBars = 0
do_sorting = False
timer_space_bar = 0
# Global Settings - used for determining with what settings to render animations
someFactor = 1
includeSettingsInOutput = False
displayValuesInOutput = False
delay = 100
show_advanced = False
ANIMATION_TABLE_TIME_ESTIMATE = "animationTimeEstimate.txt"

# Input Boxes
# To add new box, simply add one line below and then add ref to ListOfAllBoxes append call below
# If type is ButtonBox like for playButton or stopButton, look at function updateWidgets & drawBottomMenu
# because they are special

# Also, some types of buttons, eg BoxWithText, require a function at the end to call when button is pressed.
# Usually, this will be called nameOfbuttonFunction(self) and take an object as input
# If nothing should happen when pressing the button, simply do "return None"
# The function that is passed when creating the button below will be called automatically with itself as an argument
# Define all rect elements in terms of windowsize percentage
@dataclass
class GUI:
    width,height = windowSize
    ListOfAllGUIElements = []
    # Basic group
    sizeBox = TextBox('Size', standard.grey, (int((30/900)*width), int((500/1200)*height), 50, 50), '20')
    loopBox = TextBox('Loops', standard.grey, (int((580/900)*width), int((500/1200)*height), 50, 50), 'Inf')
    delayBox = SlideBox("Delay:" + "100" + "ms", standard.grey, (int((105/900)*width), int((500/1200)*height), 300, 50))
    algorithmBox = DropdownBox('Algorithm', (int((410/900)*width), int((500/1200)*height), 140, 50), baseFont, standard.grey, side_text=None)
    playButton = ButtonBox('res/playButton.png', (int((800/900)*width), int((500/1200)*height),50, 50))
    stopButton = ButtonBox('res/stopButton.png', (int((800/900)*width), int((500/1200)*height),50, 50))
    # Advanced group
    delayX10Box = BoxWithText("Increase delay", (int((100/900)*width), int(((620+50*0)/900)*width), 60, 50), "x10", "x1", delayX10BoxFunction,side_text=True)
    includeSettingsInOutputBox = BoxWithText("GUI in output", (int(((100/900)/900)*width), int((620+50*1/1200)*height), 95, 50), "Include", "Exclude", includeSettingsInOutputBoxFunction,side_text=True)
    showValueInBarsBox = BoxWithText("Display value in bars", (int(((100/900)/900)*width), int(((620+50*1)/1200)*height), 95, 50), "Include", "Exclude", showValueInBarsBox,side_text=True)
    outputFormatBox = DropdownBox('Output Format', (int((700/900)*width), int((500/1200)*height), 140, 50), baseFont, standard.grey,side_text=True)


    #Color picking - sliders
    P1_colorPickerBox = ColorPicker("Red",(int((600/900)*width), int(((850+30*0)/1200)*height), 255, 30),True)
    P2_colorPickerBox = ColorPicker("Blue",(int((600/900)*width), int(((850+30*1)/1200)*height),255, 30))
    P3_colorPickerBox = ColorPicker("Green",(int((600/900)*width), int(((850+30*2)/1200)*height), 255, 30))
    # Color picking - set/reset buttons
    BlueBarsColorBox = BoxWithText("Blue bars",(int((160/900)*width),int(((820+60*0)/1200)*height),50,50),"Set","Reset",blueBarsColorBoxFunction,side_text=True)
    RedBarsColorBox = BoxWithText("Red bars",(int((160/900)*width),int(((820+60*1)/1200)*height),50,50),"Set","Reset",redBarsColorBoxFunction,side_text=True)
    greenBarsColorBox = BoxWithText("Green bars",(int((160/900)*width),int(((820+60*2)/1200)*height),50,50),"Set","Reset",greenBarsColorBoxFunction,side_text=True)
    BaseBarsColorBox = BoxWithText("Normal bars",(int((160/900)*width),int(((820+60*3)/1200)*height),50,50),"Set","Reset",baseBarsColorBoxFunction,side_text=True)
    textInBarsColorBox = BoxWithText("Text in bars",(int((160/900)*width),int(((820+60*4)/1200)*height),50,50),"Set","Reset",textInBarsColorBoxFunction,side_text=True)
    backgroundColorBox = BoxWithText("Background",(int((160/900)*width),int(((820+60*5)/1200)*height),50,50),"Set","Reset",backgroundColorBoxFunction,side_text=True)
    # Color picking - set/reset color sample rectangles
    blueBarsColorSample = ColorSampleRectangle(name="blueBars", rect=(int((160/900)*width),int(((830+60*0)/1200)*height), 20, 20),color=animationColors.blue,outlineColor=standard.black)
    RedBarsColorSample = ColorSampleRectangle(name="redBars", rect=(int((160 / 900) * width), int(((830 + 60 * 1) / 1200) * height), 20, 20), color=standard.red,outlineColor=standard.black)
    greenBarsColorSample = ColorSampleRectangle(name="greenBars", rect=(int((160 / 900) * width), int(((830 + 60 * 2) / 1200) * height), 20, 20), color=standard.green,outlineColor=standard.black)
    BaseBarsColorSample = ColorSampleRectangle(name="baseBars", rect=(int((160 / 900) * width), int(((830 + 60 * 3) / 1200) * height), 20, 20), color=standard.grey,outlineColor=standard.black)
    textBarsColorSample = ColorSampleRectangle(name="textBars", rect=(int((160 / 900) * width), int(((830 + 60 * 4) / 1200) * height), 20, 20), color=standard.black,outlineColor=standard.black)
    backBarsColorSample = ColorSampleRectangle(name="backBars", rect=(int((160 / 900) * width), int(((830 + 60 * 5) / 1200) * height), 20, 20), color=standard.white,outlineColor=standard.black)
    #Sample animation for choosing color - included in slidersColorGroup
    preview_colors = sampleSortAnimation((int((600/900)*width),int(((850+30*4-10)/1200)*height), 255,90))

    # Text data group - only exists for displaying data
    estimatedAnimationTimeBox = justText(f"Estimated playtime for animation: sec",standard.grey,(int((450/900)*width), int((1100/1200)*height), 140, 50))

    #Groups
    # Very important, objects must be in order!
    # if not, things will not be scaled correctly
    # Outline order is: Render upper line (t/f), Render lower line (t/f), Should line cover entire width of program? (t/f)
    advancedGroup = Group((int((100/900)*width),int((600/1200)*height),int((0/900)*width),int((50/1200)*height)),(True,True,True),title="",objectFormatting="Vertical",item_collisions = [],if_different_offset=outputFormatBox,a = delayX10Box,b = includeSettingsInOutputBox,c = showValueInBarsBox,d=outputFormatBox)
    slidersColorGroup = Group((int((600/900)*width),int((850/1200)*height),int((255/900)*width),int((30/1200)*height)),(False,True,False),title = "RGB color selector",objectFormatting="Vertical",item_collisions = [],if_different_offset=None,a = P1_colorPickerBox,b = P2_colorPickerBox,c = P3_colorPickerBox,d = preview_colors)
    setResetColorGroup = Group((int((50/900)*width),int((820/1200)*height),int((50/900)*width),int((50/1200)*height)),(False,False,False), title = "Color for",objectFormatting="Vertical",item_collisions = [],if_different_offset=[blueBarsColorSample,RedBarsColorSample,greenBarsColorSample,BaseBarsColorSample,textBarsColorSample,backBarsColorSample],
                               a = BlueBarsColorBox, b = RedBarsColorBox,c = greenBarsColorBox, d = BaseBarsColorBox, e = textInBarsColorBox, f = backgroundColorBox,g = blueBarsColorSample,h = RedBarsColorSample,j = greenBarsColorSample,k = BaseBarsColorSample,l = textBarsColorSample,m = backBarsColorSample)
    basicGroup = Group((int((30/900)*width),int((510/1200)*height),int((50/900)*width),int((50/1200)*height)),(False,False,False),title="",objectFormatting="Horizontal",item_collisions = [playButton,stopButton],if_different_offset=None,a = sizeBox,b = loopBox,c = delayBox,d = algorithmBox,e=playButton,f=stopButton)
    textDataGroup = Group((int((450/900)*width),int((1150/1200)*height),int((140/900)*width),int((50/1200)*height)), (False,False,False), title="", objectFormatting="Vertical", item_collisions = [], if_different_offset=None, a = estimatedAnimationTimeBox)


    #Add ref to all elements in list.
    ListOfAllGUIElements.extend([sizeBox, loopBox, delayBox, algorithmBox, playButton, stopButton,
                           delayX10Box, includeSettingsInOutputBox, showValueInBarsBox, outputFormatBox,
                           P1_colorPickerBox,P2_colorPickerBox,P3_colorPickerBox,advancedGroup,
                           slidersColorGroup,preview_colors,BlueBarsColorBox,RedBarsColorBox,BaseBarsColorBox,
                           textInBarsColorBox,backgroundColorBox,setResetColorGroup,greenBarsColorBox,basicGroup,
                           estimatedAnimationTimeBox,blueBarsColorSample,RedBarsColorSample,greenBarsColorSample,
                           BaseBarsColorSample,textBarsColorSample,backBarsColorSample,textDataGroup])
def updateWidgets(event):
    # Instead of looping
    for aBox in GUI.ListOfAllGUIElements:
        # We have to skip stop & start button bc they are special
        if not isinstance(aBox,ButtonBox):
            aBox.update(event)
    #Stop & start button are specials
    if do_sorting:
        GUI.stopButton.update()
    else:
        GUI.playButton.update()

def drawText(myText,myColor,rect):
    rect = pygame.Rect(rect)
    label = smallBaseFont.render(myText, True, myColor)
    screen.blit(label, (rect.x - (label.get_width() / 2), rect.y - 32))


def drawBars(array, redBar1, redBar2, blueBar1, blueBar2, greenRows,displaySize,**kwargs):
    global displayValuesInOutput
    global windowSize
    global numBars
    #if displaySize is None:
    #    displaySize = (windowSize[0],430)
    width,height = displaySize
    '''Draw the bars and control their colors'''
    numBars = len(array)
    if len(array) != 0:
        bar_width = float(width) / len(array)
        ceil_width = ceil(bar_width)
        #ceil_width = bar_width
    #Check for special colors
    for num in range(0,len(array)):
        if num in (redBar1, redBar2):
            color = animationColors.red
        elif num in (blueBar1, blueBar2):
            color = animationColors.blue
        elif num in greenRows:
            color = animationColors.green
        else:
            color = animationColors.grey
        if displayValuesInOutput and numBars < 20 and do_sorting:
            top = (height - array[num]) + 15
            drawText(str(array[num]),animationColors.text,((num * bar_width) + bar_width/2,top,ceil_width/2,30))
        if kwargs.get("leftOffset") and kwargs.get("topOffset"):
            pygame.draw.rect(screen, color, (kwargs.get("leftOffset") + (num * bar_width), kwargs.get("topOffset") + (height - array[num]), ceil_width, array[num]))
        else:
            pygame.draw.rect(screen, color, (num * bar_width, height - array[num], ceil_width, array[num]))



def drawBottomMenu():
    '''Draw the menu below the bars'''
    for aBox in GUI.ListOfAllGUIElements:
        # We have to skip stop & start button bc they are special
        if not isinstance(aBox,ButtonBox):
            aBox.draw()
    if do_sorting:
        GUI.stopButton.draw()
    else:
        GUI.playButton.draw()


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


def draw_polygon_alpha(surface, color, points):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
    surface.blit(shape_surf, target_rect)


def drawInterface(array, redBar1, redBar2, blueBar1, blueBar2,greenRows,displaySize, **kwargs):
    '''Draw all the interface'''
    # This if statement gives user option to select background color for animation
    if do_sorting:
        screen.fill(animationColors.background)
    else:
        screen.fill(standard.white)
    drawBars(array, redBar1, redBar2, blueBar1, blueBar2,greenRows,displaySize)

    if (time() - timer_space_bar) < 0.1:
        x, y = (850 / 2), 150
        draw_polygon_alpha(screen, (150, 255, 150, 127),
                           ((x + 10, y + 10), (x + 10, y + 50 + 10), (x + 50, y + 25 + 10)))
    drawBottomMenu()
    pygame.display.update()


