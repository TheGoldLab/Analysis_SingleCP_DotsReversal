% this script is the standard pre-processing step to convert the data that
% we need for our analysis from .mat to .csv format.
% 
clear all
tbUseProject('SingleCP_DotsReversal_DataAnalysis');
pilot_number = '19';               % should be a string
npilot = str2double(pilot_number); % pilot number as double
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
timestamp.pilot12 = '2019_03_27_10_49';
timestamp.pilot13 = '2019_04_04_16_59';
timestamp.pilot14 = '2019_04_04_18_00';
timestamp.pilot15 = '2019_04_29_11_04';
timestamp.pilot16 = '2019_04_29_14_07';
timestamp.pilot17 = '2019_04_30_10_33';
timestamp.pilot18 = '2019_04_30_14_54';
timestamp.pilot19 = '2019_04_30_15_51';

data_timestamp = timestamp.(['pilot',pilot_number]); 

% location of .csv files to output
csvPath = ['data/Pilot',pilot_number,'/'];
fileNameWithoutExt = ['pilot',pilot_number];

%% FIRA.ecodes data
[topNode, FIRA] = ...
    topsTreeNodeTopNode.loadRawData(studyTag,...
    data_timestamp);
% T=array2table(FIRA.ecodes.data, 'VariableNames', FIRA.ecodes.name);
% writetable(T,[csvPath,fileNameWithoutExt,'_FIRA.csv'],'WriteRowNames',true)

%% Dots data
% columns of following matrix represent the following variables
dotsColNames = {...
    'xpos', ...
    'ypos', ...
    'isActive', ...
    'isCoherent', ...
    'frameIdx', ...
    'seqDumpTime', ...  % time at which whole sequence of frames was dumped; recall that this is done once per trial, right before exiting the state machine.
    'pilotID', ...
    'taskID'};

fullMatrix = zeros(0,length(dotsColNames));
end_block = 0;

for taskID=1:length(topNode.children)
    taskNode = topNode.children{taskID};
    numTrials=length(taskNode.dotsInfo.dotsPositions);
    if numTrials ~= length(taskNode.dotsInfo.dumpTime)
        error('dumpTime and dotsPositions have distinct length')
    end
        
    for trial = 1:numTrials
        dotsPositions = taskNode.dotsInfo.dotsPositions{trial};
        dumpTime = taskNode.dotsInfo.dumpTime{trial};
        numDotsFrames = size(dotsPositions,3);
        
        for frame = 1:numDotsFrames
            numDots = size(dotsPositions,2);
            
            start_block = end_block + 1;
            end_block = start_block + numDots - 1;
            
            fullMatrix(start_block:end_block,:) = [...
                squeeze(dotsPositions(:,:,frame)'),...
                repmat([frame,dumpTime,npilot,taskID],numDots,1)];
        end
   end
end
U=array2table(fullMatrix, 'VariableNames', dotsColNames);
writetable(U,[csvPath,fileNameWithoutExt,'_dotsPositions.csv'],...
    'WriteRowNames',true)
