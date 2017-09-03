"""Update the archive folder with the newest m3u files.

Updates the archive folder with the newest m3u files.
Then updates the whitelist file as well to include new programs and move the
deprected programs to the end.
It moves the old, deprecated m3u files to archive_deprecated_folder.

"""

# pylama:ignore=W0611,W0511
# TODO: put logging where needed
# TODO: Notificate user that a new show is available
import os
import re
import shutil
import logging
import urllib.request
import aux_functions as auxf


def update_m3u_files(constants, filtered_wrek_shows):
    u"""Update the archive folder with the newest m3u files.

    Downloads WREK website and parses it using regular expressions.

    Arguments:
        # TODO
        (empty)

    Returns:
        bool: True if function runs sucessfully. False otherwise.


    """
    # Setting up HTTP object, WREK website as text and local m3u files.
    logging.debug('Contacting WREK website at %s', constants['URL_WREK'])
    h = urllib.request.urlopen(constants['URL_WREK'], cafile=None, capath=None)
    response, content = (h.status, h.read())
    del response
    text = content.decode()

    # Find the name of all m3u files that are 128kbps.
    remote_m3u_file_names = re.findall('(?<=current\/)[^>]*?\.m3u(?=\">128k<)',
                                       text)

    # Get remote m3u files content.
    remote_m3u_content = dict()
    for one_show in [show for show in filtered_wrek_shows if
                     show.m3u_filename in remote_m3u_file_names]:
        m3u = one_show.m3u_filename
        show_name = one_show.name
        h = urllib.request.urlopen(constants['URL_M3U'] + m3u)
        remote_m3u_content[m3u] = h.read().decode()
        logging.debug('Added %s (%s) to m3u list.', m3u, show_name)
    # logging.debug('Got all remote m3u file contents.')
    # Put old suffix in every mp3 file as all the programs supposes that
    # they come with this prefix
    # TODO: this regex needs testing
    # We are putting old in all remote files in order to uniformize our archive
    # and because the program suposes that files have '_old' in them.
    remote_m3u_content = {k: re.sub('(?<!_old)\.mp3', '_old.mp3', v) for k, v
                          in remote_m3u_content.items()}

    # Default behavior is to add extra programs and disregard spurious ones.
    for m3u in remote_m3u_content:
        with open(
                os.path.join(constants['ARCHIVE_FOLDER'],
                             m3u),
                'wt') as f:
            f.write(remote_m3u_content[m3u])
    return True


if __name__ == '__main__':
    update_m3u_files()
