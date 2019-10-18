# functions to compute accuracy analytically for several models


#### PA #####

# accuracy of perfect accumulator on non-CP trials
acc <- function(C, t) {
  return(pnorm(abs(C)*sqrt(t)))
}

# accuracy of perfect accumulator on CP trials
# C represents |d|/sigma with d the drift rate and sigma the diffusion constant
acc_cp <- function(C, t) {
  C <- abs(C)
  if (t<=.2) {
    return(pnorm(C*sqrt(t)))
  } else {
    ccc <- t - .4  # in my equations this is -(T-tau) 
    return(pnorm(C*ccc/sqrt(t)))
  }
}



#### LA #####

# theoretical accuracy of a linear-leak model (O-U with drift)
# C is |drift|/diffusion , t is time in sec, leak is leak rate, cp is bool: whether there is a cp or not
acc_leak <- function(C, t, leak, cp) {
  C <- abs(C)
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



#### PAR #####
# we use Python base functions
acc_par <- function(drift1, drift2, diffusion, time, CPtime, h, numbins) {
  if (time <= CPtime) {
    return(acc(drift1/diffusion, time))
  } else {
    a <- log(h / (1-h))
    if (a < 0) {a <- -a}
    int_lims <- c(-a,a)  #tuple(-a,a)
    pneg = integrate_wrt_cdf_r(FFF(h, CPtime, drift1, diffusion), int_lims, numbins, time-CPtime, drift2, diffusion)
    if (drift2 < 0) {
      return(pneg)
    } else {
      return(1-pneg)
    } 
  }
}


#### PADumbR ##### 
# accuracy of perfect accumulator on non-CP trials
# drift must have the sign corresponding to the last epoch!
acc_dumbr <- function(drift, diffusion, time, CPtime, bias, CP) {
  C = drift / diffusion
  if (time <= CPtime) {
    return(acc(abs(C), time))
  } else {
    tau = time - CPtime
    numerator = tau * drift + bias
    denominator = diffusion * sqrt(tau)
    return(pnorm(sign(drift)*(numerator / denominator)))
  }
}