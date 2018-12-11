%% AIM: write a script that displays the dots stimulus from a specific trial

%% get data from the task 
filename = 'pilot1.mat';
taskName = 'SingleCP_DotsReversal';
[topNode, FIRA] = topsTreeNodeTopNode.getDataFromFile(filename, taskName);

%% set up a dotsDrawable object

% Demonstrate random dot kinetograms, allow visual inspection.
%
% @ingroup dotsDemos
delay=10;

gridSize = 1;

% create a kinetogram with minimal motion features
clean = dotsDrawableDotKinetogram();
clean.stencilNumber = 1;
clean.pixelSize = 3;
clean.diameter = 16;
clean.yCenter = gridSize;
clean.xCenter = -gridSize;
clean.direction = 180;
clean.coherence = 50;

% Aggrigate the kinetograms into one ensemble
kinetograms = topsEnsemble('kinetograms');
kinetograms.addObject(clean);

% automate the task of drawing all the objects
%   the static drawFrame() takes a cell array of objects
% isCell = true;
kinetograms.automateObjectMethod( ...
    'draw', @dotsDrawable.drawFrame, {}, [], isCell);

%% draw it
try
    % get a drawing window
    %sc=dotsTheScreen.theObject;
    %sc.reset('displayIndex', 2);
    dotsTheScreen.reset('displayIndex', 0);
    dotsTheScreen.openWindow();
    
    % get the objects ready to use the window
    kinetograms.callObjectMethod(@prepareToDrawInWindow);
    
    % let the ensemble animate for a while
    kinetograms.run(delay);
    
    % close the OpenGL drawing window
    dotsTheScreen.closeWindow();
    
catch err
    dotsTheScreen.closeWindow();
    rethrow(err)
end
