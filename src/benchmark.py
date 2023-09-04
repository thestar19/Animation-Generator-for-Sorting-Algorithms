from os import path,remove
#import display
#import main
import subprocess
import timeit
import sys
from algs import algorithmsDict
import shlex
import random
import datetime

# Global Variables
BENCHMARK_TEMP_TEXT_FILE = "temp_file_for_benchmark.txt"
BENCHMARK_RESULTS_FILE = "benchmark_results.txt"


def __uniqueid__():
    """
      generate unique id with length 17 to 21.
      ensure uniqueness even with daylight savings events (clocks adjusted one-hour backward).

      if you generate 1 million ids per second during 100 years, you will generate
      2*25 (approx sec per year) * 10**6 (1 million id per sec) * 100 (years) = 5 * 10**9 unique ids.

      with 17 digits (radix 16) id, you can represent 16**17 = 295147905179352825856 ids (around 2.9 * 10**20).
      In fact, as we need far less than that, we agree that the format used to represent id (seed + timestamp reversed)
      do not cover all numbers that could be represented with 35 digits (radix 16).

      if you generate 1 million id per second with this algorithm, it will increase the seed by less than 2**12 per hour
      so if a DST occurs and backward one hour, we need to ensure to generate unique id for twice times for the same period.
      the seed must be at least 1 to 2**13 range. if we want to ensure uniqueness for two hours (100% contingency), we need
      a seed for 1 to 2**14 range. that's what we have with this algorithm. You have to increment seed_range_bits if you
      move your machine by airplane to another time zone or if you have a glucky wallet and use a computer that can generate
      more than 1 million ids per second.

      one word about predictability : This algorithm is absolutely NOT designed to generate unpredictable unique id.
      you can add a sha-1 or sha-256 digest step at the end of this algorithm but you will loose uniqueness and enter to collision probability world.
      hash algorithms ensure that for same id generated here, you will have the same hash but for two differents id (a pair of ids), it is
      possible to have the same hash with a very little probability. You would certainly take an option on a bijective function that maps
      35 digits (or more) number to 35 digits (or more) number based on cipher block and secret key. read paper on breaking PRNG algorithms
      in order to be convinced that problems could occur as soon as you use random library :)

      1 million id per second ?... on a Intel(R) Core(TM)2 CPU 6400 @ 2.13GHz, you get :

      >>> timeit.timeit(uniqueid,number=40000)
      1.0114529132843018

      an average of 40000 id/second
    """
    mynow=datetime.datetime.now
    sft=datetime.datetime.strftime
    # store old datetime each time in order to check if we generate during same microsecond (glucky wallet !)
    # or if daylight savings event occurs (when clocks are adjusted backward) [rarely detected at this level]
    old_time=mynow() # fake init - on very speed machine it could increase your seed to seed + 1... but we have our contingency :)
    # manage seed
    seed_range_bits=14 # max range for seed
    seed_max_value=2**seed_range_bits - 1 # seed could not exceed 2**nbbits - 1
    # get random seed
    seed=random.getrandbits(seed_range_bits)
    current_seed=str(seed)
    # producing new ids
    while True:
        # get current time
        current_time=mynow()
        if current_time <= old_time:
            # previous id generated in the same microsecond or Daylight saving time event occurs (when clocks are adjusted backward)
            seed = max(1,(seed + 1) % seed_max_value)
            current_seed=str(seed)
        # generate new id (concatenate seed and timestamp as numbers)
        #newid=hex(int(''.join([sft(current_time,'%f%S%M%H%d%m%Y'),current_seed])))[2:-1]
        newid=int(''.join([sft(current_time,'%f%S%M%H%d%m%Y'),current_seed]))
        # save current time
        old_time=current_time
        # return a new id
        yield newid

""" you get a new id for each call of uniqueid() """
uniqueid=__uniqueid__()

class result(object):
    def __init__(self,format,size,algorithm,thisTime,numberOfPictures,auto_loop):
        self.rounds = auto_loop
        self.format = format
        self.algorithm = algorithm
        self.thisTime = thisTime
        self.size = size
        self.numberOfPictures = numberOfPictures

def printIF(value,print_time,end=""):
    if print_time:
        print(value,end)

def runCommand(command):
    return subprocess.Popen(shlex.split(command), shell=False, stdout=subprocess.PIPE).stdout.read()

def deleteExistingFile(name):
    if path.exists(name):
        try:
            remove(name)
        except:
            print(f"Could not remove {name}")

