% read pilot1.mat file to find out whether it contains the dots stimulus
%full path: /Users/adrian/SingleCP_DotsReversal/topsDataLog/pilot1.mat
inFilename = 'pilot2.mat';
taskName = 'SingleCP_DotsReversal';
fileWithPath = ['/Users/adrian/', taskName, '/topsDataLog/', inFilename];
contents = who('-file',fileWithPath);
[topNode, FIRA] = topsTreeNodeTopNode.getDataFromFileWithoutWho(inFilename, taskName, contents);