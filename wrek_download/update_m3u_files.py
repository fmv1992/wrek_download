u"""
Update the archive folder with the newest m3u files.

Updates the archive folder with the newest m3u files.
Then updates the whitelist file as well to include new programs and move the
deprected programs to the end.
It moves the old, deprecated m3u files to archive_deprecated_folder.

"""

# pylama:ignore=W0611,W0511
# TODO: put logging where needed
# TODO: Notificate user that a new show is available
import httplib2
import os
import re
import shutil
import logging
import main
import ssl


def update_m3u_files():
    u"""Update the archive folder with the newest m3u files.

    Downloads WREK website and parses it using regular expressions.

    Arguments:
        (empty)

    Returns:
        bool: True if function runs sucessfully. False otherwise.


    """
    # Setting up HTTP object, WREK website as text and local m3u files.
    try:
        h = httplib2.Http(os.path.join(main.TEMPORARY_FOLDER, '.wrek_cache'))
        response, content = h.request(main.URL_WREK)
        del response
    except ssl.SSLError as sslerror:
        if main.BATCH_MODE:
            raise sslerror
        else:
            if input('SSL CERTIFICATE ERROR: '
                     'Do you want to continue? [y/n]\n') == 'y':
                del h
                h = httplib2.Http(
                    os.path.join(main.TEMPORARY_FOLDER, '.wrek_cache'),
                    disable_ssl_certificate_validation=True)
                response, content = h.request(main.URL_WREK)
                del response
            else:
                raise sslerror
    text = content.decode()
    local_m3u_file_names = [
        f for f in os.listdir(main.ARCHIVE_FOLDER) if
        (os.path.isfile(os.path.join(main.ARCHIVE_FOLDER, f)) and
         (f.endswith('m3u')))]

    # Find the name of all m3u files that are 128kbps.
    remote_m3u_file_names = re.findall('(?<=current\/)[^>]*?\.m3u(?=\">128k<)',
                                       text)

    # Get remote m3u files content.
    remote_m3u_content = dict()
    for m3u in remote_m3u_file_names:
        remote_m3u_content[m3u] = h.request(main.URL_M3U + m3u)[1].decode()
        # Put old suffix in every mp3 file as all the programs supposes that
        # they come with this prefix
    # TODO: this regex needs testing
    # We are putting old in all remote files in order to uniformize our archive
    # and because the program suposes that files have '_old' in them.
    remote_m3u_content = {k: re.sub('(?<!_old)\.mp3', '_old.mp3', v) for k, v
                          in remote_m3u_content.items()}

    # Get local m3u files content.
    local_m3u_content = dict()
    for m3u in local_m3u_file_names:
        with open(os.path.join(main.ARCHIVE_FOLDER, m3u)) as f:
            local_m3u_content[m3u] = f.read()

    # Checks wheter local and remote files are the same. Moves local files that
    # are different to the deprecated folder.
    for m3u in set(local_m3u_content.keys()) & set(remote_m3u_content.keys()):
        # Reduce comparison to not include '_old' to be sure that we are as
        # general as possible.
        if (local_m3u_content[m3u].replace('_old', '') !=
                remote_m3u_content[m3u].replace('_old', '')):
            logging.info('Local m3u file: %s is different from remote.',
                         (m3u))
            logging.debug('\nLocal file:\n%sRemote file:\n%s',
                          local_m3u_content[m3u],
                          remote_m3u_content[m3u])
            # Move local file to deprecated folder.
            # TODO: check if this part of the code is working correctly.
            src = os.path.abspath(os.path.join(main.ARCHIVE_FOLDER, m3u))
            dst = os.path.abspath(
                os.path.join(main.DEPRECATED_ARCHIVE_FOLDER, m3u))
            shutil.move(
                src,
                dst)
            logging.info('Moved: %s -> %s', src, dst)
            # Save remote file.
            with open(src, 'wt') as f:
                logging.debug('Wrote remote %s with content:\n%s at %s.',
                              m3u,
                              remote_m3u_content[m3u],
                              src)
                f.write(remote_m3u_content[m3u])

    # Compares remote and local m3u files.
    extra_programs = (set(remote_m3u_content.keys())
                      - set(local_m3u_content.keys()))

    # Default behavior is to add extra programs and disregard spurious ones.
    for m3u in extra_programs:
        with open(os.path.join(main.ARCHIVE_FOLDER, m3u), 'wt') as f:
            f.write(remote_m3u_content[m3u].replace('.mp3', '_old.mp3'))
    return True

if __name__ == '__main__':
    update_m3u_files()