def readNumberOfPictures():
    global BENCHMARK_TEMP_TEXT_FILE
    f = open(BENCHMARK_TEMP_TEXT_FILE,mode="r")
    data = f.readline().split("=")[1]
    f.close()
    deleteExistingFile(BENCHMARK_TEMP_TEXT_FILE)
    return int(data)

# # are ignored
# each entry begins with 20x -----
# each entry then has a date=
# each entry then has its unique id
# each entry then has:
#   rounds=int
#   size=int
#   time=float
#   format="GIF"/"MP4"
#   alg=name of alg
#   numberOfPictures=int
def appendResult(aResult):
    global BENCHMARK_RESULTS_FILE
    with open(BENCHMARK_RESULTS_FILE, mode="a") as file:
        file.write("--------------------\n")
        file.write(f"date={datetime.datetime.now()}\n")
        file.write(f"ID={str(next(uniqueid))}\n")
        file.write(f"rounds={aResult.rounds}\n")
        file.write(f"size={aResult.size}\n")
        file.write(f"time={aResult.thisTime}\n")
        file.write(f"format={aResult.format}\n")
        file.write(f"alg={aResult.algorithm}\n")
        file.write(f"numberOfPictures={aResult.numberOfPictures}\n")

def runARound(size,format,algorithm,auto_loop = 3):
    command = f"python3 src/main.py -f {format} -s {size} -d 10 -l 0 -a {algorithm} -bench true"
    aTimer = timeit.Timer(lambda: runCommand(command))
    thisTime = aTimer.timeit(auto_loop)
    numberOfPictures = readNumberOfPictures()
    myResult = result(format,size,algorithm,thisTime,numberOfPictures,auto_loop)
    return myResult

