
import numpy as np


class CalAicObj:

    def __init__(self, RSS, tr_S, llf, aa, n):
        self.RSS = RSS
        self.tr_S = tr_S
        self.llf = llf
        self.aa = aa
        self.n = n


class CalMultiObj:

    def __init__(self, betas, reside):
        self.betas = betas
        self.reside = reside


class BaseModel:

    def __init__(self, y, X, kernel, fixed, constant):
        self.y = y
        self.X = X
        self.kernel = kernel
        self.fixed = fixed
        self.constant = constant
        self.n = X.shape[0]
        if self.constant:
            self.X = np.hstack([np.ones((self.n, 1)), X])
        else:
            self.X = X
        self.k = self.X.shape[1]


class Results(BaseModel):

    def __init__(
            self, y, X, kernel, fixed, constant,
            influ, reside, predict, betas, tr_STS
    ):
        super(Results, self).__init__(y, X, kernel, fixed, constant)
        self.influ = influ
        self.reside = reside
        self.predict = predict
        self.betas = betas
        self.tr_S = np.sum(influ)
        self.ENP = self.tr_S
        self.tr_STS = tr_STS
        self.TSS = np.sum((y - np.mean(y)) ** 2)
        self.RSS = np.sum(reside ** 2)
        self.sigma2 = self.RSS / (self.n - self.tr_S)
        self.std_res = self.reside / (np.sqrt(self.sigma2 * (1.0 - self.influ)))
        self.cooksD = self.std_res ** 2 * self.influ / (self.tr_S * (1.0 - self.influ))
        self.df_model = self.n - self.tr_S
        self.df_reside = self.n - 2.0 * self.tr_S + self.tr_STS
        self.R2 = 1 - self.RSS / self.TSS
        self.adj_R2 = 1 - (1 - self.R2) * (self.n - 1) / (self.n - self.ENP - 1)
        self.llf = -np.log(self.RSS) * self.n / 2 - (1 + np.log(np.pi / self.n * 2)) * self.n / 2
        self.aic = -2.0 * self.llf + 2.0 * (self.tr_S + 1)
        self.aicc = self.aic + 2.0 * self.tr_S * (self.tr_S + 1.0) / (self.n - self.tr_S - 1.0)
        self.bic = -2.0 * self.llf + (self.k + 1) * np.log(self.n)


class GWRResults(Results):

    """
    betas               : array
                          n*k, estimated coefficients

    predict             : array
                          n*1, predict y values

    CCT                 : array
                          n*k, scaled variance-covariance matrix

    df_model            : integer
                          model degrees of freedom

    df_reside           : integer
                          residual degrees of freedom

    reside              : array
                          n*1, residuals of the response

    RSS                 : scalar
                          residual sum of squares

    CCT                 : array
                          n*k, scaled variance-covariance matrix

    ENP                 : scalar
                          effective number of parameters, which depends on
                          sigma2

    tr_S                : float
                          trace of S (hat) matrix

    tr_STS              : float
                          trace of STS matrix

    R2                  : float
                          R-squared for the entire model (1- RSS/TSS)

    adj_R2              : float
                          adjusted R-squared for the entire model

    aic                 : float
                          Akaike information criterion

    aicc                : float
                          corrected Akaike information criterion
                          to account for model complexity (smaller
                          bandwidths)

    bic                 : float
                          Bayesian information criterion

    sigma2              : float
                          sigma squared (residual variance) that has been
                          corrected to account for the ENP

    std_res             : array
                          n*1, standardised residuals

    bse                 : array
                          n*k, standard errors of parameters (betas)

    influ               : array
                          n*1, leading diagonal of S matrix

    CooksD              : array
                          n*1, Cook's D

    tvalues             : array
                          n*k, local t-statistics

    llf                 : scalar
                          log-likelihood of the full model; see
                          pysal.contrib.glm.family for damily-sepcific
                          log-likelihoods
    """

    def __init__(
            self, coords, y, X, bw, kernel, fixed, constant, influ, reside, predict, betas, CCT, tr_STS
    ):
        super(GWRResults, self).__init__(y, X, kernel, fixed, constant, influ, reside, predict, betas, tr_STS)
        self.coords = coords
        self.bw = bw
        self.CCT = CCT * self.sigma2
        self.bse = np.sqrt(self.CCT)
        self.tvalues = self.betas / self.bse
        

class TWRResults(Results):
    """
    See Also GWRResults
    """
    
    def __init__(
            self, t, y, X, h, kernel, fixed, constant, influ, reside, predict, betas, tr_STS
    ):
        
        super(TWRResults, self).__init__(y, X, kernel, fixed, constant, influ, reside, predict, betas, tr_STS)
        self.t = t
        self.h = h


class GTWRResults(Results):
    """
    See Also GWRResults
    """

    def __init__(
            self, coords, t, y, X, bw, tau, kernel, fixed, constant, influ, reside, predict, betas, CCT, tr_STS
    ):

        super(GTWRResults, self).__init__(y, X, kernel, fixed, constant, influ, reside, predict, betas, tr_STS)
        self.coords = coords
        self.t = t
        self.bw = bw
        self.tau = tau
        self.bw_s = self.bw
        self.bw_t = np.sqrt(self.bw ** 2 / self.tau)
        self.CCT = CCT * self.sigma2
        self.bse = np.sqrt(self.CCT)
        self.tvalues = self.betas / self.bse
