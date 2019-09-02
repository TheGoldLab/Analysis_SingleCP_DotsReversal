# R script to be run with r-environment R installation
library(data.table)
library(ggforce)
source("explore_functions.r")

data <- get_full_data() 
nonQuestData <- data[block != "Quest"]

## Acc (DD) on non-CP trials as function of VD for threshold coherence, by subject by probCP
#to_plot2 <- nonQuestData[
#  coherence > 0 &
#    coherence < 100 &
#    presenceCP == "no-CP",
#  .(accuracy=mean(dirCorrect), numTrials=.N),
#  by=.(subject, viewingDuration, probCP)
#]
#to_plot2[,se:=sqrt(accuracy * (1-accuracy) / numTrials)]
#to_plot2[,ci:=1.96*se]
#
#png(filename="acc_dd_vd_thcoh_nocp_bysubj_bypcp.png", width=1600, height=1600)
#
#ggplot(aes(x=viewingDuration, y=accuracy, col=subject), data=to_plot2) +
#  geom_line(size=1.5) +
#  geom_point(size=3) +
#  geom_hline(yintercept=c(.5,.9), color="black") +
#  geom_errorbar(aes(ymin=accuracy-ci, ymax=accuracy+ci), width=10, size=1) +
#  facet_grid(subject~probCP) +
#  ggtitle("Accuracy at threshold coh on non-CP trials") +
#  theme(text = element_text(size=40))
#
#dev.off()


#Accuracy (DD) on non-CP trials as a function of coherence, for fixed viewing duration.

factored_threshold <- nonQuestData[,coh_cat:="0"]
factored_threshold[coherence > 0, coh_cat:= "th"]
factored_threshold[coherence==100, coh_cat:="100"]
factored_threshold[,coh_cat:=factor(coh_cat, levels=c("0", "th", "100"), ordered=T)]

#to_plot3 <- factored_threshold[
#    presenceCP == "no-CP",
#  .(accuracy=mean(dirCorrect), numTrials=.N),
#  by=.(subject, viewingDuration, coh_cat)
#]
#to_plot3[,se:=sqrt(accuracy * (1-accuracy) / numTrials)]
#to_plot3[,ci:=1.96*se]
#
#png(filename="acc_dd_cohcat_nocp_bysubj_byvd.png", width=1600, height=1600)
#ggplot(aes(x=coh_cat, y=accuracy, col=subject), data=to_plot3) +
#  geom_point(size=5) +
#  geom_hline(yintercept=c(.5,1), color="black") +
#  geom_errorbar(aes(ymin=accuracy-ci, ymax=accuracy+ci), width=.1, size=2) +
#  facet_grid(subject~viewingDuration) +
#  ggtitle("Acc on non-CP trials, by subject by VD") +
#  theme(text = element_text(size=40))
#dev.off()



##Accuracy at 100 & 200 msec for fixed coh is invariant across all ProbCP conditions
#to_plot4 <- factored_threshold[
#  viewingDuration < 250 &
#    coh_cat == "th",
#  .(accuracy=mean(dirCorrect), numTrials=.N),
#  by=.(subject, viewingDuration, probCP)
#]
#to_plot4[,se:=sqrt(accuracy * (1-accuracy) / numTrials)]
#to_plot4[,ci:=1.96*se]
#
#png(filename="acc_dd_pcp_nocp_bysubj_byvd.png", width=1000, height=1600)
#
#ggplot(aes(x=probCP, y=accuracy, col=subject), data=to_plot4) +
#  geom_point(size=3) +
#  geom_line(group=1, size=2) +
#  geom_hline(yintercept=c(.5,1), color="black") +
#  geom_errorbar(aes(ymin=accuracy-ci, ymax=accuracy+ci), width=.2, size=1) +
#  facet_grid(subject~viewingDuration) +
#  theme(text = element_text(size=35))
#
#dev.off()


## Per prob-CP condition, accuracy at 200 msec ishigher than at 300 msecon CP trials.
#to_plot5 <- factored_threshold[
#  ((viewingDuration == 200) | (viewingDuration == 300 & presenceCP == "CP")) &
#    coh_cat=="th",
#  .(accuracy=mean(dirCorrect), numTrials=.N),
#  by=.(presenceCP, subject, viewingDuration, probCP)
#]
#to_plot5[,se:=sqrt(accuracy * (1-accuracy) / numTrials)]
#to_plot5[,ci:=1.96*se]
#
#png(filename="acc_dd_cp_short_bysubj_bypcp.png", width=1000, height=1000)
#ggplot(to_plot5, aes(x=factor(viewingDuration), y=accuracy, col=presenceCP)) +
#  geom_point(size=5) +
#  geom_hline(yintercept=c(.5,1), color="black", linetype="dashed") +
#  geom_errorbar(aes(ymin=accuracy-ci, ymax=accuracy+ci), width=.2, size=2) +
#  facet_grid(subject~probCP) +
#  scale_color_brewer(palette="Dark2") +
#  theme(text = element_text(size=35))
#dev.off()

