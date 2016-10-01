u"""
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

class WREK_Show(object):
    u"""WREK radio show object."""

    def __init__(
            self,
            name,
            weekday,
            begin_time,
            end_time,
            m3u_filename,
            show_number_in_day):
        self.name = name
        self.weekday = weekday
        self.begin_time = begin_time
        self.end_time = end_time
        self.m3u_filename = m3u_filename
        self.show_number_in_day = show_number_in_day

    def download(self, destination_directory, temporary_directory='/tmp', download_old_archive=False):
        u"""Download all the mp3 files in the m3u file."""
        destination_directory = os.path.abspath(destination_directory)
        if not os.path.isdir(destination_directory):
            raise FileNotFoundError('Folder {} does not exist'.format(
                destination_directory))
        if download_old_archive == True:
            pass
        with open(
                os.path.join(
                    os.path.dirname(
                        os.path.dirname(
                            os.path.realpath(__file__))),
                    'archive',
                    self.m3u_filename),
                'rt') as m3ufile:
            nr_line = 0
            line = m3ufile.readline()
            while line != '':
                try:
                    urllib.request.urlretrieve(line,filename=os.path.join(
                            temporary_directory, self.name))
                    # Moves to final dir
                    os.rename(os.path.join(temporary_directory, self.name),
                                os.path.join(destination_directory, self.name))
                except:
                    pass
                # Update numbers and loop
                nr_line += 1
                line = m3ufile.readline()




    def __repr__(self):
            return 'Radio show {0.name} aired on {0.weekday} beginning at {0.begin_time} and ending at {0.end_time}.'.format(self)


def parse_wrek_website(url='http://www.wrek.org/schedule/'):
    u"""Parse WREK Atlanta website."""
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

z = parse_wrek_website()

def initialize_shows():
    u"""Initialize all the shows objects."""
    all_shows = []
    parsed_shows_data = parse_wrek_website()
    for index_day, weekday in enumerate([
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
        'saturday',
        'sunday',
    ]):
        for index_program, program in enumerate(parsed_shows_data['names'][index_day]):
            # print(program)
            all_shows.append(
                WREK_Show(
                    program,
                    weekday,
                    parsed_shows_data['begin_times'][index_day][index_program],
                    parsed_shows_data['end_times'][index_day][index_program],
                    parsed_shows_data['m3u_urls'][index_day][index_program],
                    index_program))
    return all_shows

y = initialize_shows()
p = y[0]
