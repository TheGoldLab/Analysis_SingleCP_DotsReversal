import sys
import os.path
import pprint
import json
import re
import pickle
import hashlib
import datetime as dtime
from collections import Counter, OrderedDict
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import numpy as np
import scipy.stats as sst
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib

register_matplotlib_converters()

SMALL_FONT = 10
MEDIUM_FONT = 16
LARGE_FONT = 22
FONT_OPTS = {'family': 'DejaVu Sans', 'size': LARGE_FONT}
matplotlib.rc('font', **FONT_OPTS)

LINEWIDTH = 3
MARKERSIZE = 12

THEO_DATA_FOLDER = '/home/adrian/Documents/MATLAB/projects/Task_SingleCP_DotsReversal/Blocks003/'
assert os.path.isdir(THEO_DATA_FOLDER)

IMAGE_SAVE_FOLDER = '/home/adrian/Git/dataviz/data_website/images/'
assert os.path.isdir(IMAGE_SAVE_FOLDER)

PROB_CP = {
    'Block2': 0,
    'Block3': 0.2,
    'Block4': 0.5,
    'Block5': 0.8,
    'Block6': 0.2,
    'Block7': 0.5,
    'Block8': 0.8,
    'Block9': 0.5,
    'Block10': 0.2,
    'Block11': 0.8,
}

# map probCP to colors
PCP_COLORS = {
    'Quest': 'green',
    0: 'blue',
    .2: 'purple',
    .5: 'red',
    .8: 'gray'
}

BLOCK_NAMES = ['Quest'] + list(PROB_CP.keys())

TIMESTAMPS = [
    '2019_06_20_12_54',
    '2019_06_21_13_08',
    '2019_06_24_12_38',
    '2019_06_25_13_24',
    '2019_07_03_15_03',
    '2019_07_09_11_02',
    '2019_07_10_17_40',
    '2019_07_12_11_11',
    '2019_06_20_13_27',
    '2019_06_21_13_34',
    '2019_06_24_13_06',
    '2019_06_25_14_06',
    '2019_07_03_16_32',
    '2019_07_10_12_18',
    '2019_07_10_17_42',
    '2019_07_17_17_17',
    '2019_06_20_13_45',
    '2019_06_21_14_25',
    '2019_06_24_13_31',
    '2019_06_27_11_33',
    '2019_07_08_17_13',
    '2019_07_10_17_19',
    '2019_07_11_11_21',
]

DATA_FOLDER = '/home/adrian/SingleCP_DotsReversal/raw/'
assert os.path.isdir(DATA_FOLDER)

FOLDERS = []
for t in TIMESTAMPS:
    folder = DATA_FOLDER + t + '/'
    assert os.path.isdir(folder)
    FOLDERS.append(folder)

META_FILE = '/home/adrian/Documents/MATLAB/projects/Analysis_SingleCP_DotsReversal/data/subj_metadata.json'
assert os.path.exists(META_FILE)
# hard code the first one in case file has changed
META_CHKSUM = '24e31da81bd43f2e2cd51df0ef111689'  # version 1


# first version of clean metadata (commit 9b7968e)
# NEW_META_FILE = '/home/adrian/Documents/MATLAB/projects/Analysis_SingleCP_DotsReversal/data/new_metadata.json'

# second version of clean metadata (commit 9aaafa8)
NEW_META_FILE = '/home/adrian/Documents/MATLAB/projects/Analysis_SingleCP_DotsReversal/data/new_metadata2.json'

assert os.path.exists(NEW_META_FILE)
# hard code the first one in case file has changed
# NEW_META_CHKSUM = '26e4181e0383eb34ceca75f52e2d4506'  # v1; version 0 was '13cdd7970ee824d96e132c99fcf5362a'
NEW_META_CHKSUM = '79b2958c69464a0c8204daf823d1b9f3'  # v2

# the following dict should match the row order of DefaultBlockSequence.csv
TYPE_ID_NAME = {
    1: 'Tut1',
    2: 'Quest',
    3: 'Tut2',
    4: 'Block2',
    5: 'Tut3',
    6: 'Block3',
    7: 'Block4',
    8: 'Block5',
    9: 'Block6',
    10: 'Block7',
    11: 'Block8',
    12: 'Block9',
    13: 'Block10',
    14: 'Block11'
}
NAME_TYPE_ID = {v: k for k, v in TYPE_ID_NAME.items()}

# hard code the hashes in case files change
REF_HASHES = {
    '/home/adrian/SingleCP_DotsReversal/raw/2019_06_20_12_54/2019_06_20_12_54_FIRA.csv': '046ca06830aeebb62194e3c8d2e97046',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_06_20_12_54/2019_06_20_12_54_dotsPositions.csv': 'b3aff823355bb4cda726a0857fa1ba74',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_06_20_13_27/2019_06_20_13_27_FIRA.csv': '8b945181914a9f1c6a4784c8899d72ed',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_06_20_13_27/2019_06_20_13_27_dotsPositions.csv': '92c7f5484127202f8bc088e8e025cc9e',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_06_20_13_45/2019_06_20_13_45customFIRA.csv': '9efef45496b9be2f0c914c47a9a40284',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_06_21_13_08/2019_06_21_13_08_FIRA.csv': '41485cf9922b03cd5176824887a2c99a',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_06_21_13_08/2019_06_21_13_08_dotsPositions.csv': '3073e147156bdbbffa593c190de19b91',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_06_21_13_34/2019_06_21_13_34customFIRA.csv': 'daa4d2be5663975a4d788f8a5187e93c',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_06_21_14_25/2019_06_21_14_25customFIRA.csv': '319ad81fe1c5e8bc4303ea0d57e9ce3d',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_06_24_12_38/2019_06_24_12_38_FIRA.csv': '20102a1b8e7d68305455bacccd6fc5cb',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_06_24_12_38/2019_06_24_12_38_dotsPositions.csv': '7299c4dc38bb2e519d797b4483a83c1f',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_06_24_12_38/2019_06_24_12_38customFIRA.csv': '042c94c3a793c272b8626b2e74ae9384',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_06_24_13_06/2019_06_24_13_06_FIRA.csv': 'c8423313d1e47ba799be602d3642e4eb',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_06_24_13_06/2019_06_24_13_06_dotsPositions.csv': '1be8454c740020101e4fcfc57d720b14',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_06_24_13_31/2019_06_24_13_31_FIRA.csv': '78daa9667716d994f0d75f7fb87e93b4',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_06_24_13_31/2019_06_24_13_31_dotsPositions.csv': '36ecb7509c192e14a68ec9476aca94ac',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_06_25_13_24/2019_06_25_13_24_FIRA.csv': '92d73437503dbc26a61e15c93b963773',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_06_25_13_24/2019_06_25_13_24_dotsPositions.csv': 'f1d59e1830260881749823abc670d469',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_06_25_14_06/2019_06_25_14_06customFIRA.csv': '4bc9d1ff7dc836cada9d0b4455f669c6',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_06_27_11_33/2019_06_27_11_33customFIRA.csv': '71f4944fe2829eba04e14afe556f80f9',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_07_03_15_03/2019_07_03_15_03_FIRA.csv': '7dc6c4e1c1dcef8e3bbacdb80e926435',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_07_03_15_03/2019_07_03_15_03_dotsPositions.csv': 'ddfd162fe111d466fff74d4b53657a46',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_07_03_16_32/2019_07_03_16_32_FIRA.csv': '4077575d11460a76a140f3f0ee4a3153',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_07_08_17_13/2019_07_08_17_13customFIRA.csv': '213389e2587cbf1aafa2899b5097bb10',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_07_09_11_02/2019_07_09_11_02customFIRA.csv': 'f4ddd9cdd316b0c73d0e9c93e46616d9',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_07_10_12_18/2019_07_10_12_18_FIRA.csv': '0e689f4bf92aa2c4f67eb74ee56f6046',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_07_10_12_18/2019_07_10_12_18_dotsPositions.csv': '235f0964a5d2fd088aeea66c4df97fd4',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_07_10_17_19/2019_07_10_17_19_FIRA.csv': 'b799cb9ceea49d9d7cb8616493228183',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_07_10_17_19/2019_07_10_17_19_dotsPositions.csv': '97b178d6c061d4347582f1981a420292',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_07_10_17_40/2019_07_10_17_40_FIRA.csv': 'e43b0bc86c6e02f957afbe335989c0e5',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_07_10_17_42/2019_07_10_17_42customFIRA.csv': 'c6329eb3af8defd7c3d640d39e8e62c5',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_07_11_11_21/2019_07_11_11_21customFIRA.csv': '7ee06827cde2c98079ac757a1c0a2e4a',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_07_12_11_11/2019_07_12_11_11_FIRA.csv': 'e7dd32800d1c34722fcd049f0426005d',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_07_12_11_11/2019_07_12_11_11_dotsPositions.csv': '20e2225a5eebca406372854a1beb91b7',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_07_17_17_17/2019_07_17_17_17_FIRA.csv': 'f6252353958133c4fd37aba7bc0d6570',
    '/home/adrian/SingleCP_DotsReversal/raw/2019_07_17_17_17/2019_07_17_17_17_dotsPositions.csv': 'fd77b1add52105f0ceba419f72b515b4'
}

