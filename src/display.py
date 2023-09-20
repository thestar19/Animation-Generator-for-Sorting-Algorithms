import pygame
from math import ceil
from time import time
from random import randint
from copy import copy

# Initialize pygame modules
pygame.init()

#This will be set later
#pygame.display.set_caption('Sorting Algorithm Animation Generator')
pygame.display.set_caption('Animation Generator for Sorting Algorithms')

windowSize = (900, 1200)
screen = pygame.display.set_mode(windowSize)

# Font
baseFont = pygame.font.SysFont('Arial', 24)
smallBaseFont = pygame.font.SysFont('Arial', 14)


# Used Colors
class Colors:
    grey = (100, 100, 100)
    green = (125, 240, 125)
    white = (255, 255, 255)
    red = (255, 50, 50)
    black = (0, 0, 0)
    blue = (50, 50, 255)


standard = Colors()
animationColors = Colors()

def createDisplay(showOrHide):
    #global screen
    # Display settings
    windowSize = (900, 800)
    #screen = pygame.display.set_mode(windowSize,flags=showOrHide)

class Box:
    def __init__(self, rect):
        self.isActive = False
        self.rect = pygame.Rect(rect)

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
        self.rect = pygame.Rect(rect)
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
        drawBars(array, redBar1, redBar2, blueBar1, blueBar2, displaySize=(self.rect.h,self.rect.w), leftOffset=self.rect.left,topOffset=self.rect.y, redBar_override_color=self.myRed,blueBar_override_color=self.myBlue,greenRows_override_color=self.myGreen,base_override_color=self.myBase)
        numBars = prev_numBars
        displayValuesInOutput = prev_displayValuesInOutput
        return None

class Group:
    groups = []
    def __init__(self,outline=None,title=None,**myObjects):
        if outline is None:
            outline = (False,False)
        if title is None:
            title = ""
        self.title = title
        self.items = list(myObjects.values())
        self.upper_line,self.lower_line = outline
        self.color = standard.grey
        self.groups.append(self)

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
    def draw(self):
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
        offset_height_topside = 40
        offset_height_underside = 10
        offset_width = 30
        if self.title != "":
            label = baseFont.render(self.title, True, self.color)
            screen.blit(label, (left + (width - label.get_width()) / 2, top - 32))
        if self.upper_line or self.lower_line:
            #Draw line around rect
            # If width is large enough, just do entire program width
            if width > 400:
                width = screen.get_width() - 4 * offset_width
            if self.upper_line:
                pygame.draw.line(screen,self.color,(left-offset_width,top-offset_height_topside),(left+width+offset_width,top-offset_height_topside),3)
            if self.lower_line:
                pygame.draw.line(screen, self.color, (left - offset_width, top + height + offset_height_underside), (left + width + offset_width, top + height + offset_height_underside), 3)
    def update(self,event):
        return None

class InputBox(Box):
    def __init__(self, name, color, rect):
        super().__init__(rect)
        self.name = name
        self.color = color

    def draw(self):
        label = baseFont.render(self.name, True, self.color)
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
                pygame.draw.rect(screen,(i,0,0),(self.rect.x+i,self.rect.y+self.rect.height/2-5,10,10),1)
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
    def __init__(self, text, color,rect):
        super().__init__(rect)
        self.text = text
        self.color = color


    def draw(self):
        label = baseFont.render(self.text, True, self.color)
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
        self.baseWidth = self.rect.width

        if kwargs.get("side_text"):
            self.render_text_on_side = kwargs.get("side_text")
        else:
            self.render_text_on_side = False

    def draw(self):
        # Draw button
        label2 = baseFont.render(self.text, True, standard.grey)
        screen.blit(label2, (self.rect.left+self.baseWidth/2, self.rect.y+self.rect.height/4))
        self.setRect((self.rect.left, self.rect.top, self.baseWidth + (label2.get_width()), self.rect.height))
        pygame.draw.rect(screen, standard.grey, self.rect, 3)
        # Draw explanations text for button
        label = baseFont.render(self.name, True, standard.grey)
        if self.render_text_on_side:
            screen.blit(label, (self.rect.x - label.get_width()-10, self.rect.y+(self.rect.height/4)))
        else:
            screen.blit(label, (self.rect.x + (self.rect.w - label.get_width()) / 2, self.rect.y - 32))



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


