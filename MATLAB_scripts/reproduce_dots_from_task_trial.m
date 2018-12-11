%% AIM: write a script that displays the dots stimulus from a specific trial

%% get data from the task 
filename = 'pilot1.mat';
taskName = 'SingleCP_DotsReversal';
[topNode, FIRA] = topsTreeNodeTopNode.getDataFromFile(filename, taskName);
trialNumber=10; % different from trialIndex in FIRA

%% set up a dotsDrawable object

% get specific parameters to draw the dots, namely:
% initDirection
% coherence
% viewingDuration (or dotsOff-dotsOn?)
% 
%    TODO: deal with
% endDirection
% presenceCP
% timeCP
% randSeedBase
%    TODO 2: also find a way to store and retrieve
% stencilNumber
% pixelSize
% diameter 
% speed

clean.yCenter = gridSize;
clean.xCenter = -gridSize;

% get appropriate column numbers for FIRA.ecodes.data matrix
col.direction = find(strcmp(FIRA.ecodes.name, 'initDirection'),1);
col.coherence = find(strcmp(FIRA.ecodes.name, 'coherence'),1);
col.dotsDuration = find(strcmp(FIRA.ecodes.name, 'viewingDuration'),1);

% get actual parameter values from FIRA.ecodes.data matrix
dotsParams.direction = FIRA.ecodes.data(trialNumber, col.direction);
dotsParams.coherence = FIRA.ecodes.data(trialNumber, col.coherence);
dotsParams.dotsDuration = FIRA.ecodes.data(trialNumber, col.dotsDuration);

%% Draw the dots
draw_dots(dotsParams)