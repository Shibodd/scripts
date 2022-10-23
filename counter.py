"""
Stores in a csv file the number of times a string was inserted.
The count is viewable by opening the data file, which is sorted by descending count.

csv file format:
key, count
"""

import csv
import pathlib
import argparse

DEFAULT_FILE_NAME = 'counterdata.csv'

argparser = argparse.ArgumentParser()
argparser.add_argument('-d', '--datafile', default = DEFAULT_FILE_NAME, help = 'Defaults to {0}.'.format(DEFAULT_FILE_NAME))
argparser.add_argument('--noautosave', action='store_true', help = 'If this flag is set, data is saved only when exiting on CTRL+C.'.format(True))
args = argparser.parse_args()

FIELD_NAMES = ['key', 'count']
FILE_PATH = pathlib.Path(args.datafile)
TMP_FILE_PATH = pathlib.Path(str(FILE_PATH) + '.tmp')

def sanitize(s):
    return s.strip().lower()

def add_kw(data, kw, count = 1):
    if kw in data:
        data[kw] = data[kw] + count
    else:
        data[kw] = count

def load_data():
    if not FILE_PATH.exists():
        return {}

    with FILE_PATH.open('r') as f:
        r = csv.DictReader(f, FIELD_NAMES)

        data = {}
        for row in r:
            add_kw(data, sanitize(row['key']), int(sanitize(row['count'])))

        return data

def save_data(data):
    with TMP_FILE_PATH.open('w', newline='') as f:
        w = csv.DictWriter(f, FIELD_NAMES)
        w.writerows(({ 'key': k, 'count': v } for k, v in sorted(data.items(), key = lambda kvp: kvp[1], reverse = True)))
    
    if FILE_PATH.exists():
        FILE_PATH.unlink()
    TMP_FILE_PATH.rename(FILE_PATH)

data = load_data()

print("Loaded {0} entries.".format(len(data)))
print("Press CTRL+C at any time to save and exit from the program.")

try:
    while True:
        kw = sanitize(input("Key: "))

        add_kw(data, kw)
        
        if not args.noautosave:
            save_data(data)
except KeyboardInterrupt:
    if args.noautosave:
        save_data(data)
