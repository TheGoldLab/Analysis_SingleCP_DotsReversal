% this script is the standard pre-processing step to convert the data that
% we need for our analysis from .mat to .csv format.

clear all
clear classes
clear mex
clear

%% Folders and path variables

studyTag = 'SingleCP_DotsReversal'; 

% mapping of Pilot data to timestamps
% ======  DO NOT ERASE!! ======
% '2019_03_27_10_49' = Pilot 12
% '2019_04_04_16_59' = Pilot 13
% '2019_04_04_18_00' = Pilot 14
% '2019_04_26_12_05' = test dots dump in office, no dots info in dataset
% '2019_04_26_13_17' = 2nd test of dots dump in office, there is dots info
% =============================
data_timestamp = '2019_04_26_13_17'; 

% location of .csv files to output
csvPath = 'data/Pilot14/';
fileNameWithoutExt = 'pilot14';

%% FIRA.ecodes data
[topNode, FIRA] = ...
    topsTreeNodeTopNode.loadRawData(studyTag,...
    data_timestamp);
T=array2table(FIRA.ecodes.data, 'VariableNames', FIRA.ecodes.name);
writetable(T,[csvPath,fileNameWithoutExt,'_FIRA.csv'],'WriteRowNames',true)

%% Frames data
rawDataFolder = '/Users/adrian/data/';
matFileWithPath = [rawDataFolder,data_timestamp,'/',...
    data_timestamp,'_topsDataLog.mat'];

The_Data_Log = topsDataLog.theDataLog(true);
topsDataLog.readDataFile(matFileWithPath);
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
        'frameTotCount', ...
        'onsetTime', ...
        'onsetFrame', ...
        'swapTime', ...
        'isTight', ...
        'trialIndex'};
numCols = length(colNames);

% build matrix that will be converted to a table at the end
dataMatrix = zeros(0,numCols);
realRowIdx = 1;
for frameTotCount = 1:numFrames
    currFrame = info_frames{frameTotCount};
       
    if isempty(currFrame.trialIndex)
        continue
    end
    
    standardRow = [...
        frameTotCount, ...
        currFrame.onsetTime, ...
        currFrame.onsetFrame, ...
        currFrame.swapTime, ...
        currFrame.isTight, ...
        currFrame.trialIndex];
    
    dataMatrix(realRowIdx,:) = standardRow;
    realRowIdx = realRowIdx + 1;
end

framesDataAsTable=array2table(dataMatrix, 'VariableNames', colNames);
writetable(framesDataAsTable,...
    [csvPath,fileNameWithoutExt,'_framesInfo.csv'],'WriteRowNames',true)

%% Dots data

taskNode = topNode.children{1};
numTrials=length(taskNode.dotsPositions);

% columns of following matrix represent the following variables
dotsColNames = {...
    'xpos', ...
    'ypos', ...
    'isActive', ...
    'isCoherent', ...
    'frameIdx', ...
    'trialCount'};
fullMatrix = zeros(0,length(dotsColNames));
end_block = 0;
for trial = 1:numTrials
    dotsPositions = taskNode.dotsPositions{trial};
    numDotsFrames = size(dotsPositions,3);
    for frame = 1:numDotsFrames
        numDots = size(dotsPositions,2);
        
        start_block = end_block + 1;
        end_block = start_block + numDots - 1;
        
        fullMatrix(start_block:end_block,:) = [...
            squeeze(dotsPositions(:,:,frame)'),...
            repmat([frame, trial],numDots,1)];
    end
end
U=array2table(fullMatrix, 'VariableNames', dotsColNames);
writetable(U,[csvPath,fileNameWithoutExt,'_dotsPositions.csv'],...
    'WriteRowNames',true)