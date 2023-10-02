import sys

#Define basic trace_function
def show_trace(event=""):
    print("An error has occured, printing useful info:")
    print(sys.version)
    print(sys.version_info)
    print(event)
    sys.exit(0)

from random import randint
from time import time
from algs import algorithmsDict
from os import rmdir, walk, getcwd, system, mkdir, remove,path,environ,putenv
from gc import collect
import imageio.v3 as iio
#import av #Temporary, this should be changed to only import needed functions
import pygame
from dataclasses import dataclass


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

TEXTLOG = []
TEXTLOG_UPDATE = True
DEBUG = False
CURRENT_OUTPUT_FORMATS = ["GIF","MP4"]
SCREENSHOT_FILENAME = "pictures/screenshot"  # + a counter number + JPG
BENCHMARK_TEXT_FILE = "temp_file_for_benchmark.txt"
ANIMATION_TABLE_TIME_ESTIMATE = "animationTimeEstimate.txt"
CREATE_ANIMATION_TABLE = (False,[],[])

#printL types:
# 1 = normal log message
# 2 = reserved for progress indication
# 3 = Warning message
# 4 = Reserved for debug use

#Generating animations as output requires placing files in subfolder and then loading them.
#This deletes all temporary files created during the generation of output
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

# For some uses, if the output file already exists it may cause problems.
# Therefore, this function deletes that file using os lib
def deleteExistingFile(name):
    if path.exists(name):
        try:
            remove(name)
            printL(1, f"Removed {name}")
        except:
            printL(3,f"Could not remove {name}")

#Call function with type according to above (eg 0 for normal log)
# and a string with whatever should be added to log
def printL(type,addition):
    global TEXTLOG
    global TEXTLOG_UPDATE
    TEXTLOG_UPDATE = True
    TEXTLOG.append((type,addition))

# Function that correctly inserts new progress item into log
def printProgress(progress):
    global TEXTLOG
    global TEXTLOG_UPDATE
    TEXTLOG_UPDATE = True
    #Insert at pos 0
    TEXTLOG.insert(0,(2, progress))

# Prints progress bar, only to be called if
# in log values of type 2 exists and terminal is clear
def printProgressBar(currentValue):
    print("""[""",end="")
    progressCounter = 0
    for _ in range(0,int(currentValue),5):
        print("""#""",end="")
        progressCounter +=1
    for _ in range(0,20-progressCounter):
        print("""·""", end="")
    print("""]""")

def printSign():
    print("""
                   _                    _    _               
     /\           (_)                  | |  (_)              
    /  \    _ __   _  _ __ ___    __ _ | |_  _   ___   _ __  
   / /\ \  | '_ \ | || '_ ` _ \  / _` || __|| | / _ \ | '_ \ 
  / ____ \ | | | || || | | | | || (_| || |_ | || (_) || | | |
 /_/    \_\|_| |_||_||_| |_| |_| \__,_| \__||_| \___/ |_| |_|
   _____                                 _                   
  / ____|                               | |                  
 | |  __   ___  _ __    ___  _ __  __ _ | |_  ___   _ __     
 | | |_ | / _ \| '_ \  / _ \| '__|/ _` || __|/ _ \ | '__|    
 | |__| ||  __/| | | ||  __/| |  | (_| || |_| (_) || |       
  \_____| \___||_| |_| \___||_|   \__,_| \__|\___/ |_|       
                                                             
                                                             """)

def printLimitations(myType):
    printL(myType,"Limitations exceeded. For reference see below")
    printL(myType,"Current program limitations:")
    printL(myType,"Size < 1000")
    printL(myType, "if display values in bar, Size < 20")
    printL(myType,"Loops must be < 9999, set to 0 for Inf")
# Given a type, removes all entries of that type from log

def checkVersionOfPYAV():
    with iio.imopen("temp.mp4","w",plugin="pyav") as newVideo:
        exists = False
        for attr in dir(newVideo):
            if "init_video_stream" == attr:
                exists = True
        if exists:
            printL(4,"Correct version of pyav detected")
            deleteExistingFile("temp.mp4")
            #This is kinda wierd, but is really just so control-flow works correctly.
            return
        else:
            print("Incorrect version of pyav detected")
            print("Exiting program")
    deleteExistingFile("temp.mp4")
    sys.exit(0)

