# ARGS:
#   initTable       initial data.table object
#   groupVarNames   vector of column names to use for grouping
# RETURNS:
#   combFactors     data.table with unique rows and their frequencies (i.e. count)
getFreq <- function(initTable, groupVarNames) {
  # create a smaller data table only containing the independent variables
  df <- initTable[, ..groupVarNames]
  totTrials <- nrow(df)
  # create other data table which counts trials with similar indep. vars. values (freq. column)
  combFactors <- df[, .(numTrials=.N, proportion=.N/totTrials), by=names(df)]
#   setnames(combFactors, c(groupVarNames, "numTrials"))
  return(combFactors)
}

# ARGS:
#   pilotNumber  integer representing the version of the pilot data to load
#   dataFolder   path to folder where data is stored
#   dataTag      type of data = string representing the last part of the csv filename
# RETURNS:
#   dataTable    data.table corresponding to the csv file
# NOTE: data.table package should be loaded before calling the function
loadPilotCSV <- function(pilotNumber, dataFolder, dataTag) {
    datafile <- paste(dataFolder,'Pilot',pilotNumber,"/pilot",pilotNumber,"_",dataTag,".csv",sep='')
    dataTable <- fread(file=datafile, header=TRUE, sep=",")
  return(dataTable)
}

# ARGS:
#   dataFolder   path to folder where data is stored
#   dataTag      type of data = string representing the last part of the csv filename
# RETURNS:
#   dataTable    data.table corresponding to the csv file
# NOTE: data.table package should be loaded before calling the function
loadTestCSV <- function(dataFolder, dataTag) {
    datafile <- paste(dataFolder,'test','/test2_',dataTag,".csv",sep='')
    dataTable <- fread(file=datafile, header=TRUE, sep=",")
  return(dataTable)
}
