% This script uses Quest+ to fit a psychometric curve to data collected 
% in the Quest node of our task
%% load the Quest structure from the first node
clear
studyTag = 'SingleCP_DotsReversal';
sessionTag = '2019_03_27_10_49'; % corresponds to pilot12 data

[topNode, FIRA] = ...
    topsTreeNodeTopNode.loadRawData(studyTag,...
    sessionTag);
T=array2table(FIRA.ecodes.data, 'VariableNames', FIRA.ecodes.name);

questData = topNode.children{1}.quest;
%equivalent way to access same data:
%otherQuestData = topNode.children{2}.settings.useQuest.quest;
%isequaln(questData,otherQuestData)

%% Get estimated parameters, fitted parameters and plot corresponding ...
% psychometric function with data

% source of inspiration: qpQuestPlusPaperSimpleExamplesDemo
psiParamsIndex = qpListMaxArg(questData.posterior); % essentially performs argmax operation in index space
psiParamsQuest = questData.psiParamsDomain(psiParamsIndex,:);

% Maximum likelihood fit.  Use psiParams from QUEST+ as the starting
% parameter for the search, and impose as parameter bounds the range
% provided to QUEST+.

psiParamsFit = qpFit(questData.trialData,@qpPFStandardWeibull,psiParamsQuest,questData.nOutcomes,...
    'lowerBounds', min(questData.psiParamsDomain), ...
    'upperBounds', max(questData.psiParamsDomain));
% fprintf('Maximum likelihood fit parameters: %0.1f, %0.1f, %0.1f, %0.2f\n', ...
%     psiParamsFit(1),psiParamsFit(2),psiParamsFit(3),psiParamsFit(4));

% Plot with data
figure; clf; hold on
stimCounts = qpCounts(qpData(questData.trialData),questData.nOutcomes);
stim = [stimCounts.stim];
stimFine = questData.stimParamsDomain;
plotProportionsEst = qpPFStandardWeibull(stimFine,psiParamsQuest);
plotProportionsFit = qpPFStandardWeibull(stimFine,psiParamsFit);
for cc = 1:length(stimCounts)
    nTrials(cc) = sum(stimCounts(cc).outcomeCounts);
    pCorrect(cc) = stimCounts(cc).outcomeCounts(2)/nTrials(cc);
end
for cc = 1:length(stimCounts)
    h = scatter(stim(cc),pCorrect(cc),100,'o','MarkerEdgeColor',[0 0 1],'MarkerFaceColor',[0 0 1],...
        'MarkerFaceAlpha',nTrials(cc)/max(nTrials),'MarkerEdgeAlpha',nTrials(cc)/max(nTrials));
end
p1=plot(stimFine,plotProportionsEst(:,2),'-','Color',[1 0.2 0.0],'LineWidth',3);
p2=plot(stimFine,plotProportionsFit(:,2),'-','Color',[0.0 0.2 1.0],'LineWidth',3);
xlabel('coherence');
ylabel('Proportion Correct');
xlim([0 100]); ylim([0 1]);
title({'QUEST+ Weibull (threshold and lapse)', ''});
legend([h,p1,p2], 'data', 'estimate', 'MLE fit')
drawnow;