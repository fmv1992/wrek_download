"""Download archives from WREK Atlanta student radio.

The idea is to create a timeline from the days prior to today (so today and
the two previous days are excluded as a safeguard measure for the WREK to
update their website)
and start downloading from the most distant day until the aforementioned day.

For example if today is 25 october the last available day is
12 october.
The range of downloading days should be 12 october untill 22 october
(inclusive).
"""

# TODO: download an entire week of WREK and check if there are 48 files.
import sys
import time
import queue
import threading

# For error handling.
import urllib
import socket

from datetime import datetime as dt
import argparse
import logging
import os
import tempfile

import aux_functions as auxf
import parse_wrek_website
import update_m3u_files


def threaded_download():
    """Call WREKShow download."""
    while True:
        self_download_kwargs = download_queue.get()
        if self_download_kwargs is None:
            break
        else:
            show = self_download_kwargs.pop('show')
            try:
                show.download(**self_download_kwargs)
                sucessful_queue.put(1)
            except urllib.error.URLError as urlexception:
                exception_queue.put(1)
                raise urlexception
            except socket.timeout as timeoutexception:
                exception_queue.put(1)
                raise timeoutexception
            logging.debug('Downloaded all files for show %s', str(show))
            download_queue.task_done()


def parse_cli_arguments():
    """Parse command line arguments for the main program."""
    # Parsing
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--verbose',
        help='puts the program in verbose mode.',
        action="store_true",
        default=False)
    parser.add_argument(
        '--verbosity',
        help='sets the verbosity of the program. Use 1 for info, 2 for '
             'debugging and 3 for errors.',
        type=int,
        default=1)
    parser.add_argument(
        '--outputfolder',
        help='output folder to put downloaded files when '
        'finished.',
        required=True)
    parser.add_argument(
        '--whitelist',
        help='text file with the program names to be downloaded.',
        required=True,)
    parser.add_argument(
        '--batch',
        help='if present skip any prompt and follow some '
        'default/sane option.',
        action="store_true",
        required=False,
        default=False)
    parser.add_argument(
        '--n_threads',
        help='number of threads to use for downloading.',
        action="store",
        type=int,
        required=False,
        default=3)

    args = parser.parse_args()

    return args


def define_constants(arguments):
    """Define constants for this program."""
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
    # ARCHIVE_FOLDER = os.path.abspath(arguments.archivefolder)
    # DEPRECATED_ARCHIVE_FOLDER = os.path.abspath(
    #     os.path.join(ARCHIVE_FOLDER, 'deprecated_m3u_files'))
    # TEMPORARY_FOLDER = os.path.abspath(arguments.temporaryfolder)

    TEMPORARY_FOLDER = tempfile.TemporaryDirectory(prefix='wrek_download_tmp')
    # TODO: print parsed command line arguments. Not just temp folder.
    logging.debug('Temporary folder is: %s.', TEMPORARY_FOLDER.name)
    ARCHIVE_FOLDER = os.path.join(TEMPORARY_FOLDER.name, 'archive')
    os.mkdir(ARCHIVE_FOLDER)
    TEMP_DOWNLOAD_FOLDER = os.path.join(TEMPORARY_FOLDER.name, 'temp_download')
    os.mkdir(TEMP_DOWNLOAD_FOLDER)
    # print(tuple(os.walk(TEMPORARY_FOLDER.name)))

    OUTPUT_FOLDER = os.path.abspath(arguments.outputfolder)
    WHITELIST_FILE = os.path.abspath(arguments.whitelist)
    BATCH_MODE = arguments.batch
    N_THREADS = arguments.n_threads

    # Test if target folders exist and whitelist file.
    LIST_OF_ARGUMENTS_FOLDERS = [ARCHIVE_FOLDER, TEMP_DOWNLOAD_FOLDER,
                                 OUTPUT_FOLDER]
    for one_folder in LIST_OF_ARGUMENTS_FOLDERS:
        if not os.path.isdir(one_folder):
            raise FileNotFoundError('One of the arguments: \'{0}\' does '
                                    'not exist.'.format(one_folder))
    if not os.path.isfile(WHITELIST_FILE):
        raise FileNotFoundError('Whitelist file \'{0}\' does not'
                                'exist.'.format(WHITELIST_FILE))

    # Constants
    URL_WREK = 'http://www.wrek.org/schedule/'
    URL_M3U = 'http://www.wrek.org/playlist.php/main/128kbs/current/'

    constants = {
        'ROOT_FOLDER': ROOT_FOLDER,
        'WEEKDAYS': WEEKDAYS,
        'ARCHIVE_FOLDER': ARCHIVE_FOLDER,
        # Note that if TEMPORARY_FOLDER is not passed here it ceases to exist.
        'TEMPORARY_FOLDER': TEMPORARY_FOLDER,
        'TEMP_DOWNLOAD_FOLDER': TEMP_DOWNLOAD_FOLDER,
        'OUTPUT_FOLDER': OUTPUT_FOLDER,
        'WHITELIST_FILE': WHITELIST_FILE,
        'BATCH_MODE': BATCH_MODE,
        'N_THREADS': N_THREADS,
        'URL_WREK': URL_WREK,
        'URL_M3U': URL_M3U}

    return constants


