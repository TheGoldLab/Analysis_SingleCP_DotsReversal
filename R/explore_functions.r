# load all the valid trials data for paid subjects as single data.table
get_full_data <- function() {
  # block that imports the data and casts it into useful types for R
  data <- fread('/home/adrian/SingleCP_DotsReversal/processed/all_valid_data.csv')
  
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
    CPresponseSide=factor(CPresponseSide),
    block=factor(block, levels=c('Quest', 'Block2', 'Block3', 'Block4', 'Block5', 'Block6', 'Block7',
                                 'Block8', 'Block9', 'Block10', 'Block11')),
    probCP=factor(probCP, ordered=TRUE)
  )]
  
  # render levels more human-friendly
  levels(data$dirChoice) <- c('left', 'right')
  levels(data$cpChoice) <- c('no-CP', 'CP')
  levels(data$initDirection) <- c('right', 'left')
  levels(data$endDirection) <- c('right', 'left')
  levels(data$presenceCP) <- c('no-CP', 'CP')
  levels(data$CPresponseSide) <- c('left', 'right')
  
  return(data)
}


