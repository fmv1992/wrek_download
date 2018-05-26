![](https://travis-ci.org/fmv1992/wrek_download.svg?branch=dev)

# WREK Downloader

Downloads the archive from http://www.wrek.org/ in mp3.

Music you don't hear on the radio.

## Usage

### Minimal working example

    cd wrek_download/
    python3 ./wrek_download/main.py --outputfolder /tmp/my_music_folder \
                                    --whitelist /tmp/whitelist.txt

### All arguments

    cd wrek_download/
    python3 wrek_download/main.py --help
    -h, --help              show this help message and exit
    --verbose               puts the program in verbose mode.
    --verbosity VERBOSITY
                            sets the verbosity of the program. Use 1 for info,
                            2 for debugging and 3 for errors.
    --outputfolder OUTPUTFOLDER
                            output folder to put downloaded files when
                            finished.
    --whitelist WHITELIST
                            text file with the program names to be downloaded.
    --batch                 if present skip any prompt and follow some
                            default/sane option.
    --n_threads N_THREADS
                            number of threads to use for downloading.

This program downloads the files from the archive formatted with YYYYMMDD
followed by the program number of the day NN followed by the name of the
program and lastly the block of the program (files have 30 minutes). So for
example you will get: `20160506_08_stonehenge_02.mp3` for the Stonehenge
program aired on May 06, 2016 (this file is the third block of the program as
the numbering starts with '00').

## Example of whitelist file:

Lines starting with a `#` are ignored/comments. Thus only the first block of
shows will be downloaded (from 'Inside the Black Box' to 'Friday Night Fish
Fry').

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

- Improve meaningfulness of the tests.
- ~~Download only m3u files present in the whitelist file (thus making the
  downloading phase faster).~~ (v1.1.3)
- ~~Start with a decent archive folder.~~
- ~~Uniformize descriptive strings in python3 main.py --help.~~
- ~~Use tempfile as temporary folder.~~
- ~~Move archive folder and temporary folder inside tempfile folder making both
  disposable.~~
- Kill main process if threads stop running: <https://stackoverflow.com/questions/2829329/catch-a-threads-exception-in-the-caller-thread-in-python>.
    * https://stackoverflow.com/questions/19652446/python-program-with-thread-cant-catch-ctrlc
    * https://stackoverflow.com/questions/8774958/keyerror-in-module-threading-after-a-successful-py-test-run
    * https://stackoverflow.com/questions/42131668/python-thread-terminate-or-kill-in-the-best-way
    * Very hard.
    * Don't kill the threads inside python program; improve your overall method.

## Changelog

### Version 1.1.4

- Parallelize downloads.
    - Added optional argument n_threads to CLI.
    - Added threading to `WREKShow.download`.

### Version 1.1.3

- Added threading to `update_m3u_files`.
- Filtered whitelisted WREK shows prior to calling `update_m3u_files` (thus
  saving time).
- Added several `TODO` tags to existing code.

### Version 1.1.2

- Deprecated the use of `--archivefolder`  and `--temporaryfolder` by using the
  tempfile library.
- Improved the output of `--help` message.
