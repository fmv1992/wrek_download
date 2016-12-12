# Wrek Downloader
Downloads the archive from http://www.wrek.org/ in mp3.

Music you don't hear on the radio.

## Travis CI status
[![Build Status](https://travis-ci.org/fmv1992/wrek_download.svg?branch=develop)](https://travis-ci.org/fmv1992/wrek_download)

## Usage
    cd wrek_download/
    
    python3 wrek_download/main.py --help
    
    usage: main.py [-h] [--verbose] [--verbosity VERBOSITY]
    
    optional arguments:
      -h, --help            show this help message and exit
      --verbose             puts the program in verbose mode
      --verbosity VERBOSITY
                            sets the verbosity of the program. Use 1 for error and
                            2 for info
The program then downloads the files from the archive formated with YYYYMMDD followed by the program number of the day NN followed by the name of the program and lastly the block of the program (files have 30 minutes). So for example you will get: `20160506_08_stonehenge_02.mp3` for the Stonehenge program aired on May 06, 2016 (this file is the third block of the program as the numbering starts with '00').
## Example of whitelist file:
    inside_the_black_box
    sunday_special
    stonehenge
    mobius
    high_end_theory
    back_alley_pork_roost
    friday_night_fish_fry


    ###################
    #north_avenue_lounge
    #weekend_cornucopia
    #the_longboards_show
    #bobs_slacktime_funhouse
    #kosher_noise
    #new_forces
    #rock_rythm_and_roll
    #between_the_lines
    #alternative_radio
    #planetary_radio
    #friction
    #radio_bomb
    #hour_of_slack
    #just_jazz
    #fifty_four_forty_six
    #live_at_wrek
    #atmospherics
    #mode_seven
    #coffee_and_sushi
    #tapas_and_tunes
    #shillelagh_law
    #inside_the_black_box
    #mobius
    #the_best_of_our_knowledge
    #lost_in_the_stacks
    #underground_recordings
    #electric_boogaloo
    #personality_crisis
    #edm_sound_system
    #blue_plate_special
    #back_alley_pork_roost
    #tech_nation
    #sub_saharan_vibes
    #high_end_theory
    #country_classics
    #wrekroom_renaissance
    #fifty_one_percent
    #gold_soundz
    #cambridge_forum
    #rambling_wrek_report
    #techniques
    #the_desoto_hour
    #sci_fi_lab
    #overnight_alternatives
    #this_way_out
    #freakers_balls
    #classics
    #sunday_special
    #a_bit_off_broadway
    #friday_night_fish_fry
    #wrekage
    #destroy_all_music
    #stonehenge
    #psych_out

## TODO

- *Update this readme/documentation*

- improve verbosity functionality
- rely on pathlib only instead of a mix of pathlib and strings
	- on hold since pathlib may be removed from stdlib
- put whitelitest file as an argument
- remove blacklist from code
- get m3u files from website (the program should update itself)