def setup_logging():
    """Set up logging options."""
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


def initialize_all_wrek_shows(constants):
    """Initilialize all wrek shows."""
    # Initialize shows.
    all_wrek_shows = parse_wrek_website.initialize_shows(constants)
    all_wrek_shows_names = sorted(set([x.name for x in all_wrek_shows]))
    logging.info('Initialized shows.')
    logging.debug('All shows:\n%s',
                  '\n'.join(all_wrek_shows_names))
    return all_wrek_shows


def filter_whitelisted_shows(constants, all_wrek_shows):
    """Filter wrek shows according to a whitelist file."""
    # Initialize whitelist.
    whitelist = auxf.create_whitelist(constants['WHITELIST_FILE'])
    logging.debug('Whitelist:\n%s', '\n'.join(sorted(whitelist)))

    # Remove non whitelisted programs
    whitelisted_wrek_shows = [x for x in all_wrek_shows if x.name in whitelist]
    # Sort days to start with oldest day so the program that is most near to
    # deletion is downloaded first.
    whitelisted_wrek_shows = sorted(
        whitelisted_wrek_shows,
        key=lambda x: (constants['WEEKDAYS'].index(x.weekday) -
                       dt.now().weekday() - 1) % 7)
    logging.debug('Initialized whitelist:\n%s', (
        '\n'.join(sorted(set([x.name for x in whitelisted_wrek_shows])))))

    return whitelisted_wrek_shows


def main(constants, all_wrek_shows, filtered_wrek_shows):
    """Download music from constants['WREK']."""
    all_wrek_shows_names = [show.name for show in all_wrek_shows]
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

    download_threads = []
    for _ in range(constants['N_THREADS']):
        t = threading.Thread(target=threaded_download)
        t.start()
        download_threads.append(t)

    # Populate show queue.
    for download_old in (True, False):
        for one_show in filtered_wrek_shows:
            download_queue.put(
                dict(show=one_show,
                     temporary_directory=constants['TEMPORARY_FOLDER'],
                     download_old_archive=download_old))

    # Wait for workers to execute their job.
    # TODO: define a timeout argument.
    timeout = 2
    stop = time.time() + timeout
    while ((download_queue.unfinished_tasks and time.time() < stop)
           and
           (exception_queue.qsize() < constants['N_THREADS'])):
        time.sleep(1)

    for _ in range(constants['N_THREADS']):
        download_queue.put(None)
    for i in range(constants['N_THREADS']):
        download_threads[i].join()

    # Evaluate termination condition of the main program.
    if not exception_queue.qsize() < constants['N_THREADS']:
        logging.debug('All threads ({0}} have died. Exit code: 1.'.format(
            exception_queue.qsize()))
        return 1
    elif download_queue.unfinished_tasks:
        logging.debug('Program timed out. Exit code: 2.')
        return 2
    else:
        download_queue.join()
        logging.debug('Program execution sucessful. Exit code: 0.')
        return 0


if __name__ == '__main__':
    args = parse_cli_arguments()
    setup_logging()
    constants = define_constants(args)
    all_wrek_shows = initialize_all_wrek_shows(constants)
    filtered_wrek_shows = filter_whitelisted_shows(constants, all_wrek_shows)
    update_m3u_files.update_m3u_files(constants, filtered_wrek_shows)
    download_queue = queue.Queue()
    exception_queue = queue.Queue()
    sucessful_queue = queue.Queue()
    return_code = main(constants, all_wrek_shows, filtered_wrek_shows)
    sys.exit(return_code)