# de-identified hashes for each subject
SUBJECT_HASHES = (
    'c577366758027956b21fcb95a8db0d1e',
    'x30bdd3d8ad24d522dc158030fb5c18d7',
    'c71c3808bc33ba05928e1bc5f93a9078',
    'x5f5dbb54ed21cfeb4ac045e0328181cc',
    'x648f9ad78ad1211c172d1a1cd2c5af3f'
)

NUM_SUBJECTS = len(SUBJECT_HASHES)

# short strings more human-readable than the hashes above
SUBJECT_NAMES = tuple('S' + str(j) for j in range(1, NUM_SUBJECTS + 1))


def get_name_from_hash(hashh):
    for i, h in enumerate(SUBJECT_HASHES):
        if h == hashh:
            return SUBJECT_NAMES[i]
    raise ValueError('invalid subject hash')


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


def get_files_and_hashes(show=False, hash_map=False):
    """
    builds and returns a list of dicts with fields 'FIRA', 'dots' and 'session'. The values are as follows:
    FIRA: list of pairs of the form (<path to .csv file>, <MD5 checksum for this file>)
    dots: same as for FIRA, but for dots data
    session: single string representing the timestamp of the session, in the format YYYY_MM_DD_HH_mm

    for the values corresponding to the FIRA and dots keys, the absence of any file is encoded as an empty list

    :param show: (bool) whether to print the resulting list or not
    :param hash_map: (bool) whether to return the dict of hashes <filename>:<hash> or not
    :return: (list) described above
    """
    file_names = []  # misnomer, not really a list of file names, rather a list of dict

    if hash_map:
        hashes = {}
    for timestamp, folder_name in zip(TIMESTAMPS, FOLDERS):
        # check that the standard FIRA exists
        filename = folder_name + timestamp + '_FIRA.csv'

        to_append = []
        if os.path.exists(filename):
            hash_val = md5(filename)
            to_append.append((filename, hash_val))
            if hash_map:
                hashes[filename] = hash_val

        # same for customFIRA
        custom = folder_name + timestamp + 'customFIRA.csv'
        if os.path.exists(custom):
            hash_val = md5(custom)
            to_append.append((custom, hash_val))
            if hash_map:
                hashes[custom] = hash_val

        files = {'session': timestamp, 'FIRA': to_append}

        # now deal with DOTS files
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
        print('===============================================')
        print('files info')
        print()
        pprint.pprint(file_names)

    if hash_map:
        if show:
            print('===============================================')
            print('hash info')
            print()
            pprint.pprint(hashes)

        return file_names, hashes
    else:
        return file_names


def check_homogeneity(files):
    """
    checks that all FIRA files have same column names and data types (columnwise)
    same for DOTS files
    """
    for file_dict in files:
        for k in ['FIRA', 'dots']:
            cols = []  # will be a list of dicts with key-value pairs <column name>: <dtype>
            list_of_files = file_dict[k]
            for filename, hhsh in list_of_files:
                assert REF_HASHES[filename] == hhsh, f'{filename} with hash {hhsh} does not match ref hash {REF_HASHES[filename]}'
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
    print('HOMOGENEITY TEST PASSED')


def get_keys(timestamp, meta):
    """
    for a give timestamp (i.e. a session), returns the subject code and session name required to index
    the meta_data dict appropriately to find back the session.

    Example:
        >>> c, s = get_keys('2019_06_21_11_52', meta)
        >>> session_dict = meta[c][s]

    :param timestamp: (str) timestamp of session
    :param meta: (dict) corresponds to reading the meta data json file
    """
    for subj_code, sessions_dict in meta.items():
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


def consistency_log(fname, dfiles, dmeta):
    """
    todo: check this function?
    Write log file that compares data from files with content from metadata file.
    The main thing to check is what Task blocks each subject did, and when; and
    also that the trials shown in each block agree with the theoretical dataset of
    trials produced before the experiment.

    :param fname: filename of log file to write
    :param dfiles: list of file dicts as returned by get_files_and_hashes()
    :param dmeta: (dict) as bare-imported with json.load from subj_metadata.json
    """
    old_stdout = sys.stdout
    try:
        with open(fname, 'wt') as f:  
            sys.stdout = f
            for file_dict in dfiles:
                
                time_stamp = file_dict['session']
                c, s = get_keys(time_stamp, dmeta)
                meta = dmeta[c][s]
                for filename, hhsh in file_dict['FIRA']:
                    assert REF_HASHES[filename] == hhsh
                    
                    f.write('\n --------------------------- new file -------------------------\n')
                    print(filename)
                    f.write('\n')
                    
                    table = pd.read_csv(filename)

                    # check the taskID
                    # taskID should start at 1 and increment by one for each task (block) performed in a single session
                    task_ids = table['taskID'].unique()
                    task_ids.sort()
#                     if time_stamp == '2019_06_24_13_31':
#                         print('PROOOOBLEMMMM', task_ids)

                    # data from data file
                    block_names_data = [TYPE_ID_NAME[x] for x in task_ids]
                    num_trials_data = []  # filled in incrementally in for loop below

                    for tid in task_ids:
                        print()
                        print(f'---- processing taskID {tid} -----')
                        print()

                        sub_table = table[table['taskID'] == tid].copy()
                        num_trials = len(sub_table)

                        if num_trials > 0:

                            table_trial_indices = sub_table['trialIndex'].to_numpy()

                            assert len(table_trial_indices) == num_trials, f'trivial assert that should NEVER fail'

                            # recall: if trialIndex is NOT a pure counter, possibilities are: 
                            #       1/ there are np.nan values; 
                            #       2/ counter doesn't start at 1
                            #       3/ there are repeats (should be consecutive though)
                            #       4/ after accounting for 1-3 above, the order is still not a pure counter, meaning:
                            #            a) order might not be increasing
                            #            b) some values are skipped
                            try:
                                ensure_counter(table_trial_indices, sort=False, vector_label=TYPE_ID_NAME[tid])

                            except AssertionError as err:
                                print(err, 'diagnosing ...')
                                ensure_no_nan(table_trial_indices)
                                start_val = table_trial_indices[0]

                                assert start_val == 1, f'  starting value not 1 but {start_val}'

                                # following line taken from https://stackoverflow.com/a/11528581
                                repeated_indices = [i for i, count in Counter(table_trial_indices).items() if count > 1]
                                print('  repeated trial indices:', repeated_indices)

                                repeated_removed = np.unique(table_trial_indices)
                                ensure_counter(repeated_removed)
                                num_trials = len(repeated_removed)

                            # todo: even if trialIndex behaves as a pure counter, confirm that the stimulus presented on each trial has the same properties as the planned one (from Blocki.csv)
                            block_name = TYPE_ID_NAME[tid]
                            if num_trials > 160:  # value of 160 arbitrarily picked to distinguish between Blocki blocks and the others
                                try:
                                    match = compare_with_theoretical_stimulus(block_name, sub_table)
                                except AssertionError as trial_seq_err:
                                    print(f'match fail for {block_name}')
                                    print(trial_seq_err)
                                    print()
