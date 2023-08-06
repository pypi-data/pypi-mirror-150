import numpy as np
from scipy.optimize import approx_fprime

from ThomasFermi.model import FQHE
from ThomasFermi.algo import phi
from ThomasFermi.algo import thomasfermi

def jacobian_test_1(N = 10, eps = 1e-8):
    """
        This function tests if E_tot_jac gives the correct jacobian.

    """

    pars = {'L':30., 'l_B':7., 'd_t':30, 'd_b':30, 'dx':0.5, 'dy':0.5, 'mu_factor':1, 'Ec':5.85/40., 'energy_scale':100., 'n_lower': -0.08, 'n_upper': 1.08}
    data = FQHE.FQHE_TFdata(pars)
    pars = {'TFdata': data, 'Phi_EW_ext':-0.045, 'Phi_NS_ext':-0.015, 'Phi_back':-0.055}
    Phi = phi.make_QPC_Phi(pars)
    pars = {'TFdata': data, 'Phi_ext':Phi.Phi_ext, 'n_iter':8}
    engine = thomasfermi.TF_engine(pars)

    err = 0
    for j in range(N):

        n = engine.init_n(eta = 0.5)
        jac_true = approx_fprime(n, engine.E_tot, eps)
        jac_approx = engine.E_tot_jac(n)

        err = np.max(err, np.sum(np.abs(jac_true - jac_approx))/np.sum(np.abs(jac_true)))

    assert err < 1e-3, "Jacobian is not correct"

def jacobian_test_2(N = 10, err = 1e-3):
    """
        This function tests if E_tot_jac gives the correct jacobian.

    """

    pars = {'L':20., 'l_B':7., 'd_t':30, 'd_b':30, 'dx':0.25, 'dy':0.25, 'mu_factor':1, 'Ec':5.85/40., 'energy_scale':100., 'n_lower': -0.08, 'n_upper': 1.08}
    data = FQHE.FQHE_TFdata(pars)
    pars = {'TFdata': data, 'Phi_EW_ext':-0.045, 'Phi_NS_ext':-0.015, 'Phi_back':-0.055}
    Phi = phi.make_QPC_Phi(pars)
    pars = {'TFdata': data, 'Phi_ext':Phi.Phi_ext, 'n_iter':8}
    engine = thomasfermi.TF_engine(pars)

    err = 0
    for j in range(N):

        n = engine.init_n(eta = 0.5)
        jac_true = approx_fprime(n, engine.E_tot, 1e-9)
        jac_approx = engine.E_tot_jac(n)

        err = np.max(err, np.sum(np.abs(jac_true - jac_approx))/np.sum(np.abs(jac_true)))

    assert err < 1e-3, "Jacobian is not correct"

def G0_to_G(self, G0):

    i_s = ((self.X + self.L)/self.dx).astype(int).reshape((1, -1))[0]
    j_s = ((self.Y + self.L)/self.dy).astype(int).reshape((1, -1))[0]

    G = np.zeros((len(i_s),len(i_s)))

    for k in range(len(i_s)):
        i = i_s[k]
        j = j_s[k]
        G[k,:] = (np.roll(np.roll(G0, - (self.Ny//2 - j), axis = 0), - (self.Nx//2 - i), axis = 1)).reshape((1, -1))

    return G