def deleteType(theType):
    global TEXTLOG
    counter = 0
    while True:
        if counter >= len(TEXTLOG)-2:
            return True
        type,value = TEXTLOG[counter]
        if type == theType:
            TEXTLOG.pop(counter)
            counter = counter-3
        counter +=1

# Function that clears terminal and write new info.
# To activate, set TEXTLOG_UPDATE = True
# Usually, there is no need to run the function after setting TEXTLOG_UPDATE bc it will run soon anyway.
def updateDisplay(terminal = False):
    global TEXTLOG
    global TEXTLOG_UPDATE
    if terminal:
        currentMax = 0
        for (type,value) in TEXTLOG:
            if type != 2:
                print(value)
            elif currentMax < value:
                currentMax = value
        if currentMax > 0:
            print(f"Current progress in writing to disk:{currentMax}%")
        TEXTLOG.clear()
        return -1
    # Without this, much resources would be wasted on rewriting log terminal display
    if (randint(0,20) != 5):
        return -1
    TEXTLOG_UPDATE = False
    display.displayLog_update = False
    system("clear")
    #runTime = time.strftime("%H:%M:%S", time.localtime(time.time() - startUpTime - 60 * 60))
    printSign()
    #print(str(runTime))
    maxProgress = -1
    for type,value in TEXTLOG:
        if type == 2:
            if value > maxProgress:
                maxProgress = value
    if -1 < maxProgress < 100:
        printProgressBar(maxProgress)
        print("--------------------------------------------")
    for type,value in TEXTLOG + display.displayLog:
        if type == 1:
            print(value)
        if type == 3:
            print(f"{bcolors.WARNING} Warning: {value} {bcolors.ENDC}")
        if type == 4 and DEBUG:
            print(f"{bcolors.OKBLUE} Debug: {value} {bcolors.ENDC}")
def writeGifFile(listOfImages,numberOfLoops,delay):
    newGif = iio.imopen('sorting.gif', "w", plugin="pillow")
    newGif.write(listOfImages, duration=int(delay), loop=numberOfLoops, optimize=True)
    newGif.close()

# Create GIF using existing files
def createGIF(counter,SCREENSHOT_FILENAME,delay,loops,terminal=False):
    updateDisplay(terminal)
    #Idea is that pictures are generated with numbers 0 to some MAX
    printL(1,"Trying to generate GIF, this may freeze the program and take a while")
    fileNames = []
    if loops == "Inf":
        loops = 0
    for i in range(0,counter):
        fileNames.append(f"{SCREENSHOT_FILENAME}{str(i)}.jpg")
    #This will start to load in individual pictures into gif engine
    deleteExistingFile("sorting.gif")
    printL(1, f"Adding {str(delay)} ms delay for each image in GIF")
    printL(4, "Accurate GIF settings is applied \n Therefore every frame from animation will be in GIF.")
    printL(4, "This increases time to generate, but also more accurately displays how sorting function works.")
    printL(4, f"Total number of recorded images: {str(len(fileNames))}")
    updateDisplay(terminal)
    listOfImages = []
    howManyExtraFrames = float((delay * 30) / 1000)  # Formula to get number of repeat images for delay
    if howManyExtraFrames < 0.8:
        printL(3,"Delay less than 100ms may result in skipped frames.")
        printL(3, "This is because most GIF rendering sources cannot display less than that")
        printL(3, "For better accuracy, use MP4 as output format")
    skipFrameCounter = 0
    for (counter, filename) in enumerate(fileNames):
        if counter % 500 == 217 or len(fileNames) < 50:
            updateDisplay(terminal)
            printProgress(int(((counter) / len(fileNames)) * 100 * 0.7))
            collect()
        if howManyExtraFrames < 0.8:
            if skipFrameCounter > 1:
                listOfImages.append(iio.imread(filename))
                skipFrameCounter = 0
            else:
                skipFrameCounter += howManyExtraFrames
        else:
            if howManyExtraFrames < 1:
                howManyExtraFrames = 1
            aFrame = iio.imread(filename)  # So we don't read it more than once
            for i in range(int(howManyExtraFrames)):
                listOfImages.append(aFrame)
    printL(1, "Writing GIF to disk")
    writeGifFile(listOfImages,loops,delay)
    printProgress(100)
    updateDisplay(terminal)
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
    updateDisplay(terminal)

