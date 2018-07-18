#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 02:26:26 2018

@author: ryotakata
"""

def argsparse():
    import sys
    args = sys.argv
    assert len(args) == 5,\
    "m(-_-)m This script takes just four arguments.\n \
    usage: $ python " + args[0] + " csv1.csv csv2.csv 4 2 \n \
    arg1: input file, base csv file \n \
    arg2: input file, csv file merged \n \
    arg3: parameter, column index of merge key for base csv file \n \
    arg4: parameter, column index of merge key for csv file merged \n \
    stdo: output csv file \n \
    note: [1] column indexes start at 0. \n \
        : [2] base csv file's keys to be checked whether they are unique value or not (stderr). \n \
        : [3] csv file merged's keys to be checked whether they are unique value or not (stderr). \n \
        : [4] csv file merged's keys to be checked whether they are the keys which base_csv has or not (stderr). \n \
    "
    return args[1], args[2], args[3], args[4]

def open_csv_file(path_to_csv):
    import csv
    with open(path_to_csv, 'r') as f:
        reader = csv.reader(f)
        return  [row for row in reader]

def is_this_list_unique(ls_):
    return len(ls_) == len(set(ls_))

def stderr_ununique_element(csv_, col_idx_csv):
    ls_key_ = [i[col_idx_csv] for i in csv_]
    ls_key_duplicate = [i for i in set(ls_key_) if ls_key_.count(i) > 1]
    import sys
    for k in ls_key_duplicate:
        for row in  [j for j in csv_ if j[col_idx_csv] == k]:
            print >> sys.stderr, row
        print >> sys.stderr, "--"

if __name__ == '__main__':
    """
    """
    path_to_base_csv, path_to_in_csv, col_idx_base_csv, col_idx_in_csv = argsparse()
    col_idx_base_csv = int(col_idx_base_csv)
    col_idx_in_csv = int(col_idx_in_csv)

    ### Read CSV files
    base_csv = open_csv_file(path_to_base_csv)
    in_csv = open_csv_file(path_to_in_csv)
    
    ### Unique Check at merge key
    if not is_this_list_unique([i[col_idx_base_csv] for i in base_csv]):
        import sys
        print >> sys.stderr, \
            sys.argv[0] + ": *W, base csv file is NOT unique at merge key"
        stderr_ununique_element(base_csv, col_idx_base_csv)
    if not is_this_list_unique([i[col_idx_in_csv] for i in in_csv]):
        print >> sys.stderr, \
            sys.argv[0] + ": *W, csv file merged is NOT unique at merge key"
        stderr_ununique_element(in_csv, col_idx_in_csv)

    ### Existence Check, does in_csv(csv file merged) have the key which base_csv does NOT have.
    err_csv = []
    for i in in_csv:
        ls_base_csv_has_same_key = \
            [b for b in base_csv if b[col_idx_base_csv] == i[col_idx_in_csv]]
        if ls_base_csv_has_same_key == []:
            print >> sys.stderr, \
                sys.argv[0] + \
                ": *W, in_csv(csv file merged) has the items which is unable to merged into base_csv"
            print >> sys.stderr, i 
    print >> sys.stderr, "--"


    ### merge base_csv and in_csv into stdo(csv format)
    import copy
    out_csv = []
    for b in base_csv:
        ls_in_csv_has_same_key = \
            [i for i in in_csv if b[col_idx_base_csv] == i[col_idx_in_csv]]
        if ls_in_csv_has_same_key == []:
            out_csv.append(b + ["N/A" for i in range(len(i)-1)])
            continue
        for i in ls_in_csv_has_same_key:
            tmp = copy.copy(i)
            tmp.pop(col_idx_in_csv)
            out_csv.append(b + tmp)
    
    ### sdtout output csv file
    for i in out_csv:
        print reduce(lambda x,y: x + ',' + y, i)
