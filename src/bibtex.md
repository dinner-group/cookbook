# How to make bibliographies

## Overview
Use Zotero + bibtex. [Better bibtex](https://retorque.re/zotero-better-bibtex/index.html) is also a useful pluging for setting correct capitalization and easy exporting. The docs in Overleaf are also very [useful](https://www.overleaf.com/learn/latex/Bibliography_management_with_natbib).

## Useful tools
Super useful for formatting bibtex files: [https://github.com/FlamingTempura/bibtex-tidy](https://github.com/FlamingTempura/bibtex-tidy)

A script to capitalize titles using regexes: [https://www.dlgreenwald.com/miscellanea/capitalizing-titles-in-bibtex](https://www.dlgreenwald.com/miscellanea/capitalizing-titles-in-bibtex) (can also be done using `bibtexparser`)

## How to replace journal names with their abbreviations
1. Clone this [repository](https://github.com/JabRef/abbrv.jabref.org?tab=readme-ov-file) that contains most common journals.
1. Run the script `combine_journal_lists_dots.py` to produce a `csv` file with all the abbreviations. (There's an example [here](../))
1. Run the following script (change the file names). This will require the package [bibtexparser](https://bibtexparser.readthedocs.io/en/main/)
```python
import bibtexparser
import os
import csv
import sys

abbrev_file = "/Users/Spencer/Documents/Papers/abbrv.jabref.org/journalList_dots.csv"
journal_dict = {}
with open(abbrev_file, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file, quotechar='"')
    for row in reader:
        journal_dict[row[0]] = row[1]

bibfile = sys.argv[1]
library = bibtexparser.parse_file(bibfile)
for entry in library.entries:
    if 'journal' in entry:
        # if starts with "The", remove it
        if entry['journal'].startswith("The "):
            entry['journal'] = entry['journal'][4:]
        if entry['journal'] in journal_dict:
            entry['journal'] = journal_dict[entry['journal']]
bibtexparser.write_file(os.path.splitext(bibfile)[0] + "_cleaned.bib", library)
```