# Create MP4 using existing files
def createMP4(numberOfPictures,SCREENSHOT_FILENAME,delay,terminal=False):
    updateDisplay(terminal)
    #Idea is that pictures are generated with numbers 0 to some MAX
    printL(1,"Trying to generate MP4, this may freeze the program and take a while")
    fileNames = []
    for i in range(0,numberOfPictures):
        fileNames.append(f"{SCREENSHOT_FILENAME}{str(i)}.jpg")
    deleteExistingFile("sorting.mp4")
    howManyExtraFrames = float((delay * 30) / 1000)  # Formula to get number of repeat images for delay
    printL(1, f"Adding {str(delay)} ms delay for each image in MP4")
    printL(4, "Accurate MP4 settings is applied \n Therefore every frame from animation will be in MP4.")
    printL(4, "This increases time to generate, but also more accurately displays how sorting function works.")
    printL(4, f"Total number of recorded images: {str(len(fileNames))}")
    printL(4,f"Ignoring looping options because MP4 format does not support")
    printL(1, f"Estimated total runtime of resulting animation:{round((howManyExtraFrames * len(fileNames))/32,3)} seconds")
    updateDisplay(terminal)
    with iio.imopen("sorting.mp4","w",plugin="pyav") as newVideo:
        newVideo.init_video_stream("mpeg4",fps=30)
        if howManyExtraFrames < 0.8:
            printL(3, f"Warning, FPS = 30 & Delay = {delay} means that certain frames will be skipped")
        skipFrameCounter = 0
        for (counter, filename) in enumerate(fileNames):
            if counter % 500 == 217 or numberOfPictures < 50:
                updateDisplay(terminal)
                printProgress(int(((counter) / len(fileNames)) * 100))
                collect()
            if howManyExtraFrames < 0.8:
                if skipFrameCounter > 1:
                    aFrame = iio.imread(filename)
                    newVideo.write_frame(aFrame)
                    del(aFrame)
                    skipFrameCounter = 0
                else:
                    skipFrameCounter += howManyExtraFrames
            else:
                if howManyExtraFrames < 1:
                    howManyExtraFrames = 1
                aFrame = iio.imread(filename)  # So we don't read it more than once
                for i in range(int(howManyExtraFrames)):
                    newVideo.write_frame(aFrame)
                newVideo.write_frame(aFrame)
                del(aFrame)
    printL(1, "Writing MP4 to disk")
    printProgress(100)
    updateDisplay(terminal)
    #Del latest list, this does NOT decrease current RAM usage,
    #but makes next round use the same memory area instead
    printL(1,"Cleaning up remaining files")
    del fileNames
    collect()
    printL(1,"MP4 generation complete as sorting.mp4")
    #Delete all files in folder
    deleteTempFiles()
    deleteType(2)
    updateDisplay(terminal)

#Given a list of filenames, it returns what number the highest file has.
def getMaxNumber(files):
    currentMax  = -1
    for item in files:
        myNumber = int(item[len(SCREENSHOT_FILENAME):len(item)-4])
        if myNumber > currentMax:
            currentMax = myNumber
    return currentMax

#Given a picture counter & screenshot item, takes and saves a picture of animation
def takePicture(SCREENSHOT_FILENAME,counter_for_number_pictures_created,screenshot):
    if not display.includeSettingsInOutput:
        pygame.image.save(screenshot, f"{SCREENSHOT_FILENAME}{str(counter_for_number_pictures_created)}.jpg")
    else:
        pygame.image.save(display.screen, f"{SCREENSHOT_FILENAME}{str(counter_for_number_pictures_created)}.jpg")

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

def listAsStringGood(myList):
    valid_formats = ""
    for option in myList:
        valid_formats = f"{valid_formats},{option}"
    return valid_formats


