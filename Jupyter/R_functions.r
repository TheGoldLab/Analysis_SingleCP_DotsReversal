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
  combFactors <- df[, .(numTrials=.N, percent=as.integer(100*(.N/totTrials))), by=names(df)]
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
#   pilotNumbers list of integers representing the versions of the pilot data to load
#   dataFolder   path to folder where data is stored
#   dataTag      type of data = string representing the last part of the csv filename
# RETURNS:
#   dataTable    data.table corresponding to a concatenation of the csv files. A pilotID column is added
# NOTE: data.table package should be loaded before calling the function
loadMultiplePilotCSV <- function(pilotNumbers, dataFolder, dataTag) {
    list_of_tables <- list()
    # we append the data.tables one by one, calling loadPilotCSV
    for (n in pilotNumbers) {
        individual_pilot <- loadPilotCSV(n, dataFolder, dataTag)
        individual_pilot[,pilotID:=n]
        list_of_tables <- c(list_of_tables, list(individual_pilot))
        }
  return(rbindlist(list_of_tables))
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
