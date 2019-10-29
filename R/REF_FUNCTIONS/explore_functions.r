# load all the valid trials data for paid subjects as single data.table
get_full_data <- function(probCPasFactor = TRUE, excludeQuest = TRUE) {
  # block that imports the data and casts it into useful types for R
  data <- fread('/home/adrian/SingleCP_DotsReversal/processed/all_valid_data.csv')
  
  if (excludeQuest) {
    data <- data[block != "Quest"]
    data[, block:=factor(block, levels=c('Block2', 'Block3', 'Block4', 'Block5', 'Block6', 'Block7',
                                         'Block8', 'Block9', 'Block10', 'Block11'))]
  } else {
    data[, block:=factor(block, levels=c('Quest', 'Block2', 'Block3', 'Block4', 'Block5', 'Block6', 'Block7',
                                         'Block8', 'Block9', 'Block10', 'Block11'))]
  }
  
  # set variables with appropriate type
  data[, `:=`(
    subject=as.factor(subject),
    dirChoice=as.factor(dirChoice),
    cpChoice=factor(cpChoice),  # doesn't create level for NA values
    dirCorrect=as.integer(dirCorrect),
    cpCorrect=as.integer(cpCorrect),
    initDirection=as.factor(initDirection),
    endDirection=as.factor(endDirection),
    presenceCP=factor(presenceCP, ordered=TRUE),
    viewingDuration=as.integer(viewingDuration * 1000),
    CPresponseSide=factor(CPresponseSide)
  )]
  
  if (probCPasFactor) {
    data[,probCP:=factor(probCP, ordered = TRUE)]
  }
  
  # render levels more human-friendly
  levels(data$dirChoice) <- c('left', 'right')
  levels(data$cpChoice) <- c('noCP', 'CP')
  levels(data$initDirection) <- c('right', 'left')
  levels(data$endDirection) <- c('right', 'left')
  levels(data$presenceCP) <- c('noCP', 'CP')
  levels(data$CPresponseSide) <- c('left', 'right')


  # add factor coherence category 
  data[coherence > 0, coh_cat:= "th"]
  data[coherence==100, coh_cat:="100"]
  data[,coh_cat:=factor(coh_cat, levels=c("0", "th", "100"), ordered=T)]

  return(data)
}

#####
# Theoretical accuracy functions
####

# accuracy of perfect accumulator on non-CP trials
acc <- function(C, t) {
  return(pnorm(C*sqrt(t)))
}

# accuracy of perfect accumulator on CP trials
# C represents |d|/sigma with d the drift rate and sigma the diffusion constant
acc_cp <- function(C, t) {
  if (t<=.2) {
    return(pnorm(C*sqrt(t)))
  } else {
    ccc <- t - .4  # in my equations this is -(T-tau) 
    return(pnorm(C*ccc/sqrt(t)))
  }
}



# theoretical accuracy of a linear-leak model (O-U with drift)
# C is |drift|/diffusion , t is time in sec, leak is leak rate, cp is bool: whether there is a cp or not
acc_leak <- function(C, t, leak, cp) {
  if (cp) {
    if (t <= .2) {  # before CP, compute as for cp=F case
      return(
        pnorm(
          C * ( 1 - exp(-leak*t) ) /  sqrt( (leak / 2) * (1 - exp(-2*leak*t)) )
        )
      )
    } else {  # after CP
      tau <- t-.2
      return(pnorm(
        C * (1-exp( -leak * tau ) * (2-exp( -leak*0.2 ))) / 
          sqrt( (leak / 2) * (1 - exp(-2*leak*t)) )
      ))
    }
  } else {
    return(
      pnorm(
        C * ( 1 - exp(-leak*t) ) /  sqrt( (leak / 2) * (1 - exp(-2*leak*t)) )
      )
    )
  }
}
