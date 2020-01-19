library(data.table)

# gets data from a csv file, made of the concatenation of all the .csv files (except the QUEST ones)
# as they were outputted by snow-dots
get_full_data <- function(path_to_csv) {
  return(process_raw(fread(path_to_csv)))
}

# removes (inplace) columns unnecessary for analysis
process_raw <- function(dt, restrict2task = TRUE, probCPasFactor = TRUE) {
  dt <- dt[!is.na(dirChoice)]  # delete rows where dirChoice is NA
  dt[,presenceCP:=reversal]
  dt[,`:=`(finalDuration=NULL,
           dummyBlank=NULL,
           cpScreenOn=NULL,
           feedbackOn=NULL,
           blankScreen=NULL,
           targetOn=NULL,
           fixationStart=NULL,
           randSeedBase=NULL,
           trialEnd=NULL,
           trialStart=NULL, 
           reversal=NULL)]
  if (restrict2task) {
    dt <- dt[taskID == 100]
  }
  
  # set variables with appropriate type
  dt[, `:=`(
    subject=as.factor(subject),
    dirChoice=as.factor(dirChoice),
    cpChoice=factor(cpChoice),  # doesn't create level for NA values
    dirCorrect=as.integer(dirCorrect),
    cpCorrect=as.integer(cpCorrect),
    direction=as.factor(direction),
    presenceCP=factor(presenceCP, ordered=TRUE),
    duration=as.integer(duration * 1000)
  )]
  
  if (probCPasFactor) {
    dt[,probCP:=factor(probCP, ordered = TRUE)]
  }
  
  # render levels more human-friendly
  levels(dt$dirChoice) <- c('left', 'right')
  levels(dt$cpChoice) <- c('noCP', 'CP')
  levels(dt$direction) <- c('right', 'left')
  levels(dt$presenceCP) <- c('noCP', 'CP')
  
  
  # add factor coherence category 
  dt[, coh_cat:="0"]
  dt[coherence > 0, coh_cat:="th"]
  dt[coherence==100, coh_cat:="100"]
  dt[,coh_cat:=factor(coh_cat, levels=c("0", "th", "100"), ordered=T)]
  
  return(dt)
}