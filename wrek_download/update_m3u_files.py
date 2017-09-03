"""Update the archive folder with the newest m3u files.

Updates the archive folder with the newest m3u files.
Then updates the whitelist file as well to include new programs and move the
deprected programs to the end.
It moves the old, deprecated m3u files to archive_deprecated_folder.

"""

# pylama:ignore=W0611,W0511
# TODO: put logging where needed
# TODO: Notificate user that a new show is available
import threading
import queue
import os
import re
import shutil
import logging
import urllib.request
import aux_functions as auxf


def threading_worker(constants, queue, dictionary):
    """Create threads for downloading m3u files."""
    while True:
        item = queue.get()
        if item is None:
            break
        else:
            m3u = item.m3u_filename
            url = constants['URL_M3U'] + m3u
            h = urllib.request.urlopen(url)
            website = h.read().decode()
            dictionary[m3u] = website
            show_name = item.name
            logging.debug('Added %s (%s) to m3u list.', m3u, show_name)
            queue.task_done()


def update_m3u_files(constants, filtered_wrek_shows):
    """Update the archive folder with the newest m3u files.

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

    # Start threads and queue.
    url_queue = queue.Queue()
    download_threads = []
    for _ in range(constants['N_THREADS']):
        t = threading.Thread(target=threading_worker,
                             args=(constants, url_queue, remote_m3u_content))
        t.start()
        download_threads.append(t)
    for one_show in [show for show in filtered_wrek_shows if
                     show.m3u_filename in remote_m3u_file_names]:
        url_queue.put(one_show)
    url_queue.join()
    for i in range(constants['N_THREADS']):
        url_queue.put(None)
    for i in range(constants['N_THREADS']):
        download_threads[i].join()

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
