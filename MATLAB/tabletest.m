L = length(trial_groups);
for i=1:L
    stru = trial_groups{i};
    if ~isempty(stru)
        T=struct2table(stru);
        disp(T)
    end
end