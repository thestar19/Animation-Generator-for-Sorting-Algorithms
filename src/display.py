import pygame
from math import ceil
from time import time
from random import randint

# Initialize pygame modules
pygame.init()

# Display settings
windowSize = (900, 800)
screen = pygame.display.set_mode(windowSize)

#pygame.display.set_caption('Sorting Algorithm Animation Generator')
pygame.display.set_caption('Sorting Algorithm GIF Generator')

# Font
baseFont = pygame.font.SysFont('Arial', 24)
smallBaseFont = pygame.font.SysFont('Arial', 14)

# Used Colors
grey = (100, 100, 100)
green = (125, 240, 125)
white = (250, 250, 250)
red = (255, 50, 50)
black = (0, 0, 0)
blue = (50, 50, 255)



class Box:
    def __init__(self, rect):
        self.isActive = False
        self.rect = pygame.Rect(rect)

    def update(self,event=None):
        self.mousePos = pygame.mouse.get_pos()
        self.clicked = pygame.mouse.get_pressed() != (0, 0, 0)
        self.isActive = True if self.rect.collidepoint(self.mousePos) else False


class justText(Box):
    def __init__(self, text, color,rect):
        super().__init__(rect)
        self.text = text
        self.color = color


    def draw(self):
        label = baseFont.render(self.text, True, self.color)
        screen.blit(label, (self.rect.x + (self.rect.w - label.get_width()) / 2, self.rect.y - 32))


class BoxWithText(Box):
    def __init__(self, name, rect, text1, text2=""):
        super().__init__(rect)
        self.text1 = text1
        self.text2 = text2
        self.text = text1
        self.name = name

    def draw(self):
        # Draw button
        surface = baseFont.render(self.text, True, grey)
        screen.blit(surface, (self.rect.x + 10, self.rect.y + 10))
        # Draw txt above
        label = baseFont.render(self.name, True, grey)
        screen.blit(label, (self.rect.x + (self.rect.w - label.get_width()) / 2, self.rect.y - 32))
        pygame.draw.rect(screen, grey, self.rect, 3)

    def update(self,event=None):
        global someFactor
        global includeSettingsInOutput
        global displayValuesInOutput
        super().update()
        if self.isActive and self.clicked:
            if len(self.text2) > 0:
                if self.text == self.text1:
                    self.text = self.text2
                    if self.name == delayX10Box.name:
                        someFactor = 10
                        delayBox.update(None)
                    if self.name == includeSettingsInGifBox.name: includeSettingsInOutput = True
                    if self.name == showValueInBarsBox.name: displayValuesInOutput = True

                else:
                    self.text = self.text1
                    if self.name == delayX10Box.name:
                        someFactor = 1
                        delayBox.update(None)
                    if self.name == includeSettingsInGifBox.name: includeSettingsInOutput = False
                    if self.name == showValueInBarsBox.name: displayValuesInOutput = False


class InputBox(Box):
    def __init__(self, name, color, rect):
        super().__init__(rect)
        self.name = name
        self.color = color

    def draw(self):
        label = baseFont.render(self.name, True, self.color)
        screen.blit(label, (self.rect.x + (self.rect.w - label.get_width()) / 2, self.rect.y - 32))
        pygame.draw.rect(screen, self.color, self.rect, 3)


class TextBox(InputBox):
    def __init__(self, name, color, rect, text='100'):
        super().__init__(name, color, rect)
        self.text = text
        self.draw()  # establish the correct width for initial rendering

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
        pygame.draw.line(screen, grey, (x, self.start - 6), (x, self.end), 25)
        pygame.draw.line(screen, white, (x + 5, self.value), (x + 5, self.value + 20), 8)

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
        mySurface = baseFont.render(self.myText, True, grey)
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
        self.options_color = white
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
        option_text = self.font.render(self.options[self.DEFAUTL_OPTION], 1, grey)
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

                options_color = black if i - 1 == self.active_option else grey
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


# END OF MODULE #


# Global Settings
numBars = 0
delay = 100
do_sorting = False
show_advanced = False
paused = False
timer_space_bar = 0
someFactor = 1
includeSettingsInOutput = False
displayValuesInOutput = False

# Input Boxes
# To add new box, simply add one line below and then the ref to ListOfAllBoxes append call below
# If type is ButtonBox like for playButton or stopButton, look at function updateWidgets & drawBottomMenu
# because they are special
ListOfAllBoxes = []
sizeBox = TextBox('Size', grey, (30, 440, 50, 50), '10')
loopBox = TextBox('Loops', grey, (580, 440, 50, 50), 'Inf')
delayBox = SlideBox("Delay:" + "100" + "ms", grey, (105, 440, 300, 50))
algorithmBox = DropdownBox('Algorithm', (410, 440, 140, 50), baseFont,grey,delayBox)
playButton = ButtonBox('res/playButton.png', (800, 440, 50, 50))
stopButton = ButtonBox('res/stopButton.png', (800, 440, 50, 50))
advancedText = justText("--------------------------------Advanced options--------------------------------", grey,
                        (400, 560, 100, 50))
delayX10Box = BoxWithText("Increase delay", (60, 620, 60, 50), "x10", "x1")
includeSettingsInGifBox = BoxWithText("Include settings in GIF", (250, 620, 95, 50), "Include", "Exclude")
showValueInBarsBox = BoxWithText("Display values in bar", (510, 620, 95, 50), "Include", "Exclude")
outputFormatBox = DropdownBox('Output Format', (60, 720, 220, 50), baseFont,grey,None)


#Add ref to all elements in list.
ListOfAllBoxes.extend([sizeBox,loopBox,delayBox,algorithmBox,playButton,stopButton,advancedText, \
                      delayX10Box,includeSettingsInGifBox,showValueInBarsBox,outputFormatBox])
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


def drawBars(array, redBar1, redBar2, blueBar1, blueBar2, greenRows={}, **kwargs):
    global displayValuesInOutput
    '''Draw the bars and control their colors'''
    if numBars != 0:
        bar_width = 900 / numBars
        ceil_width = ceil(bar_width)
    for num in range(numBars):
        if num in (redBar1, redBar2):
            color = red
        elif num in (blueBar1, blueBar2):
            color = blue
        elif num in greenRows:
            color = green
        else:
            color = grey
        pygame.draw.rect(screen, color, (num * bar_width, 400 - array[num], ceil_width, array[num]))
        #Maybe draw text
        if displayValuesInOutput and numBars < 20 and do_sorting:
            top = (400 - array[num])
            if 360 < (400 - array[num]):
                top = (400 - array[num]) - 30
            else:
                top = (400 - array[num]) + 40
            drawText(str(array[num]),black,((num * bar_width) + bar_width/2,top,ceil_width/2,30))


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
    screen.fill(white)
    drawBars(array, redBar1, redBar2, blueBar1, blueBar2, **kwargs)

    if paused and (time() - timer_space_bar) < 0.5:
        draw_rect_alpha(screen, (255, 255, 0, 127), [(850 / 2) + 10, 150 + 10, 10, 50])
        draw_rect_alpha(screen, (255, 255, 0, 127), [(850 / 2) + 40, 150 + 10, 10, 50])

    elif not paused and (time() - timer_space_bar) < 0.2:
        x, y = (850 / 2), 150
        draw_polygon_alpha(screen, (150, 255, 150, 127),
                           ((x + 10, y + 10), (x + 10, y + 50 + 10), (x + 50, y + 25 + 10)))

    drawBottomMenu()
    pygame.display.update()