def createTableForAnimationTimeEstimate(allNumbers,startover,rounds,algorithmsToRun):
    printL(1,f"Table generation for animation time requested")
    printL(1,f"Creating table, writing results to {ANIMATION_TABLE_TIME_ESTIMATE}")
    printL(1, f"Program will generate new table, write it to disk and then quit")
    printL(1, f"To use the new table, simply start the program again without the flag -new_time_table")
    if startover:
        remove(ANIMATION_TABLE_TIME_ESTIMATE)
    f = open(ANIMATION_TABLE_TIME_ESTIMATE,"a")
    progressCounter = 0
    for outputSize in allNumbers:
        for alg in algorithmsToRun:
            avgResult = 0
            for i in range(int(rounds)):
                numbers = [randint(10, 400) for i in range(outputSize)]  # random list to be sorted
                alg_iterator = algorithmsDict[alg](numbers, 0, outputSize-1)  # initialize iterator
                counter_for_number_pictures_created, _ = createPicturesForOutput(False, 0, 0,
                                                                                 numbers, alg_iterator, (900, 400),do_not_render_Pictures=True)
                avgResult += counter_for_number_pictures_created
            printL(1,f"({round((progressCounter / (len(allNumbers) * len(list(algorithmsDict.keys()))))*100, 2)}%)    Size = {outputSize}    |    Algorithm = {alg}    |    Average result = {round(avgResult/rounds,3)}")
            f.write(f"alg={alg},size={outputSize},result={round(avgResult/rounds,3)}\n")
            progressCounter += 1
        printL(1,"############################################################################")
        updateDisplay(False)
    # Some things are not accounted for, so just to make sure that the program begins with a clean slate.
    deleteTempFiles()
    f.close()
    sys.exit(0)

def createPicturesForOutput(TERMINAL_MODE,counter_for_number_pictures_created,counter_skipping_images_during_creation,numbers,alg_iterator,OUTPUT_WINDOW_SIZE,**kwargs):
    global SCREENSHOT_FILENAME
    screenshot = pygame.Surface(OUTPUT_WINDOW_SIZE)
    screenshot.blit(display.screen, (0, 0))
    try:
        while True:
            if kwargs.get("do_not_render_Pictures") and counter_for_number_pictures_created + counter_skipping_images_during_creation > 5000:
                display.do_sorting = False
                return (counter_for_number_pictures_created, counter_skipping_images_during_creation)
            if len(numbers) < 50 or counter_for_number_pictures_created % 1000 == 5:
                updateDisplay(TERMINAL_MODE)
                printL(4,f"Current pic count:{counter_for_number_pictures_created}")
            numbers, redBar1, redBar2, blueBar1, blueBar2 = next(alg_iterator)
            display.drawInterface(numbers, redBar1, redBar2, blueBar1, blueBar2,[],displaySize=OUTPUT_WINDOW_SIZE)
            screenshot = pygame.Surface(OUTPUT_WINDOW_SIZE)
            screenshot.blit(display.screen, (0, 0))
            # Pictures needs to be generated and saved temporarily
            if len(numbers) <= 200:
                if not kwargs.get("do_not_render_Pictures"):
                    takePicture(SCREENSHOT_FILENAME, counter_for_number_pictures_created, screenshot)
                counter_for_number_pictures_created += 1
            # If size > 200, then we need to take drastically less pictures
            else:
                if int(counter_skipping_images_during_creation) % 5 == 1:
                    if not kwargs.get("do_not_render_Pictures"):
                        takePicture(SCREENSHOT_FILENAME, counter_for_number_pictures_created, screenshot)
                    counter_for_number_pictures_created += 1
                counter_skipping_images_during_creation += 1

    except StopIteration:
        # If program stops because end of sorting
        # Create green bars
        a_set = [k for k in range(0,len(numbers))]

        printL(4,f"Green_rows at end={a_set}")
        display.drawInterface(numbers, -1, -1, -1, -1, a_set,displaySize=OUTPUT_WINDOW_SIZE)
        screenshot = pygame.Surface(OUTPUT_WINDOW_SIZE)
        screenshot.blit(display.screen, (0, 0))
        # Make sure final frame are saved for slightly longer than the rest
        takePicture(SCREENSHOT_FILENAME, counter_for_number_pictures_created, screenshot)
        counter_for_number_pictures_created += 1
        takePicture(SCREENSHOT_FILENAME, counter_for_number_pictures_created, screenshot)
        counter_for_number_pictures_created += 1
        takePicture(SCREENSHOT_FILENAME, counter_for_number_pictures_created, screenshot)
        counter_for_number_pictures_created += 1
        printL(4, f"Current pic count:{counter_for_number_pictures_created}")
        if not TERMINAL_MODE and not kwargs.get("do_not_render_Pictures"):
            if display.GUI.outputFormatBox.get_active_option() == "GIF":
                createGIF(counter_for_number_pictures_created, SCREENSHOT_FILENAME, int(display.delay), int(display.GUI.loopBox.get_value()))
            else:
                createMP4(counter_for_number_pictures_created, SCREENSHOT_FILENAME, int(display.delay))
        # Turn off sorting
        display.do_sorting = False
        return (counter_for_number_pictures_created,counter_skipping_images_during_creation)


