#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
this file will: 
- check if the abbreviations file is sorted
- [optional] overwrite the abbreviations file with a sorted version

to run locally, execute the below from the `/tools` folder
```sh

# check if sorted
python sort.py

# check if sorted and edit the csv file with sorted version
python sort.py -e
```

after sorting you will need to git commit. 
in the future it would be good to automatically sort and commit on merge.
"""

import argparse
from os.path import exists
from sys import exit
from pandas import read_csv

__author__ = "John Gunstone"
__copyright__ = "Copyright 2023, John Gunstone"
__credits__ = ["John Gunstone"]
__license__ = "Apache-2.0"
__version__ = "0.1"
__maintainer__ = "John Gunstone"
__email__ = "gunstone.john@gmail.com"
__status__ = "Dev"


def check_sorted(filename, edit):
    df = read_csv(filename)
    descriptions = df["asset_description"].to_list()
    df_new = df.sort_values("asset_description")
    if descriptions == df_new["asset_description"].to_list():
        sorted = True
    else:
        sorted = False

    if sorted:
        print("the abbreviations file is correctly sorted")
        exit(0)
    else:
        print("the abbreviations file is not correctly sorted")
        if not edit:
            exit(1)
        else:
            print("sorting...")
            df_new.to_csv(filename, index=False)
            print("sorted.")
            print(f"you must now git commit: {filename}")
            exit(0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        default="BDNS_Abbreviations_Register.csv",
        help="Input CSV file to check sorted",
    )
    parser.add_argument(
        "-e",
        "--edit",
        action="store_true",
        help="edits source file if not sorted",
    )
    args = parser.parse_args()
    if exists(args.input):
        check_sorted(args.input, args.edit)
    else:
        print("File %s does not exist" % args.input)
        exit(1)


if __name__ == "__main__":
    main()
