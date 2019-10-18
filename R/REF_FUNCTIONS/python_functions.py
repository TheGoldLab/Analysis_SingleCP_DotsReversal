import numpy as np
import scipy.stats as sp


def integrate_wrt_cdf(F, f, limits, bins):
    """
    Integrates function f between limits[0] and limits[1], with respect to the measure induced by the cdf F
    Note: this function fails when called from R. 
    :param F: cdf
    :param f: function to integrate w.r.t dF measure
    :param limits: tuple of integration bounds. It is assumed that F is undefined at the limit points
    :param bins: number of points on x-grid to use in integration (so, not quite the number of bins)
    """
    bin_width = (limits[1] - limits[0]) / bins  # just approximate, not the real bin width
    grid_points = np.linspace(limits[0] + bin_width/4, limits[1], num=bins, endpoint=False)
    cdf = F(grid_points)
    measure = np.diff(cdf)
    func = f(grid_points)
    return np.dot(measure, func[:-1])


def integrate_wrt_cdf_r(F, limits, bins, tau, dprime, sigma):
    """
    Version of integrate_wrt_cdf that should be callable from R (but some functionality is loss). Namely, ff only is used.
    :param F: cdf
    :param f: function to integrate w.r.t dF measure
    :param limits: tuple of integration bounds. It is assumed that F is undefined at the limit points
    :param bins: number of points on x-grid to use in integration (so, not quite the number of bins)
    """
    bin_width = (limits[1] - limits[0]) / bins  # just approximate, not the real bin width
    grid_points = np.linspace(limits[0] + bin_width/4, limits[1], num=bins, endpoint=False)
    cdf = F(grid_points)
    measure = np.diff(cdf)
    func = fff(tau, dprime, sigma)
    feval = func(grid_points)
    return np.dot(measure, feval[:-1])


def alpha(x, h):
    return np.log(((1-h)*np.exp(x) - h)/(1-h*(1+np.exp(x))))


def FF(x, h, T, d, sigma):
    """
    Cumulative distribution of accrued evidence at cp time T
    :param x: value at which cdf should be evaluated
    :param h: hazard rate (Prob(CP))
    :param T: cp time
    :param d: drift parameter on first epoch (before CP)
    :param sigma: diffusion coefficient
    :return: float
    """
    if h<0.5:
        cum = sp.norm.cdf((alpha(x, h) - T*d)/(sigma * np.sqrt(T)))
    else:
        cum = 1 - sp.norm.cdf((alpha(x, h) - T*d)/(sigma * np.sqrt(T)))
    return cum


def FFF(h, T, d, sigma):
    """
    Wrapper for FF, to consider it as a function of x only
    """
    def innerfunction(x):
        return FF(x, h, T, d, sigma)
    return innerfunction


def ff(tau, dprime, x, sigma):
    """
    density to integrate
    :param tau: time elapsed since CP
    :param dprime: drift term on epoch following CP
    :param x: point at which to evaluate pdf
    :param sigma: diffusion coefficient
    """
    return sp.norm.cdf(-(tau*dprime+x) / (np.sqrt(tau)*sigma))


def fff(tau, dprime, sigma):
    """
    Wrapper for ff, to consider it as a function of x only
    """
    def innerfunction(x):
        return ff(tau, dprime, x, sigma)
    return innerfunction


def acc_perfect_accum(d, sigma, t):
    """
    Computes accuracy of perfect accumulator on non-CP trials
    """
    return sp.norm.cdf(np.abs(d)/sigma * np.sqrt(t))


def acc_perfect_accum_cp(d, sigma, T, tau):
    """
    Computes accuracy of perfect accumulator on CP trials
    """
    return sp.norm.cdf(-(abs(d)/sigma)*(T-tau)/np.sqrt(T+tau))


def acc_leak_ncp(d, sigma, T, tau, leak):
    """
    Computes accuracy of leaky accumulator on non-CP trials
    """
    return sp.norm.cdf(abs(d)/sigma * (1-np.exp(-leak*(T+tau))) /np.sqrt((leak/2)*(1-np.exp(-2*leak*(T+tau)))))


def acc_leak_cp(d, sigma, T, tau, leak):
    """
    Computes accuracy of leaky accumulator on CP trials
    """
    return sp.norm.cdf(abs(d)/sigma * \
                       (1 - np.exp(-leak*tau)*(2-np.exp(-leak*(T)))) \
                       / np.sqrt((leak/2)*(1-np.exp(-2*leak*(T+tau)))))
