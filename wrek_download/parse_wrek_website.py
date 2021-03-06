"""Parse WREK website.

Create a Show object with all meaningful information regarding that show.

# TODO
Classes:
    Show: WREK radio show with meaningful attributes.
    Cl2: one line description.

# TODO
Functions:
    func1: one line description.
    func2: one line description.

# TODO
Exceptions:
    except1: one line description.
    except2: one line description.

# TODO
Examples:
    >>> print('hello world')

# TODO
References:
    [1] - Author, Work.
    [2] - Author, Work.

"""

import urllib.request
import os
import re
import string
import datetime
import aux_functions as auxf
import logging

WEEKDAYS = ['monday',  # This is day zero
            'tuesday',
            'wednesday',
            'thursday',
            'friday',
            'saturday',
            'sunday']


class WREKShow(object):
    """WREK radio show object.

    Methods:
        download: Download all the mp3 files in the m3u file.

    Attributes:
        begin_time (str): begin time in format 00:00 AM.
        end_time (str): end time in format 00:00 AM.
        m3u_filename (str): the filename for the m3u file.
        name (str): show name.
        show_number_in_day (int): the numbering of the show in the day
        (starting from zero).
        weekday (str): weekday in which the show is aired.

    """

    def __init__(self,
                 name,
                 weekday,
                 begin_time,
                 end_time,
                 m3u_filename,
                 show_number_in_day,
                 constants):
        """Initiliaze instance."""
        self.begin_time = begin_time
        self.end_time = end_time
        self.m3u_filename = m3u_filename
        self.name = name
        self.show_number_in_day = show_number_in_day
        self.weekday = weekday
        self.constants = constants

    def _download_one_file_from_m3u_file(
            self,
            target_output_folder,
            download_url,
            line_number_in_the_m3u_file,
            is_archive_file=False):
        """Download the file from the URL given and name it accordingly.

        Arguments:
            target_output_folder (str): path for the output folder.
            download_url (str): url to download.
            line_number_in_the_m3u_file (int): line number in the m3u file.
            Important because of file naming.
            is_archive_file (bool): if the file is from the previous week.

        Returns:
            bool: True if no errors happened during execution.

        """
        if not is_archive_file:
            download_url = download_url.replace('_old', '')
        filename = self._create_filename(line_number_in_the_m3u_file,
                                         is_archive_file)
        try:
            urllib.request.urlretrieve(
                download_url,
                filename=os.path.join(
                    self.constants['TEMP_DOWNLOAD_FOLDER'],
                    filename)
            )
        except urllib.error.HTTPError as error01:
            # TODO: info is not the best choice here
            # TODO: logging is not correct and error's cause is not
            # investigated yet
            logging.info(
                'Could not download {0} due to {1}'.format(
                    self.__repr__(),
                    error01))
            logging.debug(
                'Failed with URL: %s', download_url)
            return False
        return True

    def _create_filename(
            self,
            line_number_in_the_m3u_file,
            is_archive_file):
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
        aired_day = now
        # The following variable gives a safety margin to skip downloads
        # occuring too close to today's date. WREK might not update their
        # website so often.
        threshold_to_skip_download = datetime.timedelta(2)  # In days.

        while (aired_day.weekday()
               != self.constants['WEEKDAYS'].index(self.weekday)):
            aired_day -= datetime.timedelta(days=1)
        if is_archive_file:
            aired_day -= 7 * datetime.timedelta(days=1)
        if now - aired_day <= threshold_to_skip_download:
            return ''

        name = (str(aired_day.year)
                + '{0:02d}'.format(aired_day.month)
                + '{0:02d}'.format(aired_day.day) + '_'
                + '{0:02d}'.format(self.show_number_in_day) + '_'
                + self.name + '_'
                + '{0:02d}.mp3'.format(line_number_in_the_m3u_file))

        return name

    def download(
            self,
            temporary_directory='/tmp',
            download_old_archive=True):
        """Download the mp3 files referenced by the m3u file of the program.

        The procedure for downloading is the following:
            1) Check wheter destination file exists. If True then skip this
            download.
            2) Download the file.
            3) Move the file.

        Arguments:
            (empty)

        Returns:
            bool: True if function runs successfully. False otherwise.

        """
        with open(os.path.join(self.constants['ARCHIVE_FOLDER'],
                               self.m3u_filename),
                  'rt') as m3ufile:
            m3u_file_content = m3ufile.readlines()

        for line_number, m3uline in enumerate(m3u_file_content):
            filename = self._create_filename(line_number, download_old_archive)
            # Filename will return '' for days within threshold to avoid file
            # management problems (we are playing on the safe side here giving
            # WREK staff a couple of days to update their webiste).
            if not filename:
                continue
            if auxf.check_output_file_exists(
                    self.constants['OUTPUT_FOLDER'], filename):
                logging.debug('File %s exists.', filename)
            else:
                logging.debug('File %s does not exist.', filename)
                if self._download_one_file_from_m3u_file(
                            self.constants['TEMP_DOWNLOAD_FOLDER'],
                            m3uline,
                            line_number,
                            download_old_archive):
                    auxf.move_downloaded_file(
                        os.path.join(
                            self.constants['TEMP_DOWNLOAD_FOLDER'],
                            filename),
                        os.path.join(
                            self.constants['OUTPUT_FOLDER'],
                            filename))
                    logging.info('Downloaded show %s.', filename)
                else:
                    return False
        return True

    def __repr__(self):
        """Representation for this object."""
        return ('Radio show {0.name} aired on {0.weekday} beginning '
                'at {0.begin_time} and ending at {0.end_time}.'.format(self))


def parse_wrek_website(url='http://www.wrek.org/schedule/'):
    """Parse WREK Atlanta website.

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
    def filter_non_allowed_chars(
            x,
            allowed=string.ascii_letters + string.digits + '_'):
        """Filter out non allowed chars."""
        x = re.sub('[^{0}]+'.format(allowed), '_', x.lower())
        x = re.sub('_$', '', x)
        return x
    h = urllib.request.urlopen(url)
    content = h.read()
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


def initialize_shows(constants):
    """Initialize all the shows objects.

    Arguments:
        (no arguments)

    Returns:
        list: A list full list of WREKShow objects.

    """
    all_shows = []
    parsed_shows_data = parse_wrek_website()
    # Adjusing m3u
    for index_day, weekday in enumerate(WEEKDAYS):
        for index_program, program in enumerate(
                parsed_shows_data['names'][index_day]):
            all_shows.append(
                WREKShow(
                    program,    # name
                    weekday,    # weekday
                    # begin time
                    parsed_shows_data['begin_times'][index_day][index_program],
                    # end time
                    parsed_shows_data['end_times'][index_day][index_program],
                    # m3u_filename
                    parsed_shows_data['m3u_urls'][index_day][index_program],
                    index_program,  # show number in day
                    constants,  # constants
                ))
    return all_shows
