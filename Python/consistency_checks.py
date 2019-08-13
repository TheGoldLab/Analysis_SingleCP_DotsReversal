import os.path
import pprint
import json
import hashlib
from collections import Counter
import pandas as pd
import numpy as np
import sys


THEO_DATA_FOLDER = '/home/adrian/Documents/MATLAB/projects/Task_SingleCP_DotsReversal/Blocks003/'
assert os.path.isdir(THEO_DATA_FOLDER)

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
META_CHKSUM = '24e31da81bd43f2e2cd51df0ef111689'

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
    print('TEST PASSED')


def get_keys(timestamp, meta):
    """
    for a give timestamp (i.e. a session), returns the subject code and session name required to index
    the meta_data dict appropriately to find back the session.

    Example:
        >>> c, s = get_keys('2019_06_21_11_52')
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
    Write log file that compares data from files with content from metadata file.
    The main thing to check is what Task blocks each subject did, and when; and
    also that the trials shown in each block agree with the theoretical dataset of
    trials produced before the experiment.
    """
    old_stdout = sys.stdout
    try:
        with open(fname, 'wt') as f:  
            sys.stdout = f
            for file_dict in dfiles:
                
                time_stamp = file_dict['session']
                c, s = get_keys(time_stamp, meta_data)
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


def compare_with_theoretical_stimulus(block_name, df):
    """
    check whether the trials, presented in the order of trialIndex, and ignoring repeated trials, have the 
    appropriate stimulus features. 
    
    Returns True if all tests are passed and all trials match
    """
    print()
    print(f'comparing with theoretical {block_name}')

    # load theoretical stimulus corresponding to block_name
    basename = THEO_DATA_FOLDER + block_name

    theo_stim = pd.read_csv(basename + '.csv')
    with open(basename + '_metadata.json', 'r') as f:
        block_meta = json.load(f)
    theo_cond_prob_cp = block_meta['cond_prob_cp']
    
    emp_cond_prob_cps = df['condProbCP'].unique()
    assert len(emp_cond_prob_cps) == 1, f'more than one value for condProbCP found'
    emp_cond_prob_cps = emp_cond_prob_cps[0]
    
    assert emp_cond_prob_cps == theo_cond_prob_cp, f'inconsistency with condProbCP. Theo= {theo_cond_prob_cp}, Emp= {emp_cond_prob_cps}'
    
    # get trial indices that are repeated in df
    table_trial_indices = df['trialIndex'].to_numpy()
    
    # get threshold coherence in df
    df_coh = df['coherence'].unique()
    df_coh.sort()
    if len(df_coh) == 2 or len(df_coh) == 3:
        th_coh = df_coh[1]
    else:
        raise ValueError(f'invalid number of coherence values {df_coh}')
    
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
            assert ~np.isnan(row['trialStart']), f"row {tt}: trialStart total of {df['trialStart'].isna().sum()} NaN values"
            assert ~np.isnan(row['trialEnd']), f"row {tt}: trialEnd total of {df['trialEnd'].isna().sum()} NaN values"
            assert ~np.isnan(row['dirChoice']), f"row {tt}: dirChoice total of {df['dirChoice'].isna().sum()} NaN values"
            assert ~np.isnan(row['dirRT']), f'row {tt}: dirRT is NaN'
            
            for k, v in values_match.items():
                theo_col, data_col = colname_match[k]
                theo_val = theo_row[theo_col]
                data_val = row[data_col]
                assert (theo_val, data_val) in v, f'row {tt}: {(theo_val, data_val)} not found in {v}'
                curr_dict[theo_col] = theo_val
            
            # check change point congruent with endDirection
            if theo_row['cp']:
                assert row['endDirection'] != row['initDirection'], f'row {tt}: endDirection does not respect the presence of a change-point'
                
            list_dicts.append(curr_dict)
        last_visited = trial_index
       
    truncated_theo = theo_stim.iloc[:last_visited]
    return truncated_theo.equals(pd.DataFrame(list_dicts))


def get_fira_file_from_timestamp(stamp):
    all_files = get_files_and_hashes(show=False, hash_map=False)
    for ff in all_files:
        if ff['session'] == stamp:
            file = [n[0] for n in ff['FIRA'] if n[0][-9:] == '_FIRA.csv']
            if not file:  # if file is an empty list
                file = ff['FIRA'][0][0]
    return file


def get_block_data(name, stamp):
    """
    for a given block name and timestamp (corresponding to a session tag) returns the data in the corresponding file
    :param name: (str) block name, such as 'Block2', 'Block3', etc.
    :param stamp: (str) timestamp, such as '2019_06_23_13_31'
    :return: (pandas.DataFrame)
    """
    task_id = NAME_TYPE_ID[name]
    file = get_fira_file_from_timestamp(stamp)
    data = pd.read_csv(file)
    data = data[data['taskID'] == task_id]
    return data


def match_data(s):
    """
    checks whether the session's metadata in s is congruent with data on file and that the latter is congruent with the
    theoretical sequences of trials generated prior to the experiment.
    Several types of incongruences can happen, that we describe below.
      1/ tutorial blocks are simply skipped by this function
      2/ some blocks are present in data file, but are really ghost data, as trialStart (for instance) is NaN
      3/ some blocks are not present at all in the data file
      4/ some blocks are not present at all in the metadata file
    :param s: (dict) with key-value pairs described below:
        if key is one of 'Tut1', 'Block2', etc., value is dict with keys 'aborted', 'completed', 'numTrials', 'reward'
            the Quest block has extra field 'QuestFit' which is a list of values.
        if key is 'sessionTag', value is timestamp as string
        if key is 'trialFolder', value is bare folder name, like 'Blocks003' where the trial data was read from
    :return: (dict) with following structure:
        FIRA_files: [(<path to file1>, <hash of file1>), ...]
        blocks: [BlockInstance1, BlockInstance2, ...]  in order seen by subject?

    """
    timestamp = s['sessionTag']
    to_skip = ['Tut1', 'Tut2', 'Tut3', 'sessionTag', 'trialFolder']
    keys_to_visit = [k for k in s.keys() if k not in to_skip]
    for block_name in keys_to_visit:
        block_info = s[block_name]
        block_data = get_block_data(block_name, timestamp)

        # try:
        #     match = compare_with_theoretical_stimulus(block_name, block_data)
        # except AssertionError:
        #
        # else:

        # block = BlockMetaData(block_name, )


def produce_valid_metadata():
    for subject in meta_data:
        for session, session_info in subject.items():
            match_data(session_info)


class BlockMetaData:
    """
    object that stores metadata about a block of trials run in the experiment
    """
    def __init__(self, name, start, stop, date, num_trials, subject, quest_params=None):
        self.name = name
        self.start = start
        self.stop = stop
        self.data = date
        self.num_trials = num_trials
        self.subject = subject
        self.task_id = NAME_TYPE_ID[self.name]
        self.quest = quest_params
        self.threshold = self.quest[0] if (self.quest is not None) else None


if __name__ == '__main__':
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

    print('ALL GOOD!!!!')
