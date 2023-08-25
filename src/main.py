import sys

#Define basic trace_function
def show_trace(event=""):
    print("An error has occured, printing useful info:")
    print(sys.version)
    print(sys.version_info)
    print(event)
    sys.exit(0)

#Carefully import stuff
try:
    from random import randint
    from time import time
    from algs import algorithmsDict
    import display as display
    from os import rmdir, walk, getcwd, system, mkdir, remove
    from gc import collect
    import imageio.v3
    import pygame
except ImportError:
    show_trace()


#Global variables
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

textLog = []
textLogUpdate = True
DEBUG = False

#printL types:
# 1 = normal log message
# 2 = reserved for progress indication
# 3 = Warning message
# 4 = Reserved for debug use

#Generating gifs requires placing files in subfolder and then loading them.
#This deletes everything except gif
def deleteTempFiles():
    try:
        myFiles = []
        myDir = []
        for pathnames,dirnames,filenames in walk("pictures"):
            myFiles.extend(filenames)
            myDir.extend(dirnames)
        for files in myFiles:
            remove("pictures/" + files)
        for directories in myDir:
            rmdir("pictures/" + directories)
    except:
        raise EIO("Could not delete files in subfolder!")

# For some uses, having an existing sorting.gif file is a problem
# Therefore, this function deletes that file using os lib
def deleteExistingSortingGif():
    try:
        remove("sorting.gif")
        printL(1, "Removed previous GIF")
    except:
        printL(3,"Could not remove previous sorting.gif")

#Call function with type according to above (eg 0 for normal log)
# and a string with whatever should be added to log
def printL(type,addition):
    global textLog
    global textLogUpdate
    textLogUpdate = True
    textLog.append((type,addition))

# Function that correctly inserts new progress item into log
def printProgress(progress):
    global textLog
    global textLogUpdate
    textLogUpdate = True
    #Insert at pos 0
    textLog.insert(0,(2, progress))

# Prints progress bar, only to be called if
# in log values of type 2 exists and terminal is clear
def printProgressBar(currentValue):
    print("Progress:" +  str(currentValue) + "%")
    print("""[""",end="")
    progressCounter = 0
    for i in range(0,int(currentValue),5):
        print("""#""",end="")
        progressCounter +=1
    for i in range(0,20-progressCounter):
        print("""·""", end="")
    print("""]""")

def printSign():
    print("""
 _______         _______         _______ 
(  ____ \       (  ___  )       (  ____ |
| (    \/       | (   ) |       | (    \/
| (_____  _____ | (___) | _____ | |      
(_____  )(_____)|  ___  |(_____)| | ____ 
      ) |       | (   ) |       | | \_  )
/\____) |       | )   ( |       | (___) |
\_______)       |/     \|       (_______)
                                         """)

def printLimitations(myType):
    printL(myType,"Limitations exceeded. For reference see below")
    printL(myType,"Current program limitations:")
    printL(myType,"Size < 1000")
    printL(myType, "if display values in bar, Size < 20")
    printL(myType,"Loops must be < 9999, set to 0 for Inf")
# Given a type, removes all entries of that type from log
def deleteType(theType):
    global textLog
    counter = 0
    while True:
        if counter >= len(textLog)-2:
            return True
        type,value = textLog[counter]
        if type == theType:
            textLog.pop(counter)
            counter = counter-3
        counter +=1

# Function that clears terminal and write new info.
# To activate, set textLogUpdate = True, usually it will run shortly
def updateDisplay():
    global textLog
    global textLogUpdate
    # Without this, much resources would be wasted on rewriting log terminal display
    if not textLogUpdate:
        return -1
    textLogUpdate = False
    #runTime = time.strftime("%H:%M:%S", time.localtime(time.time() - startUpTime - 60 * 60))
    system("clear")
    printSign()
    #print(str(runTime))
    if len(textLog) > 20:
        for i in range(0,10):
            type,value = textLog[0]
            if type != 2:
                textLog.pop(0)
    maxProgress = -1
    for type,value in textLog:
        if type == 2:
            if value > maxProgress:
                maxProgress = value
    if -1 < maxProgress < 100:
        printProgressBar(maxProgress)
        print("--------------------------------------------")
    for type,value in textLog:
        if type == 1:
            print(value)
        if type == 3:
            print(f"{bcolors.WARNING} Warning: {value} {bcolors.ENDC}")
        if type == 4 and DEBUG:
            print(f"{bcolors.OKBLUE} Debug: {value} {bcolors.ENDC}")

