"""
csv file:
keyword, failCount
"""

import csv
import pathlib
import argparse

DEFAULT_FILE_NAME = 'counterdata.csv'

argparser = argparse.ArgumentParser()
argparser.add_argument('-d', '--datafile', default = DEFAULT_FILE_NAME, help = 'Defaults to {0}.'.format(DEFAULT_FILE_NAME))
args = argparser.parse_args()

FIELD_NAMES = ['key', 'count']
FILE_PATH = pathlib.Path(args.datafile)
TMP_FILE_PATH = pathlib.Path(str(FILE_PATH) + '.tmp')

def load_data():
    if not FILE_PATH.exists():
        return {}

    with FILE_PATH.open('r') as f:
        r = csv.DictReader(f, FIELD_NAMES)
        return { row['key'].strip(): int(row['count']) for row in r }

def save_data(data):
    with TMP_FILE_PATH.open('w') as f:
        w = csv.DictWriter(f, FIELD_NAMES)
        w.writerows(({ 'key': k, 'count': v } for k, v in sorted(data.items(), key = lambda kvp: kvp[1], reverse = True)))
    
    FILE_PATH.unlink()
    TMP_FILE_PATH.rename(FILE_PATH)

data = load_data()

print("Loaded {0} entries.".format(len(data)))
print("Press CTRL+C at any time to save and exit from the program.")

try:
    while True:
        kw = input("Key: ")

        if kw in data:
            data[kw] = data[kw] + 1
        else:
            data[kw] = 1
except KeyboardInterrupt:
    pass

save_data(data)