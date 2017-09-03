"""Auxiliar functions for the main program."""

import datetime
import time
import re
import os
import logging
import shutil


def wait_for_change_day():
    u"""Wait to change for the next day.

    This function is deprecated and will be removed in future versions. The
    idea behind wait_for_change_day is that WREK may update its website during
    the change of the day but having a threshold of days already prevents this
    problem of downloading a link which has been recently updated.

    Arguments:
        (empty)

    Returns:
        None.

    """
    if (datetime.datetime.now().hour == 23 and
            datetime.datetime.now().minute >= 50):
        print('Waiting for day to change')
        time.sleep(15*60)
        return True
    else:
        return False
    return None


def create_whitelist(whitelistpath):
    u"""Create a whitelist from whitelistpath.

    Programs to be ignored should have their lines starting with a comment (#).

    Arguments:
        whitelistpath (str): path to a text file containing the whitelisted
        programs.

    Returns:
        list: list of all whitelisted programs.

    """
    with open(whitelistpath, 'rt') as f:
        return re.findall('^[^#\s]+?$', f.read(), flags=re.MULTILINE)


def shows_in_whitelist(whitelistpath):
    u"""Show whitelist from whitelistpath. All entries are included.

    In this function all programs will be read. The purpose of this function is
    to allow for the computation of new shows.

    Arguments:
        whitelistpath (str): path to a text file containing the whitelisted
        programs.

    Returns:
        list: list of all programs included in the whitelist.

    """
    with open(whitelistpath, 'rt') as f:
        return sorted(
            [x.replace('#', '').replace('\n', '') for x in f.readlines()])


def check_output_file_exists(
        target_output_folder,
        target_output_file):
    """Check wheter file to be downloaded already exists.

    Arguments:
        target_output_folder (str): path for the output folder.
        target_output_file (str): path for the output folder.

    Returns:
        bool: True if file already exists. False otherwise.

    """
    if os.path.isfile(os.path.join(
            target_output_folder, target_output_file)):
        return True
    else:
        return False


def include_programs_in_whitelist(whitelistpath, list_of_programs_to_include):
    u"""Include a list of new programs in the whitelist file.

    The default behavior is to include them commented so they will not be
    downloaded.

    Arguments:
        whitelistpath (str): path to a text file containing the whitelisted
        programs.

        list_of_programs_to_include (list): a list of program names to include
        in the whitelist file.

    Returns:
        bool: True if function is successful. False otherwise.

    """
    with open(whitelistpath, 'r+') as f:
        raw_programs = (f.readlines()
                        + ['#' + x for x in list_of_programs_to_include])
        f.seek(0)
        program_is_commented = map(
            lambda x: True if x.startswith('#') else False,
            raw_programs)
        programs_without_hash = [x.replace('#', '').replace('\n', '')
                                 for x in raw_programs]
        map_program_to_is_commented = dict(
            zip(programs_without_hash, program_is_commented))
        all_programs = sorted(programs_without_hash)
        all_programs_adj_to_hash = map(
            lambda x: '#' + x if map_program_to_is_commented[x] else x,
            all_programs)
        f.write('\n'.join(all_programs_adj_to_hash))
        f.truncate()
        logging.debug('Included the following programs in whitelist file:\n%s',
                      '\n'.join(list_of_programs_to_include))
    return True


def move_downloaded_file(
        downloaded_file_path,
        destination_path):
    u"""Move the downloaded file to the output folder.

    Arguments:
        downloaded_file_path (str): the path to the downloaded mp3 file.
        destination_path (str): the output folder to put the download mp3
        file.

    Returns:
        bool: True if function is execution is successful. False otherwise.

    """
    shutil.move(downloaded_file_path, destination_path)
    return True