#                                    print('trying to match with other blocks')
#                                    for bname in ['Block' + str(i) for i in np.arange(2, 12) if str(i) != block_name[5]]:
#                                        try:
#                                            new_match = compare_with_theoretical_stimulus(bname, sub_table)
#                                        except AssertionError as sub_err:
#                                            print(sub_err)
#                                            continue
#                                        else:
#                                            if new_match:
#                                                print()
#                                                print(f'match found with block {bname}')
#                                                print()
                                except ValueError as trial_seq_err:
                                    print(f'pb with number of coherence values in data file')
                                    print(trial_seq_err)
                                else:
                                    if match:
                                        print('MATCH FOUND!!!!!')
                                    else:
                                        print('Match NOT FOUND :( :( :(')
                        num_trials_data.append(num_trials)

                    # data from metadata
                    block_names_meta = [s for s in meta.keys() if s in TYPE_ID_NAME.values()]
                    num_trials_meta = [meta[nn]['numTrials'] for nn in block_names_meta]

                    data_dict = {n: nn for n, nn in zip(block_names_data, num_trials_data)}
                    data_dict['type'] = 'data'
            #         print('data:', data_dict)

                    meta_dict = {n: nn for n, nn in zip(block_names_meta, num_trials_meta)}
                    meta_dict['type'] = 'metadata'
            #         print('metadata:', meta_dict)

                    data_frame = pd.DataFrame(data_dict, index=['data'])
                    meta_frame = pd.DataFrame(meta_dict, index=['meta'])

                    table_to_print = data_frame.merge(meta_frame, how='outer', sort=True)

                    for c in table_to_print.columns.to_list():
                        if c[:3] == 'Tut':
                            table_to_print.drop(c, axis=1, inplace=True)
                    table_to_print.set_index('type', inplace=True)

                    for c in table_to_print.columns.to_list():
                        # the next few lines assert that the trial numbers from the data and the metadata agree
                        # whenever none of them is np.nan and none of them is 0
                        m = table_to_print[table_to_print.index == 'metadata'][c].iloc[0]
                        d = table_to_print[table_to_print.index == 'data'][c].iloc[0]
                        if all(~np.isnan([m, d])) and m > 0 and d > 0:
                            try:
                                assert m == d, f'in {c}, metadata trial_num = {m}, data trial_num = {d}'
                            except AssertionError as num_trial_err:
                                print(num_trial_err)

                    # following line is meant to forbid line breaking at printing
                    # taken from https://stackoverflow.com/a/45709154
                    pd.set_option('display.expand_frame_repr', False)
                    print(table_to_print)
                    f.write('\n')
    finally:  
        sys.stdout = old_stdout  


def compare_with_theoretical_stimulus(block_name, df, verbose=False):
    """
    This function does the following:
        + load theoretical stimulus corresponding to block_name
        + check that cond_prob_cp agree between theory and empirical data
        + check coherence values in data
        + match trial by trial stimulus features with theoretical trial sequence
    :param block_name: (str) e.g. 'Block3'
    :param df: (pandas.DataFrame) should have a single value in the column 'taskID'
    :param verbose: (bool) if True, error strings from caught AssertionErrors will be printed
    :return: 3-tuple of the form (<integer>, <str>, <polymorph>), the first entry has the following meaning:
            0: all went well
            1: condProbCP col inconsistent with theoretical data
            2: NaN values found in one of trialStart, trialEnd, dirChoice, dirRT columns
            3: one of two things, either
                    dataframe reconstructed from data is 'valid' but doesn't match expected theoretical dataframe, or,
                    the wrong theoretical data file was read and mapping between 2 dataframes failed
        The second entry is a message giving some details about the return value
        The third entry is usually None, but if extra data needs to be returned, it is returned here
    """
    if block_name == 'Quest':
        return 0, 'Quest block: no check performed', None
    if verbose:
        print()
        print(f'comparing with theoretical {block_name}')

    # load theoretical stimulus corresponding to block_name
    basename = THEO_DATA_FOLDER + block_name

    theo_stim = pd.read_csv(basename + '.csv')
    with open(basename + '_metadata.json', 'r') as f:
        block_meta = json.load(f)

    # check that cond_prob_cp agree between theory and empirical data
    theo_cond_prob_cp = block_meta['cond_prob_cp']
    
    emp_cond_prob_cps = df['condProbCP'].unique()
    assert len(emp_cond_prob_cps) == 1, f'more than one value for condProbCP found'
    emp_cond_prob_cps = emp_cond_prob_cps[0]

    try:
        assert emp_cond_prob_cps == theo_cond_prob_cp, f'inconsistency with condProbCP. Theo= {theo_cond_prob_cp}, Emp= {emp_cond_prob_cps}'
    except AssertionError as err1:
        if verbose:
            print(err1)
        return 1, 'disagreement between condProbCP values in theoretical stimulus and empirical data', None

    # check coherence values in data
    # get threshold coherence in df
    df_coh = df['coherence'].unique()
    df_coh.sort()
    if len(df_coh) == 2 or len(df_coh) == 3:
        th_coh = df_coh[1]
    else:
        raise ValueError(f'invalid number of coherence values {df_coh}')

    # match trial by trial stimulus features with theoretical trial sequence

    # dict with values being pairs (<column name in theoretical file>, <column name in FIRA data file>)
    # note, the FIRA data file has the extra column 'endDirection'
    colname_match = {
        'coherence': ('coh', 'coherence'),
        'CP': ('cp', 'presenceCP'),
        'direction': ('dir', 'initDirection'),
        'VD': ('vd', 'viewingDuration')
    }
    
    # dict which values are lists of pairs (<value in theoretical data file>, <value in FIRA data file>)
    values_match = {
        'coherence': [
            ('0', 0),
            ('th', th_coh),  # specific to each dataset
            ('100', 100)
        ],
        'CP': [(True, 1.), (False, 0.)],
        'direction': [('right', 0.), ('left', 180.)],
        'VD': [(x, x / 1000) for x in [100., 200., 300., 400.]]
    }
    
    assert set(values_match.keys()) == set(colname_match.keys()), f'pb in code with keys to index column names'

    table_trial_indices = df['trialIndex'].to_numpy()
    # trial_count is dict with k-v pairs <trialIndex value>: <number of times it appears in df>
    trial_count = Counter(table_trial_indices)
    new_count = {k: 0 for k in trial_count.keys()}  # I re-do the count
    
    # loop over trials in FIRA df. For each trial, do:
    #    1/ check that it is not a repeat trial, if it is, skip to next
    #    2/ check that neither trialStart, nor trialEnd are nan
    #    3/ check that values of columns to match actually match

    list_dicts = []

    for tt in range(len(df)):

        row = df.iloc[tt]
        trial_index = int(row['trialIndex'])
        new_count[trial_index] += 1
        theo_count = trial_count[trial_index]
        curr_count = new_count[trial_index]
        
        assert curr_count <= theo_count, f'row {tt}: I count more repeats than collections.Counter'

        if curr_count > 1:
            # ensures repeat trials are consecutive
            assert last_visited == trial_index, f'row {tt}: found a repeat that is not juxtaposed to the first attempt'

        if curr_count == theo_count:
            theo_row = theo_stim.iloc[trial_index - 1]  # because trialIndex starts counting at 1
            curr_dict = {}
            try:
                assert ~np.isnan(row['trialStart']), f"row {tt}: trialStart total of {df['trialStart'].isna().sum()} NaN values"
                assert ~np.isnan(row['trialEnd']), f"row {tt}: trialEnd total of {df['trialEnd'].isna().sum()} NaN values"
                assert ~np.isnan(row['dirChoice']), f"row {tt}: dirChoice total of {df['dirChoice'].isna().sum()} NaN values"
                assert ~np.isnan(row['dirRT']), f'row {tt}: dirRT is NaN'
            except AssertionError as err2:
                if verbose:
                    print(err2)
                return 2, 'one of trialStart, trialEnd, dirChoice or dirRT has a NaN value', tt
            
            for k, v in values_match.items():
                theo_col, data_col = colname_match[k]
                theo_val = theo_row[theo_col]
                data_val = row[data_col]
                try:
                    assert (theo_val, data_val) in v, f'row {tt}: {(theo_val, data_val)} not found in {v}'
                except AssertionError as err3first:
                    print(err3first)
                    return 3, 'mismatch with theoretical mapping, probably wrong theoretical file used', None
                curr_dict[theo_col] = theo_val
            
            # check change point congruent with endDirection
            if theo_row['cp']:
                assert row['endDirection'] != row['initDirection'], f'row {tt}: endDirection does not respect the presence of a change-point'
                
            list_dicts.append(curr_dict)
        last_visited = trial_index
       
    truncated_theo = theo_stim.iloc[:last_visited]
    try:
        assert truncated_theo.equals(pd.DataFrame(list_dicts)), 'reconstructed dataframe does not match theory'
    except AssertionError as err3:
        if verbose:
            print(err3)
        return 3, 'dataframe could be reconstructed from data, but does not match theoretical dataframe', None
    else:
        return 0, 'all good!', None


