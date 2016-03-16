# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 19:48:42 2015

@author: monteiro

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
# imports
from datetime import datetime as dt
import os
import aux_functions as auxf
from lists import week, whitelist, program_names
import socket
import urllib.request
import logging
import argparse

# parsing
parser = argparse.ArgumentParser()
parser.add_argument('--verbose', help='puts the program in verbose mode',
                    action="store_true", default=False)
parser.add_argument('--verbosity', help='sets the verbosity of the program. '
                                        'Use 1 for error and 2 for info',
                    type=int, default=1)
args = parser.parse_args()

# definitions and parsing specifications
tmp_dir = '/tmp'
dest_dir = os.path.expandvars('$HOME/music/wrek_atlanta')
socket.setdefaulttimeout(15)
if args.verbosity == 2:
    logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s',
                        level=logging.INFO, datefmt='%Y/%m/%d %H:%M')
elif args.verbosity == 1:
    logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s',
                        level=logging.ERROR, datefmt='%Y/%m/%d %H:%M')

# body
auxf.wait_for_change_day()
# creating a black list from whitelist; it is easier this way
black_list = []
whitelist = whitelist()
for program in program_names.values():
    if program not in whitelist:
        black_list.append(program)
logging.info('Skipping black listed programs: %s', '\n'.join(black_list))

for sub in [True, False]:
    for day in week:
        for (nr_program, program) in enumerate(day):
            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   'archive', program), 'rt') as m3ufile:
                nr_line = 0
                line = m3ufile.readline()
                while line != '':
                    if sub is False:
                        line = line.replace('_old', '')
                    # creates filename
                    filename = auxf.filename(line, program, nr_program,
                                             nr_line)
                    if auxf.is_blacklisted(filename, black_list) is True:
                        logging.info('Skipping %s since it is blacklisted.',
                                     filename)
                    else:
                        # checks if program is within acceptable range.
                        if auxf.date_is_in_range(dt(int(filename[0:4]),
                           int(filename[4:6]), int(filename[6:8]))) is True:
                            # check if exists
                            if os.path.isfile(os.path.join(dest_dir,
                                                           filename)) is True:
                                logging.info('File %s already exists.'
                                             'Skipping.',
                                             os.path.join(dest_dir, filename))
                            else:
                                # downloads to tmp dir
                                logging.info('Downloading %s from %s',
                                             filename, line[:-1])
                                try:
                                    urllib.request.urlretrieve(line,
                                                 filename=os.path.join(tmp_dir,
                                                                     filename))
                                    # move to final dir
                                    os.rename(os.path.join(tmp_dir, filename),
                                              os.path.join(dest_dir, filename))
                                    logging.info('Done downloading %s',
                                                 filename)
                                except urllib.error.HTTPError:
                                    logging.error('Could not download {0} '
                                          'due to HTTP Error'.format(filename))
                    # update numbers and loop
                    nr_line += 1
                    line = m3ufile.readline()
