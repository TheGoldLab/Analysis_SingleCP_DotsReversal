% read pilot1.mat file to find out whether it contains the dots stimulus
%full path: /Users/adrian/SingleCP_DotsReversal/topsDataLog/pilot1.mat
inFilename = 'pilot1.mat';
taskName = 'SingleCP_DotsReversal';
[topNode, FIRA] = topsTreeNodeTopNode.getDataFromFile(inFilename, taskName);