def get_fira_files_from_timestamp(stamp):
    """
    returns filename and hash for a given timestamp that corresponds to an experimental session.
    Note: several FIRA files might exist
    :param stamp: (str) of the form '2019_07_04_12_18'
    :return: (list) of tuples of the form (<full path to file>, <hash of file>)
    """
    all_files = get_files_and_hashes(show=False, hash_map=False)
    for ff in all_files:
        if ff['session'] == stamp:
            return ff['FIRA']
    return []


def validate_trials(initial_df):
    """
    remove all rows from df that do not meet the following conditions:
       1. dirCorrect is not NaN
       2. cpCorrect is not NaN if probCP > 0
       3. dirChoice is not NaN
       4. cpChoice is not NaN if probCP > 0
       5. dirRT > 0
       6. cpRT > 0
       7. abs(dotsOff - dotsOn - viewingDuration) < tolerance (45 msec)
       8. trialIndex should NOT be repeated
    :param df: dataframe in the format of FIRA.ecodes
    :return: copy of the modified df, or None if nothing is left after filtering out bad trials
    """
    vd_tolerance = 45 / 1000  # in seconds
    df = initial_df.copy()  # just to make sure I don't modify the df outside of the function
    df = df[df['dirCorrect'].notna()]  # 1
    df = df[df['dirChoice'].notna()]  # 3
    df = df[df['dirRT'] > 0]  # 5
    df = df[df['cpRT'] > 0]  # 6
    df = df[((df['condProbCP'] > 0) & (df['cpCorrect'].notna())) | (df['condProbCP'] == 0)]  # 2
    df = df[((df['condProbCP'] > 0) & (df['cpChoice'].notna())) | (df['condProbCP'] == 0)]  # 4

    # the following is inspired from this answer: https://stackoverflow.com/a/18182241
    def check_vd(row):
        return abs(df['dotsOff'] - df['dotsOn'] - df['viewingDuration']) < vd_tolerance
    df = df[df.apply(check_vd, axis=1)]  # 7

    # at this point, it could be the case that the dataframe is simply a collection of empty rows
    if df['trialIndex'].notna().sum() == 0:
        return None

    try:
        assert not any(df['trialIndex'].duplicated()), 'duplicated trialIndex found'
    except AssertionError:
        print('num duplicates = ', sum(df['trialIndex'].duplicated()))
        print('length of df = ', len(df))
        print('shape of df = ', df.shape)
        df.to_csv('faulty.csv')
        raise
    # df = df.drop_duplicates('trialIndex')
    return df


def get_block_data(name, stamp=None, subject_name=None):
    """
    for a given block name and optional timestamp (corresponding to a session tag) returns the data and the
    corresponding file names.
    An attempt is made to pick each file with ending '_FIRA.csv" if it exists.
    :param name: (str) block name, such as 'Block2', 'Block3', etc.
    :param stamp: (str) timestamp, such as '2019_06_23_13_31'. If None, all sessions are parsed
    :param subject_name: (str) an element of SUBJECT_NAMES
    :return: (2-tuple) (<pandas.DataFrame>, <list of paths to files>)
             Note the dataframe is empty if the block name is not in the data
    """
    task_id = NAME_TYPE_ID[name]
    if stamp is None:
        metadata = read_new_metadata()
        if subject_name is None:
            raise NotImplementedError
        else:
            list_of_dataframes = []
            list_of_files = []
            for session in metadata[subject_name].values():
                filename = session['fira_file'][0]
                data = pd.read_csv(filename)
                data = data[data['taskID'] == task_id]
                list_of_dataframes.append(validate_trials(data))
                list_of_files.append(filename)
            return pd.concat(list_of_dataframes), list_of_files
    else:
        # todo: this whole block to get 'file' is obsolete with new metadata? Maybe not as used to produce new metadata
        file_list = get_fira_files_from_timestamp(stamp)
        assert len(file_list) <= 2, 'list of FIRA files has length greater than 2'
        file = file_list[0][0]  # get first file in list
        ending = file[-9:]
        if ending != '_FIRA.csv' and len(file_list) > 1:
            file = file_list[1][0]

        data = pd.read_csv(file)
        data = data[data['taskID'] == task_id]
        try:
            epurated_data = validate_trials(data)
        except AssertionError as err:
            print(err)
            print(f'Assertion error occurred in {name}, {stamp}')
            raise

        # keep in mind that epurated_data might well be None
        return epurated_data, [file]


def get_probcp_data(prob_changepoint, subject_name=None):
    if subject_name is None:
        raise NotImplementedError
    list_of_dataframes = []
    list_of_block_names = [k for k, v in PROB_CP.items() if v == prob_changepoint]
    for bn in list_of_block_names:
        bdata, _ = get_block_data(bn, subject_name=subject_name)
        list_of_dataframes.append(bdata)
    return pd.concat(list_of_dataframes)


