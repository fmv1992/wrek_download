# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 13:23:38 2015

@author: monteiro
"""
import lists
import datetime
import time, os
import re

# paths
archive_folder = os.path.expandvars('$HOME/bin/python/wrek_download/archive')


def wait_for_change_day():
    """Waits if we are near the end of the day. This is done to
    give the website time to update itself."""
    if datetime.datetime.now().hour == 23 and \
       datetime.datetime.now().minute >= 50:
        print('Waiting for day to change')
        time.sleep(15*60)
        return True
    else:
        return False
    return None
    
def date_is_in_range(date, margin=2):
    """Checks if the date given is within the range -14 until -margin
    from today."""
    now = datetime.datetime.now()
    if datetime.datetime(now.year, now.month, now.day)                        \
                                  - date > datetime.timedelta(days=(margin)):
        return True
    else:
        #print(date, 'is not in margin')
        return False
    return None

def return_link(link, date):
    """Returns the link according to the necessity of replacing 'main' with
    'previous'."""
    now = datetime.datetime.now()
    timedelta = now - date
    #print(timedelta.days, now.weekday())
    if timedelta.days <= now.weekday():
        pass
    else:
        link = link.replace('main','previous')
    #print(link)
    return link
    
def filename(link, m3ufilename, program_number, block_number):
    """Creates the filename with:
    yyyymmdd_pn_programname_bn.mp3"""
    now = now = datetime.datetime.now()
    for day in lists.week:
        if m3ufilename in day:
            weekday = lists.week.index(day)
    if weekday > now.weekday():
        new_date = now + datetime.timedelta(days=(-7+weekday-now.weekday()))
    else:
        new_date = now + datetime.timedelta(days=-(now.weekday()-weekday))
    if '_old' in link:
        new_date = new_date + datetime.timedelta(days=-7)
    prg_name = lists.program_names[re.search('[A-Z]{2,4}',
                                         m3ufilename).group(0)]
    name = str(str(new_date.year) + 
       str('{0:02d}'.format(new_date.month)) +
       str('{0:02d}'.format(new_date.day) +
       '_' +
       str('{0:02d}'.format(program_number)) + '_' +
       prg_name + '_' +
       str('{0:02d}'.format(block_number)) +
       '.mp3'))
    return name

#date1 = datetime.datetime.now() - datetime.timedelta(days=-2)
#filename('http:link_previous', 'SSV.m3u', 99, 99 )    
    

    
    
    
    
    
    
    
#def download(days_prior_to_today=1):
#    """Generates a list of file names from 13 days prior to today until
#    days_prior_to_today"""
#    now = datetime.datetime.now()
#    starting_day = now.weekday() - days_prior_to_today
#    new_date = now
#    print(lists.week + lists.week[starting_day:])
#    input()
#    for weekday in lists.week + lists.week[starting_day:]:
#        for (nr_pr, program) in enumerate(weekday):
#            prg_name = lists.program_names[re.search('[A-Z]{2,4}',
#                                                     program).group(0)]
#            with open(str(
#            archive_folder + '/' + program), 'rt') as m3ufile:
#                for (block_number, link) in enumerate(m3ufile.readlines()):
#                    name = str(str(new_date.year) + 
#                       str('{0:02d}'.format(new_date.month)) +
#                       str('{0:02d}'.format(new_date.day) +
#                       '_' +
#                       str('{0:02d}'.format(nr_pr)) + '_' +
#                       prg_name + '_' +
#                       str('{0:02d}'.format(block_number)) +
#                       '.mp3'))
##                    if i < now.weekday() and i >= 1:
##                        pass
##                    else:
##                        link = link.replace('main','previous')
#                    print(link, 'to', name, flush=True)
#                    #input()
#download()                    