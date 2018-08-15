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
    usage: $ python " + args[0] + " csv1.csv [-p N] [-r] 2 3 4 ... \n \
    arg1: input csv file \n \
    arg2,3,4 ... : column indexes to be stdo \n \
    option p(default=0): column index indicating priority \n \
    option r(default=Flse): reverse priority \n \
    stdo: output csv file \n \
    note: [1] column indexes start at 0. \n \
        : [2] column index indicating merge_key is 0(fixed). \n \
        : [3] This script takes only one column index indicating priority. \n \
        : [4] The higher the number, the higher the priority (where reverse priority == False). \n \
    "
    is_p_found = False
    is_r_found = False
    col_idx_prty = 0
    needs_reverse = False
    ls_idx_stdo = []
    for i in args[2:]:
        if is_p_found == "get_p":
            col_idx_prty = int(i)
            is_p_found = True
            continue
        elif (not is_p_found) and (not is_r_found):
            if i == "-p":
                is_p_found = "get_p"
                continue
            elif i == "-r":
                needs_reverse = True
                is_r_found = True
                continue
        elif (not is_p_found) and (is_r_found):
            if i == "-p":
                is_p_found = "get_p"
                continue
        elif (is_p_found) and (not is_r_found):
            if i == "-r":
                needs_reverse = True
                is_r_found = True
                continue
        assert int(i) >= 0
        ls_idx_stdo.append(int(i))
    assert ls_idx_stdo != []
    return args[0], args[1], col_idx_prty, needs_reverse, ls_idx_stdo

def open_csv_file(path_to_csv):
    import csv
    with open(path_to_csv, 'r') as f:
        reader = csv.reader(f)
        return  [row for row in reader]

if __name__ == '__main__':
    """
    """
    this_script_name, path_to_csv, col_idx_prty, needs_reverse, ls_idx_stdo = argsparse()

    ### Read CSV files
    csv_ = open_csv_file(path_to_csv)
    csv_ = [r + [float(r[col_idx_prty])] for r in csv_]

    ### Check ls_idx_stdo
    for i in ls_idx_stdo:
        assert r[i]
    
    ### Sort
    csv_.sort(key=lambda r:(r[0],r[-1]), reverse=not needs_reverse)

    ### Uniquify
    old_key = None
    for r in csv_:
        if old_key == None or old_key != r[0]:
            old_key = r[0]
            tmp_ = [r[i] for i in ls_idx_stdo]
            print reduce(lambda x,y: str(x) + ',' + str(y), tmp_)
        else:
            continue