def match_data(s, meta_data_file):
    """
    checks whether the session's metadata in s is congruent with data on file and that the latter is congruent with the
    theoretical sequences of trials generated prior to the experiment.
    Several types of incongruences can happen, that we describe below.
      1/ tutorial blocks are simply skipped by this function
      2/ some blocks are present in data file, but are really ghost data, as trialStart (for instance) is NaN
      3/ some blocks are not present at all in the data file
      4/ some blocks are not present at all in the metadata file

    :param s: (dict) with session info -- usually read from the old subj_metadata.json file -- with key-value pairs
              described below:
        if key is one of 'Tut1', 'Block2', etc., value is dict with keys 'aborted', 'completed', 'numTrials', 'reward'
            the Quest block has extra field 'QuestFit' which is a list of values.
        if key is 'sessionTag', value is timestamp as string
        if key is 'trialFolder', value is bare folder name, like 'Blocks003' where the trial data was read from
    :param meta_data_file: (dict) bare import of .json metadata file
    :return: (dict) with following structure:
        fira_file: (<path to file>, <hash of file>)
        blocks: [BlockInstance1, BlockInstance2, ...]  in order seen by subject?
    """
    min_trial_num = 10  # if fewer than this number of trials, dataset is considered as absent
    timestamp = s['sessionTag']
    dict_to_return = {}
    file_not_stored = True
    # to_skip = ['Tut1', 'Tut2', 'Tut3', 'sessionTag', 'trialFolder']
    block_names = ['Quest'] + ['Block' + str(i) for i in range(2, 12)]
    # block_names_in_meta = set([n for n in s.keys() if n not in to_skip])
    # block_names_in_data =

    blocks = []
    for block_name in block_names:
        block_data, filename = get_block_data(block_name, stamp=timestamp)
        filename = filename[0]
        # store file info only once in outer dict
        if file_not_stored:
            candidate_fira_files = get_fira_files_from_timestamp(timestamp)
            for fff, h in candidate_fira_files:
                if fff == filename:
                    dict_to_return['fira_file'] = (fff, h)
                    file_not_stored = False
                    break

        if block_data is None:
            in_file = False
        else:
            in_file = block_data['trialIndex'].max() > min_trial_num

        # check whether block in metadatafile
        in_meta = block_name in s.keys() and s[block_name]['numTrials'] > min_trial_num

        if in_meta or in_file:
            subj, ___ = get_keys(timestamp, meta_data_file)
        else:
            continue

        if in_file:
            try:
                match, msg, extra_data = compare_with_theoretical_stimulus(block_name, block_data, verbose=True)
            except ValueError as val_err:
                print()
                print(timestamp, get_fira_files_from_timestamp(timestamp))
                print()
                if timestamp in {'2019_06_20_13_45', '2019_06_21_13_34'}:
                    print(val_err)
                    print('skipping check')
                    continue
                else:
                    raise

            if match not in range(4):
                raise ValueError('unexpected returned value')

            do_not_redefine = False  # ad hoc flag needed later

            if match == 1:  # mismatch with condProbCP and theory
                print()
                print(timestamp, dict_to_return['fira_file'])
                print()
                if timestamp in {'2019_06_27_11_33'}:
                    print('skipping check')
                    continue
                else:
                    raise ValueError('inconsistency found in the condProbCP field')

            elif match == 2:  # NaN values in key columns appeared in data
                # re-run the function on truncated data if first NaN appeared above trial 10
                if extra_data > min_trial_num:
                    new_match, _, __ = compare_with_theoretical_stimulus(block_name, block_data.iloc[:extra_data])
                    assert new_match == 0, 'even after truncation, data could not be matched to theoretical trials'
                    block_data = block_data.iloc[:extra_data]
                else:
                    if not in_meta:
                        continue
                    else:
                        start_time = None
                        end_time = None
                        num_trials = None
                        do_not_redefine = True

            elif match == 3:  # match failed for some reason
                print()
                print(timestamp, dict_to_return['fira_file'])
                print()
                if timestamp in {'2019_06_27_11_33'}:
                    print('skipping check')
                    continue
                else:
                    raise ValueError('data match failed')

            if not do_not_redefine:
                start_time = float(block_data['trialStart'].min(skipna=True))
                end_time = float(block_data['trialEnd'].max(skipna=True))
                num_trials = int(block_data['trialIndex'].max())

        else:  # block data not in file
            start_time = None
            end_time = None
            num_trials = None

        if in_meta:
            block_info = s[block_name]
            if block_name == 'Quest':
                if block_info['completed']:
                    assert block_info['numTrials'] == 80
                    qparam = block_info['QuestFit']
                else:
                    qparam = None
            else:
                qparam = None
        else:
            qparam = None

        block = make_block_dict(block_name, start_time, end_time, timestamp, num_trials, subj,
                                not in_meta, not in_file, quest_params=qparam)
        blocks.append(block)
    dict_to_return['blocks'] = blocks
    return dict_to_return


def produce_valid_metadata(meta_data_import):
    """
    key processing is done by the function match_data()
    :param meta_data_import: (dict) as read by json.load on old subj_metadata.json from pilot experiment
    :return: (dict)
    """
    # initial_files = get_files_and_hashes()
    new_metadata = {}
    for subject in meta_data_import:
        subject_key = get_name_from_hash(subject)
        new_metadata[subject_key] = {}
        for session, session_info in meta_data_import[subject].items():
            session_dict = match_data(session_info, meta_data_import)
            timestamp = session_info['sessionTag']
            new_metadata[subject_key][timestamp] = session_dict
    return new_metadata


def make_block_dict(name, start, stop, date, num_trials, subject_hash, absent_meta, absent_file, quest_params=None):
    """
    object that stores metadata about a block of trials run in the experiment
    """
    return dict(
        name=name,
        start=start,
        stop=stop,
        date=date,  # to parse as datetime, use: datetime.strptime(date, '%Y_%m_%d_%H_%M')
        num_trials=num_trials,
        subject_hash=subject_hash,
        subject=get_name_from_hash(subject_hash),
        task_id=NAME_TYPE_ID[name],
        quest=quest_params,
        threshold=quest_params[0] if (quest_params is not None) else None,
        in_file_not_in_meta=absent_meta,
        in_meta_not_in_file=absent_file)


def read_new_metadata(old=False):
    if old:
        new_chksum = md5(META_FILE)
        assert new_chksum == META_CHKSUM, f'MD5: {new_chksum}'
        with open(META_FILE, 'r') as f_:
            metadata = json.load(f_, object_pairs_hook=OrderedDict)
        return metadata
    else:
        new_meta_chksum = md5(NEW_META_FILE)
        assert new_meta_chksum == NEW_META_CHKSUM, f'MD5: {new_meta_chksum}'
        with open(NEW_META_FILE, 'r') as f_:
            metadata = json.load(f_, object_pairs_hook=OrderedDict)
        return metadata


def super_power_metadata():
    """
    Reads the metadata stored in NEW_METADATA file and performs extra useful computations
    1. maximum number of days across which any subject did the experiment
    2. the empowered metadata dict
    3. list of dicts of block counts. len(list) = NUM_SUBJECTS; key-val of dicts = <block name>:<block count>
    :return: 3-tuple in the order described above
    """
    max_num_days = 1
    metadata = read_new_metadata()

    # loop over subjects
    block_counts = []
    for k, v in metadata.items():
        block_counts_dict = {k: 0 for k in BLOCK_NAMES}
        num_sessions = len(v)

        # arbitrary date before experiment started
        ref_day = dtime.datetime.strptime('2019_01_01_00_00', '%Y_%m_%d_%H_%M')
        dates_sweep = {}  # for each session, count days difference since ref_day

        # loop over sessions
        for kk in v.keys():
            # first sweep before sorting dates
            dates_sweep[kk] = (dtime.datetime.strptime(kk, '%Y_%m_%d_%H_%M') - ref_day).days  # positive integer of days

        # add relative day field to each session dict;
        # if subject did two sessions on 24 June and 26 June, rel_day will be 1 and 3
        offset = min(dates_sweep.values()) - 1  # first day for subject starts at 1
        all_rel_days = []
        for kkk, vvv in dates_sweep.items():
            all_rel_days.append(vvv - offset)
            v[kkk]['rel_day'] = vvv - offset

        # reloop over sessions to add a 'day_count' field, for axes indices below
        # so, for same example as above, session from 24 June has day_count=0 and 26 June, day_count=1
        unique_rel_days = np.unique(all_rel_days)
        ranks = np.argsort(unique_rel_days)
        rel_count_map = {d: ranks[i] for i, d in enumerate(unique_rel_days)}
        for kk, vv in v.items():
            vv['day_count'] = rel_count_map[vv['rel_day']]

        # dict with key-val = <date_str>:<datetime object>
        sessions_dates = {s: dtime.datetime.strptime(s, '%Y_%m_%d_%H_%M') for s in v.keys()}

        # dict with key-val = <session's date>:<bool>
        first_session = {s: False for s in sessions_dates.keys()}

        # now find the actual first session of each day, for this subject
        for d in range(len(unique_rel_days)):
            sessions_this_day_count = [sn for sn in sessions_dates.keys() if v[sn]['day_count'] == d]
            first_session_name = sessions_this_day_count[0]
            first_session_as_datetime = sessions_dates[first_session_name]
            if len(sessions_this_day_count) > 1:
                for s in sessions_this_day_count[1:]:
                    if sessions_dates[s] < first_session_as_datetime:
                        first_session_as_datetime = sessions_dates[s]
                        first_session_name = s
            first_session[first_session_name] = True

        # loop over sessions one last time
        for kk, vv in v.items():

            list_of_blocks = metadata[k][kk]['blocks']
            num_blocks = len(list_of_blocks)

            # loop over blocks
            for i in range(num_blocks):
                block = list_of_blocks[i]

                # convert date fields to datetime objects
                date_str = block['date']
                block['date'] = dtime.datetime.strptime(date_str, '%Y_%m_%d_%H_%M')  # time of session start

                if not block['in_meta_not_in_file']:  # ensure block's data is on file
                    block_counts_dict[block['name']] += 1
                    # add block start and stop times as datetime objects
                    try:
                        block_duration = dtime.timedelta(seconds=block['stop'] - block['start'])
                    except ValueError as val_err:
                        print('BUG AT', date_str, block['name'])
                        print(val_err)

                    if first_session[date_str]:
                        if block['name'] == 'Quest':
                            first_start = block['start']
                            block['datetime_start'] = block['date']
                        else:
                            block['datetime_start'] = block['date'] + dtime.timedelta(
                                seconds=block['start'] - first_start)
                    else:
                        block['datetime_start'] = block['date'] + dtime.timedelta(seconds=block['start'] - first_start)
                    block['datetime_stop'] = block['datetime_start'] + block_duration

                # add prob_cp field
                block['prob_cp'] = PROB_CP[block['name']] if block['name'] != 'Quest' else 0
        block_counts.append(block_counts_dict)
        # here we anticipate the number of columns in the subplots layout
        num_days = len(np.unique(list(dates_sweep.values())))
        if num_days > max_num_days:
            max_num_days += 1

    return max_num_days, metadata, block_counts