def main():
    printL(4,"Function import and program load completed")

    #Init display
    display.init()
    #Init numbers and other important vars
    numbers = []
    running = True
    display.GUI.algorithmBox.add_options(list(algorithmsDict.keys()))
    display.GUI.outputFormatBox.add_options(CURRENT_OUTPUT_FORMATS)

    alg_iterator = None
    
    #One keeps track of how many files have been created, the other when to skip images
    counter_for_number_pictures_created = 0
    counter_skipping_images_during_creation = 0

    #Used for rendering window
    # 1/h_o_scaling factor = 2.608 => Ergo, to get output to be 1920x1080, input has to be 1920x(1080*2.608)
    w_o, h_o = display.windowSize
    OUTPUT_WINDOW_SIZE = (w_o, h_o-740)

    #Just to make sure nothing from prev runs is left
    deleteTempFiles()
    
    #Create pictures if it does not exists
    createPicturesFolder()

    #Check if new table is to be generated
    doCreate,argNumbers,argAlgs = CREATE_ANIMATION_TABLE
    if doCreate:
        if argAlgs == "all":
            argAlgs = list(algorithmsDict.keys())
        createTableForAnimationTimeEstimate(argNumbers,False,5,argAlgs)

    while running:
        updateDisplay()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            display.updateWidgets(event)

        if display.GUI.playButton.isActive: # play button clicked
            try:
                if int(display.GUI.sizeBox.text) > 1000 or \
                        (display.displayValuesInOutput and int(display.GUI.sizeBox.text) > 49) or \
                        (display.GUI.loopBox.get_value() > 9999) or \
                        (display.GUI.loopBox.get_value() == "") or \
                        (display.GUI.sizeBox.text == ""):
                    # This is limitation because of RAM. size = 100 needs 2GB of RAM, so 120 is for some reason significantly higher
                    printL(3,("Halting output creation"))
                    printLimitations(3)
                else:
                    printL(1,"-------------------------------")
                    printL(1,("Creating animation"))
                    counter_for_number_pictures_created = 0
                    counter_skipping_images_during_creation = 0
                    display.do_sorting = True
                    display.GUI.playButton.isActive = False
                    current_alg = display.GUI.algorithmBox.get_active_option()
                    display.numBars = int(display.GUI.sizeBox.text)
                    if display.numBars > 20 and display.displayValuesInOutput:
                        printL(3,"Will not render values in bars because number of bars > 20")
                    numbers = [randint(10, 400) for i in range(display.numBars)]  # random list to be sorted
                    alg_iterator = algorithmsDict[current_alg](numbers, 0, display.numBars - 1)  # initialize iterator
                display.GUI.playButton.isActive = False
            except ValueError:
                printL(4,"Text in size field is not a number")

        if display.GUI.stopButton.isActive: # stop button clicked
            printL(1,("Stopping animation"))
            display.GUI.stopButton.isActive = False
            display.do_sorting = False
            try: # deplete generator to display sorted numbers
                while True:
                    numbers, redBar1, redBar2, blueBar1, blueBar2 = next(alg_iterator)
            except StopIteration:
                pass
            #Delete temp files.
            deleteTempFiles()
            counter_for_number_pictures_created = 0
            counter_skipping_images_during_creation = 0
        
        if display.do_sorting: # sorting animation
            #This is needed bc both terminal mode and GUI mode needs to exist
            createPicturesForOutput(False, counter_for_number_pictures_created,counter_skipping_images_during_creation,numbers,alg_iterator,OUTPUT_WINDOW_SIZE)
            display.do_sorting = False
            counter_for_number_pictures_created = 0
            counter_skipping_images_during_creation = 0
        else: # no animation
            a_set = set(range(display.numBars))
            display.drawInterface(numbers, -1, -1, -1, -1, greenRows=a_set,displaySize=OUTPUT_WINDOW_SIZE)

def validateInput(type,input):
    if type == "int":
        try:
            return (True,int(input))
        except TypeError:
            return (False,input)
        except ValueError:
            return (False, input)
    return (None,input)


@dataclass
class TerminalOptions:
    output_format:str = "GIF"
    output_delay:int = 1
    output_size:int = 100
    add_numbers_to_bars:bool = False
    output_loops:int = 0
    output_alg:str = "insertion"
    benchmark:bool = False