## as above, but with points for 300 msec no CP trials.
#to_plot6 <- factored_threshold[
#  ((viewingDuration == 200) | (viewingDuration == 300)) &
#    coh_cat=="th",
#  .(accuracy=mean(dirCorrect), numTrials=.N),
#  by=.(presenceCP, subject, viewingDuration, probCP)
#]
#to_plot6[,se:=sqrt(accuracy * (1-accuracy) / numTrials)]
#to_plot6[,ci:=1.96*se]
#
#pd <- position_dodge(.2) # move them .05 to the left and right
#
#png(filename="acc_dd_aroundCP_bysubj_bypcp.png", width=1050, height=1000)
#ggplot(to_plot6, aes(x=factor(viewingDuration), y=accuracy, col=presenceCP, group=presenceCP)) +
#  geom_point(size=4, position=pd) +
#  geom_hline(yintercept=c(.5,1), color="black", linetype="dashed") +
#  geom_errorbar(aes(ymin=accuracy-ci, ymax=accuracy+ci), width=.1, size=1.7, position=pd) +
#  facet_grid(subject~probCP) +
#  scale_color_brewer(palette="Dark2") +
#  theme(text = element_text(size=35))
#dev.off()

# as above, but for 200-400 msec trials.
#to_plot6 <- factored_threshold[
#  viewingDuration > 150 &
#    coh_cat=="th",
#  .(accuracy=mean(dirCorrect), numTrials=.N),
#  by=.(presenceCP, subject, viewingDuration, probCP)
#]
#to_plot6[,se:=sqrt(accuracy * (1-accuracy) / numTrials)]
#to_plot6[,ci:=1.96*se]
#
#pd <- position_dodge(.2) # move them .05 to the left and right
#
#png(filename="acc_dd_200-400_bysubj_bypcp_bycp.png", width=1600, height=1300)
#ggplot(to_plot6, aes(x=factor(viewingDuration), y=accuracy, col=presenceCP, group=presenceCP)) +
#  geom_point(size=4, position=pd) +
#  geom_line(size=2) +
#  geom_hline(yintercept=c(.5,1), color="black", linetype="dashed") +
#  geom_errorbar(aes(ymin=accuracy-ci, ymax=accuracy+ci), width=.1, size=1.7, position=pd) +
#  facet_grid(subject~probCP) +
#  scale_color_brewer(palette="Dark2") +
#  theme(text = element_text(size=35)) + 
#  ggtitle("Acc (DD) th-coh")
#dev.off()





#The probability of being correct on 300-msec change-point trials
#should be greater (but still below %50) than the probability of being
#wrong on 100-msec trials
to_plota <- factored_threshold[
  ((viewingDuration == 100) | (viewingDuration == 300 & presenceCP == "CP")) &
    coh_cat=="th",
  .(accuracy=mean(dirCorrect), numTrials=.N),
  by=.(presenceCP, subject, viewingDuration, probCP)
]
to_plota[, y:=accuracy]
to_plota[viewingDuration==100, y:=1-y]  # P(wrong)for 100 msec
to_plota[,se:=sqrt(y * (1-y) / numTrials)]
to_plota[,ci:=1.96*se]


png(filename="pwrong_pcorr_100-300_bysubj_bypcp_bycp.png", width=1150, height=1300)
ggplot(to_plota, aes(x=factor(viewingDuration), y=y, col=presenceCP)) +
  geom_point(size=5) +
  geom_hline(yintercept=c(0, .5), color="black", linetype="dashed") +
  geom_errorbar(aes(ymin=y-ci, ymax=y+ci), width=.1, size=2) +
  facet_grid(subject~probCP) +
  labs(title="") +
  xlab("Viewing Duration") + ylab("P(wrong) vs. P(correct)") +
  ggtitle("P(wrong|noCP) vs. P(correct|CP) \n on 100 vs. 300 CP trials") +
  scale_color_manual(labels = c("P(wrong|noCP)", "P(correct|CP)"), values = c("darkred", "darkgreen")) + 
  theme(text = element_text(size=35))  
#  theme_bw()
dev.off()
