% clear classes; clear mex; clear all;
filename = '2019_06_20_13_45_topsDataLog.mat';
pathname = '/Users/adrian/SingleCP_DotsReversal/raw/2019_06_20_13_45/';

logStruct = topsDataLog.readDataFile(fullfile(pathname, filename));
group='mainTreeNode';
topNode = logStruct(strncmp(group, {logStruct.group}, length(group)))