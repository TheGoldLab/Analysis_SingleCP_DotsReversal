function [topNode, FIRA] = load_SingleCP_file(pathname, filename)
% Args:
%    pathname - path ending with '/' where file dumped by task resides
%    filename - actual filename that was dumped by the MATLAB task

% Clear the data log
topsDataLog.theDataLog(true);

%% Get the ecode matrix using the topsDataLog utility
%
% get the mainTreeNode
mainTreeNodeStruct = topsDataLog.getTaggedData('mainTreeNode', ...
    fullfile(pathname, filename));
topNode = mainTreeNodeStruct.item;

FIRA =table;
disp('FIRA defined')
disp(pathname)
disp(filename)
numChildren = length(topNode.children);
for c = 1:numChildren
    task = topNode.children{c};
    trials = task.trialData;
    if length(trials) == 1 || strcmp(task.name(1:3), 'Tut')
        continue
    else
        disp('in the loop')
        disp(task.name)
        
        % replace empty vector entries by NaN before merging into table
        for trial=1:length(trials)
            if isempty(trials(trial).trialStart)
                trials(trial).trialStart = nan;
            end
            if isempty(trials(trial).trialEnd)
                trials(trial).trialEnd = nan;
            end            
        end
        FIRA = [FIRA; struct2table(trials)];
    end
end
disp('exiting load_SingleCP_file')
end
