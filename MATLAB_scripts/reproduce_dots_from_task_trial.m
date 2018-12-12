%% AIM: write a script that displays the dots stimulus from a specific trial

%% get data from the task 
filename = 'pilot1.mat';
taskName = 'SingleCP_DotsReversal';
[topNode, FIRA] = topsTreeNodeTopNode.getDataFromFile(filename, taskName);
trialNumber=10; % different from trialIndex in FIRA

% NOTE: the topNode object defined above is the topNode used for the task
% Hence, the topsTreeNodeTask object corresponding to the task is a child
% of the topNode object. In our case, our task corresponds to the class
% topsTreeNodeTaskSingleCPDotsReversal. When exploring the topNode object,
% the children field will appear with the appropriate task type only if the
% class definition is in the MATLAB path. If it isn't, the children field
% appears empty. But it is not empty, the user may still access the
% topsTreeNodeTask object by accessing topNode.children

%% set up a dotsDrawable object

% get specific parameters to draw the dots:
%    TODO: deal with
% endDirection
% presenceCP
% timeCP
% randSeedBase
% coherenceSTD
% dotsOff-dotsOn

topNodeDrawableSettings = topNode.children{1}.drawable.stimulusEnsemble.dots.settings;

dotsParams.stencilNumber = topNodeDrawableSettings.stencilNumber;
dotsParams.pixelSize = topNodeDrawableSettings.pixelSize;
dotsParams.diameter = topNodeDrawableSettings.diameter;
dotsParams.speed = topNodeDrawableSettings.speed;
dotsParams.yCenter = topNodeDrawableSettings.yCenter;
dotsParams.xCenter = topNodeDrawableSettings.xCenter;
dotsParams.density = topNodeDrawableSettings.density;

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