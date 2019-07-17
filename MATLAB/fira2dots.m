function fira2dots(fira_table, out_filename, path_to_folder, extra_params)
% Generate the dots stimulus corresponding to a FIRA.ecodes matrix and 
% write the normalized dots positions to a csv file, with column names
% ARGS:
%   fira_table      a table with the format from FIRA.ecodes
%   out_filename    string for filename, without path nor extension.
%   path_to_folder  string for path to folder where file should be
%                   written, folder should exist, and string should contain 
%                   trailing '/'. So, to write in the working directory,
%                   pass in './'
%   extra_params    a struct with fields corresponding to parameter values
%                   not contained in the FIRA table. As of 04/24/2019, the 
%                   list of such parameters is:
%                    stencilNumber
%                    pixelSize
%                    diameter
%                    density
%                    yCenter
%                    xCenter
%                    coherenceSTD
% RETURNS:
%   Nothing, but creates 1 file with full path 
%   [path_to_folder,outFilename_dotsPositions.csv]

if exist(path_to_folder)
    if ~strcmp(path_to_folder(end), '/')
        error('folder name should end with /')
    end
    ofile = [path_to_folder, out_filename, '_dotsPositions.csv'];
else
    error(['folder ', path_to_folder, ' not found; no file was written.'])
end

dots = dotsDrawableDotKinetogram();

% EXTRACT PARAMETERS FROM extra_params REQUIRED TO REPRODUCE THE DOTS STIMULUS
dots.stencilNumber = extra_params.stencilNumber;
dots.pixelSize = extra_params.pixelSize;
dots.diameter = extra_params.diameter;
dots.density = extra_params.density;
dots.yCenter = extra_params.yCenter;
dots.xCenter = extra_params.xCenter;
dots.coherenceSTD = extra_params.coherence_STD;

% EXTRACT PARAMETERS FROM FIRA REQUIRED TO REPRODUCE THE DOTS STIMULUS
 = fira_table.initDirection;
 = fira_table.endDirection;
dots.coherence = fira_table.coherence;
dots.duration = fira_table.viewingDuration;
dots.randBase = fira_table.randSeedBase;
% as of 12/13/18, this base random seed is used as described in this line:
% https://github.com/TheGoldLab/Lab-Matlab-Control/blob/bf12ab259585ba34a549f6fbbe97e8a4f4b6791d/snow-dots/classes/drawable/dotsDrawableDotKinetogram.m#L145

% REPRODUCE THE DOTS
...

% WRITE THE DOTS TO FILE
...

end