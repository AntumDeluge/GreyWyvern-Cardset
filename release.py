#!/usr/bin/env python

# This script is released under Creative Commons Zero (CC0).
#
# The author(s) hereby waives all copyright and related or
# neighboring rights together with all associated claims
# and causes of action with respect to this work to the
# extent possible under the law.
#
# See: https://creativecommons.org/publicdomain/zero/1.0/legalcode


import os, shutil, sys


root = sys.argv[0]
exe = os.path.basename(root)
root = os.path.dirname(root)
dir_pysol = os.path.join(root, 'PySol')
dir_release = os.path.join(root, 'release')
file_info = os.path.join(root, 'INFO')

exists_dir_release = os.path.isdir(dir_release)

args = sys.argv[1:]
for idx in range(len(args)):
    args[idx] = args[idx].lower()

if 'clean' in args:
    if exists_dir_release:
        print('\nCleaning ...')
        shutil.rmtree(dir_release)
    else:
        print('\nNothing to do.')

    sys.exit(0)


info = {}
# initializes info keys
def initInfo():
    if not os.path.isfile(file_info):
        print('ERROR: "INFO" file does not exist.')
        sys.exit(1)

    BUFFER = open(file_info, 'r')
    info_lines = BUFFER.read().strip(' \t\n\r').split('\n')
    BUFFER.close()

    for LINE in info_lines:
        LINE = LINE.strip(' \t\n\r')
        if '=' in LINE and not LINE.startswith('#'):
            key = LINE.split('=', 1)
            value = None
            if len(key) > 1:
                value = key[1].strip(' \t')
            key = key[0].strip(' \t').lower()

            if key and value:
                if key in info:
                    print('\nWARNING: Duplicate info key "{}".'.format(key))

                info[key] = value
        elif LINE:
            print('\nWARNING: Malformed line in INFO file: {}'.format(LINE))

initInfo()

# retrieves values from INFO file
def getInfo(key):
    key = key.lower()
    if not key in info:
        print('\nWARNING: Info key "{}" not found.'.format(key))
        return

    return info[key]

version = getInfo('version')

if os.path.exists(dir_release) and not exists_dir_release:
    print('\nERROR: Cannot create "release" directory, file exists with same name.')
    sys.exit(1)

if not os.path.isdir(dir_pysol):
    print('\nERROR: Cannot create release, "PySol" directory does not exist.')
    sys.exit(1)

if not exists_dir_release:
    os.makedirs(dir_release)

releases = os.listdir(dir_pysol)
for idx in reversed(range(len(releases))):
    if not os.path.isdir(os.path.join(dir_pysol, releases[idx])):
        releases.pop(idx)

if not releases:
    print('\nERROR: No releases in "PySol" directory.')
    sys.exit(1)

for REL in releases:
    src = os.path.join(dir_pysol, REL)
    tgt = os.path.join(dir_release, REL)

    # clean release directory
    if os.path.isdir(tgt):
        shutil.rmtree(tgt)
    elif os.path.isfile(tgt):
        os.remove(tgt)

    shutil.copytree(src, tgt)

here = os.getcwd()
os.chdir(dir_release)

for REL in releases:
    if not os.path.isdir(REL):
        print('WARNING: Missing release: {}'.format(REL))
        continue

    if version:
        file_rel = '{}-{}'.format(REL, version)
    else:
        file_rel = '{}'.format(REL)

    if os.path.isfile('{}.zip'.format(file_rel)):
        os.remove('{}.zip'.format(file_rel))

    shutil.make_archive(file_rel, 'zip', base_dir=REL)
    shutil.rmtree(REL) # cleanup

os.chdir(here)
