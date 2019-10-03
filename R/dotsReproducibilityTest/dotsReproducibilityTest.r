# this is a script that complements the notebook
library(data.table)
library(ggforce)

path_to_fira <- "/home/adrian/SingleCP_DotsReversal/DotsReproducibilityTest/raw/2019_10_01_11_53/2019_10_01_11_53_FIRA.csv"
fira <- fread(path_to_fira)

path_to_dots <- "/home/adrian/SingleCP_DotsReversal/DotsReproducibilityTest/raw/2019_10_01_11_53/2019_10_01_11_53_dotsPositions.csv"
dots <- fread(path_to_dots)

dots[,trial:=factor(seqDumpTime, ordered=T)]
dotsTrials <- length(levels(dots$trial))

if (dotsTrials == max(fira$trialIndex)) {
  levels(dots$trial) <- seq(dotsTrials)
}

frames <- unique(dots[,.(frameIdx), by=trial])
frameCounts <- frames[,.(maxFrames=max(frameIdx), numFrames=.N), by=trial]

frameCounts[,reltrial:=.I]

png(filename="dotsReproducibilityTest_5th_1_frameCount.png", width=400, height=350)
ggplot(frameCounts, aes(x=reltrial, y=numFrames)) +
  geom_point(size=4) +
  scale_y_continuous(breaks = seq(0, 15, 1)) +
  theme(text=element_text(size=20),
        panel.grid.minor = element_blank(),
        panel.grid.major = element_line(colour = "white",size=0.75))
dev.off()


dots_dt <- dots[isActive == 1, .(xpos, ypos, trial, frameIdx)]
dots_dt[,dotID:=seq(.N), by=.(trial, frameIdx)]

png(filename="dotsReproducibilityTest_5th_1_2.png", width=5000, height=3000)
ggplot(dots_dt, aes(x=xpos, y=ypos, color=xpos)) + geom_point() + facet_grid(trial~frameIdx) + theme(text=element_text(size=20))
dev.off()

dots_melted <- melt(dots_dt, measure.vars=c("xpos", "ypos"), variable.name="axis", value.name="position", id.vars=c("trial", "frameIdx", "dotID"))

png(filename="dotsReproducibilityTest_5th_1_histograms_xpos_ypos.png", width=400, height=1200)
ggplot(dots_melted, aes(x=position, group=axis)) + geom_histogram(bins=500) + facet_grid(frameIdx~axis) + 
	theme(text=element_text(size=15), panel.spacing.y=unit(0, "lines"))
dev.off()
