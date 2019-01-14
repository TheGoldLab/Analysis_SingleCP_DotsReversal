% read pilot1.mat file to find out whether it contains the dots stimulus
%full path: /Users/adrian/SingleCP_DotsReversal/topsDataLog/pilot1.mat
inFilename = 'data_2019_01_14_10_21.mat';
taskName = 'SingleCP_DotsReversal';
fileWithPath = ['/Users/adrian/', taskName, '/topsDataLog/', inFilename];
%contents = who('-file',fileWithPath);
[topNode, FIRA] = topsTreeNodeTopNode.getDataFromFile(inFilename, taskName);