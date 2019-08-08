import os.path
import pprint
import json
import hashlib
from collections import Counter
import pandas as pd
import numpy as np
import sys


def md5(fname):
    """
    function taken from here
    https://stackoverflow.com/a/3431838
    :param fname: filename
    :return: string of hexadecimal number
    """
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_files_and_hashes(timestamps, folder_list, show=False, hash_map=False):
    """
    builds and returns a list of dicts with fields 'FIRA', 'dots' and 'session'. The values are as follows:
    FIRA: list of pairs of the form (<path to .csv file>, <MD5 checksum for this file>)
    dots: same as for FIRA, but for dots data
    session: single string representing the timestamp of the session, in the format YYYY_MM_DD_HH_mm

    for the values corresponding to the FIRA and dots keys, the absence of any file is encoded as an empty list

    :param show: (bool) whether to print the resulting list or not
    :return: (list) described above
    """
    file_names = []
    if hash_map:
        hashes = {}
    for timestamp, folder_name in zip(timestamps, folder_list):

        # check that the standard FIRA exists
        filename = folder_name + timestamp + '_FIRA.csv'
        custom = folder_name + timestamp + 'customFIRA.csv'
        to_append = []
        if os.path.exists(filename):
            hash_val = md5(filename)
            to_append.append((filename, hash_val))
            if hash_map:
                hashes[filename] = hash_val
        if os.path.exists(custom):
            has_val = md5(custom)
            to_append.append((custom, hash_val))
            if hash_map:
                hashes[custom] = hash_val

        files = {'session': timestamp, 'FIRA': to_append}
        dots = folder_name + timestamp + '_dotsPositions.csv'
        if os.path.exists(dots):
            hash_val = md5(dots)
            string = [(dots, hash_val)]
            if hash_map:
                hashes[dots] = hash_val
        else:
            string = []
        files['dots'] = string

        file_names.append(files)
    if show:
        pprint.pprint(file_names)
    if hash_map:
        return file_names, hashes
    else:
        return file_names


def check_homogeneity(files_data, ref_hashes):
    """
    checks that all FIRA files have same column names and data types (columnwise)
    same for DOTS files
    """
    counter_f = 0
    for file_dict in files_data:
        for k in ['FIRA','dots']:
            cols = []  # will be a list of dicts with key-value pairs <column name>: <dtype>
            list_of_files = file_dict[k]
            for filename, hhsh in list_of_files:
                assert ref_hashes[filename] == hhsh
                table = pd.read_csv(filename)

                # build dict with key-value pairs <column name>: <dtype>
                types_dict = {}
                for col in table.columns:
                    types_dict[col] = table[col].dtype
                cols.append(types_dict)

            counter = 0
            for new in cols:
                if counter == 0:
                    last = new
                    counter += 1
                assert set(new.keys()) == set(last.keys())
                assert set(new.values()) == set(last.values())
    print('TEST PASSED')


def get_keys(timestamp, meta_data):
    """
    for a give timestamp (i.e. a session), returns the subject code and session name required to index
    the meta_data dict appropriately to find back the session.

    Example:
        >>> c, s = get_keys('2019_06_21_11_52')
        >>> session_dict = meta_data[c][s]
    """
    for subj_code, sessions_dict in meta_data.items():
        for session_name, session_metadata in sessions_dict.items():
            if session_metadata['sessionTag'] == timestamp:
                return subj_code, session_name


def ensure_counter(vec, sort=True, vector_label=''):
    if sort:
        new_vec = np.sort(vec)
    else:
        new_vec = vec
    numel = len(new_vec)
    assert ((new_vec == np.arange(1, numel + 1)).sum() == numel), f'vector {vector_label} distinct from pure counter'


def ensure_no_nan(vec):
    num_nans = np.count_nonzero(np.isnan(vec))
    assert num_nans == 0, f'{num_nans} np.nan values found'
