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
info_frames = The_Data_Log.getAllItemsFromGroup('frameInfo');


% count number of frames actually drawn
numFrames=1;
if isempty(info_frames{end})
    while ~isempty(info_frames{numFrames})
        numFrames = numFrames+1;
    end
    numFrames = numFrames - 1; % correct for last increment of while loop
else
    numFrames = length(info_frames);
end

colNames = {...
        'frameIdx', ...
        'onsetTime', ...
        'onsetFrame', ...
        'swapTime', ...
        'isTight'};
numCols = length(colNames);
% build matrix that will be converted to a table at the end
dataMatrix = zeros(numFrames,numCols);

for frameIdx = 1:numFrames
    currFrame = info_frames{frameIdx};
       
    % prepare all but last 3 cols of the 'standard row' to fill
    standardRow = [frameIdx, currFrame.onsetTime, currFrame.onsetFrame,...
        currFrame.swapTime, currFrame.isTight];
    
    dataMatrix(frameIdx,:) = standardRow;
end



framesDataAsTable=array2table(dataMatrix, 'VariableNames', colNames);
writetable(framesDataAsTable,...
    ['/Users/adrian/SingleCP_DotsReversal/pilot4',...
    '_framesInfo.csv'],'WriteRowNames',true)


