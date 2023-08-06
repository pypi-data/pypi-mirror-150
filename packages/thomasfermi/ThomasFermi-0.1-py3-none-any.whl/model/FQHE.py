import numpy as np
import scipy as sp
from scipy import optimize
from scipy import interpolate
from scipy import integrate
import functools
import time
import copy

import os
from scipy import fft

from ThomasFermi.algo.thomasfermi import TFdata
from ThomasFermi.model import FQHE

class FQHE_TFdata(TFdata):

    def __init__(self, pars):
        """
            Base class for representing the Thomas-Fermi calculation.
            Input dictionary pars encodes all the relevant parameters.

            l_B - magnetic length
            L - system size in l_B
            dx, dy - mesh size in l_B

            d_t, d_b - distance (in nm) from 2DEG to top/bottom gates

            eps_xy, eps_z - anisotropic permitivities depending on the material
                filling the space between the 2DEG and gates.

            Ec - strength of the Coulomb term in eV

            a - lattice spacing of graphene

        """

        self.dx = pars.setdefault('dx', 0.5)
        self.dy = pars.setdefault('dy', 0.5)
        self.l_B = pars.setdefault('l_B', 9.2)

        super().__init__(pars)

        self.Sq = self.gaussian_conv()/(self.dx*self.dy/self.a**2)

        self.mu_factor = pars.setdefault('mu_factor', 3)

        self.mu_model = pars.setdefault('mu_model', 'expt')

        if self.mu_model == 'expt':
            self.make_mu_experimental(self.mu_factor)
        elif self.mu_model == 'phenom':
            self.make_mu_phenom()
        else:
            raise ValueError("mu model does not exist")

    def gaussian_conv(self):
        """
            Helper function for constructing the Gaussian convolution.
        """

        Q = (self.qx,self.qy)

        Q = np.linalg.norm(Q, axis = 0)

        ans = np.exp(-(Q/self.a)**2/2.)

        return ans/(np.sum(ans)*self.dqx*self.dqy)

    def make_mu_experimental(self, mu_factor):
        """
            Load experimental data from arXiv: 2008.05466
            Create interpolated functions for dmu/dn, mu, and E_int
        """

        d = np.loadtxt(os.path.dirname(FQHE.__file__) + "\\nu_to_mu.dat")
        d[:,1] *= self.mu_factor*1.
        self.mu = interpolate.interp1d(d[:,0], d[:,1])
        self.dmu = interpolate.interp1d(0.5 * (d[1:,0] + d[:-1,0]), np.diff(self.mu(d[:,0])))
        integrated_mu = integrate.cumtrapz(self.mu(d[:,0]), x=d[:,0], initial=0.)
        integrated_mu -= integrated_mu[np.argmin(np.abs(d[:,0]))]
        self.E_int = interpolate.interp1d(d[:,0], integrated_mu)

        self.T = np.abs(self.E_int(1) - self.E_int(0))

        if self.n_lower == None:
            self.n_lower = -1.
            self.n_upper = 1.9

        return True

    def make_mu_phenom(self, dos_gap = 0.6, dos_plateau = 1.1, dos_frac_plateau=0.15, dn=1e-4):
        """
            Construct a phenomenological model for mu involving stepwise
            constant compressibility.
        """

        dn_plateau = 0.05
        dn_frac_plateau = 0.025
        n = np.arange(-2,2+1e-16,dn)

        plateau = np.abs(n - np.round(n)) < dn_plateau
        frac_plateau = (np.abs((n - 1./3) % 1) < dn_frac_plateau) + (np.abs((n - 2./3) % 1) < dn_frac_plateau)
        dos = n*0 - dos_gap
        dos[plateau] = dn_plateau / dos_plateau
        dos[frac_plateau] = dn_frac_plateau / dos_frac_plateau
        dmu_vec = 1. / dos

        mu = sp.integrate.cumtrapz(dmu_vec, dx=dn, initial=0.)
        mu -= mu[np.argmin(np.abs(n))]
        mu = sp.interpolate.interp1d(n, mu)
        dmu = sp.interpolate.interp1d(n, dmu_vec)
        E_int = sp.integrate.cumtrapz(mu(n), dx=dn, initial=0.)
        E_int -= E_int[np.argmin(np.abs(n))]
        E_int = sp.interpolate.interp1d(n, E_int)
        self.dmu = dmu
        self.mu = mu
        self.E_int = E_int

    