def plot_meta_data(plot_file):
    # todo: fix wrong trial count for second Quest block of subj1 day1
    y_values = OrderedDict(
        {
            'Quest': 0,
            'Block2': 1,
            'Block3': 2,
            'Block4': 3,
            'Block5': 4,
            'Block6': 5,
            'Block7': 6,
            'Block8': 7,
            'Block9': 8,
            'Block10': 9,
            'Block11': 10
        }
    )

    lines = []
    for p, c in PCP_COLORS.items():
        lines.append(mlines.Line2D([], [],
                                   linewidth=LINEWIDTH, color=c,
                                   marker='+', markersize=MARKERSIZE,
                                   label=f'prob CP = {p}' if not isinstance(p, str) else p))
    delta_y = 3
    ddy = 1
    for i, value in enumerate(y_values.keys()):
        y_values[value] = i * delta_y

    """first we process the metadata"""
    max_num_days, metadata, block_counts = super_power_metadata()

    """actual plotting"""

    # create figure
    fig, axes = plt.subplots(NUM_SUBJECTS, max_num_days + 1, figsize=(20, 26), sharey='col', sharex=False)
    all_dates = {}
    all_titles = {}
    dy_dict = {}
    for i in range(NUM_SUBJECTS):
        for j in range(max_num_days):
            all_dates[(i, j)] = []
            all_titles[(i, j)] = 0
            dy_dict[(i, j)] = -1
    # loop through subjects
    scount = -1
    for k, v in metadata.items():
        scount += 1
        # print(list(zip(
        #     list(v.keys()),
        #     [dc['day_count'] for dc in v.values()]
        # )))
        # loop through sessions
        for kk, vv in v.items():
            list_of_blocks = metadata[k][kk]['blocks']
            num_blocks = len(list_of_blocks)
            day_count = vv['day_count']
            all_titles[(scount, day_count)] = vv['rel_day']
            try:
                curr_ax = axes[scount, day_count]
            except IndexError:
                print(scount, day_count)
                raise

            # loop over blocks
            for block in list_of_blocks:

                if block['name'] == 'Quest':
                    linecolor = PCP_COLORS[block['name']]
                else:
                    linecolor = PCP_COLORS[PROB_CP[block['name']]]

                if not block['in_meta_not_in_file']:
                    list_of_datetimes = [block['datetime_start'], block['datetime_stop']]
                    all_dates[(scount, day_count)] += list_of_datetimes
                    dy_dict[(scount, day_count)] += delta_y
                    dy = y_values[block['name']]
                    dates = matplotlib.dates.date2num(list_of_datetimes)
                    if (scount, day_count) == (0, 0):
                        print(kk, block['name'], dates)
                    curr_ax.plot_date(dates, [dy, dy],
                                      fmt='-+', linewidth=LINEWIDTH, markersize=MARKERSIZE,
                                      color=linecolor, xdate=True)
                    # annotate block number
                    bname = block['name']
                    if bname not in {'Quest', 'Block2'}:
                        bnum = re.findall('\\d+', bname)[0]
                        # bnum = bname[-1]
                        curr_ax.annotate(bnum + ':' + str(block['num_trials']), (dates[0], dy+.5), fontsize=SMALL_FONT)
                    else:
                        curr_ax.annotate(str(block['num_trials']), (dates[0], dy+.5), fontsize=SMALL_FONT)
    # print()
    # pprint.pprint(all_dates[(0, 0)])
    # pprint.pprint(matplotlib.dates.date2num(all_dates[(0, 0)]))
    # print()
    DX = .13
    for subj in range(NUM_SUBJECTS):
        for dd in range(max_num_days):
            if (subj, dd) in {(3, 2), (4, 2)}:
                continue
            curr_ax = axes[subj, dd]

            curr_ax.set_title('day ' + str(all_titles[(subj, dd)]))
            if dd == 0:
                curr_ax.set_ylabel('subj ' + str(subj + 1))
            curr_ax.tick_params(
                axis='y',  # changes apply to the x-axis
                which='both',  # both major and minor ticks are affected
                left=False,  # ticks along the bottom edge are off
                right=False,  # ticks along the top edge are off
                labelleft=False)  # labels along the bottom edge are off
            curr_ax.spines['top'].set_visible(False)
            curr_ax.spines['right'].set_visible(False)
            curr_ax.spines['bottom'].set_visible(False)
            curr_ax.spines['left'].set_visible(False)
            # orig_y1, orig_y2 = curr_ax.get_ylim()
            curr_ax.set_ylim(min(y_values.values())-3*ddy, max(y_values.values())+3*ddy)
            curr_ax.set_ylim(min(y_values.values())-3*ddy, max(y_values.values())+3*ddy)
            orig_x1, orig_x2 = curr_ax.get_xlim()
            curr_ax.set_xlim(orig_x1, orig_x1 + DX)

            try:
                xticks = [matplotlib.dates.num2date(x) for x in curr_ax.get_xticks()]
            except ValueError:
                print('subject', subj, 'day', dd)
                print(curr_ax.get_xticks())
                raise
            curr_ax.set_xticklabels([d.strftime('%H:%M') for d in xticks], fontsize=SMALL_FONT)
            # curr_ax.format_xdata = matplotlib.dates.DateFormatter('%H:%M')
            curr_ax.grid(b=True)
    fig.delaxes(axes[3, 2])
    fig.delaxes(axes[4, 2])
    plt.legend(handles=lines, bbox_to_anchor=(-1.1, 1.3), loc=2, borderaxespad=0., fontsize=2*SMALL_FONT)
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=.7)

    def get_block_color(blockname):
        if blockname == 'Quest':
            return PCP_COLORS[blockname]
        else:
            pcp = PROB_CP[blockname]
            return PCP_COLORS[pcp]

    # plot block counts in right-most column
    for subj in range(NUM_SUBJECTS):
        curr_ax = axes[subj, max_num_days]
        counts_dict = block_counts[subj]

        # dict with key-val = <block name>:<index on x axis>
        xindices = {k:x for x, k in enumerate(y_values.keys())}
        # print(xindices)
        xs, ys, cs = [], [], []  # x values, y values and color values
        for k, v in counts_dict.items():
            xs.append(xindices[k])
            ys.append(v)
            cs.append(get_block_color(k))
        curr_ax.barh(xs, ys, color=cs)
        curr_ax.set_yticks(list(xindices.values()))
        yticklabels = ['Q'] + [str(i) for i in range(2,12)]
        curr_ax.set_yticklabels(yticklabels)
        curr_ax.set_xlabel('block count', fontsize=1.8*SMALL_FONT)
        curr_ax.set_xlim(0, 4)
        for label in (curr_ax.get_xticklabels() + curr_ax.get_yticklabels()):
            label.set_fontsize(SMALL_FONT)
    plt.savefig(plot_file)
    # plt.show()


