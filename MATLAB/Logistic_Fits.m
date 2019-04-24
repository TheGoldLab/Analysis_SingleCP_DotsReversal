% reproducing section 4.2.4 from Kingdom and Prins' book
% uses palamedes toolbox
% I imported the data from this cell
% https://nbviewer.jupyter.org/github/aernesto/SingleCP_DotsReversal_DataAnalysis/blob/e7d1eb466f88b69dee72062974551e1b4b973a25/Jupyter/pilot11.ipynb#Accuracy-as-a-function-of-coherence-level

clear

%% Standard vectors required by Palamedes fitting routines
StimLevels=[12,24,36,48,60];
NumPos=[43,44,45,60,75];
OutOfNum=[79,87,70,80,80];

%% use demo file
% 'PAL_PFML_Demo.m'
%% alternatively, follow book section by section
PF=@PAL_Logistic;
paramsValues=[48, 1, .5, 0];
paramsFree=[1 1 0 0];
[paramsValues LL exitflag] = ...
    PAL_PFML_Fit(StimLevels, NumPos, OutOfNum, paramsValues, ...
    paramsFree, PF)
PropCorrectData=NumPos./OutOfNum;
StimLevelsFine=[min(StimLevels):max(StimLevels)];
Fit=PF(paramsValues,StimLevelsFine);
plot(StimLevelsFine, PropCorrectData, 'k.','markersize',40);
Error using plot
Vectors must be the same length.
 
plot(StimLevels, PropCorrectData, 'k.','markersize',40);
set(gca,'fontsize',12);
axis([0,.12,.4,1]);
axis([10,60,.4,1]);
axis([10,62,.4,1]);
hold on;
plot(StimLevelsFine, Fit, 'g-','linewidth',4);
hold off;

% following section 4.2.5 for error on fitted parameters
B=400;
[SD paramsSim LLSim converged] = ...
    PAL_PFML_BootstrapParametric(StimLevels, OutOfNum, paramsValues, ...
    paramsFree, B, PF);
SD

% following section 4.2.6 for goodness of fit
B=1000;
[Dev pDev DevSim converged] = ...
    PAL_PFML_GoodnessOfFit(StimLevels, NumPos, OutOfNum, ...
    paramsValues, paramsFree, B, PF);