import numpy as np
from .diagnosis import get_AICc, get_AIC, get_BIC, get_CV
from .obj import BaseModel
from scipy.spatial.distance import pdist
from .model import GWR, TWR, GTWR
from .search import golden_section, twostep_golden_section

getDiag = {'AICc': get_AICc, 'AIC': get_AIC, 'BIC': get_BIC, 'CV': get_CV}

delta = 0.38197


class SearchGWRParameter(BaseModel):
    """
    Select bandwidth for GWR model

    Parameters
    ----------
    coords        : array-like
                    n*2, collection of n sets of (x,y) coordinates of
                    observations

    y             : array-like
                    n*1, dependent variable

    X             : array-like
                    n*k, independent variable, excluding the constant
   
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
    from gtwr.sel import SearchGWRParameter
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
    sel = SearchGWRParameter(coords, y, X, kernel = 'gaussian', fixed = True)
    bw = sel.search(bw_max = 40, verbose = True)
    2.0   
    """
    
    def __init__(
            self,
            coords: np.ndarray,
            y: np.ndarray,
            X: np.ndarray,
            kernel: str = 'exponential',
            fixed: bool = False,
            constant: bool = True):

        super(SearchGWRParameter, self).__init__(y, X, kernel, fixed, constant)
        self.coords = coords
        self.int_score = not self.fixed
        
    def search(self,
               criterion: str = 'AICc',
               bw_min: float = None,
               bw_max: float = None,
               tol: float = 1.0e-6,
               bw_decimal: int = 0,
               max_iter: int = 200,
               verbose: bool = False):
        """
        Method to select one unique bandwidth for a GWR model.

        Parameters
        ----------
        criterion      : string
                         bw selection criterion: 'AICc', 'AIC', 'BIC', 'CV'
        bw_min         : float
                         min value used in bandwidth search
        bw_max         : float
                         max value used in bandwidth search  
        tol            : float
                         tolerance used to determine convergence
        max_iter       : integer
                         max iterations if no convergence to tol
                         
        bw_decimal      : scalar
                         The number of bandwidth's decimal places saved during the search
                 
        verbose        : Boolean
                         If true, bandwidth searching history is printed out; default is False.
        """

        def gwr_func(x):
            return getDiag[criterion](GWR(
                self.coords, self.y, self.X, x, kernel=self.kernel,
                fixed=self.fixed, constant=False).cal_aic())

        bw_min, bw_max = self._init_section(bw_min, bw_max)
        bw = golden_section(bw_min, bw_max, delta, bw_decimal, gwr_func, tol, max_iter, verbose)
        return bw
    
    def _init_section(self, bw_min, bw_max):
        if bw_min is not None and bw_max is not None:
            return bw_min, bw_max

        if len(self.X) > 0:
            n_glob = self.X.shape[1]
        else:
            n_glob = 0
        if self.constant:
            n_vars = n_glob + 1
        else:
            n_vars = n_glob
        n = np.array(self.coords).shape[0]

        if self.int_score:
            a = 40 + 2 * n_vars
            c = n
        else:
            sq_dists = pdist(self.coords)
            a = np.min(sq_dists) / 2.0
            c = np.max(sq_dists) 
        if bw_min is None:
            bw_min = a
        if bw_max is None:
            bw_max = c
            
        return bw_min, bw_max


class SearchTWRParameter(BaseModel):
    """
    Select h for TWR model

    Parameters
    ----------
    t             : array-like
                    n*1, time location

    y             : array-like
                    n*1, dependent variable

    X             : array-like
                    n*k, independent variable, excluding the constant
   
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
    from gtwr.sel import SearchTWRParameter
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
    sel = SearchTWRParameter(t, y, X, kernel = 'gaussian', fixed = True)
    h = sel.search(verbose = True)
    10.0  
    """
    
    def __init__(
            self,
            t: np.ndarray,
            y: np.ndarray,
            X: np.ndarray,
            kernel: str = 'exponential',
            fixed: bool = False,
            constant: bool = True):

        super(SearchTWRParameter, self).__init__(y, X, kernel, fixed, constant)
        self.t = t
        
    def search(
            self,
            criterion: str = 'AICc',
            h_min: float = None,
            h_max: float = None,
            tol: float = 1.0e-6,
            h_decimal: float = 0,
            max_iter: int = 200,
            verbose: bool = False):
        """
        Method to select one unique smooth parameter for a TWR model.

        Parameters
        ----------
        criterion      : string
                         bw selection criterion: 'AICc', 'AIC', 'BIC', 'CV'
        h_min          : float
                         min value used in smooth parameter search
        h_max          : float
                         max value used in smooth parameter search  
        tol            : float
                         tolerance used to determine convergence
        max_iter       : integer
                         max iterations if no convergence to tol
                         
        h_decimal       : scalar
                         The number of smooth parameter's decimal places saved during the search
                 
        verbose        : Boolean
                         If true, bandwidth searching history is printed out; default is False.
        """

        def twr_func(x):
            return getDiag[criterion](TWR(
                self.t, self.y, self.X, x, kernel=self.kernel,
                fixed=self.fixed, constant=False).cal_aic())

        h_min, h_max = self._init_section(h_min, h_max)
        h = golden_section(h_min, h_max, delta, h_decimal, twr_func, tol, max_iter, verbose)

        return h

    def _init_section(self, h_min, h_max):
        if h_min is not None and h_max is not None:
            return h_min, h_max

        sq_dists = pdist(self.t)
        a = np.min(sq_dists) / 2.0
        c = np.max(sq_dists) 
        if h_min is None:
            h_min = a
        if h_max is None:
            h_max = c
        return h_min, h_max