class TextBox(InputBox):
    def __init__(self, name, color, rect, text='100'):
        super().__init__(name, color, rect)
        self.text = text
        #self.draw()  # establish the correct width for initial rendering

    def draw(self):
        super().draw()
        if self.name == "Log":
            surface = baseFont.render(self.text, True, self.color)
            screen.blit(surface, (self.rect.x + 10, self.rect.y + 10))
        else:
            surface = baseFont.render(self.text, True, self.color)
            screen.blit(surface, (self.rect.x + 10, self.rect.y + 10))
            self.rect.w = max(surface.get_width() + 20, 50)

    def update(self, event):
        super().update()
        if self.name == "Loops" and self.text == "0":
            self.text = "Inf"
        else:
            if self.isActive and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.unicode.isdigit():
                    self.text += event.unicode

    def get_value(self):
        if self.name == "Loops" and self.text == "Inf":
            return 0
        else:
            return int(self.text)

class SlideBox(InputBox):
    def __init__(self, name, color, rect):
        super().__init__(name, color, rect)
        self.start = self.rect.x + 6
        self.end = self.rect.x + self.rect.w - 6
        self.value = self.start

    def draw(self):
        super().draw()
        pygame.draw.line(screen, self.color, (self.start, self.rect.y + 25), (self.end, self.rect.y + 25), 2)
        pygame.draw.line(screen, self.color, (self.value, self.rect.y + 5), (self.value, self.rect.y + 45), 12)

    def update(self, event):
        global someFactor
        global delay
        super().update()
        previousStart = self.start
        self.rect.x = sizeBox.rect.x + sizeBox.rect.w + 20
        self.start = self.rect.x + 6
        self.end = self.rect.x + self.rect.w - 6
        self.value += self.start - previousStart
        if "Delay" in self.name:
            delay = ((self.value-self.start) * someFactor)+1
            self.name = "Delay:" + str(((self.value-self.start) * someFactor)+1) + "ms"
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

    def draw(self):
        if self.myFunction == "start_stop_generation":
            self.rect.x = loopBox.rect.x + loopBox.rect.w + 20
        else:
            self.rect.x = playButton.rect.x + playButton.rect.w + 20
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
        self.rect.x = playButton.rect.x + playButton.rect.w + 30
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
    DEFAUTL_OPTION = 0

    def __init__(self, name, rect, font, color,buddyToLeft):
        super().__init__(name, color, rect)
        self.isActive = False
        self.font = font
        self.options_color = standard.white
        self.active_option = -1
        self.buddyToLeft = buddyToLeft
        self.options = None

    def add_options(self, options):
        self.options = options
        dropdown_width = ceil((len(self.options) - 1) * self.rect.height / self.rect.y) * self.rect.width
        self.dropdown_rect = pygame.Rect((self.rect.x, 0, dropdown_width, self.rect.y))

    def get_active_option(self):
        return self.options[self.DEFAUTL_OPTION]

    def draw(self):
        super().draw()
        option_text = self.font.render(self.options[self.DEFAUTL_OPTION], 1, standard.grey)
        screen.blit(option_text, option_text.get_rect(center=self.rect.center))

        if self.isActive:
            column = 0
            index = 0
            rect_start = self.rect.y - self.rect.height
            for i in range(self.DEFAUTL_OPTION + 1, len(self.options)):
                rect = self.rect.copy()
                rect.y -= (index + 1) * self.rect.height
                if rect.y <= self.dropdown_rect.y:
                    column += 1
                    index = 0
                    rect.y = rect_start
                index += 1
                rect.x = self.rect.x + column * self.rect.width

                options_color = standard.black if i - 1 == self.active_option else standard.grey
                pygame.draw.rect(screen, self.options_color, rect, 0)
                pygame.draw.rect(screen, self.color, rect, 3)  # draw border
                option_text = self.font.render(self.options[i][:12], 1, options_color)
                screen.blit(option_text, option_text.get_rect(center=rect.center))

    def update(self,event=None):
        if self.buddyToLeft:
            self.rect.x = self.buddyToLeft.rect.w + self.buddyToLeft.rect.x + 20
        mouse_position = pygame.mouse.get_pos()
        column = 0
        index = 0
        rect_start = self.rect.y - self.rect.height
        for i in range(len(self.options) - 1):
            rect = self.rect.copy()
            rect.y -= (index + 1) * self.rect.height
            if rect.y <= self.dropdown_rect.y:
                column += 1
                index = 0
                rect.y = rect_start
            index += 1
            rect.x = self.rect.x + column * self.rect.width

            if rect.collidepoint(mouse_position):
                self.active_option = i

        if pygame.mouse.get_pressed() != (0, 0, 0):
            if self.isActive and self.dropdown_rect.collidepoint(mouse_position):
                self.options[self.DEFAUTL_OPTION], self.options[self.active_option + 1] = \
                    self.options[self.active_option + 1], self.options[self.DEFAUTL_OPTION]
                self.active_option = -1
            self.isActive = self.rect.collidepoint(mouse_position)
        if not self.isActive:
            self.active_option = -1


