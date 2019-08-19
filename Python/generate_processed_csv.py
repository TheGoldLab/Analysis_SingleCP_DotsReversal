"""
This module's purpose is to leverage the consistency_checks module to produce csv files that are ready to use in R
"""
from consistency_checks import *

VIEWING_DURATIONS = [.1, .2, .3, .4]

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