def analyzeInputsArgs(available_args):
    global DEBUG
    all_args = sys.argv.copy()
    all_args.pop(0)
    print("--------------------")
    instructions = []
    while True:
        if len(all_args) > 1:
            if all_args[0] in available_args:
                instructions.append((all_args.pop(0), all_args.pop(0)))
            else:
                print(f"Incorrects arg options")
                print(f"Available args:{available_args}")
                sys.exit(0)
        else:
            break
    options = TerminalOptions()
    for inst, value in instructions:
        # Check for output format
        if inst == "-f" and value in CURRENT_OUTPUT_FORMATS:
            options.output_format = value
        elif inst == "-f":
            print(f"Incorrect args, -f value {value} is not supported")
            sys.exit(0)
        # Check for debug mode, verbose
        elif (inst == "-v" or inst == "-V") and value == "true":
            DEBUG = True
        elif inst == "-v" or inst == "-V":
            print(f"Incorrect args, -v value {value} is not true or false")
            sys.exit(0)
        # Check for including numbers in bars or entire GUI
        elif inst == "-include" and value == "numbers":
            options.add_numbers_to_bars = True
        elif inst == "-include":
            print(f"Incorrect args, -include value {value} is not text \"numbers\"")
            sys.exit(0)
        # Check for which algorithm to run
        elif inst == "-a" and value in list(algorithmsDict.keys()):
            options.output_alg = value
        elif inst == "-a":
            print(f"Incorrect args, -a value {value} is not in accepted sorting alg")
            sys.exit(0)
        elif inst == "-bench" and value == "true":
            options.benchmark = True
        elif inst == "-bench":
            print(f"Incorrect args, -bench value {value} is not true or false")
            sys.exit(0)
        isInt, newValue = validateInput("int", value)
        if isInt and inst in "-d -s -l":
            # Check for delay value
            if inst == "-d" and 1 <= int(newValue) <= 3000:
                options.output_delay = int(newValue)
            elif inst == "-d":
                print(f"Incorrect args, -d value {newValue} is not an int between 1 and 3000")
                sys.exit(0)
            # Check for size value
            elif inst == "-s" and 5 < int(newValue) <= 1000:
                options.output_size = int(newValue)
            elif inst == "-s":
                print(f"Incorrect args, -s value {newValue} is not an int between 5 and 1000")
                sys.exit(0)
            # Check for number of loops
            elif inst == "-l" and 0 <= int(newValue) <= 9999:
                options.output_loops = int(newValue)
            elif inst == "-l":
                print(f"Incorrect args, -l value {newValue} is not 0 <= value <= 9999")
                sys.exit(0)
    print(f"Creating output with these settings:")
    print(f"    Output format={options.output_format}")
    print(f"    Delay for each pic={options.output_delay}")
    print(f"    Number of elements in list to sort={options.output_size}")
    print(f"    Include numbers in bars={options.add_numbers_to_bars}")
    print(f"    Sorting alg={options.output_alg}")
    if options.output_format == "GIF":
        print(f"    Number of loops={options.output_loops}")
    return options


