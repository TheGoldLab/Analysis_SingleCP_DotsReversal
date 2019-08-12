import os.path
import pprint
import json
import hashlib
from collections import Counter
import pandas as pd
import numpy as np
import sys


theoretical_data_folder = '/home/adrian/Documents/MATLAB/projects/Task_SingleCP_DotsReversal/Blocks003/'

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


def consistency_log(fname, files_data, meta_data, ref_hashes, mapping_task_type_id_name):
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
            for file_dict in files_data:
                
                time_stamp = file_dict['session']
                c, s = get_keys(time_stamp, meta_data)
                meta = meta_data[c][s]
                for filename, hhsh in file_dict['FIRA']:
                    assert ref_hashes[filename] == hhsh
                    
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
                    block_names_data = [mapping_task_type_id_name[x] for x in task_ids]
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
                                ensure_counter(table_trial_indices, sort=False, vector_label=mapping_task_type_id_name[tid])

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

                            # todo: even if trialIndex behaves as a pure counter, confirm that the stimulus
                            #       presented on each trial has the same properties as the planned one (from Blocki.csv)
                            block_name = mapping_task_type_id_name[tid]
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
                    block_names_meta = [s for s in meta.keys() if s in mapping_task_type_id_name.values()]
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
    basename = theoretical_data_folder + block_name

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

    for t in range(len(df)):

        row = df.iloc[t]
        trialIndex = int(row['trialIndex'])
        new_count[trialIndex] += 1
        theo_count = trial_count[trialIndex] 
        curr_count = new_count[trialIndex]
        
        assert curr_count <= theo_count, f'row {t}: I count more repeats than collections.Counter'

        if curr_count > 1:
            # ensures repeat trials are consecutive
            assert last_visited == trialIndex, f'row {t}: found a repeat that is not juxtaposed to the first attempt'

        if curr_count == theo_count:
            theo_row = theo_stim.iloc[trialIndex - 1]  # because trialIndex starts counting at 1
            curr_dict = {}
            assert ~np.isnan(row['trialStart']), f"row {t}: trialStart total of {df['trialStart'].isna().sum()} NaN values"
            assert ~np.isnan(row['trialEnd']), f"row {t}: trialEnd total of {df['trialEnd'].isna().sum()} NaN values"
            assert ~np.isnan(row['dirChoice']), f"row {t}: dirChoice total of {df['dirChoice'].isna().sum()} NaN values"
            assert ~np.isnan(row['dirRT']), f'row {t}: dirRT is NaN'
            
            for k, v in values_match.items():
                theo_col, data_col = colname_match[k]
                theo_val = theo_row[theo_col]
                data_val = row[data_col]
                assert (theo_val, data_val) in v, f'row {t}: {(theo_val, data_val)} not found in {v}'
                curr_dict[theo_col] = theo_val
            
            # check change point congruent with endDirection
            if theo_row['cp']:
                assert row['endDirection'] != row['initDirection'], f'row {t}: endDirection does not respect the presence of a change-point'
                
            list_dicts.append(curr_dict)
        last_visited = trialIndex
       
    truncated_theo = theo_stim.iloc[:last_visited]
    return truncated_theo.equals(pd.DataFrame(list_dicts))
