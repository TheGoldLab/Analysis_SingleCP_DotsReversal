"""test validate_trials method"""
import numpy as np
import pandas as pd


def validate_trials(initial_df):
    """
    remove all rows from df that do not meet the following conditions:
       1. dirCorrect is not NaN
       2. cpCorrect is not NaN if probCP > 0
       3. dirChoice is not NaN
       4. cpChoice is not NaN if probCP > 0
       5. dirRT > 0
       6. cpRT > 0 if probCP > 0
       7. abs(dotsOff - dotsOn - viewingDuration) < tolerance (45 msec)
       8. trialIndex should NOT be repeated
    :param initial_df: dataframe in the format of FIRA.ecodes
    :return: copy of the modified df, or None if nothing is left after filtering out bad trials
    """
    vd_tolerance = 45 / 1000  # in seconds

    print('original')
    print(initial_df)
    print()
    df = initial_df.copy()  # just to make sure I don't modify the df outside of the function
    df = df[df['dirCorrect'].notna()]  # 1 -- checked
    # print(1)
    # print(df)
    # print()
    df = df[df['dirChoice'].notna()]  # 3 -- checked
    # print(3)
    # print(df)
    # print()
    df = df[df['dirRT'] > 0]  # 5  -- checked
    # print(5)
    # print(df)
    # print()
    df = df[((df['condProbCP'] > 0) & (df['cpRT'] > 0)) | (df['condProbCP'] == 0)]  # 6  -- checked
    print(6)
    print(df)
    print()
    df = df[((df['condProbCP'] > 0) & (df['cpCorrect'].notna())) | (df['condProbCP'] == 0)]  # 2  --  checked
    print(2)
    print(df)
    print()
    df = df[((df['condProbCP'] > 0) & (df['cpChoice'].notna())) | (df['condProbCP'] == 0)]  # 4  --  checked
    print(4)
    print(df)
    print()

    # the following is inspired from this answer: https://stackoverflow.com/a/18182241
    def check_vd(row):
        return abs(row['dotsOff'] - row['dotsOn'] - row['viewingDuration']) < vd_tolerance

    print('pb')
    print(df.apply(check_vd, axis=1))
    print()
    df = df[df.apply(check_vd, axis=1)]  # 7  -- checked
    print(7)
    print(df)
    print()
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


if __name__ == '__main__':
    # get a mock data frame
    custom_fira_file = '/home/adrian/SingleCP_DotsReversal/raw/2019_07_10_17_42/2019_07_10_17_42customFIRA.csv'
    quest_file = '/home/adrian/SingleCP_DotsReversal/raw/2019_06_20_12_54/2019_06_20_12_54_FIRA.csv'
    data = pd.read_csv(quest_file)
    data = data.drop(['taskID', 'endDirection', 'startResponseTwo', 'targetOff', 'fixationOff', 'feedbackOn', 'CPresponseSide',
                      'dirReleaseChoiceTime', 'cpChoiceTime', 'dirChoiceTime', 'targetOn', 'fixationStart',
                      'fixationOn', 'randSeedBase', 'timeCP', 'coherence', 'presenceCP', 'trialEnd',
                      'trialStart'], axis=1)
    data = data.iloc[:5]
    # print('mock data frame')
    print(data.columns)

    # # populate it with bad rows
    # last_row = data.iloc[-1]
    #
    # corrupted = [dict(last_row.copy()) for _ in range(7)]
    # corrupted[0]['dirCorrect'] = np.nan
    # corrupted[1]['cpCorrect'] = np.nan
    # corrupted[2]['dirChoice'] = np.nan
    # corrupted[3]['cpChoice'] = np.nan
    # corrupted[4]['dirRT'] = -.1
    # corrupted[5]['cpRT'] = -.2
    # corrupted[6]['dotsOff'] = corrupted[6]['dotsOff'] + 1
    # # for i, c in enumerate(corrupted):
    # #     c.set_index(i+5)
    #
    # new_data = pd.DataFrame(corrupted)
    # fin = pd.concat([data.reset_index(drop=True), new_data.reset_index(drop=True)], axis=0)
    # # print('corrupted dataframe')
    # # print(fin)
    # print('epurated one')

    validate_trials(data)

