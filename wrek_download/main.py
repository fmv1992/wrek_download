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
from datetime import datetime as dt
import update_m3u_files


def parse_cli_arguments():
    u"""Parse command line arguments for the main program."""

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

    # TODO: add an argument for putting new programs to download on whitelist or
    # just put them on #program_name
    args = parser.parse_args()

    return args


def define_constants(arguments):
    u"""Define constants for this and other modules."""

    ROOT_FOLDER = os.path.dirname(
            os.path.dirname(
                        os.path.abspath(__file__)))

    # TODO: already declared somewhere, jsut to cover a hole.
    WEEKDAYS = ['monday',  # This is day zero
                'tuesday',
                'wednesday',
                'thursday',
                'friday',
                'saturday',
                'sunday']
    # Path specifications
    ARCHIVE_FOLDER = os.path.abspath(arguments.archivefolder)
    DEPRECATED_ARCHIVE_FOLDER = os.path.abspath(
        os.path.join(ARCHIVE_FOLDER, 'deprecated_m3u_files'))
    TEMPORARY_FOLDER = os.path.abspath(arguments.temporaryfolder)
    OUTPUT_FOLDER = os.path.abspath(arguments.outputfolder)
    WHITELIST_FILE = os.path.abspath(arguments.whitelist)
    BATCH_MODE = arguments.batch

    # Test if target folders exist and whitelist file.
    LIST_OF_ARGUMENTS_FOLDERS = [ARCHIVE_FOLDER, DEPRECATED_ARCHIVE_FOLDER,
                            TEMPORARY_FOLDER, OUTPUT_FOLDER]
    for one_folder in LIST_OF_ARGUMENTS_FOLDERS:
        if not os.path.isdir(one_folder):
            raise FileNotFoundError('One of the arguments: \'{0}\' does '
                                    'not exist.'.format(one_folder))
    if not os.path.isfile(WHITELIST_FILE):
        raise FileNotFoundError('Whitelist file \'{0}\' does not exist.'.format(
            WHITELIST_FILE))

    # Constants
    URL_WREK = 'http://www.wrek.org/schedule/'
    URL_M3U = 'http://www.wrek.org/playlist.php/main/128kbs/current/'

    constants = {
        'ROOT_FOLDER': ROOT_FOLDER,
        'WEEKDAYS': WEEKDAYS,
        'ARCHIVE_FOLDER': ARCHIVE_FOLDER,
        'DEPRECATED_ARCHIVE_FOLDER': DEPRECATED_ARCHIVE_FOLDER,
        'TEMPORARY_FOLDER': TEMPORARY_FOLDER,
        'OUTPUT_FOLDER': OUTPUT_FOLDER,
        'WHITELIST_FILE': WHITELIST_FILE,
        'BATCH_MODE': BATCH_MODE,
        'URL_WREK': URL_WREK,
        'URL_M3U': URL_M3U
    }

    return constants


def setup_logging():
    u"""Setup logging options."""
    # Logging level and format definitions.
    socket.setdefaulttimeout(15)
    if not args.verbose:  # If verbose is false do not log anything.
        logging.disable(logging.CRITICAL)
    else:
        if args.verbosity == 1:
            LOGGING_LEVEL = logging.INFO
        elif args.verbosity == 2:
            LOGGING_LEVEL = logging.DEBUG
        elif args.verbosity == 3:
            LOGGING_LEVEL = logging.ERROR
        MESSAGE_FORMAT = '{levelname: <6}: {asctime}: {message}'
        DATE_FORMAT = '%Y/%m/%d %H:%M'
        logging.basicConfig(
            format=MESSAGE_FORMAT,
            level=LOGGING_LEVEL,
            datefmt=DATE_FORMAT,
            style='{')


def main(constants):
    """Main function to download music from constants['WREK']."""
    # Initialize shows.
    all_wrek_shows = parse_wrek_website.initialize_shows(constants)
    all_wrek_shows_names = sorted(set([x.name for x in all_wrek_shows]))
    logging.info('Initialized shows.')
    logging.debug('All shows:\n%s',
                  '\n'.join(all_wrek_shows_names))

    # Initialize whitelist.
    whitelist = auxf.create_whitelist(constants['WHITELIST_FILE'])
    logging.debug('Whitelist:\n%s', '\n'.join(sorted(whitelist)))

    # Remove non whitelisted programs
    whitelisted_wrek_shows = [x for x in all_wrek_shows if x.name in whitelist]
    # Sort days to start with oldest day so the program that is most near to
    # deletion is downloaded first.
    whitelisted_wrek_shows = sorted(
        whitelisted_wrek_shows,
        key=lambda x: (constants['WEEKDAYS'].index(x.weekday) - dt.now().weekday() -1)%7)
    logging.debug('Initialized whitelist:\n%s', (
        '\n'.join(sorted(set([x.name for x in whitelisted_wrek_shows])))))

    # Show new programs
    set_of_new_programs = (
        set(all_wrek_shows_names)
        - set(auxf.shows_in_whitelist(constants['WHITELIST_FILE'])))
    if set_of_new_programs:
        logging.info('New shows not included in the whitelist:\n%s',
                     '\n'.join(sorted(set_of_new_programs)))
        # Here the default is to include the new program in a comment in the
        # whitelist file and create a file warning for new programs.
        if constants['BATCH_MODE']:
            auxf.include_programs_in_whitelist(
                constants['WHITELIST_FILE'],
                sorted(set_of_new_programs))
        else:
            if input('Do you want to include the new programs in your '
                     'whitelist file? [y/n]\n') == 'y':
                auxf.include_programs_in_whitelist(
                    constants['WHITELIST_FILE'],
                    sorted(set_of_new_programs))

    for download_old in (True, False):
        for show in whitelisted_wrek_shows:
            show.download(
                temporary_directory=constants['TEMPORARY_FOLDER'],
                download_old_archive=download_old)
            logging.debug('Downloaded all files for show %s',
                        str(show))


if __name__ == '__main__':
    args = parse_cli_arguments()
    constants = define_constants(args)
    setup_logging()
    update_m3u_files.update_m3u_files(constants)
    main(constants)
