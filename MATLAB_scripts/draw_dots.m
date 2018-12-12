function draw_dots(dotsParams)

% create a kinetogram with minimal motion features
clean = dotsDrawableDotKinetogram();

clean.stencilNumber = dotsParams.stencilNumber;
clean.pixelSize = dotsParams.pixelSize;
clean.diameter = dotsParams.diameter;
clean.density = dotsParams.density;

clean.yCenter = dotsParams.yCenter;
clean.xCenter = dotsParams.xCenter;

clean.direction = dotsParams.direction;
clean.coherence = dotsParams.coherence;

% Aggrigate the kinetograms into one ensemble
kinetograms = topsEnsemble('kinetograms');
kinetograms.addObject(clean);

% automate the task of drawing all the objects
%   the static drawFrame() takes a cell array of objects
isCell = true;
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
    time = mglGetSecs;
    while mglGetSecs < time + dotsParams.dotsDuration
       ret = dotsDrawable.drawFrame(kinetograms.objects)
    end
    %kinetograms.run(dotsParams.dotsDuration);
    
    % close the OpenGL drawing window
    dotsTheScreen.closeWindow();
    
catch err
    dotsTheScreen.closeWindow();
    rethrow(err)
end

end