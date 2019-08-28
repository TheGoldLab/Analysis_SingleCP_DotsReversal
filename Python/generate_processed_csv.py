"""
This module's purpose is to leverage the consistency_checks module to produce csv files that are ready to use in R
"""
from consistency_checks import *

VIEWING_DURATIONS = [.1, .2, .3, .4]


def dump_all_data(file_to_write):
    """
    todo: filter --> use superpower metadata
    read all FIRA data files (all subjects, all sessions),
    filter out invalid trials,
    delete columns that I don't think I will need (see cols_to_delete variable in code)
    add: subject, block, date, day and probCP columns
    concatenate into a giant dataframe and writes it to file
    :return: Nothing
    """
    _, metadata, _ = super_power_metadata()

    # debug
    pprint.pprint(metadata)
    list_of_df = []
    for subj_name, sessions in metadata.items():
        for session_date, session_info in sessions.items():
            sess_day = session_info['day_count'] + 1

            # quick exit for debug
            if session_date != '2019_06_20_12_54':
                break

            blocks = [b for b in session_info['blocks'] if (not b['in_meta_not_in_file']) and b['num_trials'] > 0]

            for b in blocks:
                clean_data, _ = get_block_data(b['name'], stamp=session_date)
                # debug
                # print(clean_data.head())
                cols_to_delete = [
                    'targetOff',
                    'fixationOff',
                    'feedbackOn',
                    'dirReleaseChoiceTime',
                    'randSeedBase',
                    'timeCP'
                ]
                clean_data.drop(columns=cols_to_delete, inplace=True)

                # add columns with subject name, session timestamp and block name
                # num_rows = len(clean_data)
                clean_data.insert(0, 'subject', subj_name)
                clean_data.insert(1, 'date', session_date)

                clean_data['block'] = b['name']
                clean_data['day'] = sess_day

                clean_data['probCP'] = np.nan
                for name, pcp in PROB_CP.items():
                    row_selector = clean_data.block == name
                    clean_data.loc[row_selector, 'probCP'] = pcp

                list_of_df.append(clean_data)
    all_data = pd.concat(list_of_df)
    all_data.to_csv(file_to_write, index=False)


def dump_all_pcorr_by_vd_subj_probcp(save_file=None):
    """
    produce a .csv file with the following header:
    probCP,subject,pCorr,lowErr,highErr,numTrials,VD

    And where each row corresponds to a valid trial! This means:
    dirChoice, cpChoice, dirRT, cpRT are not NaN and the RTs are not negative
    """
    # 1. read new metadata
    metadata = read_new_metadata()

    # 2. loop over all FIRA files while keeping running tally of what we need
    keys = []
    for pcp in [0, 0.2, 0.5, 0.8]:
        for s in SUBJECT_NAMES:
            for vdd in VIEWING_DURATIONS:
                keys.append((pcp, s, vdd))

    def accumulate(df, probcp, subj_name):
        # loop over vd
        for vd in VIEWING_DURATIONS:
            key = (probcp, subj_name, vd)
            # todo: finish this function (find out how to update the tally sequentially)
            # update pCorr, lowErr and highErr, numTrials

    for subject, scontent in metadata.items():
        for session, sesscontent in scontent.items():
            # session_data = pd.read_csv(sesscontent['fira_file'][0])
            for b in sesscontent['blocks']:
                if b['in_meta_not_in_file']:
                    continue
                bname = b['name']
                block_data, _ = get_block_data(bname, stamp=session)
                prob_cp = PROB_CP[bname]
                accumulate(block_data, prob_cp, subject)

    if save_file:
        pd.to_csv(save_file, index=False)


if __name__ == '__main__':
    dump_all_data('test_dump.csv')
