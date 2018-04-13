# python3
from os import path
import glob
import csv
import re

"""
N;CHARSET=UTF-8;ENCODING=8BIT:Ernser;Kaci
ADR;CHARSET=UTF-8;ENCODING=8BIT:;;282 Kevin Brook;New York;;23285-4905
TEL;PREF;VOICE;ENCODING=8BIT:1-333-333-3333
"""

INPUT_DIR = './data/vcf-files/'
INPUT_MASK = INPUT_DIR + '*.vcf'
OUTPUT_FILE = './data/output.csv'
CSV_COLUMNS_NAMES = [
    'name',
    'phone',
    'address',
]

def parseAttr(content, attrName):
    search = re.findall(attrName + ';(.*)8BIT:(.*)', content)
    if not len(search):
        return ''
    trimmed = str(search[0][1]).strip()
    mapped = map(lambda x: x.strip(), trimmed.split(';'))
    filtered = filter(None, mapped)
    reversedList = reversed(list(filtered))
    formatted = ', '.join(reversedList)
    return formatted

def parseVCard(vCardFile, csvWriter):
    content = vCardFile.read()
    name = parseAttr(content, 'N')
    phone = parseAttr(content, 'TEL')
    if not len(name) or not len(phone):
        return
    row = {
        'name': name,
        'phone': phone,
        'address': parseAttr(content, 'ADR'),
    }
    csvWriter.writerow(row)

def main():
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as csvFile:
        csvWriter = csv.DictWriter(
            csvFile,
            fieldnames=CSV_COLUMNS_NAMES,
            delimiter=',',
            quotechar='"',
            quoting=csv.QUOTE_ALL
        )
        files = glob.glob(INPUT_MASK)
        print('Found {:d} files in {:s}'.format(len(files), INPUT_DIR))
        for fullPath in files:
            with open(fullPath, 'r', encoding='utf-8') as vCardFile:
                parseVCard(vCardFile, csvWriter)

    with open(OUTPUT_FILE, 'r', encoding='utf-8') as csvFile:
        csvReader = csv.reader(csvFile)
        amount = sum(1 for row in csvReader)
        print('Saved {:d} rows in {:s}'.format(amount, OUTPUT_FILE))

if __name__ != '__name__':
    main()

