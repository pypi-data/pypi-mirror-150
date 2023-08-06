import numpy as np
from .kernels import GWRKernel, GTWRKernel
from .obj import BaseModel, CalAicObj, GWRResults, TWRResults, GTWRResults
from scipy import linalg


def _compute_betas_gwr(y, x, wi):
    """
    compute MLE coefficients using iwls routine

    Methods: p189, Iteratively (Re)weighted Least Squares (IWLS),
    Fotheringham, A. S., Brunsdon, C., & Charlton, M. (2002).
    Geographically weighted regression: the analysis of spatially varying relationships.
    """
    xT = (x * wi).T
    xtx = np.dot(xT, x)
    xtx_inv_xt = linalg.solve(xtx, xT)
    betas = np.dot(xtx_inv_xt, y)
    return betas, xtx_inv_xt


class GWR(BaseModel):
    """
    Geographically Weighted Regression

    Parameters
    ----------
    coords        : array-like
                    n*2, collection of n sets of (x,y) coordinates of
                    observations
                
    y             : array-like
                    n*1, dependent variable

    X             : array-like
                    n*k, independent variable, excluding the constant

    bw            : scalar
                    bandwidth value consisting of either a distance or N
                    nearest neighbors; user specified or obtained using
                    sel                   
   
    kernel        : string
                    type of kernel function used to weight observations;
                    available options:
                    'gaussian'
                    'bisquare'
                    'exponential'

    fixed         : boolean
                    True for distance based kernel function and  False for
                    adaptive (nearest neighbor) kernel function (default)

    constant      : boolean
                    True to include intercept (default) in model and False to exclude
                    intercept.

    Examples
    --------
    import numpy as np
    from gtwr.model import GWR
    np.random.seed(1)
    u = np.array([(i-1)%12 for i in range(1,1729)]).reshape(-1,1)
    v = np.array([((i-1)%144)//12 for i in range(1,1729)]).reshape(-1,1)
    t = np.array([(i-1)//144 for i in range(1,1729)]).reshape(-1,1)
    x1 = np.random.uniform(0,1,(1728,1))
    x2 = np.random.uniform(0,1,(1728,1))
    epsilon = np.random.randn(1728,1)
    beta0 = 5
    beta1 = 3 + (u + v + t)/6
    beta2 = 3+((36-(6-u)**2)*(36-(6-v)**2)*(36-(6-t)**2))/128
    y = beta0 + beta1 * x1 + beta2 * x2 + epsilon
    coords = np.hstack([u,v])
    X = np.hstack([x1,x2])
    gwr = GWR(coords, y, X, 0.8, kernel='gaussian', fixed=True).fit()
    print(gwr.R2)
    0.673048927289592
    """
    
    def __init__(
            self,
            coords: np.ndarray,
            y: np.ndarray,
            X: np.ndarray,
            bw: float,
            kernel: str = 'gaussian',
            fixed: bool = False,
            constant: bool = True):

        super(GWR, self).__init__(y, X, kernel, fixed, constant)
        self.coords = coords
        self.bw = bw
            
    def _build_wi(self, i, bw):

        try:
            gwr_kernel = GWRKernel(self.coords, bw, fixed=self.fixed, function=self.kernel)
            distance = gwr_kernel.cal_distance(i)
            wi = gwr_kernel.cal_kernel(distance)
        except BaseException:
            raise  # TypeError('Unsupported kernel function  ', kernel)
            
        return wi

    def cal_aic(self):
        RSS = 0
        tr_S = 0
        aa = 0
        for i in range(self.n):
            err2, hat = self._local_fit(i, final=False)
            aa += err2 / ((1 - hat) ** 2)
            RSS += err2
            tr_S += hat
        llf = -np.log(RSS) * self.n / 2 - (1 + np.log(np.pi / self.n * 2)) * self.n / 2
        return CalAicObj(float(RSS), tr_S, float(llf), float(aa), self.n)

    def _local_fit(self, i, final=True):
        wi = self._build_wi(i, self.bw).reshape(-1, 1)
        betas, inv_xtx_xt = _compute_betas_gwr(self.y, self.X, wi)
        predict = np.dot(self.X[i], betas)[0]
        reside = self.y[i] - predict
        influx = np.dot(self.X[i], inv_xtx_xt[:, i])
        if not final:
            return reside * reside, influx
        Si = np.dot(self.X[i], inv_xtx_xt).reshape(-1)
        CCT = np.diag(np.dot(inv_xtx_xt, inv_xtx_xt.T)).reshape(-1)
        Si2 = np.sum(Si ** 2)
        return influx, reside, predict, betas.reshape(-1), CCT, Si2
    
    def fit(self):
        """
        fit GWR models
        """

        influ, reside, predict = np.empty((self.n, 1)), np.empty((self.n, 1)), np.empty((self.n, 1))
        betas, CCT = np.empty((self.n, self.k)), np.empty((self.n, self.k))
        tr_STS = 0
        for i in range(self.n):
            influ_i, reside_i, predict_i, betas_i, CCT_i, tr_STS_i = self._local_fit(i)
            influ[i] = influ_i
            reside[i] = reside_i
            predict[i] = predict_i
            betas[i] = betas_i
            CCT[i] = CCT_i
            tr_STS += tr_STS_i
        return GWRResults(self.coords, self.y, self.X, self.bw, self.kernel, self.fixed, self.constant, influ,
                          reside, predict, betas, CCT, tr_STS)