# Button specific functions
def delayX10BoxFunction(self):
    global someFactor
    global delayBox
    if someFactor == 1:
        someFactor = 10
    else:
        someFactor = 1
    delayBox.update(None)

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


def BlueBarsColorBoxFunction(self):
    global P1_colorPickerBox
    global preview_colors
    if self.text == "Set":
        animationColors.blue = copy(P1_colorPickerBox.combinedColor)
    else:
        animationColors.blue = standard.blue
    preview_colors.update(None)
def RedBarsColorBoxFunction(self):
    global P1_colorPickerBox
    global preview_colors
    if self.text == "Set":
        animationColors.red = copy(P1_colorPickerBox.combinedColor)
    else:
        animationColors.red = standard.red
    preview_colors.update(None)
def BaseBarsColorBoxFunction(self):
    global P1_colorPickerBox
    global preview_colors
    if self.text == "Set":
        animationColors.grey = copy(P1_colorPickerBox.combinedColor)
    else:
        animationColors.grey = standard.grey
    preview_colors.update(None)

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

# Input Boxes
# To add new box, simply add one line below and then add ref to ListOfAllBoxes append call below
# If type is ButtonBox like for playButton or stopButton, look at function updateWidgets & drawBottomMenu
# because they are special

# Also, some types of buttons, eg BoxWithText, require a function at the end to call when button is pressed.
# Usually, this will be called nameOfbuttonFunction(self) and take an object as input
# If nothing should happen when pressing the button, simply do "return None"
# The function that is passed when creating the button below will be called automatically with itself as an argument
ListOfAllBoxes = []
sizeBox = TextBox('Size', standard.grey, (30, 500, 50, 50), '10')
loopBox = TextBox('Loops', standard.grey, (580, 500, 50, 50), 'Inf')
delayBox = SlideBox("Delay:" + "100" + "ms", standard.grey, (105, 500, 300, 50))
algorithmBox = DropdownBox('Algorithm', (410, 500, 140, 50), baseFont, standard.grey, delayBox)
playButton = ButtonBox('res/playButton.png', (800, 500, 50, 50))
stopButton = ButtonBox('res/stopButton.png', (800, 500, 50, 50))
advancedText = justText("--------------------------------Advanced options--------------------------------", standard.grey,
                        (400, 560, 100, 50))
delayX10Box = BoxWithText("Increase delay", (60, 620, 60, 50), "x10", "x1", delayX10BoxFunction)
includeSettingsInOutputBox = BoxWithText("Include settings in Animation", (250, 620, 95, 50), "Include", "Exclude", includeSettingsInOutputBoxFunction)
showValueInBarsBox = BoxWithText("Output values in bars", (510, 620, 95, 50), "Include", "Exclude", showValueInBarsBox)
outputFormatBox = DropdownBox('Output Format', (60, 720, 220, 50), baseFont, standard.grey,None)

