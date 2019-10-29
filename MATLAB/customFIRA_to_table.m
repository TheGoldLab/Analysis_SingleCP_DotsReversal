clear
list_of_files = { ...
'/home/adrian/SingleCP_DotsReversal/raw/2019_06_21_14_25/trials_2019_06_21_14_25_topsDataLog.mat', ...
'/home/adrian/SingleCP_DotsReversal/raw/2019_07_10_17_42/trials_2019_07_10_17_42_topsDataLog.mat', ...
'/home/adrian/SingleCP_DotsReversal/raw/2019_06_20_13_45/trials_2019_06_20_13_45_topsDataLog.mat', ...
'/home/adrian/SingleCP_DotsReversal/raw/2019_07_08_17_13/trials_2019_07_08_17_13_topsDataLog.mat', ...
'/home/adrian/SingleCP_DotsReversal/raw/2019_06_25_14_06/trials_2019_06_25_14_06_topsDataLog.mat', ...
'/home/adrian/SingleCP_DotsReversal/raw/2019_06_24_12_38/trials_2019_06_24_12_38_topsDataLog.mat', ...
'/home/adrian/SingleCP_DotsReversal/raw/2019_07_09_11_02/trials_2019_07_09_11_02_topsDataLog.mat', ...
'/home/adrian/SingleCP_DotsReversal/raw/2019_07_11_11_21/trials_2019_07_11_11_21_topsDataLog.mat', ...
'/home/adrian/SingleCP_DotsReversal/raw/2019_06_27_11_33/trials_2019_06_27_11_33_topsDataLog.mat', ...
'/home/adrian/SingleCP_DotsReversal/raw/2019_06_21_13_34/trials_2019_06_21_13_34_topsDataLog.mat' ...
};


for i=1:length(list_of_files)  % loop over files
    f = list_of_files{i};
    timestamp=f(40:55);
    folder = f(1:56);
    disp(timestamp)
    
    fstruct = load(f);
    FIRA = table();
    session_cells = fstruct.trial_groups;
    for s = 1:length(session_cells)  % loop over blocks
        if isempty(session_cells{s})
            continue
        else
            c = session_cells{s};  % this is  a struct
            for t=1:length(c)
                trial = c(t);
                if isempty(trial.trialStart)
                    c(t).trialStart = nan;
                end
                if isempty(trial.trialEnd)
                    c(t).trialEnd = nan;
                end
            end
            FIRA = [FIRA; struct2table(c)];
        end
    end
    fname = [folder, timestamp, 'customFIRA.csv'];
    writetable(FIRA, fname)
end