def main():
    global BENCHMARK_RESULTS_FILE
    if len(sys.argv) < 2:
        print(f"No valid arguments found")
        sys.exit(0)
    # ----------------------------------------------------------------------------------------------
    #This section is for dealing with accepting all args
    all_args = sys.argv.copy()
    all_args.pop(0)
    print("--------------------------------------------------------------")
    instructions = []
    while True:
        if len(all_args) > 1:
            if all_args[0] in available_args:
                instructions.append((all_args.pop(0),all_args.pop(0)))
            else:
                print(f"Incorrect arguments")
                print(f"Available args:{available_args}")
                sys.exit(0)
        else:
            break
    rounds = 5
    append = False
    max_len = 50
    min_len = 10
    size = 0
    print_time = True
    standard_benchmark = False
    format = "GIF"
    algorithm = "insertion"
    for inst,value in instructions:
        # Check for -a arg
        if (inst == "-atl" or inst == "-append_to_log") and (value == "true" or value == "false"):
            append = True
        elif (inst == "-atl" or inst == "-append_to_log"):
            print(f"Incorrect args, -atl value {value} is not an int between 1 and 999")
            sys.exit(0)
        # Check for standard arg
        if (inst == "-standard") and (value == "true"):
            standard_benchmark = True
        elif (inst == "-standard"):
            print(f"Incorrect args, -s value {value} is not true or false")
            sys.exit(0)
        if (inst == "-t" or inst == "-time") and (value == "true" or value == "false"):
            print_time = True
        elif (inst == "-t" or inst == "-time"):
            print(f"Incorrect args, -t value {value} is not true or false")
            sys.exit(0)
        if (inst == "-f" or inst == "-format") and (value == "MP4" or value == "GIF"):
            format = value
        elif (inst == "-f" or inst == "-format"):
            print(f"Incorrect args, -f value {value} is not GIF or MP4")
            sys.exit(0)
        if (inst == "-alg" or inst == "-algorithm") and (value in list(algorithmsDict.keys())):
            algorithm = value
        elif (inst == "-alg" or inst == "-algorithm"):
            print(f"Incorrect args, -algorithm value {value} is not in list of alg")
            sys.exit(0)
        isInt, newValue = validateInput("int", value)
        if isInt:
            if (inst == "-r" or inst == "-rounds") and 0 < newValue < 1000:
                rounds = newValue
            elif (inst == "-r" or inst == "-rounds"):
                print(f"Incorrect args, -r value {value} is not an int between 1 and 999")
                sys.exit(0)
            if (inst == "-max") and 1 < newValue < 1000:
                max_len = newValue
            elif (inst == "-max"):
                print(f"Incorrect args, -max value {value} is not an int between 100 and 1000")
                sys.exit(0)
            if (inst == "-min") and 1 < newValue < 1000:
                min_len = newValue
            elif (inst == "-min"):
                print(f"Incorrect args, -min value {value} is not an int between 1 and 1000")
                sys.exit(0)
            if (inst == "-s" or inst == "-size") and 5 < newValue < 1000:
                size = newValue
            elif (inst == "-s" or inst == "-size"):
                print(f"Incorrect args, -s value {value} is not an int between 1 and 1000")
                sys.exit(0)
    if max_len < min_len:
        print(f"Incorrect args, min value {min_len} is not smaller than max value {max_len}")
        sys.exit(0)
    #----------------------------------------------------------------------------------------------
    # This is where actual benchmark happens
    # Change to standard_benchmark
    if standard_benchmark:
        print(f"Standard benchmark is true, therefore most other settings are ignored")
        # what is standard benchmark:
        # For multiple alg and size, log number of pic & times in both MP4 and GIF
        # What alg: quick, insertion, merge, shell
        # What sizes: 10,20,50
        # What formats: MP4 and GIF
        resultCounter = 0
        for format in ["GIF","MP4"]:
            for alg in  ["quick","insertion","shell"]:
                for size in [10, 20, 50]:
                    aResult = runARound(size, format, alg, 1)
                    printIF(f"Format={format} | Alg={alg} | Size={size} | Total number of pics={aResult.numberOfPictures} | Total time={aResult.thisTime} | Avg pic/time={aResult.numberOfPictures/aResult.thisTime}",True)
                    if append:
                        appendResult(aResult)
                        resultCounter +=1
                printIF(("------------------------------------------------------------------------------------------------"), True)
            printIF(("################################################################################################################"), True)
        if resultCounter > 0:
            print(f"Appended {resultCounter} results to {BENCHMARK_RESULTS_FILE}")
    else:
        if size == 0:
            size = random.randint(min_len,max_len)
        aResult = runARound(size, format, algorithm, rounds)
        if append and rounds == 1:
            appendResult(aResult)
            print(f"Appended results to {BENCHMARK_RESULTS_FILE}")
        printIF(f"------Timing results------", print_time)
        printIF(f"Rounds:{rounds}",print_time)
        printIF(f"Array size:{size}",print_time)
        printIF(f"Total length of all arrays sorted:{size*rounds}",print_time)
        printIF(f"Total number of pictures created:{aResult.numberOfPictures*rounds}", print_time)
        printIF(f"Avg time:{aResult.thisTime}",print_time)
        printIF(f"Avg time/size:{(aResult.thisTime/rounds)/aResult.numberOfPictures}",print_time)
        printIF(f"Avg pic per time:{aResult.numberOfPictures/aResult.thisTime}",print_time)

def validateInput(type,input):
    if type == "int":
        try:
            return (True,int(input))
        except TypeError:
            return (False,input)
        except ValueError:
            return (False, input)
    return (None,input)


if __name__ == '__main__':
    available_args = ["-r","-rounds","-max","-min","-time","-t", \
                      "-append_to_log","-atl","-standard","-f","-format", \
                      "-algorithm","-alg","-s","-size"]
    if len(sys.argv) > 1:
        if len(sys.argv) == 2 and sys.argv[1] == "help":
            print("--------------------------------------------------------------")
            print(f"Benchmarking program for")
            print(f"Sorting Algorithm GIF Generator by TheStar19")
            print(f"https://github.com/thestar19/Sorting-Algorithm-GIF-Generator")
            print(f"A fork of Sorting Algorithm Visualizer by LucasPilla")
            print(f"Available arguments:{available_args}")
            print(f"------------------------")
            print(f"Valid inputs for each argument:")
            print(f"Number of rounds to run: -r or -rounds => 0 < int < 1000")
            print(f"Size of length of array: -s or -size => 0 < int < 1000")
            print(f"Append results to log, only works for -r 1: -atl or -append_to_log => true/false")
            print(f"Run standard benchmark, ignores other options: -standard => true/false")
            print(f"Format for testing: -f or -format => GIF or MP4")
            print(f"For random size, specify max & min:")
            print(f"        Max/min value for random length of array: -max or -min => min < max < 1000")
            print(f"What sorting algorithm: -alg or -algorithm => {list(algorithmsDict.keys())}\n\n")
            print("--------------------------------------------------------------")
    main()
