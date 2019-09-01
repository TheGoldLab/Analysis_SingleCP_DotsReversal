# R script to be run with r-environment R installation
library(data.table)
library(ggforce)
source("explore_functions.r")

data <- get_full_data() 
nonQuestData <- data[block != "Quest"]
to_plot2 <- nonQuestData[
  coherence > 0 &
    coherence < 100 &
    presenceCP == "no-CP",
  .(accuracy=mean(dirCorrect), numTrials=.N),
  by=.(subject, viewingDuration, probCP)
]
to_plot2[,se:=sqrt(accuracy * (1-accuracy) / numTrials)]
to_plot2[,ci:=1.96*se]

png(filename="acc_dd_vd_thcoh_nocp_bysubj_bypcp.png", width=1600, height=1600)

ggplot(aes(x=viewingDuration, y=accuracy, col=subject), data=to_plot2) +
  geom_line(size=1.5) +
  geom_point(size=3) +
  geom_hline(yintercept=c(.5,.9), color="black") +
  geom_errorbar(aes(ymin=accuracy-ci, ymax=accuracy+ci), width=10, size=1) +
  facet_grid(subject~probCP) +
  ggtitle("Accuracy at threshold coh on non-CP trials") +
  theme(text = element_text(size=40))

dev.off()
