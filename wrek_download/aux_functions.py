"""Description: auxiliar functions for the main program."""

import datetime
import time
import re
import os


def wait_for_change_day():
    u"""Wait to change for the next day.

    This function is deprecated and will be removed in future versions.
    The idea behind wait_for_change_day is that WREK may update its website
    during the change of the day but having a threshold of days already prevents
    this problem of downloading a link which has been recently updated.

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
        return list(re.findall('^[^#\s]+?$', f.read(), flags=re.MULTILINE))


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
    os.rename(downloaded_file_path, destination_path)

    return True
