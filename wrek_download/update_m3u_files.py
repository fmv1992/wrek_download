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


def main():
    u"""Update the archive folder with the newest m3u files."""
    # Define all variables.
    tmpdir = '/tmp'
    url = 'http://www.wrek.org/schedule/'
    url_m3u = 'http://www.wrek.org/playlist.php/main/128kbs/current/'
    archive_path = '../archive'
    deprec_archive_path = '../archive/deprecated_m3u_files'

    h = httplib2.Http(os.path.join(tmpdir, '.wrek_cache'))
    _, content = h.request(url)
    text = content.decode()
    local_m3u_files_name = [f for f in os.listdir(archive_path) if
                            (os.path.isfile(os.path.join(archive_path, f)) and
                             (f.endswith('m3u')))]

    # Find the name of all m3u files that are 128kbps.
    remote_m3u_files_name = re.findall('(?<=current\/)[^>]*?\.m3u(?=\">128k<)',
                                       text)

    # Get remote m3u files content.
    remote_m3u_content = dict()
    for m3u in remote_m3u_files_name:
        remote_m3u_content[m3u] = h.request(url_m3u + m3u)[1].decode()

    # Get local m3u files content.
    local_m3u_content = dict()
    for m3u in local_m3u_files_name:
        with open(os.path.join(archive_path, m3u)) as f:
            local_m3u_content[m3u] = f.read()

    # Checks wheter local and remote files are the same. Moves local files that
    # are different to the deprecated folder.
    for m3u in set(local_m3u_content.keys()) & set(remote_m3u_content.keys()):
        if local_m3u_content[m3u].replace('_old',
                                          '') != remote_m3u_content[m3u]:
            try:
                shutil.move(os.path.join(archive_path, m3u),
                            deprec_archive_path)
            except shutil.Error as error01:
                # if 'already exists' in error01:
                    # TODO: fix this.
                    # logging.info('Shutil error:', error01)
                print(error01)

    # Compares remote and local m3u files.
    extra_programs = (set(remote_m3u_content.keys())
                      - set(local_m3u_content.keys()))

    # Default behavior is to add extra programs and disregard spurious ones.
    for m3u in extra_programs:
        with open(os.path.join(archive_path, m3u), 'wt') as f:
            f.write(remote_m3u_content[m3u].replace('.mp3', '_old.mp3'))
    # print(remote_m3u_content)
    # print(local_m3u_content)
    # print(extra_programs)

if __name__ == '__main__':
    main()
