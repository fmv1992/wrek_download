"""
Parse WREK website correctly identifying shows and their important attributes.

Create a Show object with all meaningful information regarding that show.

Classes:
    Show: WREK radio show with meaningful attributes.
    Cl2: one line description.

Functions:
    func1: one line description.
    func2: one line description.

Exceptions:
    except1: one line description.
    except2: one line description.

Examples:
    >>> print('hello world')

References:
    [1] - Author, Work.
    [2] - Author, Work.

"""
# pylama:skip=1
# pylama:ignore=W:ignore=C101
import httplib2
import urllib
import os
import re
import string
import datetime
import logging

WEEKDAYS = [ 'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
        'saturday',
        'sunday',
           ]


# TODO: this class is lacking modularity.
# Each function should do one thing well:
#   Download
#   Move

class WREK_Show(object):
    u"""WREK radio show object.

    Methods:
        download: Download all the mp3 files in the m3u file.

    Attributes:
        begin_time (str): begin time in format 00:00 AM.
        end_time (str): end time in format 00:00 AM.
        m3u_filename (str): the filename for the m3u file.
        name (str): show name.
        show_number_in_day (int): the numbering of the show in the day (starting
        from zero).
        weekday (str): weekday in which the show is aired.

    """

    # TODODONE: Function to check wheter the target file already exists
    # TODO: Function to download one line of the m3u file
    # TODO: Function to move this downloaded file
    # TODO: Global functio to call all those three

    def __init__(self,
                 name,
                 weekday,
                 begin_time,
                 end_time,
                 m3u_filename,
                 show_number_in_day):
        u""" The init function for this class."""

        self.begin_time = begin_time
        self.end_time = end_time
        self.m3u_filename = m3u_filename
        self.name = name
        self.show_number_in_day = show_number_in_day
        self.weekday = weekday


    def _check_output_file_exists(
            self,
            target_output_folder,
            target_output_file):
        """Checks wheter file to be downloaded already exists.

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


    def _download_one_file_from_m3u_file(
            self,
            target_output_folder,
            dowload_url,
            line_number_in_the_m3u_file
            is_archive_file=False):
        u"""Download the file from the URL given and name it accordingly.

        Arguments:
            target_output_folder (str): path for the output folder.
            download_url (str): url to download.
            line_number_in_the_m3u_file (int): line number in the m3u file.
            Important because of file naming.

        Returns:
            bool: True if no errors happened during execution.

        """
        def _create_filename(
                self,
                line_number_in_the_m3u_file,
                is_archive_file=is_archive_file):
            """Create a unique filename for each show based on its attributes.

            Create a filename of the format:
                yyyymmdd_pn_programname_bn.mp3
            where:
                'yyyy' is the year of the program.
                'mm' is the month of the program.
                'dd' is the day of the program.
                'pn' is the program number of the program in that day. 00 for
                the first program.
                'programname' is the program name.
                'bn' is the block number. WREK's show are composed of half hour
                blocks so a full day would have 2 * 24 = 48 blocks

            Arguments:
                download_old_archive (bool): True to download files from the
                old archive. False to download only files from the most
                recent week.

            Returns:
                str: the show's name.

            """
            now = datetime.datetime.now()
            aired_day = datetime.datetime.now()
            # The following variable gives a safety margin to skip downloads
            # occuring too close to today's date. WREK might not update their
            # website so often.
            threshold_to_skip_download = datetime.timedelta(2)  # In days.

            while aired_day.weekday() != WEEKDAYS.index(self.weekday):
                aired_day -= datetime.timedelta(days=1)
            if now - aired_day <= threshold_to_skip_download:
                # TODO: fix this for 'old' in name.
                # logging.info('Skipping program {0} due to closeness with today\'s date'.format(self.name))
                # return Fals
                pass
            if is_archive_file:
                aired_day -= 7 * datetime.timedelta(days=1)

            name = (str(aired_day.year)
                    + '{0:02d}'.format(aired_day.month)
                    + '{0:02d}'.format(aired_day.day) + '_'
                    + '{0:02d}'.format(self.show_number_in_day) + '_'
                    + self.name + '_'
                    + '{0:02d}.mp3'.format(line_number_in_the_m3u_file)
                    + '.mp3')

            return name


        if is_archive_file:
            download_url = m3ufile.readline().replace('_old', '')


    def _move_downloaded_file(
            self,
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


    def download(
            self,
            destination_path,
            temporary_directory,
            download_old_archive=True):
        u"""Download the mp3 files referenced by the m3u file of the program.

        The procedure for downloading is the following:
            1) Check wheter destination file exists. If True then skip this download.
            2) Download the file.
            3) Move the file.

        Arguments:
            (empty)

        Returns:
            bool: True if function runs successfully. False otherwise.

        """



    def OLD_download(
            self,
            destination_directory,
            temporary_directory='/tmp',
            download_old_archive=True):
        u"""Download all the mp3 files in the m3u file.

        Download the mp3 file contained in the m3u file using a temporary
        directory and moving finished downloaded files to a destination
        directory. Name them accordingly.

        Arguments:
            destination_directory (str): the output folder for the downloaded
            files.
            temporary_directory (str): the temporary folder to hold the files
            while they are being downloaded.
            download_old_archive (bool): True to download files from the old
            archive. False to download only files from the most recent week.

        Returns:
            bool: True if the function ran without errors.

        """

        destination_directory = os.path.abspath(destination_directory)
        if not os.path.isdir(destination_directory):
            raise FileNotFoundError('Folder {0} does not exist'.format(
                destination_directory))
        if download_old_archive == True:
            pass
        # if not filename:  # In case filename gets False.
            # return False
        # TODO: check oif file already exists in destination folder

        with open(
                os.path.join(
                    os.path.dirname(
                        os.path.dirname(
                            os.path.realpath(__file__))),
                    'archive',
                    self.m3u_filename),
                'rt') as m3ufile:
            nr_line = 0
            line = m3ufile.readline().replace('_old', '')

            if download_old_archive:
                iterate_over_old = (True, False)
            else:
                iterate_over_old = (False, )
            for download_old_archive in iterate_over_old:
                while line != '':
                    filename = create_filename(self, download_old_archive)
                    filename = filename.replace('.mp3', '{0:02d}.mp3'.format(nr_line))
                    if download_old_archive:
                        line = line.replace('.mp3', '_old.mp3')
                    try:
                        urllib.request.urlretrieve(
                            line,
                            filename=os.path.join(
                                temporary_directory,
                                filename,
                                ))
                        if destination_directory != temporary_directory:
                            os.rename(os.path.join(temporary_directory, filename),
                                        os.path.join(destination_directory, filename))
                    # TODO: improve this excpetin.
                    except Exception as e:
                        pass
                    # Update numbers and loop
                    nr_line += 1
                    line = m3ufile.readline().replace('_old', '')
        return True


def parse_wrek_website(url='http://www.wrek.org/schedule/'):
    u"""Parse WREK Atlanta website.

    Parse WREK Atlanta website using a set of regular expressions to properly
    initialize each program and its attributes.

    Arguments:
        url (str): URL string of the website to be parsed.

    Returns:
        dict: the dictionary containing keys for each of WREK's shows'
        attributes and a list of values.
            keys: begin_times, end_times, m3u_urls, names
            values: list of lists of strings. The first level of the list
            corrisponds to each day of the week starting from Monday.

    """
    def filter_non_allowed_chars(x,
            allowed=string.ascii_letters + string.digits + '_'):
        u"""Filters out non allowed chars."""
        x = re.sub('[^{0}]+'.format(allowed), '_', x.lower())
        x = re.sub('_$', '', x)
        return x
    TMPDIR = '/tmp'
    h = httplib2.Http(os.path.join(TMPDIR, '.wrek_cache'))
    response, content = h.request(url)
    weekdays = re.findall(
        'schedule-day' + '.*?' + 'grid_3',
        content.decode())
    parsed_times = [re.findall('(?<=schedule-time">)(.+?)<',
                               x) for x in weekdays]
    begin_times = [['00:00 AM'] + x for x in parsed_times]
    end_times = [x[1:] + ['11:59 PM'] for x in parsed_times]
    names = [re.findall('(?<=schedule-show">)(.+?)<', x) for x in weekdays]
    names = list(list(map(filter_non_allowed_chars, n)) for n in names)
    parsed_m3u_urls = [
        re.findall('(?<=schedule-archive"><a href="/playlist\.php/main/128kbs/'
                   'current/)(.+?)">', x) for x in weekdays]
    attributes_to_show_object = {
        'begin_times': begin_times,
        'end_times': end_times,
        'names': names,
        'm3u_urls': parsed_m3u_urls
    }
    return attributes_to_show_object


def initialize_shows():
    u"""Initialize all the shows objects.

    Arguments:
        (no arguments)

    Returns:
        list: A list full list of WREK_Show objects.

    """
    all_shows = []
    parsed_shows_data = parse_wrek_website()
    # Adjusing m3u
    for index_day, weekday in enumerate(WEEKDAYS):
        for index_program, program in enumerate(
                parsed_shows_data['names'][index_day]):
            all_shows.append(
                WREK_Show(
                    program,
                    weekday,
                    parsed_shows_data['begin_times'][index_day][index_program],
                    parsed_shows_data['end_times'][index_day][index_program],
                    parsed_shows_data['m3u_urls'][index_day][index_program],
                    index_program))
    return all_shows
