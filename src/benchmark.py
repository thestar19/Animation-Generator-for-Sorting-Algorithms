import os
#import display
#import main
import subprocess
import timeit
import sys
from algs import algorithmsDict
import shlex


def runCommand(command):
    return subprocess.Popen(shlex.split(command), shell=False, stdout=subprocess.PIPE).stdout.read()

def main(rounds,append,max_len,min_len,print_time,standard_benchmark):
    command = "python3 src/main.py -f MP4 -s 10 -d 10 -l 0 -a quick"
    list(algorithmsDict.keys())
    aTimer = timeit.Timer(lambda: runCommand(command))
    #duration = timeit.timeit(runCommand,number=10,globals = command)
    print(f"------Timing results------")
    timeLog = []
    for i in range(rounds):
        thisTime = aTimer.timeit(5)
        timeLog.append(thisTime)
        print(f"{i}:{thisTime}")
    print(f"Avg time: {sum(timeLog)/len(timeLog)}")

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
    available_args = ["-r","-rounds","-max","-min","-time","-t","-append_to_log","-a","-standard","-s"]
    if len(sys.argv) > 1:
        if len(sys.argv) == 2 and sys.argv[1] == "help":
            print("--------------------------------------------------------------")
            print(f"Benchmarking program for")
            print(f"Sorting Algorithm GIF Generator by TheStar19")
            print(f"https://github.com/thestar19/Sorting-Algorithm-GIF-Generator")
            print(f"A fork of Sorting Algorithm Visualizer by LucasPilla")
            #print(f"")
            print("--------------------------------------------------------------")
    if len(sys.argv) > 2:
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
        rounds = 10
        append = False
        max_len = 100
        min_len = 10
        print_time = True
        standard_benchmark = False
        for inst,value in instructions:
            # Check for -a arg
            if (inst == "-a" or inst == "-append_to_log") and (value == "true" or value == "false"):
                append = True
            elif (inst == "-a" or inst == "-append_to_log"):
                print(f"Incorrect args, -a value {value} is not an int between 1 and 999")
                sys.exit(0)
            # Check for standard arg
            if (inst == "-s" or inst == "-standard") and (value == "true" or value == "false"):
                standard_benchmark = True
            elif (inst == "-s" or inst == "-standard"):
                print(f"Incorrect args, -s value {value} is not true or false")
                sys.exit(0)
            # Check for -time arg
            if (inst == "-t" or inst == "-time") and (value == "true" or value == "false"):
                print_time = True
            elif (inst == "-t" or inst == "-time"):
                print(f"Incorrect args, -t value {value} is not true or false")
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
                if (inst == "-min") and   1 < newValue < 1000:
                    min_len = newValue
                elif (inst == "-min"):
                    print(f"Incorrect args, -min value {value} is not an int between 1 and 1000")
                    sys.exit(0)
        if max_len < min_len:
            print(f"Incorrect args, min value {min_len} is not smaller than max value {max_len}")
            sys.exit(0)
        if standard_benchmark:
            print("No standard implemented")
        # Only call main iff all criteria have been satisfied
        main(rounds,append,max_len,min_len,print_time,standard_benchmark)
