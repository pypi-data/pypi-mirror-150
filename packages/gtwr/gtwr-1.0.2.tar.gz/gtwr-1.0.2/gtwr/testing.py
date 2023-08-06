import numpy as np
from .kernels import GTWRKernel, GWRKernel
from .obj import BaseModel
from .model import _compute_betas_gwr
from scipy.stats import f


class Test(BaseModel):
    
    def __init__(
            self,
            coords: np.ndarray,
            t: np.ndarray,
            y: np.ndarray,
            X: np.ndarray,
            bw_GTWR: float,
            tau_GTWR: float,
            kernel_GTWR: str = 'gaussian',
            fixed_GTWR: bool = False,
            constant: bool = True):

        super(Test, self).__init__(y, X, None, None, constant)
        self.coords = coords
        self.t = t
        self.bw_GTWR = bw_GTWR
        self.tau_GTWR = tau_GTWR
        self.kernel_GTWR = kernel_GTWR
        self.fixed_GTWR = fixed_GTWR
        self.RSS_GTWR = 0
        S = np.empty((self.n, self.n))
        for i in range(self.n):
            gtwr_kernel = GTWRKernel(self.coords, self.t, self.bw_GTWR, self.tau_GTWR, fixed=self.fixed_GTWR,
                                     function=self.kernel_GTWR)
            distance = gtwr_kernel.cal_distance(i)
            wi = gtwr_kernel.cal_kernel(distance).reshape(-1, 1)
            wi[wi <= 1e-6] = 1e-6
            betas, xtx_inv_xt = _compute_betas_gwr(self.y, self.X, wi)
            predict = np.dot(self.X[i], betas)[0]
            reside = self.y[i] - predict
            self.RSS_GTWR += float(reside ** 2)
            S[i] = np.dot(self.X[i], xtx_inv_xt)
        self.Rs = np.dot((np.eye(self.n)-S).T, (np.eye(self.n)-S))
        del S
        self.trRs = 0
        trRsRs = 0
        for i in range(self.n):
            self.trRs += self.Rs[i, i]
            trRsRs += float(self.Rs[i, :] @ self.Rs[:, i])
        self.r_s = self.trRs ** 2 / trRsRs
       
    def spacialtimetest(self):
        
        H = self.X @ np.linalg.inv(self.X.T @ self.X) @ self.X.T
        Rh = (np.eye(self.n)-H).T @ (np.eye(self.n)-H)
        del H
        RSS_OLS = (self.y.T @ Rh @ self.y)[0][0]
        Rhs = Rh - self.Rs
        del Rh
        trRhs = 0
        trRhsRhs = 0
        for i in range(self.n):
            trRhs += Rhs[i, i]
            trRhsRhs += float(Rhs[i, :] @ Rhs[:, i])
        r_h_s = trRhs**2 / trRhsRhs
        gttest = (RSS_OLS - self.RSS_GTWR) / self.RSS_GTWR * self.trRs/trRhs        
        gtF = f.sf(gttest, r_h_s, self.r_s)
        return gttest, gtF, r_h_s, self.r_s
    
    def spacialtest(
            self,
            h: float,
            kernel_TWR: str = 'gaussian',
            fixed_TWR: bool = False):
        
        RSS_TWR = 0
        M = np.empty((self.n, self.n))
        for i in range(self.n):
            gwr_kernel = GWRKernel(self.t, h, fixed=fixed_TWR, function=kernel_TWR)
            distance = gwr_kernel.cal_distance(i)
            wi = gwr_kernel.cal_kernel(distance).reshape(-1, 1)
            X_derivative = self.X * (self.t-self.t[i])
            X_new = np.hstack([self.X, X_derivative])
            xT = (X_new * wi).T
            xtx_inv_xt = np.dot(np.linalg.inv(np.dot(xT, X_new)), xT)
            x_stack = np.hstack([self.X[i].reshape(1, self.k), np.zeros((1, self.k))])
            predict = (np.dot(np.dot(x_stack, xtx_inv_xt), self.y))[0]
            reside = self.y[i] - predict
            RSS_TWR += float(reside ** 2)
            M[i] = np.dot(x_stack, xtx_inv_xt)
        Rm = (np.eye(self.n)-M).T @ (np.eye(self.n)-M)
        del M
        Rms = Rm - self.Rs
        del Rm
        trRms = 0
        trRmsRms = 0
        for i in range(self.n):
            trRms += Rms[i, i]
            trRmsRms += float(Rms[i, :] @ Rms[:, i])
        r_m_s = trRms**2 / trRmsRms
        gtest = (RSS_TWR - self.RSS_GTWR) / self.RSS_GTWR * self.trRs/trRms        
        gF = f.sf(gtest, r_m_s, self.r_s)
        return gtest, gF, r_m_s, self.r_s
    
    def timetest(
            self,
            bw_GWR: float,
            kernel_GWR: str = 'gaussian',
            fixed_GWR: bool = False):
        
        RSS_GWR = 0
        L = np.empty((self.n, self.n))
        for i in range(self.n):
            gwr_kernel = GWRKernel(self.coords, bw_GWR, fixed=fixed_GWR, function=kernel_GWR)
            distance = gwr_kernel.cal_distance(i)
            wi = gwr_kernel.cal_kernel(distance).reshape(-1, 1)
            betas, xtx_inv_xt = _compute_betas_gwr(self.y, self.X, wi)
            predict = np.dot(self.X[i], betas)[0]
            reside = self.y[i] - predict
            RSS_GWR += float(reside ** 2)
            L[i] = np.dot(self.X[i], xtx_inv_xt)
        Rl = (np.eye(self.n)-L).T @ (np.eye(self.n)-L)
        del L
        Rls = Rl - self.Rs
        del Rl
        trRls = 0
        trRlsRls = 0
        for i in range(self.n):
            trRls += Rls[i, i]
            trRlsRls += float(Rls[i, :] @ Rls[:, i])
        r_l_s = trRls**2 / trRlsRls
        ttest = (RSS_GWR - self.RSS_GTWR) / self.RSS_GTWR * self.trRs/trRls                
        tF = f.sf(ttest, r_l_s, self.r_s)
        return ttest, tF, r_l_s, self.r_s
