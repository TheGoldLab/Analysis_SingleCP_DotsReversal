# this is a script that complements the notebook
library(data.table)
library(ggforce)

path_to_fira <- "/home/adrian/SingleCP_DotsReversal/DotsReproducibilityTest/raw/2019_09_23_14_49/2019_09_23_14_49_FIRA.csv"
fira <- fread(path_to_fira)

path_to_dots <- "/home/adrian/SingleCP_DotsReversal/DotsReproducibilityTest/raw/2019_09_23_14_49/2019_09_23_14_49_dotsPositions.csv"
dots <- fread(path_to_dots)

dots[,trial:=factor(seqDumpTime, ordered=T)]
dotsTrials <- length(levels(dots$trial))

if (dotsTrials == max(fira$trialIndex)) {
  levels(dots$trial) <- seq(dotsTrials)
}

dots_dt <- dots[isActive == 1, .(xpos, ypos, trial, frameIdx)]
dots_dt[,dotID:=seq(.N), by=.(trial, frameIdx)]

png(filename="dotsReproducibilityTest_2.png", width=5000, height=3000)
ggplot(dots_dt, aes(x=xpos, y=ypos, color=xpos)) + geom_point() + facet_grid(trial~frameIdx) + theme(text=element_text(size=20))
dev.off()