class SearchGTWRParameter(BaseModel):
    """
    Select bandwidth for GTWR model

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
    from gtwr.sel import SearchGTWRParameter
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
    sel = SearchGTWRParameter(coords, t, y, X, kernel = 'gaussian', fixed = True)
    bw, tau = sel.search(tau_max = 20, verbose = True)
    0.9, 1.5
    """

    def __init__(
            self,
            coords: np.ndarray,
            t: np.ndarray,
            y: np.ndarray,
            X: np.ndarray,
            kernel: str = 'exponential',
            fixed: bool = False,
            constant: bool = True):

        super(SearchGTWRParameter, self).__init__(y, X, kernel, fixed, constant)
        self.coords = coords
        self.t = t
        self.int_score = not self.fixed
        
    def search(
            self,
            criterion: str = 'AICc',
            bw_min: float = None,
            bw_max: float = None,
            tau_min: float = None,
            tau_max: float = None,
            tol: float = 1.0e-6,
            bw_decimal: int = 1,
            tau_decimal: int = 1,
            max_iter: int = 200,
            verbose: bool = False,
            mpi: bool = False):
        """
        Method to select one unique bandwidth and Spatio-temporal scale for a GTWR model.

        Parameters
        ----------
        criterion      : string
                         bw selection criterion: 'AICc', 'AIC', 'BIC', 'CV'
        bw_min         : float
                         min value used in bandwidth search
        bw_max         : float
                         max value used in bandwidth search
        tau_min        : float
                         min value used in spatio-temporal scale search
        tau_max        : float
                         max value used in spatio-temporal scale search     
        tol            : float
                         tolerance used to determine convergence
        max_iter       : integer
                         max iterations if no convergence to tol   
        bw_decimal      : scalar
                         The number of bandwidth's decimal places saved during the search
        tau_decimal     : scalar
                         The number of Spatio-temporal decimal places saved during the search
        verbose        : Boolean
                         If true, bandwidth searching history is printed out; default is False.
        mpi            : bool
                        Parallel computing using Message Passing Interface
        """

        def gtwr_func(x, y):
            if mpi:
                return getDiag[criterion](GTWR(
                    self.coords, self.t, self.y, self.X, x, y, kernel=self.kernel,
                    fixed=self.fixed, constant=False).cal_aic(mpi=True), mpi=True)
            return getDiag[criterion](GTWR(
                self.coords, self.t, self.y, self.X, x, y, kernel=self.kernel,
                fixed=self.fixed, constant=False).cal_aic(mpi=False))

        bw_min, bw_max, tau_min, tau_max = self._init_section(bw_min, bw_max, tau_min, tau_max)
        bw, tau = twostep_golden_section(bw_min, bw_max, tau_min, tau_max, delta, gtwr_func, tol, max_iter, bw_decimal,
                                         tau_decimal, verbose, mpi)

        return bw, tau

    def _init_section(self, bw_min, bw_max, tau_min, tau_max):
        if (bw_min is not None) and (bw_max is not None) and (tau_min is not None) and (tau_max is not None):
            return bw_min, bw_max, tau_min, tau_max
        if len(self.X) > 0:
            n_glob = self.X.shape[1]
        else:
            n_glob = 0
        if self.constant:
            n_vars = n_glob + 1
        else:
            n_vars = n_glob
        n = np.array(self.coords).shape[0]

        if self.int_score:
            a = 40 + 2 * n_vars
            c = n
        else:
            sq_dists = pdist(self.coords)
            a = np.min(sq_dists) / 2.0
            c = np.max(sq_dists) 

        if bw_min is None:
            bw_min = a
        if bw_max is None:
            bw_max = c
        
        if tau_min is None:
            tau_min = 0
        if tau_max is None:
            tau_max = 4
        return bw_min, bw_max, tau_min, tau_max
