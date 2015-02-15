#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2015 OpenLP Developers                                   #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################
"""
This script (re)generates a SHA256 hash for each file in the download.cfg file
"""

from configparser import ConfigParser
from hashlib import sha256
import os


def hash_file(file_path, block_size=65536):
    """
    Hash the given file block by block for memory efficiency

    :param file_path: Path to file to hash. Type str
    :param block_size: Size of blocks to process the file in. Type int
    :return: None
    """
    file = open(file_path, 'rb')
    hasher = sha256()
    buf = file.read(block_size)
    while len(buf) > 0:
        hasher.update(buf)
        buf = file.read(block_size)
    return hasher.hexdigest()


def write_hash(section, path):
    """
    Get the name of the a file from a config section and write its hash back to the same section.

    :param section: Config section to read the filename from and write the hash to. Type configparser.SectionProxy
    :param path: Path to the folder containg the file to hash. Type str
    :return: None
    """
    section['sha256'] = hash_file(os.path.join(path, section['filename']))


def main():
    cfg_file = os.path.join('..', 'download.cfg')
    config = ConfigParser()
    config.read(cfg_file)

    song_folder = os.path.join('..', config['songs']['directory'])
    for lang in config['songs']['languages'].split(','):
        section = config['songs_{}'.format(lang)]
        write_hash(section, song_folder)

    bible_folder = os.path.join('..', config['bibles']['directory'])
    for translation in config['bibles']['translations'].split(','):
        section = config['bible_{}'.format(translation)]
        write_hash(section, bible_folder)

    theme_folder = os.path.join('..', config['themes']['directory'])
    for file in config['themes']['files'].split(','):
        section = config['theme_{}'.format(file)]
        write_hash(section, theme_folder)

    with open(cfg_file, 'w') as configfile:
        configfile.write('# The most recent version should be added to http://openlp.org/files/frw/download.cfg\n')
        config.write(configfile)

if __name__ == '__main__':
    main()