def writeGifFile(listOfImages,numberOfLoops):
    newGif = imageio.v3.imopen('sorting.gif', "w", plugin="pillow")
    newGif.write(listOfImages, duration=int(display.delay), loop=numberOfLoops, optimize=True)
    newGif.close()

# Create GIF using existing files
def CreateGIF(counter,SCREENSHOT_FILENAME):
    updateDisplay()
    #Idea is that pictures are generated with numbers 0 to some MAX
    printL(1,"Trying to generate GIF, this may freeze the program and take a while")
    fileNames = []
    for i in range(0,counter):
        fileNames.append(f"{SCREENSHOT_FILENAME}{str(i)}.jpg")
    #This will start to load in individual pictures into gif engine
    numberOfLoops = 0
    deleteExistingSortingGif()
    printL(1, f"Adding {str(display.delay)} ms delay for each image in GIF")
    printL(4, "Accurate gif settings is applied \n Therefore every frame from animation will be in GIF.")
    printL(4, "This increases time to generate, but also more accurately displays how sorting function works.")
    printL(4, f"Total number of recorded images: {str(len(fileNames))}")
    updateDisplay()
    try:
        listOfImages = []
        for (counter, filename) in enumerate(fileNames):
            if counter % 100 == 1:
                updateDisplay()
            listOfImages.append(imageio.v3.imread(filename))
            printProgress(int(((counter) / len(fileNames)) * 100*0.7))
    except Exception:
        printL(4,"Tried to create GIF, something went wrong")
        printL(4,"Terminating program")
        updateDisplay()
        show_trace(Exception)
    printL(1, "Writing GIF to disk")
    writeGifFile(listOfImages, display.loopBox.get_value())
    printProgress(100)
    updateDisplay()
    #Del latest list, this does NOT decrease current RAM usage,
    #but makes next round use the same memory area instead
    printL(1,"Cleaning up remaining files")
    del listOfImages
    del fileNames
    collect()
    printL(1,"GIF generation complete as sorting.gif")
    #Delete all files in folder
    deleteTempFiles()
    deleteType(2)
    updateDisplay()
    
#Given a list of filenames, it returns what number the highest file has.
def getMaxNumber(files):
    currentMax  = -1
    for item in files:
        myNumber = int(item[len(SCREENSHOT_FILENAME):len(item)-4])
        if myNumber > currentMax:
            currentMax = myNumber
    return currentMax

#Given a picture counter & screenshot item, takes and saves a picture of animation
def takePicture(SCREENSHOT_FILENAME,GIF_picture_counter,screenshot):
    if not display.includeSettingsInOutput:
        pygame.image.save(screenshot, f"{SCREENSHOT_FILENAME}{str(GIF_picture_counter)}.jpg")
    else:
        pygame.image.save(display.screen, f"{SCREENSHOT_FILENAME}{str(GIF_picture_counter)}.jpg")

# We need a place to write pictures currently
# Yes, this is bad design.
# Checks if picture folder exists, and if not it is created.
def createPicturesFolder():
    myDir = []
    for pathnames,dirnames,filenames in walk(getcwd()):
            myDir.extend(dirnames)
    for directory in myDir:
        if directory == "pictures":
            return -1
    try:
        mkdir("pictures")
    except:
        raise Exception("Could not create pictures folder")

