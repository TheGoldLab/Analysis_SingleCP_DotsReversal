function [topNode, FIRA] = load_SingleCP_file(pathname, filename)

% Clear the data log
topsDataLog.theDataLog(true);

%% Get the ecode matrix using the topsDataLog utility
%
% get the mainTreeNode
mainTreeNodeStruct = topsDataLog.getTaggedData('mainTreeNode', ...
    fullfile(pathname, filename));
topNode = mainTreeNodeStruct.item;

% Now read the ecodes -- note that this works only if the trial
%  struct was made with SCALAR entries only
FIRA.ecodes = myTopsDataLog.parseEcodes('trialData');

%% Get the readable-specific data
%
[~, sessionTag] = fileparts(pathname);
D = dir([fullfile(pathname, sessionTag) '_*']);
for ff = setdiff({D.name}, filename)
    
    % Save as field named after readable subclass
    [~,name] = fileparts(ff{:});
    helperType = name(find(name=='_',1,'last')+1:end);
    
    % Get helper class
    helperClass = ['dotsReadable' helperType];
    
    % Get the helper
    if strcmp(helperType, 'Spike2')
        helper = topNode.helpers.dotsReadableEyeEOG.theObject;
    else
        helper = topNode.helpers.(helperType).theObject;
    end
    
    % Call the dotsReadable static loadDataFile method
    FIRA.(helperType) = feval([helperClass '.loadRawData'], ...
        fullfile(pathname, ff{:}), FIRA.ecodes, helper);
end
% 
% % Look for readableEye data
% helpers = fieldnames(FIRA);
% 
% % Look for spike2 data
% if any(strcmp('Spike2', helpers))
%     FIRA.analog = FIRA.Spike2.analog;
%     FIRA.spikes = FIRA.Spike2.spikes;
% end
end