def pcorrect_coh_all_subj_plot():
    """
    Produce plot https://scienceprojects.altervista.org/plots/coh_perf_block2.html (as of 08/20/2019)
    :return:
    """
    max_num_days, metadata, block_counts = super_power_metadata()
    fig, axes = plt.subplots(NUM_SUBJECTS, max_num_days + 1, figsize=(25, 21), sharey=True, sharex=False)
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=.1, hspace=.2)

    def get_first_session_of_day(dict_of_sessions, day_count):
        for sess, content in dict_of_sessions.items():
            if content['day_count'] < day_count:
                continue
            else:
                return sess

    for subj in range(NUM_SUBJECTS):
        # # debug
        # if subj < NUM_SUBJECTS-1:
        #     continue
        subj_name = SUBJECT_NAMES[subj]
        bottom_label = True  # use the following to only draw xlabel on bottom-most panels: subj == NUM_SUBJECTS - 1
        for day in range(max_num_days):
            if (subj, day) in {(3, 2), (4, 2)}:
                continue
            curr_ax = axes[subj, day]
            subj_info = metadata[subj_name]
            first_session = get_first_session_of_day(subj_info, day)
            left_label = day == 0

            pcorrect_coh_plot(subj_name, first_session, curr_ax, figure=fig,
                              bottom_left_labels=(bottom_label, left_label))
            if day == 0:
                curr_ax.set_ylabel('subj ' + str(subj + 1))
            if subj < NUM_SUBJECTS - 1:
                curr_ax.tick_params(axis='x', labelsize=SMALL_FONT)
            elif subj == NUM_SUBJECTS - 1:
                curr_ax.set_xlabel('coherence', fontsize=MEDIUM_FONT)

    fig.delaxes(axes[3, 2])
    fig.delaxes(axes[4, 2])

    # plot all Block2 data together in right-most column
    for subj in range(NUM_SUBJECTS):
        ax = axes[subj, max_num_days]
        all_block2, _ = get_block_data('Block2', subject_name=SUBJECT_NAMES[subj])
        all_block2 = all_block2[all_block2['viewingDuration'] == .4]
        y_vals, y_err, trial_numbers = build_y_axis_pcorrect(all_block2,
                                                             err_margin=(.01, .99), err_method='Bayes')
        x_vals = all_block2['coherence'].unique()
        x_vals.sort()

        # plot the points
        ax.errorbar(x_vals, y_vals, yerr=y_err, fmt='o')
        for xcoh, tn in enumerate(trial_numbers):
            ax.annotate(str(tn), (x_vals[xcoh] + 2, y_vals[xcoh]), fontsize=SMALL_FONT)

        if subj == 0:
            ax.set_title("All block 2's", fontsize=MEDIUM_FONT)

        ax.tick_params(axis='y', labelright=True, right=True, labelsize=MEDIUM_FONT)
        ax.set_ylabel('P(Correct)', fontsize=MEDIUM_FONT, rotation=90)
        ax.yaxis.set_label_position("right")

        ax.set_xticks(x_vals)
        ax.set_xlim(-2, 103)
        ax.tick_params(axis='x', labelsize=SMALL_FONT)

        # ax.set_ylim(0, 1.2)
    # plt.show()
    for ax in axes.flat:
        ax.axhline(.5, linestyle='--', color='k')
        ax.axhline(1, linestyle='--', color='k')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    plt.savefig('coh_perf_Block2.png')


def pcorrect_coh_all_subj_probcp_plot(vd_filter=0.4):
    """
    Produce plot https://scienceprojects.altervista.org/plots/coh_perf_all_prob_cp.html (as of .../2019)
    :param vd_filter: (float) the viewing duration through which data should be filtered. Default 400 msec.
    :return:
    """
    # get superpower metadata
    # max_num_days, metadata, block_counts = super_power_metadata()

    # unique prob_cp values
    prob_cp_vals = np.unique(list(PROB_CP.values()))
    prob_cp_vals.sort()

    # create figure and axes
    fig, axes = plt.subplots(NUM_SUBJECTS, len(prob_cp_vals), figsize=(25, 21), sharey=False, sharex=False)
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=.2, hspace=.2)

    # loop over subjects
    for subj in range(NUM_SUBJECTS):
        subj_name = SUBJECT_NAMES[subj]
        # # debug
        # if subj > 0:
        #     continue
        for pcp_idx in range(len(prob_cp_vals)):
            prob_cp = prob_cp_vals[pcp_idx]
            ax = axes[subj, pcp_idx]
            all_probcp = get_probcp_data(prob_cp, subject_name=subj_name)
            all_probcp = all_probcp[all_probcp['viewingDuration'] == vd_filter]
            y_vals, y_err, trial_numbers = build_y_axis_pcorrect(all_probcp,
                                                                 err_margin=(.01, .99), err_method='Bayes')
            x_vals = all_probcp['coherence'].unique()
            x_vals.sort()

            # plot the points
            ax.errorbar(x_vals, y_vals, yerr=y_err, fmt='o', color=PCP_COLORS[prob_cp])
            for xcoh, tn in enumerate(trial_numbers):
                ax.annotate(str(tn), (x_vals[xcoh] + 2, y_vals[xcoh]), fontsize=SMALL_FONT)

            if subj == 0:
                ax.set_title(f"Prob CP = {prob_cp}", fontsize=MEDIUM_FONT)
            elif subj == len(NUM_SUBJECTS) - 1:
                ax.set_xlabel('coherence')

            if prob_cp == 0:
                ax.set_ylabel(subj_name, fontsize=MEDIUM_FONT)
            elif prob_cp == max(prob_cp_vals):
                ax.yaxis.set_label_position("right")
                ax.set_ylabel('P(Correct)', fontsize=MEDIUM_FONT)

            ax.set_xticks(x_vals)
            ticks = np.arange(0.2, 1.1, 0.2)
            # labels = [f"{x:.1f}" for x in ticks]
            ax.set_yticks(ticks)  # todo: still not happy with yticks in this plot

            ax.set_xlim(-2, 103)
            ax.set_ylim(.2, 1.1)

            ax.tick_params(axis='both', labelleft=True, left=True, labelbottom=True, bottom=True, labelsize=SMALL_FONT)

        # ax.set_ylim(0, 1.2)
    # plt.show()
    for ax in axes.flat:
        ax.axhline(.5, linestyle='--', color='k')
        ax.axhline(1, linestyle='--', color='k')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    vd_msec = str(int(1000*vd_filter))
    fig.suptitle('Viewing Duration = ' + vd_msec + ' msec', fontsize=LARGE_FONT)

    file_to_save = IMAGE_SAVE_FOLDER + 'coh_perf_all_prob_cp_' + vd_msec + '_.png'
    plt.savefig(file_to_save)
    # plt.show()


