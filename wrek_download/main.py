"""
Created on Sun Oct 25 19:48:42 2015

author: monteiro

Description: downloads archives from WREK Atlanta

The idea is to create a timeline from the days prior to today (so today and
the two previous days are excluded as a safeguard measure for the WREK to
update their website)
and start downloading from the most distant day until the aforementioned day.

For example if today is 25 october the last available day is
12 october.
The range of downloading days should be 12 october untill 22 october
(inclusive).
"""
# pylama:skip=1
from datetime import datetime as dt
import os
import socket
import urllib.request
import logging
import argparse
import aux_functions as auxf
from lists import week, program_names
import parse_wrek_website

ROOT_FOLDER = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)))

# Parsing
parser = argparse.ArgumentParser()
parser.add_argument('--verbose',
                    help='Puts the program in verbose mode.',
                    action="store_true",
                    default=False)
parser.add_argument('--verbosity',
                    help='Sets the verbosity of the program. '
                         'Use 1 for error and 2 for info.',
                    type=int, default=1)
parser.add_argument('--archivefolder',
                    help='Archive folder where the m3u files are.',
                    required=False,
                    default=os.path.join(ROOT_FOLDER, 'archive')
                    )
parser.add_argument('--temporaryfolder',
                    help='Temporary folder for ongoing downloads.',
                    required=False,
                    default='/tmp'
                    )
parser.add_argument('--outputfolder',
                    help='Output folder to put downloaded files when '
                         'finished.',
                    required=True
                    )
parser.add_argument('--whitelist',
                    help='Selected programs to be downloaded.',
                    required=True,
                    )
args = parser.parse_args()

# Path specifications
# TODO use the pathlib library to open files etc.
ARCHIVE_FOLDER = os.path.abspath(str(args.archivefolder))
TEMPORARY_FOLDER = os.path.abspath(str(args.temporaryfolder))
OUTPUT_FOLDER = os.path.abspath(str(args.outputfolder))
WHITELIST = os.path.abspath(str(args.whitelist))

# Definitions and parsing specifications
socket.setdefaulttimeout(15)
if args.verbosity == 2:
    logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s',
                        level=logging.INFO, datefmt='%Y/%m/%d %H:%M')
elif args.verbosity == 1:
    logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s',
                        level=logging.ERROR, datefmt='%Y/%m/%d %H:%M')

def main():
    """Main function to download music from WREK."""

    # Wait for change day for them to update their data base.
    #
    # TODO: What is the purpose of this func?
    # TODO: does this make sense? If we are offsetting the days (like waiting
    # for two days to download) we are covered against this problem.
    # TODO: maybe this could be called in between each downloads in case they
    # take a long time.
    auxf.wait_for_change_day()

    # Initialize shows.
    all_wrek_shows = parse_wrek_website.initialize_shows()

    # Initialize whitelist.
    whitelist = auxf.create_whitelist(WHITELIST)

    # Remove non whitelisted programs
    whitelisted_wrek_shows = [x for x in all_wrek_shows if x.name in whitelist]

    for show in whitelisted_wrek_shows:
        show.download(
            temporary_directory=TEMPORARY_FOLDER,
            download_old_archive=True)

if __name__ == '__main__':
    main()
