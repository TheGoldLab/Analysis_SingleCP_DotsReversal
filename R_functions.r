# ARGS:
#   initTable       initial data.table object
#   groupVarNames   vector of column names to use for grouping
# RETURNS:
#   combFactors     data.table with unique rows and their frequencies (i.e. count)
getFreq <- function(initTable, groupVarNames) {
  # create a smaller data table only containing the independent variables
  df <- initTable[, ..groupVarNames]

  # create other data table which counts trials with similar indep. vars. values (freq. column)
  combFactors <- df[, .N, by=names(df)]
  setnames(combFactors, c(groupVarNames, "freq."))
  return(combFactors)
}
