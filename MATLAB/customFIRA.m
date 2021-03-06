%% test section
tbUseProject('Analysis_SingleCP_DotsReversal');
timestamp='2019_07_11_11_21';
filename = [timestamp,'_topsDataLog.mat'];
pathname = ['/Users/adrian/SingleCP_DotsReversal/raw/',timestamp,'/'];
D = topsDataLog.readDataFile([pathname,filename]);
LD = length(D);
trial_groups = {};  % one group per block in the task
cc = 0;  % index for trial_groups
old_taskID = -1;
for i = 1:LD
    s=D(i).group;
    if strcmp(s(1:6),'trial_')
        trialDataStruct = D(i).item;
        new_taskID = trialDataStruct.taskID;
        if old_taskID < new_taskID
            cc = cc + 1;
            % save trials from block
            if old_taskID > 0
                trial_groups{cc} = aggregate_struct;
            end
            
            % reset
            aggregate_struct = trialDataStruct;
        elseif old_taskID == new_taskID
            aggregate_struct = [aggregate_struct, trialDataStruct];
        else
            error('taskID non monotonic')
        end
        old_taskID = new_taskID;
    end
end
save([pathname, 'trials_', filename], 'trial_groups', '-v7.3')
