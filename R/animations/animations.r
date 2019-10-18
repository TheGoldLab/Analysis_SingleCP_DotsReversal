library(ggplot2)
library(data.table)
library(reticulate)
library(gganimate)
use_python("/home/adrian/anaconda3/envs/r-environment/bin/python", required = T)
source_python("../REF_FUNCTIONS/python_functions.py")
source("../REF_FUNCTIONS/accuracy_functions.r")

get_acc_data <- function(){
  baseC <- c(1.5)
  baset <- seq(.1,.4,.1)#c(seq(.1, .2, .01), seq(.201,.25,.001), seq(.26,.4, .01))Z
  
  C <- c()
  t <- c()
  norm_ncp <- c()
  norm_cp <- c()
  lowleak_ncp <- c()
  highleak_ncp <- c()
  lowleak_cp <- c()
  highleak_cp <- c()
  
  dumbr_ncp <- c()
  dumbr_cp <- c()
  
  lowh_par_ncp <- c()
  lowh_par_cp <- c()
  highh_par_ncp <- c()
  highh_par_cp <- c()
  
  #actual leak values
  lowl <- 3
  highl <- 10
  lowh <- .2
  highh <- .8
  
  # iteration <- 1
  
  for (cc in baseC) {
    for (tt in baset) {
      #### extra params ####
      d1 <- cc
      d2 <- -cc
      dfsion <- 1
      CPtime <- .2
      nbins <- 10000
      ######################
      
      
      C <- c(C, cc)
      t <- c(t, tt)
      norm_ncp <- c(norm_ncp, acc(cc, tt))
      norm_cp <- c(norm_cp, acc_cp(cc, tt))
      lowleak_ncp <- c(lowleak_ncp, acc_leak(cc, tt, lowl, F))
      highleak_ncp <- c(highleak_ncp, acc_leak(cc, tt, highl, F))
      lowleak_cp <- c(lowleak_cp, acc_leak(cc, tt, lowl, T))
      highleak_cp <- c(highleak_cp, acc_leak(cc, tt, highl, T))
      if (tt <= .2) {
        dumbr_cp <- c(dumbr_cp, acc_dumbr(cc, 1, tt, .2, 0, TRUE))  
      } else {
        dumbr_cp <- c(dumbr_cp, acc_dumbr(-cc, 1, tt, .2, 0, TRUE))
      }
      dumbr_ncp <- c(dumbr_ncp, acc_dumbr(cc, 1, tt, .2, 0, FALSE))
      lowh_par_cp <- c(lowh_par_cp, acc_par(d1, d2, dfsion, tt, CPtime, lowh, nbins))
      lowh_par_ncp <- c(lowh_par_ncp, acc_par(d1, d1, dfsion, tt, CPtime, lowh, nbins))
      highh_par_cp <- c(highh_par_cp, acc_par(d1, d2, dfsion, tt, CPtime, highh, nbins))
      highh_par_ncp <- c(highh_par_ncp, acc_par(d1, d1, dfsion, tt, CPtime, highh, nbins))
    }
  }
  
  data <- data.table(C, t, norm_ncp, norm_cp, lowleak_ncp, highleak_ncp, lowleak_cp, highleak_cp, dumbr_cp, dumbr_ncp, lowh_par_cp, lowh_par_ncp, highh_par_cp, highh_par_ncp)
  
  
  
  #convert to long format
  long_data = melt(data, id.vars = c("C", "t"),
                  measure.vars = c("norm_ncp", "norm_cp", "lowleak_ncp", "highleak_ncp", "lowleak_cp", "highleak_cp", "dumbr_cp", "dumbr_ncp", "lowh_par_cp", "lowh_par_ncp", "highh_par_cp", "highh_par_ncp"))
  long_data[,Pwrong := 1-value]
  
  long_data[,CP:="no-CP"]
  long_data[,model:="DDM"]
  
  long_data[variable == "norm_cp" |
              variable == "lowleak_cp" |
              variable == "highleak_cp" |
              variable == "dumbr_cp" | 
              variable == "lowh_par_cp" | 
              variable == "highh_par_cp", `:=`(CP="CP")]
  long_data[variable == "lowleak_cp" | variable == "lowleak_ncp", `:=`(model="Low Leak")]
  long_data[variable == "highleak_cp" | variable == "highleak_ncp", `:=`(model="High Leak")]
  long_data[variable == "dumbr_cp" | variable == "dumbr_ncp", `:=`(model="DumbR")]
  long_data[variable == "lowh_par_cp" | variable == "lowh_par_ncp", `:=`(model="PAR low h")]
  long_data[variable == "highh_par_cp" | variable == "highh_par_ncp", `:=`(model="PAR high h")]
  long_data[,model:=factor(model, levels = c("DDM", "Low Leak", "High Leak", "DumbR", "PAR low h", "PAR high h"))]
  long_data[,CP:=factor(CP, levels=c("no-CP", "CP"))]
  return(long_data)
}

get_anim <- function() {
  anim <- ggplot(aes(x=t, y=value, col=model), data=get_acc_data()) + 
    stat_identity(yintercept=0.5, geom='hline', color='black', inherit.aes=TRUE) +
    geom_line(size=1.5, group=1) +
    facet_wrap(model~CP) +
    ylab("P(correct)") + xlab("time (s)") +
    labs(title = "Theoretical Curves Perfect Accumulator",
         subtitle = "CP vs. no-CP trials", 
         col="") +
    transition_reveal(t)
  return(anim)
}


#-------------------- ACTUAL CODE -----------------------#

g <- get_anim()
anim_save("test4.gif", g)

#time <- seq(12)
#x <- -time
#data <- data.table(time, x)
#
#g <- ggplot(data, aes(x=time, y=x, group=1)) + geom_line() +
#	transition_reveal(time)
#anim_save("test2.gif", g)
#anim_save("test2.mp4", g)

#animate(anim, renderer = gifski_renderer("gganim.gif"))

#library(gapminder)
#p <- ggplot(
#  gapminder,
#  aes(x = gdpPercap, y=lifeExp, size = pop, colour = country)
#  ) +
#  geom_point(show.legend = FALSE, alpha = 0.7) +
#  scale_color_viridis_d() +
#  scale_size(range = c(2, 12)) +
#  scale_x_log10() +
#  labs(x = "GDP per capita", y = "Life expectancy") + 
#  transition_time(year) +
#  labs(title = "Year: {frame_time}")
#anim_save("test3.gif", p)
#anim_save("test3.mp4", p)