def build_y_axis_pcorrect(data, err_margin=(.01, .99), err_method='Bayes'):
    percent_correct, errors, coh_trial_counts = [], [], []

    def get_coh_values(dataframe):
        assert dataframe['coherence'].isna().sum() == 0, 'some nan values in coherence column'
        coh_vals = dataframe['coherence'].unique()
        coh_vals.sort()
        return coh_vals

    for coh_val in get_coh_values(data):
        extracted_df = data[data['coherence'] == coh_val].copy()
        num_nan = extracted_df['dirCorrect'].isna().sum()

        data_point = extracted_df['dirCorrect'].mean()
        percent_correct.append(data_point)

        # compute error bars
        num_trials = len(extracted_df) - num_nan
        coh_trial_counts.append(num_trials)
        num_correct = extracted_df['dirCorrect'].sum()
        num_incorrect = num_trials - num_correct

        if err_method == 'Bayes':
            # compute Beta posterior
            if coh_val == 0:
                alpha_prior, beta_prior = 3.6, 3.6
            elif coh_val == 100:
                alpha_prior, beta_prior = 3, 1
            else:
                alpha_prior, beta_prior = 2.85, 2.33
            b_alpha = alpha_prior + num_correct
            b_beta = beta_prior + num_incorrect

            # find quantiles of the posterior
            percentiles = sst.beta.ppf(err_margin, b_alpha, b_beta)
            errors.append([abs(xx - data_point) for xx in percentiles])
        else:
            pihat = num_correct / num_trials
            stderr = np.sqrt(pihat * (1-pihat) / num_trials)
            low_err = -sst.norm.ppf(err_margin[0]) * stderr
            high_err = sst.norm.ppf(err_margin[1]) * stderr
            errors.append([low_err, high_err])
    return percent_correct, np.transpose(np.array(errors)), coh_trial_counts


def pcorrect_coh_plot(subject, session_timestamp, ax, err_method='Bayes', detail=True, figure=None,
                      bottom_left_labels=(True, True)):
    assert err_method in {'Bayes', 'CI'}, 'error method unknown'
    if detail:
        assert figure is not None

    # get the metadata from the Quest block
    meta_data = read_new_metadata()
    blocks = meta_data[subject][session_timestamp]['blocks']

    def extract_quest_parameters():
        for b in blocks:
            if b['name'] == 'Quest':
                params = tuple(b['quest'])
                threshold, slope, guess_rate, lapse_rate = params
                return threshold, slope, guess_rate, lapse_rate

    def extract_block2_dataframe():
        whole_block, _ = get_block_data('Block2', stamp=session_timestamp)
        if whole_block is None:
            return whole_block
        block_to_return = whole_block[whole_block['viewingDuration'] == .4]
        # pprint.pprint(block_to_return.head())
        return block_to_return

    def build_x_axis():
        th, _, __, ___ = extract_quest_parameters()
        if th == 100:
            return 0, 100
        else:
            return 0, th, 100

    def weibull(x, guess, lapse, alpha, beta):
        p_success = guess + (1 - guess - lapse) * (1 - np.exp(-(x / alpha)**beta))
        return p_success  # 1-np.exp(-((x/alpha)**beta))

    x_vals = build_x_axis()
    y_vals, y_err, trial_numbers = build_y_axis_pcorrect(extract_block2_dataframe(),
                                                         err_margin=(.01, .99), err_method=err_method)

    # plot the points with error bars
    try:
        ax.errorbar(x_vals, y_vals, yerr=y_err, fmt='o')
    except ValueError:
        print(subject, session_timestamp, x_vals, y_vals)
        raise

    # plot the Weibull
    x_weibull = np.linspace(0, 100)
    qthreshold, qslope, qguess_rate, qlapse_rate = extract_quest_parameters()
    y_weibull = weibull(x_weibull, qguess_rate, qlapse_rate, qthreshold, qslope)

    ax.plot(x_weibull, y_weibull)

    for xcoh, tn in enumerate(trial_numbers):
        ax.annotate(str(tn), (x_vals[xcoh]+2, y_vals[xcoh]), fontsize=SMALL_FONT)

    ax.set_title(session_timestamp, fontsize=MEDIUM_FONT)
    ax.tick_params(
        axis='both',
        labelbottom=bottom_left_labels[0],
        labelleft=bottom_left_labels[1],
        labelsize=MEDIUM_FONT
    )
    # if bottom_left_labels[1]:
    #     ax.set_ylabel('P(Correct)', fontsize=MEDIUM_FONT)
    # if bottom_left_labels[0]:
    #     ax.set_xlabel('coherence', fontsize=MEDIUM_FONT)
    ax.set_xlim(-2, 103)
    ax.set_ylim(0.25, 1.1)

    # plot inset optionally
    if detail:
        # These are in unitless percentages of the figure size. (0,0 is bottom left)
        container_pos = ax.get_position()
        delta_h, delta_w = 0.01 * container_pos.height, 0.01 * container_pos.width
        # print(container_pos)
        left = container_pos.x0 + .5 * container_pos.width
        bottom = container_pos.y0 + delta_h
        width = container_pos.x1 - left - delta_w
        height = .5 * container_pos.height
        ax2 = figure.add_axes([left, bottom, width, height])
        quest_data, _ = get_block_data('Quest', stamp=session_timestamp)
        quest_data = quest_data[quest_data['dirChoice'].notnull()]
        ax2.step(quest_data['trialIndex'], quest_data['coherence'])
        ax2.tick_params(
            axis='x',  # changes apply to the x-axis
            which='both',  # both major and minor ticks are affected
            bottom=False,  # ticks along the bottom edge are off
            top=False,  # ticks along the top edge are off
            labelbottom=False)  # labels along the bottom edge are off
        for tick in ax2.yaxis.get_major_ticks():
            tick.label.set_fontsize(SMALL_FONT)


if __name__ == '__main__':
    read_new_metadata()  # a quick way to do a check sum on metadata
    # plot_meta_data('metadata.png')
    # pcorrect_coh_all_subj_plot()  # Quest + Block2
    # for vd in [.1, .2, .3, .4]:
    #     pcorrect_coh_all_subj_probcp_plot(vd_filter=vd)  # Perf by subject by PROB_CP
    """
    When called from the command line, this script must have one argument. If the arg is 
    'check': checks are performed on the data
    'log': a log file is written to disc
    'plot': a plot summarizing valid metadata is saved to file
    """
    _, arg = sys.argv

    if arg == 'check':
        # todo: turn this whole block into a function
        files_data, latest_hashes = get_files_and_hashes(show=False, hash_map=True)

        assert latest_hashes == REF_HASHES, 'latest hashes do not match reference hashes'
        # pprint.pprint(latest_hashes)
        """
        Recall: files_data is a list of dicts with fields 'FIRA', 'dots' and 'session'. The values are as follows:
            FIRA: list of pairs of the form (<path to .csv file>, <MD5 checksum for this file>)
            dots: same as for FIRA, but for dots data
            session: single string representing the timestamp of the session, in the format YYYY_MM_DD_HH_mm

            for the values corresponding to the FIRA and dots keys, the absence of any file is encoded as an empty list
        """
        # get checksum of metadata file ...
        meta_chksum = md5(META_FILE)
        assert meta_chksum == META_CHKSUM

        num_folder_on_disk = len([i for i in os.listdir(DATA_FOLDER) if i[:5] == '2019_'])

        # number of timestamps in notebook variable
        num_timestamps = len(TIMESTAMPS)

        # number of timestamps in metadafile
        with open(META_FILE, 'r') as f:
            meta_data = json.load(f)
        # recall: meta_data is a dict. Its keys are hash codes for subjects.
        # its values are themselves dicts, with keys session names and values dicts with session info.
        # So, to access the session info corresponding to the first session of the the first subject, do:
        # meta_data[<subj code>]['session1']
        num_metadata_sessions = 0
        for v in meta_data.values():
            num_metadata_sessions += len(v)

        assert num_timestamps == num_folder_on_disk, f'{num_timestamps} timestamps in module vs. {num_folder_on_disk} data folders on disk'
        assert num_metadata_sessions == num_timestamps, 'distinct number of sessions in metadata than timestamps in module'

        check_homogeneity(files_data)

    elif arg == 'log':
        original_meta = read_new_metadata(old=True)
        valid_meta_data = produce_valid_metadata(original_meta)
        with open('new_metadata', 'w') as fp:
            try:
                json.dump(valid_meta_data, fp, indent=4, sort_keys=True)
            except TypeError:
                print('pickling')
                pickle.dump(valid_meta_data, fp)

        print()
        pprint.pprint(valid_meta_data)

        print('ALL GOOD!!!!')
    elif arg == 'plot':
        plot_meta_data('metaplot.png')