if __name__ == '__main__':
    available_args = ["-f","-d","-s","-include","-l","-v","-a","-bench","-custom_res","-t"]
    custom_display_res = []
    if len(sys.argv) >= 2:
        if sys.argv[1] == "help" or sys.argv[1] == "HELP" or sys.argv[1] == "Help":
            print("--------------------------------------------------------------")
            print(f"Animation Generator for Sorting Algorithms")
            print(f"https://github.com/thestar19/Animation-Generator-for-Sorting-Algorithms")
            print(f"A fork of Sorting Algorithm Visualizer by LucasPilla")
            print(f"A GIF or video can be created either by:")
            print(f"    1) Interacting with the GUI by running python3 src/main.py")
            print(f"    2) Only using the terminal by providing arguments with flag -t")
            print(f"")
            print(f"Valid inputs for terminal arguments:")
            print(f"    Format: -f => GIF or MP4")
            print(f"    Delay for each pic: -d => 1-3000")
            print(f"    Size of array to sort: -s => 5-1000")
            print(f"    Include numbers in bars in output: -include => true/false")
            print(f"    Number of loops (GIF ONLY): -l => 0(inf)-9999")
            print(f"    Output debug info (verbose): -v => true/false")
            print(f"    Use in terminal mode: -t => true/false")
            print(f"    Reserved use for time table creation: -new_time_table => int,int,int... [valid alg]/all ")
            print(f"    Reserved use for benchmark: -bench => true/false")
            print(f"        -bench has other req, may not work without benchmark.py")
            print(f"")
            print(f"    Custom resolution[BETA,MAY BE UNSTABLE, ONLY WORKS IN GUI MODE]:")
            print(f"         -custom_res => WidthxHeight where width & height are ints")
            print(f"         Eg, for output to be 1920x1080, add: -custom_res 1920x1080")
            print(f"")
            print(f"Available sorting algorithms:{list(algorithmsDict.keys())}")
            print(f"Available args:{available_args}")
            print("--------------------------------------------------------------")
            sys.exit(0)
        if "-custom_res" in sys.argv:
            pos_arg = sys.argv.index("-custom_res")
            value = sys.argv[pos_arg+1]
            try:
                custom_display_res = value.split("x")
                printL(4,f"Req custom display:{custom_display_res}")
            except Exception as e:
                print(f"Got arg -custom_res, but value was incorrectly formatted")
                print(f"Exception:{e}")
                print(f"This is a beta feature, and may therefore be unstable like this")
                print(f"Ending program")
                sys.exit(0)
        if "-V" in sys.argv or "-V" in sys.argv:
            printL(4,"Debug enabled")
            DEBUG = True
        if "-new_time_table" in sys.argv:
            pos_arg = sys.argv.index("-new_time_table")
            argNumbers = list(int(k) for k in sys.argv[pos_arg+1].split(","))
            if sys.argv[pos_arg+2] != "all":
                argAlgs = list(int(k) for k in sys.argv[pos_arg+1].split(","))
            else:
                argAlgs = sys.argv[pos_arg+2]
            CREATE_ANIMATION_TABLE = (True,argNumbers,argAlgs)
    #Check if correct software is installed
    #checkVersionOfPYAV()
    #Check for any args in program init
    if len(sys.argv) > 2:
        if sys.argv[1] == "-t":
            shell_options = analyzeInputsArgs(available_args)
            # Just to make sure nothing from prev runs is left
            deleteTempFiles()
            # Create pictures if it does not exists
            createPicturesFolder()
            #Okay, so get this.
            # If I import display before this, the window will render
            # If I first do putenv & environ crap, then no window.
            # For terminal mode, having no display thing pop up is a good feature.
            putenv('SDL_VIDEODRIVER', 'fbcon')
            environ["SDL_VIDEODRIVER"] = "dummy"
            import display as display
            display.init()
            numbers = [randint(10, 400) for i in range(shell_options.output_size)]  # random list to be sorted
            alg_iterator = algorithmsDict[shell_options.output_alg](numbers, 0, shell_options.output_size - 1)  # initialize iterator
            #Okay so, for the display module to work this has to be set.
            # So honestly, instead of doing extra work this should be solved some other way.
            display.GUI.algorithmBox.add_options(list(algorithmsDict.keys()))
            display.GUI.outputFormatBox.add_options(CURRENT_OUTPUT_FORMATS)
            display.numBars = shell_options.output_size
            counter_for_number_pictures_created,_ = createPicturesForOutput(True,0,0,numbers,alg_iterator,(900, 400))
            if shell_options.output_format == "GIF":
                createGIF(counter_for_number_pictures_created,SCREENSHOT_FILENAME,shell_options.output_delay,shell_options.output_loops,True)
            else:
                createMP4(counter_for_number_pictures_created,SCREENSHOT_FILENAME,shell_options.output_delay,True)
            if shell_options.benchmark:
                deleteExistingFile(BENCHMARK_TEXT_FILE)
                f = open(BENCHMARK_TEXT_FILE,"w+")
                f.write(f"pictures={counter_for_number_pictures_created}")
                f.close()
            print("Output generation finished!")
            sys.exit()
            #all_args = sys.argv.split[]
    # Yes, this is a really wierd place to import stuff
    # But this is needed for current version of program
    # This sets a custom resolution
    # Only way I found is via txt files.
    if len(custom_display_res) != 0:
        f = open("CUSTOM_RES.txt","w+")
        f.write(custom_display_res[1])
        f.write(",")
        f.write(custom_display_res[0])
        f.close()
    import display as display
    if len(custom_display_res) != 0:
        remove("CUSTOM_RES.txt")
    main()


