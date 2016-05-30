# Wrek Downloader
Downloads the archive from http://www.wrek.org/ in mp3.

Music you don't hear on the radio.

## Usage
    cd wrek_download/
    
    python3 wrek_download/main.py --help
    
    usage: main.py [-h] [--verbose] [--verbosity VERBOSITY]
    
    optional arguments:
      -h, --help            show this help message and exit
      --verbose             puts the program in verbose mode
      --verbosity VERBOSITY
                            sets the verbosity of the program. Use 1 for error and
                            2 for info
The program then downloads the files from the archive formated with YYYYMMDD followed by the program number of the day NN followed by the name of the program and lastly the block of the program (files have 30 minutes). So for example you will get: `20160506_08_stonehenge_02.mp3` for the Stonehenge program aired on May 06, 2016 (this file is the third block of the program as the numbering starts with '00').

## TODO
- improve verbosity functionality
- rely on pathlib only instead of a mix of pathlib and strings
