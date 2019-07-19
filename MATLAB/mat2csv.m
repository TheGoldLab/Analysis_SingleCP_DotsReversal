% this script is the standard pre-processing step to convert the data that
% we need for our analysis from .mat to .csv format.
% Since the loading of a .mat file currently causes MATLAB to crash on
% every second attempt, the script can only load one .mat file in a given
% MATLAB session. For this reason, metadata about the loading/dumping is
% stored in another file named metaDump.csv
% The present script reads off the subject and session number to load and
% dump in the current execution, and if everything succeeds, the
% metaDump.csv file is updated (a new row is appended).

clear all
tbUseProject('Analysis_SingleCP_DotsReversal');

%% Load metadata
metadata = loadjson('subj_metadata.json');
subjects = fieldnames(metadata); % 5x1 cell of strings

metadump = readtable('metaDump.csv');  % required to know which subject and session to load
subjNumber = metadump.subject(end);
curr_session = metadump.session(end);

subjStruct = metadata.(subjects{subjNumber});
sessions = fieldnames(subjStruct);  % session names for 

timestamp = subjStruct.(sessions{curr_session}).sessionTag;
datapath = ['/Users/adrian/SingleCP_DotsReversal/raw/',timestamp,'/'];
filename = [timestamp, '_topsDataLog.mat'];


csvPath = datapath;
fileNameWithoutExt = timestamp;
%% FIRA.ecodes data
[topNode, FIRA] = load_SingleCP_file(datapath,filename);

writetable(FIRA,[csvPath,fileNameWithoutExt,'_FIRA.csv'],'WriteRowNames',true)

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
                repmat([frame,dumpTime,subjNumber,taskID],numDots,1)];
        end
   end
end
U=array2table(fullMatrix, 'VariableNames', dotsColNames);
writetable(U,[csvPath,fileNameWithoutExt,'_dotsPositions.csv'],...
    'WriteRowNames',true)
%% Update 
if curr_session < length(sessions)
    metadump(end+1,:) = {subjNumber, curr_session+1};
    writetable(metadump, 'metaDump.csv', 'WriteRowNames',false);
elseif subjNumber < length(subjects)
    metadump(end+1, :) = {subjNumber + 1, 1};
    writetable(metadump, 'metaDump.csv', 'WriteRowNames',false);
else
    disp('all dumped, for all subjects and all sessions')
end
