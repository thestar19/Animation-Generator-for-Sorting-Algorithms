# Animation-Generator-for-Sorting-Algorithms
Program made with Python and Pygame module for generating animations of how sorting algorithms function.\
Supports over 26 different algorithms eg: Bubblesort, Quicksort, Selectionsort, Mergesort, Radixsort.

Originally created by LucasPilla, this is a fork of his project "Sorting Algorithms Visualizer" that instead generates files of sorting animations. Additional options are implemented to create better videos or GIFs.

Original project: https://github.com/LucasPilla/Sorting-Algorithms-Visualizer

 \
Support this project by leaving a :star:

## Program preview
<img src="res/sorting_thumbnail.gif" alt="Program preview" width="450" height=400>

<img src="res/terminal_view.png" alt="Terminal preview" width="520" height=225>

## Contribute
Contributions are welcome. This project is still very new so much work is needed.
:exclamation: Feel free to open an issue if you have some problem :exclamation:

## Using the application

### Installation Windows (10+) (beta)
- Download [zip](https://github.com/thestar19/Animation-Generator-for-Sorting-Algorithms/raw/main/bin/Animation-Generator-for-Sorting-Algorithms_beta.zip) file from bin folder
- Extract content
- Run main.exe
  
Some features may not yet be implemented in the Windows version (eg terminal mode and benchmark), and not much testing has been done.
Further, it is also possible to run the program in python3 in Windows without the zip file by modifying the code.


### Installation Ubuntu
Only tested in Ubuntu x64 22.04.1-desktop
- Clone GitHub repository `git clone https://github.com/thestar19/Animation-Generator-for-Sorting-Algorithms.git`
- Install requirements: `pip3 install -r requirements.txt`
- Run: `python3 src/main.py`
### Verbose mode
- To output extra info, run `python3 src/main.py -v`
- To see further information about the program, run `python3 src/main.py help`
### Terminal mode
To generate an animation without interacting with the program's graphical interface:
- Run eg `python3 src/main.py -f GIF -s 50 -d 50 -l 0 -a quick`
  
This will create a GIF in the main folder depicting the algorithm Quicksort sorting an array of 50 elements with a delay for each pic of 50ms and infinite looping.\
To see all options, run `python3 src/main.py help`
### Benchmark
To better optimize the program & to enable features such as "estimated time for creation", a benchmark exists.
You can contribute too:
- Install the program so that `python3 src/main.py` runs correctly
- Run `python3 src/benchmark.py -standard true -atl true`. This may take a while (10min is common on modern computers) \
    The results will be appended to benchmark_results.txt, which contains results from other systems.
- Upload your results to [benchmark_results.txt](benchmark_results.txt) in the repo, either by manually copying and pasting the results into the file on the repo or by simply uploading the complete file.


To see all options for the benchmark, run `python3 src/benchmark.py help`

## Common troubleshooting steps:
### Install pip
For ubuntu: sudo apt-get update\
            sudo apt-get upgrade\
            sudo apt-get install pip3


### Multiple python installs
Check what version of python runs:\
  python3 -V\
  python3.7 -V
  
Then, install and upgrade imageio,pyav & pillow manually\
  python3 -m pip install imageio\
  python3 -m pip install --upgrade imageio\
  python3 -m pip install pillow\
  python3 -m pip install --upgrade pillow\
  python3 -m pip install imageio[pyav]\
  python3 -m pip install --upgrade imageio[pyav]
