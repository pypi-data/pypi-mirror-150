import numpy as np


def golden_section(a, c, delta, decimal, function, tol, max_iter, verbose=False):
    b = a + delta * np.abs(c - a)
    d = c - delta * np.abs(c - a)
    diff = 1.0e9
    iter_num = 0
    score_dict = {}
    opt_val = None
    while np.abs(diff) > tol and iter_num < max_iter:
        iter_num += 1
        b = np.round(b, decimal)
        d = np.round(d, decimal)

        if b in score_dict:
            score_b = score_dict[b]
        else:
            score_b = function(b)
            score_dict[b] = score_b

        if d in score_dict:
            score_d = score_dict[d]
        else:
            score_d = function(d)
            score_dict[d] = score_d

        if score_b <= score_d:
            opt_val = b
            opt_score = score_b
            c = d
            d = b
            b = a + delta * np.abs(c - a)

        else:
            opt_val = d
            opt_score = score_d
            a = b
            b = d
            d = c - delta * np.abs(c - a)

        opt_val = np.round(opt_val, decimal)        
        diff = score_b - score_d
        if verbose:
            print('bw:', opt_val, ', score:', np.round(opt_score, 2))

    return opt_val


def onestep_golden_section(A, C, x, delta, tau_decimal, function, tol, mpi=False):
    iter_num = 0
    score_dict = {}
    diff = 1e9
    opt_score = None
    opt_tau = None
    B = A + delta * np.abs(C - A)
    D = C - delta * np.abs(C - A)
    while np.abs(diff) > tol and iter_num < 200:
        iter_num += 1
        B = np.round(B, tau_decimal)
        D = np.round(D, tau_decimal)
        if B in score_dict:
            score_B = score_dict[B]
        else:
            score_B = function(x, B)
            score_dict[B] = score_B

        if D in score_dict:
            score_D = score_dict[D]
        else:
            score_D = function(x, D)
            score_dict[D] = score_D
        if mpi:
            from mpi4py import MPI
            comm = MPI.COMM_WORLD
            rank = comm.Get_rank()
            if rank == 0:
                if score_B <= score_D:
                    opt_score = score_B
                    opt_tau = B
                    C = D
                    D = B
                    B = A + delta * np.abs(C - A)
                else:
                    opt_score = score_D
                    opt_tau = D
                    A = B
                    B = D
                    D = C - delta * np.abs(C - A)
                diff = score_B - score_D
                opt_tau = np.round(opt_tau, tau_decimal)
            B = comm.bcast(B, root=0)
            D = comm.bcast(D, root=0)
            diff = comm.bcast(diff, root=0)
            opt_score = comm.bcast(opt_score, root=0)
            opt_tau = comm.bcast(opt_tau, root=0)
        else:
            if score_B <= score_D:
                opt_score = score_B
                opt_tau = B
                C = D
                D = B
                B = A + delta * np.abs(C - A)
            else:
                opt_score = score_D
                opt_tau = D
                A = B
                B = D
                D = C - delta * np.abs(C - A)
            diff = score_B - score_D     
    return opt_tau, opt_score


def twostep_golden_section(
        a, c, A, C, delta, function,
        tol, max_iter, bw_decimal, tau_decimal, verbose=False, mpi=False):
    b = a + delta * np.abs(c - a)
    d = c - delta * np.abs(c - a)
    opt_bw = None
    opt_tau = None
    diff = 1e9
    score_dict = {}
    iter_num = 0
    while np.abs(diff) > tol and iter_num < max_iter:
        iter_num += 1
        b = np.round(b, bw_decimal)
        d = np.round(d, bw_decimal)
        if b in score_dict:
            tau_b, score_b = score_dict[b]
        else:
            if mpi:
                tau_b, score_b = onestep_golden_section(A, C, b, delta, tau_decimal, function, tol, mpi=True)
            else:
                tau_b, score_b = onestep_golden_section(A, C, b, delta, tau_decimal, function, tol)
            score_dict[b] = [tau_b, score_b]
        if d in score_dict:
            tau_d, score_d = score_dict[d]
        else:
            if mpi:
                tau_d, score_d = onestep_golden_section(A, C, d, delta, tau_decimal, function, tol, mpi=True)
            else:
                tau_d, score_d = onestep_golden_section(A, C, d, delta, tau_decimal, function, tol)
            score_dict[d] = [tau_d, score_d]
        if mpi:
            from mpi4py import MPI
            comm = MPI.COMM_WORLD
            rank = comm.Get_rank()
            if rank == 0:
                if score_b <= score_d:
                    opt_score = score_b
                    opt_bw = b
                    opt_tau = tau_b
                    c = d
                    d = b
                    b = a + delta * np.abs(c - a)
                else:
                    opt_score = score_d
                    opt_bw = d
                    opt_tau = tau_d
                    a = b
                    b = d
                    d = c - delta * np.abs(c - a) 
                diff = score_b - score_d
                opt_tau = np.round(opt_tau, tau_decimal)
                opt_bw = np.round(opt_bw, bw_decimal)
                if verbose:            
                    print('bw: ', opt_bw, ', tau: ', opt_tau, ', score: ', opt_score)
            b = comm.bcast(b, root=0)
            d = comm.bcast(d, root=0)
            diff = comm.bcast(diff, root=0)
            opt_bw = comm.bcast(opt_bw, root=0)
            opt_tau = comm.bcast(opt_tau, root=0)
        else:
            if score_b <= score_d:
                opt_score = score_b
                opt_bw = b
                opt_tau = tau_b
                c = d
                d = b
                b = a + delta * np.abs(c - a)
            else:
                opt_score = score_d
                opt_bw = d
                opt_tau = tau_d
                a = b
                b = d
                d = c - delta * np.abs(c - a) 
            diff = score_b - score_d
            if verbose:
                print('bw: ', opt_bw, ', tau: ', opt_tau, ', score: ', opt_score)
    return opt_bw, opt_tau
