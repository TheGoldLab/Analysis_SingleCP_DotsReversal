function dumpFIRAecodes2csv(inFilename, outFilename, taskName, fetchDots)
% writes the FIRA.ecodes matrix to csv file, with column names
% ARGS:
%   inFilename      input filename with .mat extension but without full
%                   path
%   outFilename     output filename, including full path but NOT the extension
%   taskName        e.g. 'SingleCP_DotsReversal'
%   fetchDots       boolean. If true, dumps topNode.dotsPositions to a
%                   separate csv file
% RETURNS:
%   Nothing, but creates 1 (or 2 if fetchDots = true) files with full path 
%   outFilename_FIRA.csv and outFilename_dotsPositions.csv

% read data from file
[topNode, FIRA] = topsTreeNodeTopNode.getDataFromFile(inFilename, taskName);
fileWithPath = ['/Users/adrian/',taskName,'/topsDataLog/',inFilename];
The_Data_Log = topsDataLog.theDataLog(true);
topsDataLog.readDataFile(fileWithPath);
all_frameInfo = The_Data_Log.getAllItemsFromGroup('frameInfo');


taskNode = topNode.children{1};
numTrials=length(taskNode.dotsPositions);

T=array2table(FIRA.ecodes.data, 'VariableNames', FIRA.ecodes.name);
writetable(T,[outFilename,'_FIRA.csv'],'WriteRowNames',true)

if fetchDots
    % columns of following matrix represent the following variables
    colNames = {...
        'xpos', ...
        'ypos', ...
        'isActive', ...
        'isCoherent', ...
        'frameIdx', ...
        'trialIdx'};
    fullMatrix = zeros(0,length(colNames));
    end_block = 0;
    for trial = 1:numTrials
        dotsPositions = taskNode.dotsPositions{trial};
        numFrames = size(dotsPositions,3);
        for frame = 1:numFrames
            numDots = size(dotsPositions,2);
            
            start_block = end_block + 1;
            end_block = start_block + numDots - 1;
                       
            fullMatrix(start_block:end_block,:) = [...
                squeeze(dotsPositions(:,:,frame)'),...
                repmat([frame, trial],numDots,1)]; 
        end
    end
    U=array2table(fullMatrix, 'VariableNames', colNames);
    writetable(U,[outFilename,'_dotsPositions.csv'],'WriteRowNames',true)
end
end
