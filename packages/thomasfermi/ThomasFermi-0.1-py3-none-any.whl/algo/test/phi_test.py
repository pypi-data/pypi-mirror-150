import numpy as np
from scipy.optimize import approx_fprime

from ThomasFermi.model import FQHE
from ThomasFermi.algo import phi

def QPC_test_1():
    """
        This function tests if make_QPC_Phi gives the correct external potential.

    """

    pars = {'L':30., 'l_B':7., 'd_t':30, 'd_b':30, 'dx':0.5, 'dy':0.5, 'mu_factor':1, 'Ec':5.85/40., 'energy_scale':100., 'n_lower': -0.08, 'n_upper': 1.08}
    data = FQHE.FQHE_TFdata(pars)
    pars = {'TFdata': data, 'Phi_EW':0, 'Phi_NS':0, 'Phi_back':-0.055}
    Phi_QPC = phi.make_QPC_Phi(pars)
    pars = {'TFdata': data, 'Phi_top':0, 'Phi_back':-0.055}
    Phi_uniform = phi.make_uniform_Phi(pars)

    err = np.sum(np.abs(Phi_QPC.Phi_ext - Phi_uniform.Phi_ext))/np.sum(np.abs(Phi_uniform.Phi_ext))

    assert err < 1e-3, "QPC potential is not correct"

def QPC_test_2():
    """
        This function tests if make_QPC_Phi gives the correct external potential.

    """

    pars = {'L':30., 'l_B':7., 'd_t':1, 'd_b':1, 'dx':0.5, 'dy':0.5, 'mu_factor':1, 'Ec':5.85/40., 'energy_scale':100., 'n_lower': -0.08, 'n_upper': 1.08}
    data = FQHE.FQHE_TFdata(pars)
    pars = {'TFdata': data, 'Phi_EW_ext':0.05, 'Phi_NS_ext':-0.03, 'Phi_back':0.01}
    Phi_QPC = phi.make_QPC_Phi(pars)

    err1 = Phi_QPC.Phi_ext.reshape((data.Nx, data.Ny))[data.Nx//4, data.Ny//4] - 0.05
    err2 = Phi_QPC.Phi_ext.reshape((data.Nx, data.Ny))[data.Nx//4, 3*data.Ny//4] - -0.03

    assert np.max(err1, err2) < 1e-3, "QPC potential is not correct"