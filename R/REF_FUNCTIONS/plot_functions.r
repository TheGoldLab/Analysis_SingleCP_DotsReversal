# R script to be run with r-environment R installation
library(data.table)
library(ggforce)
source("explore_functions.r")

# The palette with black:  ref = http://www.cookbook-r.com/Graphs/Colors_(ggplot2)/
                # black      golden     blue       green      yellow   dark blue    orange     pink
cbbPalette <- c("#000000", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")

############# SET UP DATA.TABLES NEEDED

data <- get_full_data()

# following two are for legacy code
nonQuestData <- data
#factored_threshold <- data
#############

##============ Accuracy for fixed coh across all ProbCP conditions AVG SUBJ ===============#
#to_plot41 <- data[
#  coh_cat == "th",
#  .(accuracy=mean(dirCorrect), numTrials=.N),
#  by=.(viewingDuration, probCP, presenceCP)
#]
#to_plot41[,se:=sqrt(accuracy * (1-accuracy) / numTrials)]
#to_plot41[,ci:=1.96*se]
#
#png(filename="acc_dd_pcp_byvd_bypresencecp.png", width=1000, height=500)
#
#ggplot(aes(x=probCP, y=accuracy, col=presenceCP, group=presenceCP), data=to_plot41) +
#  geom_point(size=3) +
#  geom_line(size=2) +
#  geom_hline(yintercept=c(.5,1), color="black") +
#  geom_errorbar(aes(ymin=accuracy-ci, ymax=accuracy+ci), width=.2, size=1) +
#  facet_grid(~viewingDuration) +
#  theme(text = element_text(size=25)) +
#  scale_color_manual(values=c(cbbPalette[4], cbbPalette[7]) , name = "", labels = c("no CP", "CP"))
#dev.off()
###============================================#


##============ Acc(400)-Acc(300) vs. Acc(200)-Acc(100) AVG SUBJ ===============#
## sfn3.png
#data[,`:=`(acc=mean(dirCorrect),
#           vv=mean(dirCorrect)*(1-mean(dirCorrect))/.N),
#     by=.(viewingDuration, probCP, presenceCP, coh_cat)]
#tocast <- unique(data[coh_cat == "th", .(acc, probCP, presenceCP, viewingDuration, vv)])
#wide <- dcast(tocast, probCP + presenceCP ~ viewingDuration, value.var = c("acc", "vv"))
#wide[,`:=`(
#  accDiffPost=acc_400 - acc_300,
#  ciPost=1.96*sqrt(vv_400+vv_300),
#  accDiffPre=acc_200 - acc_100,
#  ciPre=1.96*sqrt(vv_200+vv_100))]
#wide[,`:=`(acc_100=NULL, acc_200=NULL, acc_300=NULL, acc_400=NULL,
#           vv_100=NULL, vv_200=NULL, vv_300=NULL, vv_400=NULL)]
#listForAcc <- paste("accDiff", c("Pre", "Post"), sep = "")
#listForCI <- paste("ci", c("Pre", "Post"), sep = "")
#long_again <- melt(wide, measure = list(listForAcc, listForCI),
#               variable.name = "TimeLoc", value.name = c("AccChange", "CI"))
#levels(long_again$TimeLoc) <- c("pre", "post")
#pd <- position_dodge(.14) 
#
#png(filename="sfn3.png", width=900, height=400)
#ggplot(long_again, aes(x=TimeLoc, y=AccChange, col=presenceCP)) + 
#  geom_hline(yintercept = 0, linetype='dashed') + 
#  geom_errorbar(aes(ymin=AccChange - CI, ymax=AccChange + CI), width=.2, position=pd, size=1.2) +
#  geom_point(position=pd, size=6.5) + 
#  facet_grid(~probCP) + 
#  theme(text=element_text(size=35)) + 
#  ylab("Accuracy Increase") + xlab("100-ms epoch") +  
#  labs(title="Accuracy Change pre- vs. post-CP") +
#  theme(plot.title = element_text(hjust = 0.5)) +
#  scale_color_manual(values=c(cbbPalette[4], cbbPalette[7]) , name = "", labels = c("no CP", "CP")) 
#dev.off()
##============================================#

##============ Priming Effect ===============#
#subdata <- data[(viewingDuration == 100 | viewingDuration == 300) & coh_cat == "th",
#                .(dirCorrect, subject, probCP, presenceCP, viewingDuration)]
#subdata[, `:=`(accuracy=mean(dirCorrect), vv=mean(dirCorrect)*(1-mean(dirCorrect))/.N),
#        by=.(viewingDuration, subject, probCP, presenceCP)]
#tocast <- unique(subdata[,dirCorrect:=NULL])
#
#wide <- dcast(tocast, 
#              subject + probCP + presenceCP ~ viewingDuration, value.var = c("accuracy", "vv"))
#
#for (subj in c("S1", "S2", "S3", "S4", "S5")) {
#  for (pcp in c("0", "0.2", "0.5", "0.8")) {
#  wide[subject == subj & probCP == pcp & presenceCP == "CP",
#       accuracy_100 := wide[subject == subj & probCP == pcp & presenceCP == "noCP", accuracy_100]]
#  wide[subject == subj & probCP == pcp & presenceCP == "CP",
#       vv_100 := wide[subject == subj & probCP == pcp & presenceCP == "noCP", vv_100]]
#  }
#}
#
#wide[,`:=`(accDiff=accuracy_300 - accuracy_100,ci=1.96*sqrt(vv_100+vv_300))]
#
#png(filename="priming_effect.png", width=600, height=800)
#ggplot(wide, aes(x=presenceCP, y=accDiff)) + 
#  geom_point(size=3.7) + 
#  geom_line(aes(group=interaction(probCP, subject)), size=1.5) +
#  geom_hline(yintercept = 0, linetype='dashed') + 
#  geom_errorbar(aes(ymin=accDiff - ci, ymax=accDiff + ci), width=.1, size=1) +
#  facet_grid(subject~probCP) + theme(text=element_text(size=20)) + ylab("Acc(300) - Acc(100)") + 
#  labs(title="Effect of pre-CP stim on post-CP acc", subtitle="threshold coherence")
#dev.off()
##============================================#

##============ Priming Effect Subject Average ===============#
#subdata <- data[(viewingDuration == 100 | viewingDuration == 300) & coh_cat == "th",
#                .(dirCorrect, probCP, presenceCP, viewingDuration)]
#subdata[, `:=`(accuracy=mean(dirCorrect), vv=mean(dirCorrect)*(1-mean(dirCorrect))/.N),
#        by=.(viewingDuration, probCP, presenceCP)]
#tocast <- unique(subdata[,dirCorrect:=NULL])
#
#wide <- dcast(tocast, 
#              probCP + presenceCP ~ viewingDuration, value.var = c("accuracy", "vv"))
#
#for (pcp in c("0", "0.2", "0.5", "0.8")) {
#  wide[probCP == pcp & presenceCP == "CP",
#       accuracy_100 := wide[probCP == pcp & presenceCP == "noCP", accuracy_100]]
#  wide[probCP == pcp & presenceCP == "CP",
#       vv_100 := wide[probCP == pcp & presenceCP == "noCP", vv_100]]
#}
#
#wide[,`:=`(accDiff=accuracy_300 - accuracy_100,ci=1.96*sqrt(vv_100+vv_300))]
#
#png(filename="priming_effect_avg_subj.png", width=600, height=300)
#ggplot(wide, aes(x=presenceCP, y=accDiff)) + 
#  geom_point(size=3.7) + 
#  geom_line(aes(group=probCP), size=1.5) +
#  geom_hline(yintercept = 0, linetype='dashed') + 
#  geom_errorbar(aes(ymin=accDiff - ci, ymax=accDiff + ci), width=.1, size=1) +
#  facet_grid(~probCP) + theme(text=element_text(size=20)) + ylab("Acc(300) - Acc(100)") + 
#  labs(title="Effect of pre-CP stim on post-CP acc", subtitle="threshold coherence")
#dev.off()
##============================================#


##============ Acc(300) - Acc(200) ==============#
#data[,`:=`(acc=mean(dirCorrect),
#           vv=mean(dirCorrect)*(1-mean(dirCorrect))/.N),
#     by=.(viewingDuration, subject, probCP, presenceCP, coh_cat)]
#tocast <- unique(data[(viewingDuration == 200 | viewingDuration == 300) & coh_cat == "th", 
#                      .(acc, subject, probCP, presenceCP, viewingDuration, vv)])
#wide <- dcast(tocast, 
#              subject + probCP + presenceCP ~ viewingDuration, value.var = c("acc", "vv"))
#
## fill NA values for vd200 at CP trials to vd200 at noCP trials
#for (subj in c("S1", "S2", "S3", "S4", "S5")) {
#  for (pcp in c("0", "0.2", "0.5", "0.8")) {
#  wide[subject == subj & probCP == pcp & presenceCP == "CP",
#       acc_200 := wide[subject == subj & probCP == pcp & presenceCP == "noCP", acc_200]]
#  wide[subject == subj & probCP == pcp & presenceCP == "CP",
#       vv_200 := wide[subject == subj & probCP == pcp & presenceCP == "noCP", vv_200]]
#  }
#}
#
#wide[,`:=`(accDiff=acc_300 - acc_200,ci=1.96*sqrt(vv_200+vv_300))]
#
#png(filename="Acc300-Acc200.png", width=600, height=800)
#ggplot(wide, aes(x=presenceCP, y=accDiff)) + 
#  geom_point(size=3.7) + 
#  geom_line(aes(group=interaction(probCP, subject)), size=1.5) +
#  geom_hline(yintercept = 0, linetype='dashed') + 
#  geom_errorbar(aes(ymin=accDiff - ci, ymax=accDiff + ci), width=.1, size=1) +
#  facet_grid(subject~probCP) + theme(text=element_text(size=20)) + ylab("Acc(300) - Acc(200)") + 
#  labs(title="Accuracy difference around CP", subtitle="threshold coherence")
#dev.off()
##=======================================================#

##============ Acc(300) - Acc(200) AVG across subjects ==============#
## snf2.png
#data[,`:=`(acc=mean(dirCorrect),
#           vv=mean(dirCorrect)*(1-mean(dirCorrect))/.N),
#     by=.(viewingDuration, probCP, presenceCP, coh_cat)]
#tocast <- unique(data[(viewingDuration == 200 | viewingDuration == 300) & coh_cat == "th", 
#                      .(acc, probCP, presenceCP, viewingDuration, vv)])
#wide <- dcast(tocast, probCP + presenceCP ~ viewingDuration, value.var = c("acc", "vv"))
#
## fill NA values for vd200 at CP trials to vd200 at noCP trials
#for (pcp in c("0", "0.2", "0.5", "0.8")) {
#  wide[probCP == pcp & presenceCP == "CP",
#       acc_200 := wide[probCP == pcp & presenceCP == "noCP", acc_200]]
#  wide[probCP == pcp & presenceCP == "CP",
#       vv_200 := wide[probCP == pcp & presenceCP == "noCP", vv_200]]
#}
#
#wide[,`:=`(accDiff=acc_300 - acc_200,ci=1.96*sqrt(vv_200+vv_300))]
#
#png(filename="sfn2.png", width=800, height=400)
#ggplot(wide, aes(x=presenceCP, y=accDiff)) + 
#  geom_line(aes(group=probCP), size=2.2) +
#  geom_hline(yintercept = 0, linetype='dashed') + 
#  geom_errorbar(aes(ymin=accDiff - ci, ymax=accDiff + ci), width=.13, size=1.2) +
#  geom_point(aes(col=presenceCP), size=6.5) + 
#  facet_grid(~probCP) + 
#  theme(text=element_text(size=35)) + 
#  ylab("Acc(300) - Acc(200)") + 
#  xlab("Presence of CP") +
#  labs(title="Accumulation across CP") + 
#  theme(plot.title = element_text(hjust = 0.5),
#	axis.text.x=element_blank()) +
#  scale_color_manual(values=c(cbbPalette[4], cbbPalette[7]) , name = "", labels = c("no CP", "CP")) 
#dev.off()
##=======================================================#


##============ 100 msec window integration ==============#
#subdata <- data[(viewingDuration == 100 | viewingDuration == 300) & coh_cat == "th", 
#                `:=`(accuracy=mean(dirCorrect), se=sqrt(mean(dirCorrect)*(1-mean(dirCorrect))/.N)),
#                by=.(viewingDuration, subject, probCP, presenceCP, coh_cat)]
#subdata <- unique(subdata[,.(accuracy, subject, probCP, presenceCP, viewingDuration, se)])
#subdata[, `:=`(priming='None', ci=1.96*se)]
#subdata[viewingDuration == 300 & presenceCP == "CP", priming := "Neg"]
#subdata[viewingDuration == 300 & presenceCP == "noCP", priming := "Pos"]
#subdata[,priming := as.factor(priming)]
#
#png(filename="100_msec_window.png", width=800, height=800)
#ggplot(subdata, aes(x=priming, y=accuracy, col=priming, group=priming)) + geom_point(size=4) +
#  geom_errorbar(aes(ymin=accuracy-ci, ymax=accuracy+ci), width=0.17, size=1.4) + geom_hline(yintercept = 0.5, linetype='dashed') +
#  facet_grid(subject~probCP) + theme_bw() + theme(text=element_text(size=20)) + 
#  labs(title="Accuracy on 100-msec window", subtitle="threshold coherence")
#dev.off()
##=======================================================#




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


######### Main result plot ##########
## as above, but for 200-400 msec trials.
#to_plot6 <- factored_threshold[
#  coh_cat=="th",
#  .(accuracy=mean(dirCorrect), numTrials=.N),
#  by=.(presenceCP, subject, viewingDuration, probCP)
#]
#to_plot6[,se:=sqrt(accuracy * (1-accuracy) / numTrials)]
#to_plot6[,ci:=1.96*se]
#
#pd <- position_dodge(.2) # move them .05 to the left and right
#
#png(filename="acc_dd_100-400_bysubj_bypcp_bycp.png", width=1600, height=1300)
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
#####################################


########### Main result plot AVG SUBJ ##########
## sfn1.png
#to_plot6 <- data[
#  coh_cat=="th",
#  .(accuracy=mean(dirCorrect), numTrials=.N),
#  by=.(presenceCP, viewingDuration, probCP, cpChoice)
#]
#to_plot6[,se:=sqrt(accuracy * (1-accuracy) / numTrials)]
#to_plot6[,ci:=1.96*se]
#
#pd <- position_dodge(.2) # move them .05 to the left and right
#
#png(filename="main_choice_split.png", width=1500, height=485)
#ggplot(to_plot6, aes(x=factor(viewingDuration), y=accuracy, col=presenceCP)) +
#  geom_point(size=6, aes(shape=cpChoice)) +
#  geom_line(size=1.5, aes(linetype=cpChoice, group=interaction(cpChoice, presenceCP))) +
#  geom_hline(yintercept=c(.5,1), color="black", linetype="dashed") +
#  facet_grid(~probCP) +
#  scale_color_brewer(palette="Dark2") +
#  theme(text = element_text(size=35)) + 
#  ggtitle("Accuracy across 5 subjects") + 
#  xlab("Viewing Duration (ms)") +
#  ylab("P(Correct)") +
#  theme(plot.title = element_text(hjust = 0.5)) +
#  scale_color_manual(values=c(cbbPalette[4], cbbPalette[7]) , name = "", labels = c("no CP", "CP")) 
##  labs(color="")
#dev.off()
#####################################
########### accuracy AVG SUBJ ##########
#
#to_plot6 <- factored_threshold[
#  coh_cat=="th",
#  .(accuracy=mean(dirCorrect), numTrials=.N),
#  by=.(viewingDuration, probCP)
#]
#to_plot6[,se:=sqrt(accuracy * (1-accuracy) / numTrials)]
#to_plot6[,ci:=1.96*se]
#
#pd <- position_dodge(.2) # move them .05 to the left and right
#
#png(filename="bare_acc.png", width=1500, height=385)
#ggplot(to_plot6, aes(x=factor(viewingDuration), y=accuracy)) +
#  geom_point(size=4, position=pd) +
#  geom_line(size=2.2) +
#  geom_hline(yintercept=c(.5,1), color="black", linetype="dashed") +
#  geom_errorbar(aes(ymin=accuracy-ci, ymax=accuracy+ci), width=.1, size=1.7, position=pd) +
#  facet_grid(~probCP) +
#  scale_color_brewer(palette="Dark2") +
#  theme(text = element_text(size=35)) + 
#  ggtitle("Accuracy across 5 subjects") + 
#  xlab("Viewing Duration (ms)") +
#  ylab("P(Correct)") +
#  theme(plot.title = element_text(hjust = 0.5)) +
#  scale_color_manual(values=c(cbbPalette[4], cbbPalette[7]) , name = "", labels = c("no CP", "CP")) 
##  labs(color="")
#dev.off()
#######################################

######### Acc diff plot ##########
#to_plot <- factored_threshold[
#  probCP > 0 & probCP < 0.8 &
#  coh_cat=="th",
#  .(accuracy=mean(dirCorrect), numTrials=.N),
#  by=.(presenceCP, subject, viewingDuration, probCP)
#]
#to_plot[,se:=sqrt(2*accuracy * (1-accuracy) / numTrials)]
#to_plot[,numTrials:=NULL]
#
#levels(to_plot$presenceCP) <- c("noCP","CP")
#to_plot2 <- dcast(to_plot, subject+viewingDuration+probCP~presenceCP, value.var=c("accuracy","se"))
#to_plot2[,accdiff:=0]
#to_plot2[viewingDuration > 200, accdiff:=accuracy_noCP - accuracy_CP]
#to_plot2[,ci:=1.96*se_noCP]
#to_plot2[viewingDuration > 200, ci:=1.96*sqrt(se_CP^2+se_noCP^2)]
#
#pd <- position_dodge(.2) # move them .05 to the left and right
#
#png(filename="acc_diff_dd_bysubj_bypcp_bycp.png", width=800, height=1300)
#ggplot(to_plot2, aes(x=viewingDuration, y=accdiff)) +
#  geom_point(size=4, position=pd) +
#  geom_line(size=2) +
#  geom_hline(yintercept=c(0,-.5,.5), color="black", linetype="dashed") +
#  geom_errorbar(aes(ymin=accdiff-ci, ymax=accdiff+ci), width=.1, size=1.7, position=pd) +
#  facet_grid(subject~probCP) +
#  scale_color_brewer(palette="Dark2") +
#  theme(text = element_text(size=35)) + 
#  ggtitle("Acc (DD) th-coh")
#dev.off()
#####################################



######### Acc diff plot AVG SUBJ ##########
#to_plot <- factored_threshold[
#  probCP > 0 & probCP < 0.8 &
#  coh_cat=="th" & 
#  viewingDuration > 250,
#  .(accuracy=mean(dirCorrect), numTrials=.N),
#  by=.(presenceCP, viewingDuration, probCP)
#]
#to_plot[,se:=sqrt(2*accuracy * (1-accuracy) / numTrials)]
#to_plot[,numTrials:=NULL]
#
#levels(to_plot$presenceCP) <- c("noCP","CP")
#to_plot2 <- dcast(to_plot, viewingDuration+probCP~presenceCP, value.var=c("accuracy","se"))
#to_plot2[,accdiff:=0]
#to_plot2[viewingDuration > 200, accdiff:=accuracy_noCP - accuracy_CP]
#to_plot2[,ci:=1.96*se_noCP]
#to_plot2[viewingDuration > 200, ci:=1.96*sqrt(se_CP^2+se_noCP^2)]
#
#pd <- position_dodge(.2) # move them .05 to the left and right
#
#to_plot2[,viewingDuration:=factor(viewingDuration, ordered=T)]
#
#png(filename="acc_diff_dd_bysubj_bypcp_bycp_avg_subj.png", width=500, height=360)
#ggplot(to_plot2, aes(x=viewingDuration, y=accdiff)) +
#  geom_point(size=4, position=pd) +
#  geom_line(size=2, aes(group=1)) +
#  geom_hline(yintercept=c(0,-.5,.5), color="black", linetype="dashed") +
#  geom_errorbar(aes(ymin=accdiff-ci, ymax=accdiff+ci), width=.1, size=1.7, position=pd) +
#  facet_grid(~probCP) +
#  scale_color_brewer(palette="Dark2") +
#  theme(text = element_text(size=35)) + 
#  ggtitle("Acc (DD) th-coh")
#dev.off()
#####################################

## as above, but for perceived CP as opposed to real CPs
#to_plotx <- factored_threshold[
#  viewingDuration > 150 &
#    coh_cat=="th" &
#    probCP > 0,
#  .(accuracy=mean(dirCorrect), numTrials=.N),
#  by=.(cpChoice, subject, viewingDuration, probCP)
#]
#to_plotx[,se:=sqrt(accuracy * (1-accuracy) / numTrials)]
#to_plotx[,ci:=1.96*se]
#
#pd <- position_dodge(.2) # move them .05 to the left and right
#
#png(filename="acc_dd_200-400_bysubj_bypcp_byperceivedcp.png", width=1600, height=1400)
#ggplot(to_plotx, aes(x=factor(viewingDuration), y=accuracy, col=cpChoice, group=cpChoice)) +
#  geom_point(size=4, position=pd) +
#  geom_line(size=2) +
#  geom_hline(yintercept=c(0,.5,1), color="black", linetype="dashed") +
#  geom_errorbar(aes(ymin=accuracy-ci, ymax=accuracy+ci), width=.1, size=1.7, position=pd) +
#  facet_grid(subject~probCP) +
#  scale_color_brewer(palette="Dark2") +
#  theme(text = element_text(size=35)) + 
#  ggtitle("Acc (DD) at th-coh, by perceived CP")
#dev.off()




##The probability of being correct on 300-msec change-point trials
##should be greater (but still below %50) than the probability of being
##wrong on 100-msec trials
#to_plota <- factored_threshold[
#  ((viewingDuration == 100) | (viewingDuration == 300 & presenceCP == "CP")) &
#    coh_cat=="th",
#  .(accuracy=mean(dirCorrect), numTrials=.N),
#  by=.(presenceCP, subject, viewingDuration, probCP)
#]
#to_plota[, y:=accuracy]
#to_plota[viewingDuration==100, y:=1-y]  # P(wrong)for 100 msec
#to_plota[,se:=sqrt(y * (1-y) / numTrials)]
#to_plota[,ci:=1.96*se]
#
#
#png(filename="pwrong_pcorr_100-300_bysubj_bypcp_bycp.png", width=1150, height=1300)
#ggplot(to_plota, aes(x=factor(viewingDuration), y=y, col=presenceCP)) +
#  geom_point(size=5) +
#  geom_hline(yintercept=c(0, .5), color="black", linetype="dashed") +
#  geom_errorbar(aes(ymin=y-ci, ymax=y+ci), width=.1, size=2) +
#  facet_grid(subject~probCP) +
#  labs(title="") +
#  xlab("Viewing Duration") + ylab("P(wrong) vs. P(correct)") +
#  ggtitle("P(wrong|noCP) vs. P(correct|CP) \n on 100 vs. 300 CP trials") +
#  scale_color_manual(labels = c("P(wrong|noCP)", "P(correct|CP)"), values = c("darkred", "darkgreen")) + 
#  theme(text = element_text(size=35))  
##  theme_bw()
#dev.off()




############ THEORETICAL ACCURACY SECTION ################
#
#baseC <- seq(.2, 4, .1)
#baset <- seq(.1, .4, .01)
#
#C <- c()
#t <- c()
#norm_ncp <- c()
#norm_cp <- c()
#lowleak_ncp <- c()
#highleak_ncp <- c()
#lowleak_cp <- c()
#highleak_cp <- c()
#
##actual leak values
#lowl <- 3
#highl <- 10
#
## iteration <- 1
#
#for (cc in baseC) {
#  for (tt in baset) {
#    C <- c(C, cc)
#    t <- c(t, tt)
#    norm_ncp <- c(norm_ncp, acc(cc, tt))
#    norm_cp <- c(norm_cp, acc_cp(cc, tt))
#    lowleak_ncp <- c(lowleak_ncp, acc_leak(cc, tt, lowl, F))
#    highleak_ncp <- c(highleak_ncp, acc_leak(cc, tt, highl, F))
#    lowleak_cp <- c(lowleak_cp, acc_leak(cc, tt, lowl, T))
#    highleak_cp <- c(highleak_cp, acc_leak(cc, tt, highl, T))
#    # print(iteration)
#    # print(norm_ncp)
#    # iteration <- iteration + 1
#  }
#}
#
#data <- data.table(C, t, norm_ncp, norm_cp, lowleak_ncp, highleak_ncp, lowleak_cp, highleak_cp)
#
##convert to long format
#long_data = melt(data, id.vars = c("C", "t"),
#                measure.vars = c("norm_ncp", "norm_cp", "lowleak_ncp", "highleak_ncp", "lowleak_cp", "highleak_cp"))
#long_data[,Pwrong := 1-value]
#
#long_data[,CP:="no-CP"]
#long_data[,model:="DDM"]
#
#long_data[variable == "norm_cp" |
#            variable == "lowleak_cp" |
#            variable == "highleak_cp", `:=`(CP="CP")]
#long_data[variable == "lowleak_cp" | variable == "lowleak_ncp", `:=`(model="Low Leak")]
#long_data[variable == "highleak_cp" | variable == "highleak_ncp", `:=`(model="High Leak")]
#long_data[,model:=factor(model, levels = c("DDM", "Low Leak", "High Leak"))]
#long_data[,CP:=factor(CP, levels=c("no-CP", "CP"))]
#
###### Heat maps
#
#png(filename="heatmaps_theoretical_acc.png", width=900, height=1000)
#ggplot(data=long_data, aes(x=t, y=C, fill=value, group=variable)) + 
#      theme_bw() +
#      geom_tile() +
#      ggtitle("Theoretical Accuracy") + 
#      scale_fill_gradientn(colors=colorRampPalette(c("white","royalblue","seagreen","orange","red","brown"))(500),name="Accuracy\n[P(correct)]") +
#      labs(x = "Time [sec]",y="SNR [|d|/sigma]") +
#      facet_grid(model~CP) + 
#      theme(text=element_text(size=32)) 
#dev.off()
#
###### Single curves
#
#png(filename="theoretical_acc_curves.png", width=1350, height=600)
#ggplot(aes(x=t, y=value, col=CP), data=long_data[C==0.8 | C==1.5 | abs(C-3)<0.0001,]) + 
#  geom_line(aes(group=interaction(model, CP), linetype=model), size=1.5) +
#  # geom_hline(yintercept = long_data[model == "DDM" & (C==0.8 | C==1.5 | abs(C-3)<0.0001) & t ==.1, Pwrong],
#  #            linetype="dotted") +
#  facet_wrap(~factor(C)) +
#  ylab("P(correct)") + xlab("time (s)") +
#  labs(title = "Theoretical Curves Perfect vs. Leaky accumulators",
#       subtitle = "By SNR", 
#       caption = paste("low leak =",lowl,"; high leak =",highl),
#       col="") +
#  theme(text=element_text(size=35), legend.key.width = unit(5, "line"))  # text size would look better at 32... 
#dev.off()

#################################################


################## LATEST THEO - SINGLE SNR #####################
#library(reticulate)
#
#source_python("python_functions.py")
#source("accuracy_functions.r")
#
#baseC <- seq(.2, 4, .1)
#baset <- seq(.1,.4,.01)#c(seq(.1, .2, .01), seq(.201,.25,.001), seq(.26,.4, .01))
#
#C <- c()
#t <- c()
#norm_ncp <- c()
#norm_cp <- c()
#lowleak_ncp <- c()
#highleak_ncp <- c()
#lowleak_cp <- c()
#highleak_cp <- c()
#
#dumbr_ncp <- c()
#dumbr_cp <- c()
#
#lowh_par_ncp <- c()
#lowh_par_cp <- c()
#highh_par_ncp <- c()
#highh_par_cp <- c()
#
##actual leak values
#lowl <- 3
#highl <- 10
#lowh <- .2
#highh <- .8
#
## iteration <- 1
#
#for (cc in baseC) {
#  for (tt in baset) {
#    #### extra params ####
#    d1 <- cc
#    d2 <- -cc
#    dfsion <- 1
#    CPtime <- .2
#    nbins <- 10000
#    ######################
#    
#    
#    C <- c(C, cc)
#    t <- c(t, tt)
#    norm_ncp <- c(norm_ncp, acc(cc, tt))
#    norm_cp <- c(norm_cp, acc_cp(cc, tt))
#    lowleak_ncp <- c(lowleak_ncp, acc_leak(cc, tt, lowl, F))
#    highleak_ncp <- c(highleak_ncp, acc_leak(cc, tt, highl, F))
#    lowleak_cp <- c(lowleak_cp, acc_leak(cc, tt, lowl, T))
#    highleak_cp <- c(highleak_cp, acc_leak(cc, tt, highl, T))
#    if (tt <= .2) {
#      dumbr_cp <- c(dumbr_cp, acc_dumbr(cc, 1, tt, .2, 0, TRUE))  
#    } else {
#      dumbr_cp <- c(dumbr_cp, acc_dumbr(-cc, 1, tt, .2, 0, TRUE))
#    }
#    dumbr_ncp <- c(dumbr_ncp, acc_dumbr(cc, 1, tt, .2, 0, FALSE))
#    lowh_par_cp <- c(lowh_par_cp, acc_par(d1, d2, dfsion, tt, CPtime, lowh, nbins))
#    lowh_par_ncp <- c(lowh_par_ncp, acc_par(d1, d1, dfsion, tt, CPtime, lowh, nbins))
#    highh_par_cp <- c(highh_par_cp, acc_par(d1, d2, dfsion, tt, CPtime, highh, nbins))
#    highh_par_ncp <- c(highh_par_ncp, acc_par(d1, d1, dfsion, tt, CPtime, highh, nbins))
#  }
#}
#
#data <- data.table(C, t, norm_ncp, norm_cp, lowleak_ncp, highleak_ncp, lowleak_cp, highleak_cp, dumbr_cp, dumbr_ncp, lowh_par_cp, lowh_par_ncp, highh_par_cp, highh_par_ncp)
#
##convert to long format
#long_data = melt(data, id.vars = c("C", "t"),
#                measure.vars = c("norm_ncp", "norm_cp", "lowleak_ncp", "highleak_ncp", "lowleak_cp", "highleak_cp", "dumbr_cp", "dumbr_ncp", "lowh_par_cp", "lowh_par_ncp", "highh_par_cp", "highh_par_ncp"))
#long_data[,Pwrong := 1-value]
#
#long_data[,CP:="no-CP"]
#long_data[,model:="DDM"]
#
#long_data[variable == "norm_cp" |
#            variable == "lowleak_cp" |
#            variable == "highleak_cp" |
#            variable == "dumbr_cp" | 
#            variable == "lowh_par_cp" | 
#            variable == "highh_par_cp", `:=`(CP="CP")]
#long_data[variable == "lowleak_cp" | variable == "lowleak_ncp", `:=`(model="Low Leak")]
#long_data[variable == "highleak_cp" | variable == "highleak_ncp", `:=`(model="High Leak")]
#long_data[variable == "dumbr_cp" | variable == "dumbr_ncp", `:=`(model="DumbR")]
#long_data[variable == "lowh_par_cp" | variable == "lowh_par_ncp", `:=`(model="PAR low h")]
#long_data[variable == "highh_par_cp" | variable == "highh_par_ncp", `:=`(model="PAR high h")]
#long_data[,model:=factor(model, levels = c("DDM", "Low Leak", "High Leak", "DumbR", "PAR low h", "PAR high h"))]
#long_data[,CP:=factor(CP, levels=c("no-CP", "CP"))]
#
#
#
### HEATMAPS 
##ggplot(data=long_data, aes(x=t, y=C, fill=value, group=variable)) + 
##      geom_tile() +
##      ggtitle("Theoretical Accuracy") + 
##      scale_fill_gradientn(colors=colorRampPalette(c("white","royalblue","seagreen","orange","red","brown"))(500),name="Accuracy\n[P(correct)]") +
##      labs(x = "Time [sec]",y="SNR [|d|/sigma]") +
##      facet_grid(model~CP) + 
##      theme(text=element_text(size=20)) +
##      theme_bw()
#
#png(filename="theo_acc_curves_singleSNR.png", width=1350, height=600)
#ggplot(aes(x=t, y=value, col=model), data=long_data[C==1.5,]) + 
#  # geom_hline(yintercept=.5, color='black', inherit.aes=FALSE) +  # buggy because of facet_wrap. See https://github.com/tidyverse/ggplot2/issues/2091
#  stat_identity(yintercept=0.5, geom='hline', color='black', inherit.aes=TRUE) +
#  geom_line(aes(group=interaction(model, CP), color=model, linetype=CP), size=1.5) +
#  ylab("P(correct)") + xlab("time (s)") +
#  labs(title = "Theoretical Curves Perfect Accumulator",
#       subtitle = "CP vs. no-CP trials", 
#       caption = paste("low leak =",lowl,"; high leak =",highl, "; low h = ", lowh, "; high h = ", highh),
#       col="") +
#  theme(text=element_text(size=35), legend.key.width = unit(5, "line")) 
#dev.off()
#
#tmp <- long_data[C==1.5, ]
#tmp[, Pwrong:=NULL]
#filtered <- dcast(tmp, C + t + model ~ CP, value.var = "value")
#names(filtered)<-c("C", "t", "model", "noCP", "CP")
#
##Difference:
#png(filename="theo_acc_diff_curves_singleSNR.png", width=1350, height=600)
#ggplot(aes(x=t, y=noCP - CP, col=model), data=filtered) + 
#  geom_line(aes(group=model),size=1.5) +
#  # geom_hline(yintercept = long_data[model == "DDM" & (C==0.8 | C==1.5 | abs(C-3)<0.0001) & t ==.1, Pwrong],
#  #            linetype="dotted") +
#  ylab("Diff Acc") + xlab("time (s)") +
#  labs(title = "Accuracy Differential",
#       subtitle = "Acc(no-CP)-Acc(CP)", 
#       caption = paste("low leak =",lowl,"; high leak =",highl),
#       col="") +
#  theme(text=element_text(size=35), legend.key.width = unit(5, "line")) 
#dev.off()




##------------------------------ TEMPLATE FOR POSTER ANIMATION ----------------------------------#
## sfn4.png
#
#library('sde')
#library('fBasics')
#library('ggplot2')
#library('reshape2')
#
## Produce trajectories for various models
### PA model
##Set up parameters
#d0 <- 1.5 # drift magnitude
#s0 <- 1 # stdev magnitude
#cp <- 0.2 # change point time
#
#viewing_duration <- .4;
#
#num_traj=3;
#num_time_points=500;
#t <- 0:num_time_points  # time
#dt <- 1/num_time_points # time step in sec
#tt <- seq(0,viewing_duration, length.out=num_time_points + 1) # in sec
#cp_idx <- floor(num_time_points/2)
#
##Simulate 'num_traj' trajectories from the normative model
#s <- expression(s0)
#d <- expression(d0*(Heaviside(-t,-cp)-Heaviside(t,cp)))
#nocpd <- expression(d0)
#sde.sim(t0 = 0, T = viewing_duration, X0 = 0, N = num_time_points, drift=d,
#        sigma=s, sigma.x=0, method = "euler",M=num_traj) -> PAmodel
#sde.sim(t0 = 0, T = viewing_duration, X0 = 0, N = num_time_points, drift=nocpd,
#        sigma=s, sigma.x=0, method = "euler",M=num_traj) -> PAmodelNoCP
#
### Linear-leak models
##Simulate 'num_traj' trajectories from the linear-leak model
#lowLeak <- 3
#d <- expression(d0*(Heaviside(-t,-cp)-Heaviside(t,cp))-lowLeak*x)
#sde.sim(t0 = 0, T = viewing_duration, X0 = 0, N = num_time_points, drift=d,
#        sigma=s, sigma.x=0, method = "euler",M=num_traj) -> linModelLowLeak
#sde.sim(t0 = 0, T = viewing_duration, X0 = 0, N = num_time_points, drift=nocpd,
#        sigma=s, sigma.x=0, method = "euler",M=num_traj) -> linModelLowLeakNoCP
#
#highLeak <- 10
#d <- expression(d0*(Heaviside(-t,-cp)-Heaviside(t,cp))-highLeak*x)
#sde.sim(t0 = 0, T = viewing_duration, X0 = 0, N = num_time_points, drift=d,
#        sigma=s, sigma.x=0, method = "euler",M=num_traj) -> linModelHighLeak
#sde.sim(t0 = 0, T = viewing_duration, X0 = 0, N = num_time_points, drift=nocpd,
#        sigma=s, sigma.x=0, method = "euler",M=num_traj) -> linModelHighLeakNoCP
#
### Reset models
## ZERO RESET
#short_viewing_duration <- .2;
#
#num_time_points_short=num_time_points / 2;
#
##Simulate 'num_traj' trajectories from the normative model
#d <- expression(d0)
#sde.sim(t0 = 0, T = short_viewing_duration, X0 = 0, N = num_time_points_short, drift=d,
#        sigma=s, sigma.x=0, method = "euler",M=num_traj) -> ZeroResetmodel1
#
#new_drift <- expression(-d0)
#sde.sim(t0 = cp+.01, T = cp+short_viewing_duration, X0 = 0, N = num_time_points_short-1, drift=new_drift,
#        sigma=s, sigma.x=0, method = "euler",M=num_traj) -> ZeroResetmodel2  # CP
#
#sde.sim(t0 = cp+.01, T = cp+short_viewing_duration, X0 = 0, N = num_time_points_short-1, drift=d,
#        sigma=s, sigma.x=0, method = "euler",M=num_traj) -> ZeroResetmodel3  # NO CP
#
## CLEVER RESETS
#
## First Epoch (pre CP)
#sde.sim(t0 = 0, T = short_viewing_duration, X0 = 0, N = num_time_points_short, drift=d,
#        sigma=s, sigma.x=0, method = "euler",M=num_traj) -> LowhResetmodel1
#sde.sim(t0 = 0, T = short_viewing_duration, X0 = 0, N = num_time_points_short, drift=d,
#        sigma=s, sigma.x=0, method = "euler",M=num_traj) -> HighhResetmodel1
#
#lowh <- 0.2
#highh <- 0.8
#
## get end values of 2N trajectories
#all_end <- as.vector(c(LowhResetmodel1[num_time_points_short + 1,],HighhResetmodel1[num_time_points_short+1,]))
#
#reset_evidence <- function(ev, h) {
#  return(ev + log((h * exp(-ev)+1-h)/(h * exp(ev)+1-h)))
#}
#
## reset half of them with low h and the other half with high h
#lowh_reset_vals <- reset_evidence(all_end[1:num_traj/2], lowh)
#highh_reset_vals <- reset_evidence(all_end[num_traj/2+1:num_traj], highh)
#
## simulate second epoch with appropriate starting points
## Don't forget the possibly new drift rate!
#
#sde.sim(t0 = cp+.01, T = cp+short_viewing_duration, X0 = lowh_reset_vals, N = num_time_points_short-1, drift=new_drift,
#        sigma=s, sigma.x=0, method = "euler",M=num_traj) -> LowhResetmodel2
#sde.sim(t0 = cp+.01, T = cp+short_viewing_duration, X0 = highh_reset_vals, N = num_time_points_short-1, drift=new_drift,
#        sigma=s, sigma.x=0, method = "euler",M=num_traj) -> HighhResetmodel2
#
#sde.sim(t0 = cp+.01, T = cp+short_viewing_duration, X0 = lowh_reset_vals, N = num_time_points_short-1, drift=d,
#        sigma=s, sigma.x=0, method = "euler",M=num_traj) -> LowhResetmodel2NoCP
#sde.sim(t0 = cp+.01, T = cp+short_viewing_duration, X0 = highh_reset_vals, N = num_time_points_short-1, drift=d,
#        sigma=s, sigma.x=0, method = "euler",M=num_traj) -> HighhResetmodel2NoCP
#
## Comparison of mean trajectories between the two models
#
## get mean trajectories
## meanPA <- rowMeans(PAmodel)
## meanLinLow <- rowMeans(linModelLowLeak)
## meanLinHigh <- rowMeans(linModelHighLeak)
## meanZeroReset <- c(rowMeans(ZeroResetmodel1), rowMeans(ZeroResetmodel2))
## meanLowhReset <- c(rowMeans(LowhResetmodel1), rowMeans(LowhResetmodel2))
## meanHighhReset <- c(rowMeans(HighhResetmodel1), rowMeans(HighhResetmodel2))
## meanPAnocp <- rowMeans(PAmodelNoCP)
## meanLinLownocp <- rowMeans(linModelLowLeakNoCP)
## meanLinHighnocp <- rowMeans(linModelHighLeakNoCP)
## meanZeroResetnocp <- c(rowMeans(ZeroResetmodel1), rowMeans(ZeroResetmodel3))
## meanLowhResetnocp <- c(rowMeans(LowhResetmodel1), rowMeans(LowhResetmodel2NoCP))
## meanHighhResetnocp <- c(rowMeans(HighhResetmodel1), rowMeans(HighhResetmodel2NoCP))
#
#last_ix_before_cp <- function(timev){
#  tx <- sort(abs(timev-cp), index.return=T)$ix[1]
#  if (timev[tx] > cp) {
#    tx <- tx - 1
#  }
#  return(tx)
#}
#
#meanPA <- function(ttt, drift, hasCP, start_offset){
#  if (hasCP) {
#    trunc_ix <- last_ix_before_cp(ttt)
#    first_half <- start_offset + drift * ttt[1:trunc_ix]
#    second_offset <- tail(first_half, 1)
#    return(c(first_half, second_offset - drift* (ttt[-(1:trunc_ix)] - cp)))
#  } else {
#    return(start_offset + drift * ttt)
#  }
#}
#
#meanLeak <- function(ttt, drift, hasCP, leakk){
#  # leakk is positive scalar
#
#  evolve <- function(time_vec, start_pt, ddrift){
#    cf <- ddrift / leakk
#    return(start_pt*exp(-leakk*time_vec)+cf * (1-exp(-leakk*time_vec)))
#  }
#
#  if (hasCP) {
#    trunc_ix <- last_ix_before_cp(ttt)
#    first_half <- evolve(ttt[1:trunc_ix], 0, drift)
#    return(c(first_half, evolve(ttt[-(1:trunc_ix)]-cp, tail(first_half, 1), -drift)))
#  } else {
#    return(evolve(ttt, 0, drift))
#  }
#}
#
#meanReset <- function(ttt, hasCP, reset_func){
#  trunc_ix <- last_ix_before_cp(ttt)
#  first_half <- meanPA(ttt[1:trunc_ix], d0, FALSE, 0)
#  start_pt <- reset_func(tail(first_half, 1))
#  if (hasCP) {
#    return(c(first_half, meanPA(ttt[-(1:trunc_ix)]-cp, -d0, FALSE, start_pt)))
#  } else {
#    return(c(first_half, meanPA(ttt[-(1:trunc_ix)]-cp, d0, FALSE, start_pt)))
#  }
#}
#
#zeroreset <- function(val){
#  return(0)
#}
#
#lowhreset <- function(val){
#  return(reset_evidence(val, lowh))
#}
#highhreset <- function(val){
#  return(reset_evidence(val, highh))
#}
#
#means_df <- data.frame("time" = tt,
#                       "singlePAcp" = PAmodel[,"X1"],
#                       "singlelowLeakcp" = linModelLowLeak[,"X1"],
#                       "singleHighLeakcp" = linModelHighLeak[,"X1"],
#                       "singleZeroResetcp" = c(ZeroResetmodel1[,"X1"], ZeroResetmodel2[,"X1"]),
#                       "singleLowHresetcp" = c(LowhResetmodel1[,"X1"], LowhResetmodel2[,"X1"]),
#                       "singleHighHresetcp" = c(HighhResetmodel1[,"X2"], HighhResetmodel2[,"X1"]),  #cheat
#                       "singlePAnoCP" = PAmodelNoCP[,"X1"],
#                       "singlelowLeaknoCP" = linModelLowLeakNoCP[,"X1"],
#                       "singleHighLeaknoCP" = linModelHighLeakNoCP[,"X1"],
#                       "singleZeroResetnoCP" = c(ZeroResetmodel1[,"X2"], ZeroResetmodel3[,"X1"]),  #cheat
#                       "singleLowHresetnoCP" = c(LowhResetmodel1[,"X1"], LowhResetmodel2NoCP[,"X1"]),
#                       "singleHighHresetnoCP" = c(HighhResetmodel1[,"X2"], HighhResetmodel2NoCP[,"X1"]), # cheat
#                       "PAcp" = meanPA(tt, d0, TRUE,0),
#                       "lowLeakcp" = meanLeak(tt, d0, TRUE, lowLeak),
#                       "HighLeakcp" = meanLeak(tt, d0, TRUE, highLeak),
#                       "ZeroResetcp" = meanReset(tt, TRUE, zeroreset),
#                       "LowHresetcp" = meanReset(tt, TRUE, lowhreset),
#                       "HighHresetcp" = meanReset(tt, TRUE, highhreset),
#                       "PAnoCP" = meanPA(tt, d0, FALSE,0),
#                       "lowLeaknoCP" = meanLeak(tt, d0, FALSE, lowLeak),
#                       "HighLeaknoCP" = meanLeak(tt, d0, FALSE, highLeak),
#                       "ZeroResetnoCP" = meanReset(tt, FALSE, zeroreset),
#                       "LowHresetnoCP" = meanReset(tt, FALSE, lowhreset),
#                       "HighHresetnoCP" = meanReset(tt, FALSE, highhreset))
#library(data.table)
## plotting script
#options(scipen=999)
#theme_set(theme_bw())
#
## Load data (to be developed) ------------------------------------------
#X <- melt(means_df,id=c("time"))
#head(X)
#colnames(X)[2] <- "model"
#
#X <- as.data.table(X)
#X[,`:=`(modelClass="Reset")]
#X[model=="singlePAcp" | model=="singlePAnoCP"|model=="PAcp" | model=="PAnoCP",modelClass:="Perfect Accum."]
#X[model=="singlelowLeakcp" | model=="singleHighLeakcp" | model=="singlelowLeaknoCP" | model=="singleHighLeaknoCP"| model=="lowLeakcp" | model=="HighLeakcp" | model=="lowLeaknoCP" | model=="HighLeaknoCP", modelClass:="Leak"]
#X[,modelClass:=factor(modelClass, levels = c("Perfect Accum.", "Leak", "Reset"))]
#
#X[,CP:="CP"]
#X[model == "PAnoCP" |
#    model == "lowLeaknoCP" |
#    model == "HighLeaknoCP" |
#    model == "ZeroResetnoCP" |
#    model == "LowHresetnoCP" |
#    model == "HighHresetnoCP" |
#    model == "singlePAnoCP" |
#    model == "singlelowLeaknoCP" |
#    model == "singleHighLeaknoCP" |
#    model == "singleZeroResetnoCP" |
#    model == "singleLowHresetnoCP" |
#    model == "singleHighHresetnoCP", CP:="no-CP"]
#X[,CP:=factor(CP)]
#print(levels(X$CP))
#X$CP = factor(X$CP,levels(X$CP)[c(2,1)])
#
#X[,model2:="PA"]
#X[model == "singlelowLeaknoCP" | model == "singlelowLeakcp" | model == "lowLeaknoCP" | model == "lowLeakcp", model2:="LowLeak"]
#X[model == "singleHighLeaknoCP" | model == "singleHighLeakcp" | model == "HighLeaknoCP" | model == "HighLeakcp", model2:="HighLeak"]
#X[model == "singleZeroResetnoCP" | model == "singleZeroResetcp"|model == "ZeroResetnoCP" | model == "ZeroResetcp", model2:="ZeroReset"]
#X[model == "singleLowHresetnoCP" | model == "singleLowHresetcp"|model == "LowHresetnoCP" | model == "LowHresetcp", model2:="lowHreset"]
#X[model == "singleHighHresetnoCP" | model == "singleHighHresetcp"|model == "HighHresetnoCP" | model == "HighHresetcp", model2:="highHreset"]
#
#X[,model2:=factor(model2)]
#print(levels(X$model2))
#X$model2 = factor(X$model2,levels(X$model2)[c(5,4,2,6,3,1)])
#
#
#X[,ttype:="mean"]
#X[model == "singlePAcp" |
#    model == "singlelowLeakcp" |
#    model == "singleHighLeakcp" |
#    model == "singleZeroResetcp" |
#    model == "singleLowHresetcp" |
#    model == "singleHighHresetcp" |
#    model == "singlePAnoCP" |
#    model == "singlelowLeaknoCP" |
#    model == "singleHighLeaknoCP" |
#    model == "singleZeroResetnoCP" |
#    model == "singleLowHresetnoCP" |
#    model == "singleHighHresetnoCP", ttype:="trajectory"]
#
#cp_time=0.2
#model_list=c("PA", "Low Leak", "High Leak", "Zero Reset", "Low-h Reset", "High-h Reset")
#
## Add plot components --------------------------------
#gg <- ggplot(X[ttype=="mean"], aes(x=time, y=value, group=model)) +
#  geom_line(aes(col=model2, linetype=ttype), size=4) +
#  geom_line(aes(x=time, y=value, col=model2, group=model), data=X[ttype=="trajectory"], size=1) +
#  geom_vline(xintercept = cp_time, linetype="dashed",
#             color = "blue", size=1.5) +
#  geom_hline(yintercept = 0, color="black")+
#  facet_grid(modelClass~CP) +
#  xlim(c(0, .4)) + ylim(c(-.7, .7)) +
#  labs(title="Single Trial Evidence",
#       y="Evidence",
#       x="Viewing Duration (s)") +
#  scale_color_discrete(name="Model", labels=model_list) + 
#  guides(linetype=FALSE)
#
## Modify theme components -------------------------------------------
#bf <- 35
#sf <- 17
#gg <- gg + theme(text=element_text(size=35),
#		 plot.title = element_text(hjust = 0.5),
#		 legend.position = "bottom",
#                 panel.grid.minor = element_blank()) # remove minor grid
#
#
#
## save as png
##png(filename="sfn4.png", width=1100, height=1000)
##plot(gg)
##dev.off()
#
## Uncomment following two lines to get an actual GIF animation
#library(gganimate)
#animate(gg + transition_reveal(time), height = 1000, width =1100)
#anim_save("evidence.gif")
##anim_save('evidence.gif',gg + transition_reveal(time))
#



#----------------------------- END sfn4.png --------------------------#
##------------------------------START sfn5.png ------------------------#
#
## sfn5.png
#
#library(gganimate)
#library(ggplot2)
#library(data.table)
#
#old_wd <- getwd()
#setwd('/home/adrian/Documents/MATLAB/projects/Analysis_SingleCP_DotsReversal/R/animations/')
#
## BUG HERE, WHY???
##anim_save("test5.gif", p)
#
#source("animations.r")
#
#theme_set(theme_bw())
#
#d1 <- get_acc_data()
#
#d1[,`:=`(Pwrong=NULL, C=NULL, variable=NULL)]
#d1[,`:=`(modelClass="Reset")]
#d1[model=="DDM",modelClass:="Perfect Accum."]
#d1[model=="Low Leak" | model=="High Leak", modelClass:="Leak"]
#
#d1[,modelClass:=factor(modelClass, levels = c("Perfect Accum.", "Leak", "Reset"))]
#
#names(d1) <- c("time", "value", "CP", "model", "modelClass")
#
#model_list=c("PA", "Low Leak", "High Leak", "Zero Reset", "Low-h Reset", "High-h Reset")
#anim <- ggplot(d1, aes(x=time, y=value, group=model, col=model)) + geom_line(size=4) +
#  facet_grid(modelClass~CP) + geom_hline(yintercept = 0.5, linetype="dashed") +
#  geom_vline(xintercept = 0.2, color="blue", size=1.5, linetype="dashed") +
#  guides(colour=FALSE) + # turn legend off
#  xlim(c(0,.4)) +
#  ylab("Accuracy") + xlab("Viewing Duration (s)") + ggtitle("Theoretical Accuracy") + 
#  scale_color_discrete(name="Model", labels=model_list) + theme(text=element_text(size=35),
#                plot.title = element_text(hjust = 0.5),
#                 panel.grid.minor = element_blank()) # remove minor grid
#  #transition_reveal(t)
#
#setwd(old_wd)
#png(filename="sfn5.png", width=1100, height=900)
#plot(anim)
#dev.off()
##anim_save('accuracies.gif',anim + transition_reveal(time))







#------------------------------------------ CPD investigation"
d <- data
#
## Accuracy at Change-Point Detection Task
#acc_cpd <- unique(d[,.(acc=sum(cpCorrect)/.N, numTrials=.N), by=.(subject, probCP, viewingDuration, coh_cat)])
#acc_cpd[, `:=`(ci=1.96*sqrt(acc * (1-acc) / numTrials))]
#acc_cpd_avg_subj <- unique(d[,.(acc=sum(cpCorrect)/.N, numTrials=.N), by=.(probCP, viewingDuration, coh_cat)])
#acc_cpd_avg_subj[, `:=`(ci=1.96*sqrt(acc * (1-acc) / numTrials))]
#
#ggplot(acc_cpd, aes(x=probCP, y=acc, group=coh_cat, col=coh_cat)) + geom_point(size=4) + geom_line(size=1.5) + 
#  geom_hline(yintercept = c(0.5,1), linetype='dashed') +
#  geom_errorbar(aes(ymin=acc-ci, ymax=acc+ci), width=.3, size=.7) +
#  facet_grid(subject ~ viewingDuration) +
#  scale_color_manual(values=cbbPalette) +
#  # scale_color_brewer(palette = "Dark2") +
#  theme_bw() +
#  theme(text=element_text(size=17)) + ylim(0,1) 
#
### Average across subjects
#ggplot(acc_cpd_avg_subj, aes(x=probCP, y=acc, group=coh_cat, col=coh_cat)) + geom_point(size=4) + geom_line(size=1.5) + 
#  geom_hline(yintercept = c(0.5,1), linetype='dashed') +
#  geom_errorbar(aes(ymin=acc-ci, ymax=acc+ci), width=.3, size=.7) +
#  facet_grid(~ viewingDuration) +
#  scale_color_manual(values=cbbPalette) +
#  # scale_color_brewer(palette = "Dark2") +
#  theme_bw() +
#  theme(text=element_text(size=17)) + ylim(0,1) 
#
#
## ROC plane
#d_modified <- d[probCP > 0 & coh_cat != "100"]
#d_modified[, `:=`(respondedCP=0, isCP=0)]
#d_modified[cpChoice == "CP", respondedCP:=1]
#d_modified[presenceCP == "CP", isCP:=1]
#dd <- d_modified[,.(isCP, respondedCP, subject, probCP, dirChoice, dirCorrect, cpCorrect, viewingDuration, coh_cat)]
#roc_cpd <- unique(dd[,.(propCP=sum(respondedCP)/.N, trueProp=sum(isCP)/.N, numTrials=.N), 
#                     by=.(subject, probCP, viewingDuration, coh_cat)])
#roc_cpd[, `:=`(ciPropCP=1.96*sqrt(propCP * (1-propCP) / numTrials), ciTrueProp=1.96*sqrt(trueProp * (1-trueProp) / numTrials))]
#
#roc_cpd_avg_subj <- unique(dd[,
#                              .(propCP=sum(respondedCP)/.N, trueProp=sum(isCP)/.N, numTrials=.N), 
#                              by=.(probCP, viewingDuration, coh_cat)])
#roc_cpd_avg_subj[, `:=`(ciPropCP=1.96*sqrt(propCP * (1-propCP) / numTrials), ciTrueProp=1.96*sqrt(trueProp * (1-trueProp) / numTrials))]
#
#
#ggplot(roc_cpd, aes(x=probCP, y=propCP, group=coh_cat, col=coh_cat)) + 
#  geom_point(size=4) + 
#  geom_line(size=1.5) + 
#  geom_line(aes(x=probCP, y=trueProp)) + 
#  geom_hline(yintercept = c(0.5,1), linetype='dashed') +
#  geom_errorbar(aes(ymin=propCP-ciPropCP, ymax=propCP+ciPropCP), width=.3, size=.7) +
#  facet_grid(subject ~ viewingDuration) +
#  scale_color_manual(values=cbbPalette) +
#  # scale_color_brewer(palette = "Dark2") +
#  theme_bw() +
#  theme(text=element_text(size=17))
#
### Average across 5 subjects
#
#ggplot(roc_cpd_avg_subj, aes(x=probCP, y=propCP, group=coh_cat, col=coh_cat)) + 
#  geom_point(size=4) + 
#  geom_line(size=1.5) + 
#  geom_line(aes(x=probCP, y=trueProp)) + 
#  geom_hline(yintercept = c(0.5,1), linetype='dashed') +
#  geom_errorbar(aes(ymin=propCP-ciPropCP, ymax=propCP+ciPropCP), width=.3, size=.7) +
#  facet_grid(~ viewingDuration) +
#  scale_color_manual(values=cbbPalette) +
#  # scale_color_brewer(palette = "Dark2") +
#  theme_bw() +
#  theme(text=element_text(size=17))
#

#--------------Hist CPD subj -by -subj
# Hit/FA/Miss/CR
#roc2 <- d[,.(presenceCP, cpChoice, subject, viewingDuration, probCP)]
#roc2[presenceCP=="CP" & cpChoice == "noCP",cpd:="Miss"]
#roc2[presenceCP == "CP" & cpChoice == "CP", cpd:="Hit"]
#roc2[presenceCP == "noCP" & cpChoice == "CP", cpd:="FA"]
#roc2[presenceCP == "noCP" & cpChoice == "noCP", cpd:="CR"]
#roc2[,cpd:=factor(cpd, levels = c("Hit", "FA", "CR", "Miss"))]
#
#roc2[cpd=="Miss", `:=`(len=.N), by=.(subject, viewingDuration, probCP)]
#roc2[cpd=="CR", len:=.N, by=.(subject, viewingDuration, probCP)]
#roc2[cpd=="Hit", len:=.N, by=.(subject, viewingDuration, probCP)]
#roc2[cpd=="FA", len:=.N, by=.(subject, viewingDuration, probCP)]
#roc2 <- unique(roc2[,`:=`(presenceCP=NULL, cpChoice=NULL)])
#rocflat <- dcast(roc2, subject + viewingDuration + probCP ~ cpd, value.var="len")
#names(rocflat)[4] <- "NAvals"
#rocflat[,`:=`(total=0)]
#rocflat[!is.na(Miss),`:=`(total=total + Miss)]
#rocflat[!is.na(Hit),`:=`(total=total + Hit)]
#rocflat[!is.na(FA),`:=`(total=total + FA)]
#rocflat[!is.na(CR),`:=`(total=total + CR)]
#rocflat[,Hit:=Hit/total]
#rocflat[,Miss:=Miss / total]
#rocflat[,CR:=CR / total]
#rocflat[,FA:=FA / total]
#rocflat[,total:=NULL]
#roc3 <- melt(rocflat, measure.vars = c("Hit", "FA", "Miss", "CR", "NAvals"), variable.name = "cpd", value.name = "len")
#head(roc3)
#
#ggplot(data=roc3, aes(x=probCP, y=len, fill=cpd)) +
#  geom_bar(stat="identity", position=position_dodge()) +
#  facet_grid(subject~viewingDuration) +
#  theme_bw() +
#  ylab("%") +
#  theme(text=element_text(size=17))

#--------------Hist CPD AVG-subj
# Hit/FA/Miss/CR
get_dprime <- function(hits, fas) {
  return(qnorm(hits) - qnorm(fas))
}

roc2 <- data[coh_cat=="th" & viewingDuration > 200,.(presenceCP, cpChoice, viewingDuration, probCP, coh_cat)]
roc2[presenceCP=="CP" & cpChoice == "noCP",cpd:="Miss"]
roc2[presenceCP == "CP" & cpChoice == "CP", cpd:="Hit"]
roc2[presenceCP == "noCP" & cpChoice == "CP", cpd:="FA"]
roc2[presenceCP == "noCP" & cpChoice == "noCP", cpd:="CR"]
roc2[,cpd:=factor(cpd, levels = c("Hit", "FA", "CR", "Miss"))]

roc2[cpd=="Miss" & presenceCP == "CP", `:=`(len=.N), by=.(viewingDuration, probCP)]
roc2[cpd=="CR" & presenceCP == "noCP", len:=.N, by=.(viewingDuration, probCP)]
roc2[cpd=="Hit" & presenceCP == "CP", len:=.N, by=.(viewingDuration, probCP)]
roc2[cpd=="FA" & presenceCP == "noCP", len:=.N, by=.(viewingDuration, probCP)]
roc2 <- unique(roc2[,`:=`(presenceCP=NULL, cpChoice=NULL)])
rocflat <- dcast(roc2, viewingDuration + probCP ~ cpd, value.var="len")
rocflat[,`:=`(totalCP=0L, totalNoCP=0L)]
rocflat[!is.na(Miss) & !is.na(Hit),`:=`(totalCP=Hit + Miss)]
rocflat[!is.na(FA) & !is.na(CR),`:=`(totalNoCP=CR + FA)]
rocflat[,Hit:=Hit/totalCP]
rocflat[,Miss:=Miss / totalCP]
rocflat[,CR:=CR / totalNoCP]
rocflat[,FA:=FA / totalNoCP]
rocflat[,total:=NULL]
rocflat[,dprime := get_dprime(Hit, FA)]

# histograms
roc3 <- melt(rocflat, measure.vars = c("Hit", "FA", "Miss", "CR"), variable.name = "cpd", value.name = "len")
# head(roc3)

#png(filename="newhist_cpd_avg_subj.png", width=600, height=360)
#ggplot(data=roc3, aes(x=probCP, y=len, fill=cpd)) +
#  geom_bar(stat="identity", position=position_dodge()) +
#  facet_grid(~viewingDuration) +
#  theme_bw() +
#  ylab("%") +
#  ggtitle("CPD performance") +
#  theme(text=element_text(size=18))
#
#png(filename="hist_cpd_avg_subj.png", width=600, height=360)
#ggplot(data=roc3, aes(x=probCP, y=len, fill=cpd)) +
#  geom_bar(stat="identity", position=position_dodge()) +
#  facet_grid(~viewingDuration) +
#  theme_bw() +
#  ylab("%") +
#  ggtitle("CPD performance") +
#  theme(text=element_text(size=18))
#dev.off()
png(filename="dprime_avg_subj.png", width=600, height=360)
ggplot(rocflat, aes(x=probCP, y=dprime)) + geom_point(size=4) + facet_grid(~viewingDuration) +
  geom_hline(yintercept=0, linetype="dashed") +
  theme(text=element_text(size=18))
dev.off()
