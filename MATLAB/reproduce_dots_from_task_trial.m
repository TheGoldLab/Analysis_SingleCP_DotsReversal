%% AIM: run script that generates the dots frames based on task parameters and seed values

%% get data from the task (currently who-MEX bug)
clear all

% filename = 'raw/2019_06_07_14_32/2019_06_07_14_32_topsDataLog.mat';
% taskName = 'SingleCP_DotsReversal';
studyTag = 'SingleCP_DotsReversal';
sessionTag = '2019_06_07_14_32';
[topNode, FIRA] = topsTreeNodeTopNode.loadRawData(studyTag, sessionTag);


% NOTE: the topNode object defined above is the topNode used for the task
% Hence, the topsTreeNodeTask object corresponding to the task is a child
% of the topNode object. In our case, our task corresponds to the class
% topsTreeNodeTaskSingleCPDotsReversal. When exploring the topNode object,
% the children field will appear with the appropriate task type only if the
% class definition is in the MATLAB path. If it isn't, the children field
% appears empty. But it is not empty, the user may still access the
% topsTreeNodeTask object by accessing topNode.children

% NOTE 2: to get frame rate from the monitor that produced the original
% stimulus, access
% topNode.helpers.screenEnsemble.theObject.objects{1}.windowFrameRate
% recall that the dotsDrawableDotKinetogram.prepareToDrawInWindow rounds
% this to the nearest 10 (so 56 Hz becomes 60, and 55 becomes 60 too since 
% 'round()' is used).

%% set up a dotsDrawable object

% get specific parameters to draw the dots:
%    TODO: deal with
% endDirection
% presenceCP
% timeCP
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
col.randSeedBase = find(strcmp(FIRA.ecodes.name, 'randSeedBase'),1);

trialNumber=10; % different from trialIndex in FIRA
% get actual parameter values from FIRA.ecodes.data matrix
dotsParams.direction = FIRA.ecodes.data(trialNumber, col.direction);
dotsParams.coherence = FIRA.ecodes.data(trialNumber, col.coherence);
dotsParams.dotsDuration = FIRA.ecodes.data(trialNumber, col.dotsDuration);
dotsParams.randSeedBase = FIRA.ecodes.data(trialNumber, col.randSeedBase);

%% Draw the dots
draw_dots(dotsParams)