class TWR(BaseModel):
    """
    Temporally Weighted Regression

    Parameters
    ----------
    t             : array-like
                    n*1, time location

    y             : array-like
                    n*1, dependent variable

    X             : array-like
                    n*k, independent variable, excluding the constant

    h             : scalar
                    bandwidth value consisting of either a distance or N
                    nearest neighbors; user specified or obtained using
                    Sel                    
   
    kernel        : string
                    type of kernel function used to weight observations;
                    available options:
                    'gaussian'
                    'bisquare'
                    'exponential'

    fixed         : boolean
                    True for distance based kernel function and  False for
                    adaptive (nearest neighbor) kernel function (default)

    constant      : boolean
                    True to include intercept (default) in model and False to exclude
                    intercept.
    Examples
    --------
    import numpy as np
    from gtwr.model import TWR
    np.random.seed(1)
    t = np.array([(i-1)//144 for i in range(1,1729)]).reshape(-1,1)
    x1 = np.random.uniform(0,1,(1728,1))
    x2 = np.random.uniform(0,1,(1728,1))
    epsilon = np.random.randn(1728,1)
    beta0 = 5
    beta1 = 3 + t/6
    beta2 = 3+(36-(6-t)**2)/128
    y = beta0 + beta1 * x1 + beta2 * x2 + epsilon
    X = np.hstack([x1,x2])
    twr = TWR(t, y, X, 0.8, kernel='gaussian', fixed=True).fit()
    print(twr.R2)
    0.6975043786214365
    """
    
    def __init__(
            self,
            t: np.ndarray,
            y: np.ndarray,
            X: np.ndarray,
            h: float,
            kernel: str = 'gaussian',
            fixed: bool = False,
            constant: bool = True):

        super(TWR, self).__init__(y, X, kernel, fixed, constant)
        self.t = t
        self.h = h
            
    def _build_wi(self, i, h):

        try:
            gwr_kernel = GWRKernel(self.t, h, fixed=self.fixed, function=self.kernel)
            distance = gwr_kernel.cal_distance(i)
            wi = gwr_kernel.cal_kernel(distance)
        except BaseException:
            raise  # TypeError('Unsupported kernel function  ', kernel)
            
        return wi

    def cal_aic(self):
        RSS = 0
        tr_S = 0
        aa = 0
        for i in range(self.n):
            err2, hat = self._local_fit(i, final=False)
            aa += err2 / ((1 - hat) ** 2)
            RSS += err2
            tr_S += hat
        llf = -np.log(RSS) * self.n / 2 - (1 + np.log(np.pi / self.n * 2)) * self.n / 2
        return CalAicObj(float(RSS), tr_S, float(llf), float(aa), self.n)
    
    def _local_fit(self, i, final=True):
        
        wi = self._build_wi(i, self.h).reshape(-1, 1)
        X_derivative = self.X * (self.t-self.t[i])
        X_new = np.hstack([self.X, X_derivative])
        xT = (X_new * wi).T
        xtx_inv_xt = np.dot(np.linalg.inv(np.dot(xT, X_new)), xT)
        x_stack = np.hstack([self.X[i].reshape(1, self.k), np.zeros((1, self.k))])
        predict = (np.dot(np.dot(x_stack, xtx_inv_xt), self.y))[0]
        reside = self.y[i] - predict
        influ = np.dot(x_stack, xtx_inv_xt[:, i])[0]
        if not final:
            return reside * reside, influ
        else:
            betas = np.dot(xtx_inv_xt, self.y)[:self.k]
            zeros = np.zeros((1, self.k))
            Si = np.dot(np.hstack([self.X[i].reshape(1, self.k), zeros]), xtx_inv_xt).reshape(-1)
            Si2 = np.sum(Si**2)
            return influ, reside, predict, betas.reshape(-1), Si2
    
    def fit(self):
        """
        fit TWR models
        """
        influ, reside, predict = np.empty((self.n, 1)), np.empty((self.n, 1)), np.empty((self.n, 1))
        betas = np.empty((self.n, self.k))
        tr_STS = 0
        for i in range(self.n):
            influ_i, reside_i, predict_i, betas_i, tr_STS_i = self._local_fit(i)
            influ[i] = influ_i
            reside[i] = reside_i
            predict[i] = predict_i
            betas[i] = betas_i
            tr_STS += tr_STS_i
        return TWRResults(self.t, self.y, self.X, self.h, self.kernel, self.fixed, self.constant, influ, reside,
                          predict, betas, tr_STS)
       

