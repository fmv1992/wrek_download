"""
Download archives from WREK Atlanta student radio.

The idea is to create a timeline from the days prior to today (so today and
the two previous days are excluded as a safeguard measure for the WREK to
update their website)
and start downloading from the most distant day until the aforementioned day.

For example if today is 25 october the last available day is
12 october.
The range of downloading days should be 12 october untill 22 october
(inclusive).
"""

# TODO: add flexibility for not to depent of external libraries (urllib if I'm
# not wrong)
# TODO: download an entire week of WREK and check if there are 48 files.
# TODO: create a notify flag to permanently notify the user of a new program.
import os
import socket
import logging
import argparse
import aux_functions as auxf
import parse_wrek_website
import update_m3u_files

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
                         'Use 1 for info, 2 for debugging and 3 for errors.',
                    type=int, default=1)
parser.add_argument('--archivefolder',
                    help='Archive folder where the m3u files are.',
                    required=False,
                    default=os.path.join(ROOT_FOLDER, 'archive'))
parser.add_argument('--temporaryfolder',
                    help='Temporary folder for ongoing downloads.',
                    required=False,
                    default='/tmp')
parser.add_argument('--outputfolder',
                    help='Output folder to put downloaded files when '
                         'finished.',
                    required=True)
parser.add_argument('--whitelist',
                    help='Selected programs to be downloaded.',
                    required=True,)
parser.add_argument('--batch',
                    help='If present skip any prompt and follow some '
                    'default/sane option.',
                    action="store_true",
                    required=False,
                    default=False)
args = parser.parse_args()

# Path specifications
ARCHIVE_FOLDER = os.path.abspath(args.archivefolder)
DEPRECATED_ARCHIVE_FOLDER = os.path.abspath(
    os.path.join(ARCHIVE_FOLDER, 'deprecated_m3u_files'))
TEMPORARY_FOLDER = os.path.abspath(args.temporaryfolder)
OUTPUT_FOLDER = os.path.abspath(args.outputfolder)
WHITELIST_FILE = os.path.abspath(args.whitelist)
BATCH_MODE = args.batch

# Constants
URL_WREK = 'http://www.wrek.org/schedule/'
URL_M3U = 'http://www.wrek.org/playlist.php/main/128kbs/current/'

# Definitions and parsing specifications
socket.setdefaulttimeout(15)
if args.verbosity == 1:
    logging.basicConfig(format='%(levelname)s:%(asctime)s: %(message)s',
                        level=logging.INFO, datefmt='%Y/%m/%d %H:%M')
elif args.verbosity == 2:
    logging.basicConfig(format='%(levelname)s:%(asctime)s: %(message)s',
                        level=logging.DEBUG, datefmt='%Y/%m/%d %H:%M')
elif args.verbosity == 3:
    logging.basicConfig(format='%(levelname)s:%(asctime)s: %(message)s',
                        level=logging.ERROR, datefmt='%Y/%m/%d %H:%M')


def main():
    """Main function to download music from WREK."""
    # Initialize shows.
    all_wrek_shows = parse_wrek_website.initialize_shows()
    all_wrek_shows_names = sorted(set([x.name for x in all_wrek_shows]))
    logging.info('Initialized shows.')
    logging.debug('All shows:\n%s',
                  '\n'.join(all_wrek_shows_names))

    # Initialize whitelist.
    whitelist = auxf.create_whitelist(WHITELIST_FILE)
    logging.debug('Whitelist:\n%s', '\n'.join(sorted(whitelist)))

    # Remove non whitelisted programs
    whitelisted_wrek_shows = [x for x in all_wrek_shows if x.name in whitelist]
    logging.info('Initialized whitelist:\n%s', (
        '\n'.join(sorted(set([x.name for x in whitelisted_wrek_shows])))))

    # Show new programs
    set_of_new_programs = (
        set(all_wrek_shows_names)
        - set(auxf.shows_in_whitelist(WHITELIST_FILE)))
    if set_of_new_programs:
        logging.info('New shows not included in the whitelist:\n%s',
                     '\n'.join(sorted(set_of_new_programs)))
        # Here the default is to include the new program in a comment in the
        # whitelist file and create a file warning for new programs.
        if BATCH_MODE:
            auxf.include_programs_in_whitelist(
                WHITELIST_FILE,
                sorted(set_of_new_programs))
        else:
            if input('Do you want to include the new programs in your '
                     'whitelist file? [y/n]\n') == 'y':
                auxf.include_programs_in_whitelist(
                    WHITELIST_FILE,
                    sorted(set_of_new_programs))

    for show in whitelisted_wrek_shows:
        show.download(
            temporary_directory=TEMPORARY_FOLDER,
            download_old_archive=True)
        logging.debug('Downloaded all files for show %s',
                      str(show))


if __name__ == '__main__':
    update_m3u_files.update_m3u_files()
    main()
