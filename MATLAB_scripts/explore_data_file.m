% read pilot1.mat file to find out whether it contains the dots stimulus
%full path: /Users/adrian/SingleCP_DotsReversal/topsDataLog/pilot1.mat
clear
inFilename = 'data_2019_01_28_10_22.mat';
taskName = 'SingleCP_DotsReversal';

%contents = who('-file',fileWithPath);
[topNode, FIRA] = topsTreeNodeTopNode.getDataFromFile(inFilename, taskName);

% the lines below illustrate how to access a specific group in the
% topsDataLog from the .mat file
fileWithPath = ['/Users/adrian/',taskName,'/topsDataLog/',inFilename];
The_Data_Log = topsDataLog.theDataLog(true);
topsDataLog.readDataFile(fileWithPath);
all_frameInfo = The_Data_Log.getAllItemsFromGroup('frameInfo');