#Color picking
P1_colorPickerBox = ColorPicker("Red",(600, 850+30*0, 255, 30),True)
P2_colorPickerBox = ColorPicker("Blue",(600, 850+30*1, 255, 30))
P3_colorPickerBox = ColorPicker("Green",(600, 850+30*2, 255, 30))
BlueBarsColorBox = BoxWithText("Color blue bars:",(210,800+60*0,50,50),"Set","Reset",BlueBarsColorBoxFunction,side_text=True)
RedBarsColorBox = BoxWithText("Color red bars:",(210,800+60*1,50,50),"Set","Reset",RedBarsColorBoxFunction,side_text=True)
BaseBarsColorBox = BoxWithText("Color base bars:",(210,800+60*2,50,50),"Set","Reset",BaseBarsColorBoxFunction,side_text=True)

#Groups
# Very important, objects must be in order!
# if not, things will not be scaled correctly
AdvancedGroup = Group((True,True),a = delayX10Box,b = includeSettingsInOutputBox,c = showValueInBarsBox,d = outputFormatBox)
ColorGroup = Group((False,True),title = "RGB color selector",a = P1_colorPickerBox,b = P2_colorPickerBox,c = P3_colorPickerBox)

#Sample animation for choosing color
preview_colors = sampleSortAnimation((600,720,280,350))

#Add ref to all elements in list.
ListOfAllBoxes.extend([sizeBox, loopBox, delayBox, algorithmBox, playButton, stopButton, \
                       delayX10Box, includeSettingsInOutputBox, showValueInBarsBox, outputFormatBox, \
                       P1_colorPickerBox,P2_colorPickerBox,P3_colorPickerBox,AdvancedGroup,ColorGroup,preview_colors, \
                       BlueBarsColorBox,RedBarsColorBox,BaseBarsColorBox])
def updateWidgets(event):
    global ListOfAllBoxes
    # Instead of looping
    for aBox in ListOfAllBoxes:
        # We have to skip stop & start button bc they are special
        if type(aBox) != ButtonBox:
            aBox.update(event)
    #Stop & start button are specials
    if do_sorting:
        stopButton.update()
    else:
        playButton.update()

def drawText(myText,myColor,rect):
    rect = pygame.Rect(rect)
    label = smallBaseFont.render(myText, True, myColor)
    screen.blit(label, (rect.x - (label.get_width() / 2), rect.y - 32))


def drawBars(array, redBar1, redBar2, blueBar1, blueBar2, greenRows={},displaySize=None, **kwargs):
    global displayValuesInOutput
    global windowSize
    if displaySize is None:
        displaySize = (430,900)
    height,width = displaySize
    '''Draw the bars and control their colors'''
    if numBars != 0:
        bar_width = float(width) / numBars
        ceil_width = ceil(bar_width)
        #ceil_width = bar_width
    #Check for special colors
    for num in range(0,numBars):
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
            #if 360 < (width - array[num]):
            #    top = (width - array[num]) - 30
            #else:
                #top = (width - array[num]) + 40
            drawText(str(array[num]),standard.black,((num * bar_width) + bar_width/2,top,ceil_width/2,30))
        if kwargs.get("leftOffset") and kwargs.get("topOffset"):
            pygame.draw.rect(screen, color, (kwargs.get("leftOffset") + (num * bar_width), kwargs.get("topOffset") + (height - array[num]*1.2), ceil_width, array[num]*1.2))
        else:
            pygame.draw.rect(screen, color, (num * bar_width, 30 + height - array[num], ceil_width, array[num]))
        #Maybe draw text



def drawBottomMenu():
    '''Draw the menu below the bars'''
    global ListOfAllBoxes
    for aBox in ListOfAllBoxes:
        # We have to skip stop & start button bc they are special
        if type(aBox) != ButtonBox:
            aBox.draw()
    if do_sorting:
        stopButton.draw()
    else:
        playButton.draw()


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


def drawInterface(array, redBar1, redBar2, blueBar1, blueBar2, **kwargs):
    '''Draw all the interface'''
    screen.fill(standard.white)
    drawBars(array, redBar1, redBar2, blueBar1, blueBar2, **kwargs)

    if (time() - timer_space_bar) < 0.1:
        x, y = (850 / 2), 150
        draw_polygon_alpha(screen, (150, 255, 150, 127),
                           ((x + 10, y + 10), (x + 10, y + 50 + 10), (x + 50, y + 25 + 10)))

    drawBottomMenu()
    pygame.display.update()


