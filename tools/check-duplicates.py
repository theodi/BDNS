#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from pyfiglet import Figlet
from os.path import exists
from sys import exit
from pandas import read_csv, DataFrame

__author__ = "Francesco Anselmo"
__copyright__ = "Copyright 2022, Francesco Anselmo"
__credits__ = ["Francesco Anselmo"]
__license__ = "Apache-2.0"
__version__ = "0.1"
__maintainer__ = "Francesco Anselmo"
__email__ = "francesco.anselmo@gmail.com"
__status__ = "Dev"

def show_title():
    """Show the program title
    """
    f1 = Figlet(font='standard')
    print(f1.renderText('BDNS check duplicates'))

def check_duplicates(filename):
    df = read_csv(filename)
    ids = df["asset_abbreviation"]
    dups = ids.duplicated()
    result = df[ids.isin(ids[dups])]
    if len(result)>0:
        print("Number of duplicates found in abbreviation file: %s" % len(result))
        print(result)
        exit(1)
    else:
        print("No duplicates found in abbreviation file")
        exit(0)

def main():
    show_title()
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input", default="abbreviations.csv", help="Input CSV file to check for duplicates")
    args = parser.parse_args()
    if exists(args.input):
        check_duplicates(args.input)
    else:
        print("File %s does not exist" % args.input)
        exit(1)

if __name__ == "__main__":
    main()