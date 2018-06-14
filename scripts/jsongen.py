#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2018 OpenLP Developers                                   #
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
This script (re)generates a SHA256 hash for each file in the download_3.0.json file
"""
import json
from hashlib import sha256
from pathlib import Path

CONFIG_FILE_NAME = 'download_3.0.conf'

def hash_file(file_path, block_size=65536):
    """
    Hash the given file block by block for memory efficiency

    :param pathlib.Path file_path: Path to file to hash.
    :param int block_size: Size of blocks to process the file in.
    :return: The sha256 hash of the file.
    :rtype: str
    """
    with file_path.open(mode='rb') as file:
        print(f'Calculating hash for {file_path}')
        hasher = sha256()
        buf = file.read(block_size)
        while len(buf) > 0:
            hasher.update(buf)
            buf = file.read(block_size)
        return hasher.hexdigest()


def main():
    """
    Parse the json resource file and calculate a hash for each file
    """
    cfg_file_path = Path('..', CONFIG_FILE_NAME)
    if not cfg_file_path.exists():
        print('Can\'t find download_3.0.json. You need to run hashgen.py from the scripts directory.')
        return False

    with cfg_file_path.open(mode='r', encoding='utf-8') as config_file:
        config = json.load(config_file)

    meta = config['_meta']
    song_folder = Path('..', meta['songs_dir'])
    for lang in config['songs'].values():
        song_db_path = song_folder / lang['file_name']
        lang['sha256'] = hash_file(song_db_path)

    bible_folder = Path('..', meta['bibles_dir'])
    for lang in config['bibles'].values():
        for translation in lang['translations'].values():
            bible_db_path = bible_folder / translation['file_name']
            translation['sha256'] = hash_file(bible_db_path)

    theme_folder = Path('..', meta['themes_dir'])
    for theme in config['themes'].values():
        theme_db_path = theme_folder / theme['file_name']
        theme['sha256'] = hash_file(theme_db_path)

    with cfg_file_path.open(mode='w', encoding='utf-8') as config_file:
        json.dump(config, config_file, sort_keys=True, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    main()
