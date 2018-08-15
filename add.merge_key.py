#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 23:23:23 2018

@author: ryotakata
"""

def argsparse():
    import sys
    args = sys.argv
    assert len(args) >= 3,\
    "m(-_-)m This script takes two or more arguments.\n \
    usage: $ python " + args[0] + " csv1.csv 2 3 4 ... \n \
    arg1: input csv file \n \
    arg2,3,4 ... : column indexes used to generate merge_key \n \
    stdo: output csv file \n \
    note: [1] column indexes start at 0. \n \
        : [2] merge_key to be added at column 0. \n \
    "
    return args[0], args[1], [int(i) for i in args[2:]]

def open_csv_file(path_to_csv):
    import csv
    with open(path_to_csv, 'r') as f:
        reader = csv.reader(f)
        return  [row for row in reader]

if __name__ == '__main__':
    """
    """
    this_script_name, path_to_csv, ls_col_idx = argsparse()

    ### Read CSV files
    csv_ = open_csv_file(path_to_csv)
    
    ### Generate merge_key
    for r in csv_:
        tmp_ = [r[i] for i in ls_col_idx]
        key = reduce(lambda x,y: str(x) + str(y), tmp_)
        print reduce(lambda x,y: str(x) + ',' + str(y), [key] + r)