class GTWR(BaseModel):
    """
    Geographically and Temporally Weighted Regression

    Parameters
    ----------
    coords        : array-like
                    n*2, collection of n sets of (x,y) coordinates of
                    observations
                    
    t             : array-like
                    n*1, time location

    y             : array-like
                    n*1, dependent variable

    X             : array-like
                    n*k, independent variable, excluding the constant

    bw            : scalar
                    bandwidth value consisting of either a distance or N
                    nearest neighbors; user specified or obtained using
                    sel
                    
    tau           : scalar
                    spatio-temporal scale
   
    kernel        : string
                    type of kernel function used to weight observations;
                    available options:
                    'gaussian'
                    'bisquare'
                    'exponential'

    fixed         : boolean
                    True for distance based kernel function and  False for
                    adaptive (nearest neighbor) kernel function (default)

    constant      : boolean
                    True to include intercept (default) in model and False to exclude
                    intercept.
    
    Examples
    --------
    import numpy as np
    from gtwr.model import GTWR
    np.random.seed(10)
    u = np.array([(i-1)%12 for i in range(1,1729)]).reshape(-1,1)
    v = np.array([((i-1)%144)//12 for i in range(1,1729)]).reshape(-1,1)
    t = np.array([(i-1)//144 for i in range(1,1729)]).reshape(-1,1)
    x1 = np.random.uniform(0,1,(1728,1))
    x2 = np.random.uniform(0,1,(1728,1))
    epsilon = np.random.randn(1728,1)
    beta0 = 5
    beta1 = 3 + (u + v + t)/6
    beta2 = 3+((36-(6-u)**2)*(36-(6-v)**2)*(36-(6-t)**2))/128
    y = beta0 + beta1 * x1 + beta2 * x2 + epsilon
    coords = np.hstack([u,v])
    X = np.hstack([x1,x2])
    gtwr = GTWR(coords, t, y, X, 0.8, 1.9, kernel='gaussian', fixed=True).fit()
    print(gtwr.R2)
    0.9899869616636376
    """

    def __init__(
            self,
            coords: np.ndarray,
            t: np.ndarray,
            y: np.ndarray,
            X: np.ndarray,
            bw: float,
            tau: float,
            kernel: str = 'gaussian',
            fixed: bool = False,
            constant: bool = True):
        super(GTWR, self).__init__(y, X, kernel, fixed, constant)
        self.coords = coords
        self.t = t
        self.bw = bw
        self.tau = tau
        self.bw_s = self.bw
        self.bw_t = np.sqrt(self.bw**2 / self.tau)
        
    def _build_wi(self, i, bw, tau):

        try:
            gtwr_kernel = GTWRKernel(self.coords, self.t, bw, tau, fixed=self.fixed, function=self.kernel)
            distance = gtwr_kernel.cal_distance(i)
            wi = gtwr_kernel.cal_kernel(distance)
        except BaseException:
            raise  # TypeError('Unsupported kernel function  ', kernel)
            
        return wi

    def cal_aic(self, mpi: bool = False):
        if mpi:
            from mpi4py import MPI
            import math
            comm = MPI.COMM_WORLD
            size = comm.Get_size()
            rank = comm.Get_rank()
            iter_num = np.arange(self.n)
            m = int(math.ceil(float(len(iter_num)) / size))
            x_chunk = iter_num[rank * m:(rank + 1) * m]
            RSS = 0
            tr_S = 0
            aa = 0
            for i in x_chunk:
                err2, hat = self._local_fit(i, final=False)
                aa += err2 / ((1 - hat) ** 2)
                RSS += err2
                tr_S += hat
            aa_list = comm.gather(aa, root=0)
            RSS_list = comm.gather(RSS, root=0)
            trS_list = comm.gather(tr_S, root=0)
            if rank == 0:
                RSS = sum(RSS_list)
                tr_S = sum(trS_list)
                aa = sum(aa_list)
                llf = -np.log(RSS) * self.n / 2 - (1 + np.log(np.pi / self.n * 2)) * self.n / 2
                return CalAicObj(float(RSS), tr_S, float(llf), float(aa), self.n)
        else:
            RSS = 0
            tr_S = 0
            aa = 0
            for i in range(self.n):
                err2, hat = self._local_fit(i, final=False)
                aa += err2 / ((1 - hat) ** 2)
                RSS += err2
                tr_S += hat
            llf = -np.log(RSS) * self.n / 2 - (1 + np.log(np.pi / self.n * 2)) * self.n / 2
            return CalAicObj(float(RSS), tr_S, float(llf), float(aa), self.n)

    def _local_fit(self, i, final=True):
        
        wi = self._build_wi(i, self.bw, self.tau).reshape(-1, 1)
        betas, xtx_inv_xt = _compute_betas_gwr(self.y, self.X, wi)
        predict = np.dot(self.X[i], betas)[0]
        reside = self.y[i] - predict
        influ = np.dot(self.X[i], xtx_inv_xt[:, i])
        if not final:
            return reside * reside, influ
        else:
            Si = np.dot(self.X[i], xtx_inv_xt).reshape(-1)
            CCT = np.diag(np.dot(xtx_inv_xt, xtx_inv_xt.T)).reshape(-1)
            Si2 = np.sum(Si**2)
            return influ, reside, predict, betas.reshape(-1), CCT, Si2
        
    def fit(self, mpi=False):
        """
        fit GTWR models

        """
        
        if mpi:
            from mpi4py import MPI
            import math
            comm = MPI.COMM_WORLD
            size = comm.Get_size()
            rank = comm.Get_rank()
            iter_num = np.arange(self.n)
            m = int(math.ceil(float(len(iter_num)) / size))
            x_chunk = iter_num[rank * m:(rank + 1) * m]
            n_chunk = x_chunk.shape[0]
            influ, reside, predict = np.empty((n_chunk, 1)), np.empty((n_chunk, 1)), np.empty((n_chunk, 1))
            betas, CCT = np.empty((n_chunk, self.k)), np.empty((n_chunk, self.k))
            tr_STS = 0
            pos = 0
            for i in x_chunk:
                influ_i, reside_i, predict_i, betas_i, CCT_i, tr_STS_i = self._local_fit(i)
                influ[pos] = influ_i
                reside[pos] = reside_i
                predict[pos] = predict_i
                betas[pos] = betas_i
                CCT[pos] = CCT_i
                tr_STS += tr_STS_i
                pos += 1
            influ_list = comm.gather(influ, root=0)
            reside_list = comm.gather(reside, root=0)
            predict_list = comm.gather(predict, root=0)
            betas_list = comm.gather(betas, root=0)
            CCT_list = comm.gather(CCT, root=0)
            tr_STS_list = comm.gather(tr_STS, root=0)
            if rank == 0:
                influ = np.vstack(influ_list)
                reside = np.vstack(reside_list)
                predict = np.vstack(predict_list)
                betas = np.vstack(betas_list)
                CCT = np.vstack(CCT_list)
                tr_STS = sum(tr_STS_list)
                return GTWRResults(
                    self.coords, self.t, self.y, self.X, self.bw, self.tau, self.kernel, self.fixed, self.constant,
                    influ, reside, predict, betas, CCT, tr_STS)

        influ, reside, predict = np.empty((self.n, 1)), np.empty((self.n, 1)), np.empty((self.n, 1))
        betas, CCT = np.empty((self.n, self.k)), np.empty((self.n, self.k))
        tr_STS = 0
        for i in range(self.n):
            influ_i, reside_i, predict_i, betas_i, CCT_i, tr_STS_i = self._local_fit(i)
            influ[i] = influ_i
            reside[i] = reside_i
            predict[i] = predict_i
            betas[i] = betas_i
            CCT[i] = CCT_i
            tr_STS += tr_STS_i
        return GTWRResults(
            self.coords, self.t, self.y, self.X, self.bw, self.tau, self.kernel, self.fixed, self.constant,
            influ, reside, predict, betas, CCT, tr_STS
        )
