#---------------------------------------------------------------------
#
# 		FUNCTIONS TO PROCESS FIRST-STAGE CSV FILES
#
#---------------------------------------------------------------------

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


#---------------------------------------------------------------------
#
#       	FUNCTIONS TO PROCESS PSYCHOMETRIC CSV FILES
#
#---------------------------------------------------------------------

# DESCR:
#   applies logistic function, after transforming the input with a given
#   linear functional
# ARGS:
#   x_vals       	vector of scalars
#   linear_functional  	R function that accepts vector as input; typically, this is the output of linear_func() defined below
# RETURNS:
#   a vector
my_logistic <- function(x_vals, linear_functional) {
    return(exp(linear_functional(x_vals))/(1+exp(linear_functional(x_vals))))
}


# DESCR:
#   creates a linear functional
# ARGS:
#   coefs  vector of two scalars
# RETURNS:
#   a function that can take vector as argument
linear_func <- function(coefs) {
    f <- function(x) {
        return(coefs[1]+coefs[2]*x)
    }
    return(f)
}


# DESCR:
#   Fits a logistic regression model with a single predictor and produces plot
#   Uses R's glm
#   This function is not very modular...
# ARGS:
#   datatable        a data.table
#   response         name of variable in datatable that contains the response (this is NOT a string), simply pass in the column name, without quotes.
#   response_value   whatever value that the binomial model should consider as a "success"; it can be "right" if response is choice, or TRUE if response is correct 
#   predictor        name of variable in datatable that glm should use as a predictor
# RETURNS:
#   call to ggplot()
fit_logistic_single_pred <- function(datatable, response, response_value, predictor) {
    logistic_fit <- substitute(glm(response ~ predictor, family=binomial(), data=datatable))
    print(summary(eval(logistic_fit)))
    betas <- coef(eval(logistic_fit))
#     print(betas)
    x <- substitute(
        unique(datatable[order(predictor),.(predictor),by=.(predictor)][,predictor])
        )
    fit_prop <- my_logistic(eval(x), linear_func(betas))
    fitted_curve <- data.table(x=eval(x), y=fit_prop)
    
    # control output figure size
    options(repr.plot.width=8, repr.plot.height=4)
    g <- substitute(
        ggplot(datatable[,.(prop=sum(response==response_value)/.N),by=predictor], aes(x=predictor, y=prop)) + 
        geom_point() +
        geom_line(aes(x=x, y=y),data=fitted_curve,inherit.aes=FALSE) +
        ylim(0,1)
        )
    return(eval(g))
}


# DESCR:
#   Standard Weibull
# ARGS:
#   x           vector of stimulus values (should be positive)
#   params      a 4-element vector with the following names: 'guess' 'threshold' 'lapse' 'slope'
# RETURNS:
#   a vector of scalars between 0 and 1
weibull <- function(x, params){
    return(1-exp(-(x/params[['threshold']])^params[['slope']]))
}


# DESCR:
#   Applies standard transformation to sensory performance function
# ARGS:
#   perf_func   a function with signature perf_func(x, params), with params defined below
#   params      a 4-element vector with the following names: 'guess' 'threshold' 'lapse' 'slope'
# RETURNS:
#   a function of stimulus values
psi_corr <- function(perf_func, params){
    psychometric <- function(x){
        return(params[['guess']]+(1-params[['guess']]-params[['lapse']])*perf_func(x, params))
    }
    return(psychometric)
}