def main():
    updateDisplay()
    printL(4,"Function import and program load completed")
    SCREENSHOT_FILENAME = "pictures/screenshot" #+ a counter number + JPG
    
    numbers = []
    running = True
    display.algorithmBox.add_options(list(algorithmsDict.keys()))

    alg_iterator = None
    
    #One keeps track of how many files have been created, the other when to skip images
    GIF_picture_counter = 0
    GIF_skip_image_counter = 0

    #Used for rendering window
    GIF_WINDOW_SIZE = (900, 400)
    
    #Just to make sure nothing from prev runs is left
    deleteTempFiles()
    
    #Create pictures if it does not exists
    createPicturesFolder()
    
    while running:
        updateDisplay()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and display.do_sorting:
                display.paused = not display.paused
                display.timer_space_bar = time()

            display.updateWidgets(event)

        if display.playButton.isActive: # play button clicked
            try:
                if int(display.sizeBox.text) > 1000 or \
                        (display.displayValuesInOutput and int(display.sizeBox.text) > 49) and \
                        (display.loopBox.get_value() < 9999):
                    # This is limitation because of RAM. size = 100 needs 2GB of RAM, so 120 is for some reason significantly higher
                    printL(3,("Halting output creation"))
                    printLimitations(3)
                else:
                    printL(1,"-------------------------------")
                    printL(1,("Creating animation"))
                    GIF_picture_counter = 0
                    GIF_picture_counter = 0
                    display.do_sorting = True
                    display.playButton.isActive = False
                    current_alg = display.algorithmBox.get_active_option()
                    display.numBars = int(display.sizeBox.text)
                    if display.numBars > 20 and display.displayValuesInOutput:
                        printL(3,"Will not render values in bars because number of bars > 20")
                    numbers = [randint(10, 400) for i in range(display.numBars)]  # random list to be sorted
                    alg_iterator = algorithmsDict[current_alg](numbers, 0, display.numBars - 1)  # initialize iterator
                display.playButton.isActive = False
            except ValueError:
                printL(4,"Text in size field is not a number")

        if display.stopButton.isActive: # stop button clicked
            printL(1,("Stopping animation"))
            display.stopButton.isActive = False
            display.do_sorting = False
            display.paused = False
            try: # deplete generator to display sorted numbers
                while True:
                    numbers, redBar1, redBar2, blueBar1, blueBar2 = next(alg_iterator)
            except StopIteration:
                pass
            #Delete temp files. No gif is possible because early stop
            deleteTempFiles()
            GIF_picture_counter = 0
            GIF_skip_image_counter = 0
                
        #GIF may need own thing
        screenshot = pygame.Surface(GIF_WINDOW_SIZE)
        screenshot.blit(display.screen, (0,0))
        
        if display.do_sorting and not display.paused: # sorting animation
            try:
                numbers, redBar1, redBar2, blueBar1, blueBar2 = next(alg_iterator)
                display.drawInterface(numbers, redBar1, redBar2, blueBar1, blueBar2)
                #Pictures needs to be generated and saved temporarily
                if int(display.sizeBox.text) <= 200:
                    takePicture(SCREENSHOT_FILENAME,GIF_picture_counter,screenshot)
                    GIF_picture_counter +=1
                #If size > 200, then we need to take drastically less pictures
                else:
                    if int(GIF_skip_image_counter) % int(5) == 1:
                        takePicture(SCREENSHOT_FILENAME,GIF_picture_counter,screenshot)
                        GIF_picture_counter +=1
                        GIF_skip_image_counter = 0
                    GIF_skip_image_counter +=1
                    
            except StopIteration:
                #If program stops because end of sorting, gif needs to be created if selected
                #Create green bars
                a_set = set(range(display.numBars))
                display.drawInterface(numbers, -1, -1, -1, -1, greenRows=a_set)
                #Make sure they are saved for a second
                takePicture(SCREENSHOT_FILENAME, GIF_picture_counter, screenshot)
                GIF_picture_counter += 1
                takePicture(SCREENSHOT_FILENAME, GIF_picture_counter, screenshot)
                GIF_picture_counter += 1
                takePicture(SCREENSHOT_FILENAME, GIF_picture_counter, screenshot)
                GIF_picture_counter += 1
                # Call function for GIF
                CreateGIF(GIF_picture_counter,SCREENSHOT_FILENAME)
                #Reset counter
                GIF_picture_counter = 0
                GIF_skip_image_counter = 0
                # Turn off sorting
                display.do_sorting = False
                
        elif display.do_sorting and display.paused: # animation paused
            display.drawInterface(numbers, -1, -1, -1, -1)
        else: # no animation
            a_set = set(range(display.numBars))
            display.drawInterface(numbers, -1, -1, -1, -1, greenRows=a_set)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "True" or sys.argv[1] == "true":
            DEBUG = True
    main()


