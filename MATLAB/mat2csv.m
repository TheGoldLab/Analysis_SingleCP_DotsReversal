% this script is the standard pre-processing step to convert the data that
% we need for our analysis from .mat to .csv format.
% 
clear all
% clear classes
% clear mex
% clear

%% Folders and path variables

studyTag = 'SingleCP_DotsReversal'; 

% mapping of Pilot data to timestamps
% ======  DO NOT ERASE!! ======
% '2019_03_27_10_49' = Pilot 12
% '2019_04_04_16_59' = Pilot 13
% '2019_04_04_18_00' = Pilot 14
% '2019_04_26_12_05' = test dots dump in office, no dots info in dataset
% '2019_04_26_13_17' = 2nd test of dots dump in office, there is dots info
% '2019_04_29_11_04' = Pilot 15
% '2019_04_29_14_07' = Pilot 16
% '2019_04_30_10_33' = Pilot 17
% '2019_04_30_14_54' = Pilot 18
% '2019_04_30_15_51' = Pilot 19
% =============================
data_timestamp = '2019_04_30_14_54'; 

% location of .csv files to output
csvPath = 'data/Pilot18/';
fileNameWithoutExt = 'pilot18';

%% FIRA.ecodes data
[topNode, FIRA] = ...
    topsTreeNodeTopNode.loadRawData(studyTag,...
    data_timestamp);
T=array2table(FIRA.ecodes.data, 'VariableNames', FIRA.ecodes.name);
writetable(T,[csvPath,fileNameWithoutExt,'_FIRA.csv'],'WriteRowNames',true)
