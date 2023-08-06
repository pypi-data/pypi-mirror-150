import numpy as np
import scipy as sp
from scipy import optimize
from scipy import interpolate
from scipy import integrate
import functools
import time
import copy

from scipy import fft

class TFdata(object):

    def __init__(self, pars):
        """
            Base class for representing the Thomas-Fermi calculation.
            Input dictionary pars encodes all the relevant parameters.

            L - system size
            dx, dy - mesh size

            l_B - default length scale in nm, only for the FQHE model

            d_t, d_b - distance (in nm) from 2DEG to top/bottom gates

            eps_xy, eps_z - anisotropic permitivities depending on the material
                filling the space between the 2DEG and gates.

            Ec - strength of the Coulomb term in eV
            a - lattice spacing

        """
              
        self.L = pars.setdefault('L', 20)
        self.dx = pars.setdefault('dx', 1) # don't change unless for the FQHE model
        self.dy = pars.setdefault('dy', 1) # don't change unless for the FQHE model

        self.l_B = pars.setdefault('l_B', 0.246) # default length scale in nm, only for the FQHE model

        self.x = np.arange(-self.L, self.L-1e-8, self.dx) + self.dx/2
        self.y = np.arange(-self.L, self.L-1e-8, self.dy) + self.dy/2
        self.Nx = len(self.x)
        self.Ny = len(self.y)
        self.X, self.Y = np.meshgrid(self.x, self.y)
        self.R2 = self.X**2 + self.Y**2

        if (self.Nx//4)*4 != self.Nx:
            raise ValueError('Wrong Nx, Ny.')

        self.d_t = pars.setdefault('d_t', 65)
        self.d_b = pars.setdefault('d_b', 35)
        self.d_t = self.d_t/self.l_B
        self.d_b = self.d_b/self.l_B


        # Make G

        self.eps = pars.setdefault('eps', 6.85)

        # Default values for hBN
        self.eps_z = pars.setdefault('eps_z', 3.)
        self.eps_xy = pars.setdefault('eps_xy', 6.6)

        # Default value for graphene
        self.Ec = pars.setdefault('Ec', 5.85)

        self.energy_scale = pars.setdefault('energy_scale', 1)

        # Default value for graphene
        self.a = pars.setdefault('a', 0.246)
        self.a = self.a/self.l_B

        self.dqx = np.pi*self.a/self.L
        self.dqy = np.pi*self.a/self.L
        self.qx, self.qy = np.meshgrid(np.arange(-np.pi*self.a/self.dx, np.pi*self.a/self.dx-1e-8, self.dqx), np.arange(-np.pi*self.a/self.dy, np.pi*self.a/self.dy-1e-8, self.dqy))

        self.Gq = self.Ec*self.screened_coulomb()/(2*self.L/self.a)**2

        self.Gq_g = self.screened_coulomb_gate()

        # Make convolution mask, default off, only for FQHE model

        self.S0 = np.exp(-self.R2/2)/(np.sum(np.exp(-self.R2))*self.dx*self.dy)

        self.Sq = (1 + 0*self.qx)/(self.dx*self.dy/self.a**2)

        self.Sq = self.Sq/(np.sum(self.Sq)*self.dqx*self.dqy)

        self.n_lower = pars.setdefault('n_lower', None)
        self.n_upper = pars.setdefault('n_upper', None)

    def logsinh(self, x, oflow = 1e25):

            xflat = x.reshape((-1,))
            mask = xflat<np.log(oflow)

            ans = xflat - np.log(2)
            ans[mask] = np.log(np.sinh(xflat[mask]))

            return ans.reshape((self.Nx,self.Ny))

    def screened_coulomb(self):
        """
            Construct the screened Coulomb matrix in momentum space for self.Gq
        """

        Q = (self.qx,self.qy)
        D = (self.d_t + self.d_b)/2/self.a

        epsf = np.sqrt(self.eps_xy / self.eps_z)

        smear = 10 # in a
        Q = np.linalg.norm(Q, axis = 0)
        # ans = 4*np.pi*np.sinh(self.d_t/self.a*Q*epsf)*np.sinh(self.d_b/self.a*Q*epsf)/np.sinh(2*D*Q*epsf)/Q

        s1 = self.logsinh(self.d_t/self.a*Q*epsf)
        s2 = self.logsinh(self.d_b/self.a*Q*epsf)
        s3 = self.logsinh(2*D*Q*epsf)

        ans = 4*np.pi*np.exp(s1 + s2 - s3) / Q

        ans *= np.exp(-(Q*smear)**2/2.)
        ans[Q == 0] = 2*np.pi*D

        ans /= np.sqrt(self.eps_xy * self.eps_z)

        return ans

    def screened_coulomb_gate(self):
        """
            Construct the screened Coulomb potential from the gate in momentum space.
        """

        Q = (self.qx,self.qy)
        D = (self.d_t + self.d_b)/2/self.a

        epsf = np.sqrt(self.eps_xy / self.eps_z)

        Q = np.linalg.norm(Q, axis = 0)
        s2 = self.logsinh(self.d_b/self.a*Q*epsf)
        s3 = self.logsinh(2*D*Q*epsf)
        ans = np.exp(s2 - s3)

        return ans


class TF_engine(object):

    def __init__(self, pars):
        """
            Class for running the optimization.

            Input is a TFdata with desired parameters already set.

            New parameters are:
                n_iter - number of iterations to run for global optimizer (basinhopping)

        """

        self.TFdata = pars["TFdata"]

        self.L = self.TFdata.L

        self.Nx = self.TFdata.Nx
        self.Ny = self.TFdata.Ny

        self.dx = self.TFdata.dx
        self.dy = self.TFdata.dy

        self.X = self.TFdata.X
        self.Y = self.TFdata.Y

        self.E_int = self.TFdata.E_int
        self.Gq = self.TFdata.Gq
        self.mu = self.TFdata.mu
        self.T = self.TFdata.T

        self.Sq = self.TFdata.Sq
        self.Sq = self.Sq/self.make_n(self.init_n(eta = 0, uniform = True))[0]

        self.Phi_ext = pars['Phi_ext']

        self.energy_scale = self.TFdata.energy_scale

        self.n_lower = self.TFdata.n_lower
        self.n_upper = self.TFdata.n_upper

        self.n_iter = pars.setdefault('n_iter', 20)


    def make_n(self, n0):
        """
            Construct the (convolved) density n on the enlarged system from n
            given on the reduced system.
        """

        n = copy.deepcopy(n0)

        n = n.reshape((self.Nx//2, self.Ny//2))

        n = np.concatenate((n,n[::-1,:]), axis=0)
        n = np.concatenate((n,n[:,::-1]), axis=1)

        n = np.roll(np.roll(n, self.Nx//4, axis = 0), self.Ny//4, axis = 1)

        n = (fft.ifft2(fft.fftshift(self.Sq)*fft.fft2(fft.fftshift(n)))).reshape((-1,))

        return np.real(n)

    def E_tot(self, n):
        """
            Calculate the total energy for a given density configuration n
        """

        ns = self.make_n(n)
        E = np.vdot(ns*(self.dx*self.dy), 0.5*(fft.ifft2(fft.fftshift(self.Gq)*fft.fft2((ns).reshape((self.Nx,self.Ny))))).reshape((-1,)))*(2*self.L)**2
        E += np.dot(ns*(self.dx*self.dy), self.Phi_ext) + np.sum(self.E_int(ns))*(self.dx*self.dy)

        return np.real(E)/(2*self.L)**2*self.energy_scale

    def jac_E_tot(self, n):
        """
            Calcu late the gradient of the energy function for a given configuration n.
        """

        ns = self.make_n(n)

        jac_G = fft.fftshift(self.Gq)*np.conjugate(fft.fft2((ns*(self.dx*self.dy)).reshape((self.Nx,self.Ny))))
        jac_G = fft.ifft2(fft.fftshift(self.Sq)*jac_G)
        jac_G = np.roll(np.roll(jac_G, -1, axis = 0), -1, axis = 1)*(2*self.L)**2

        jac_ext = fft.fft2(((self.Phi_ext)*(self.dx*self.dy)).reshape((self.Nx,self.Ny)))
        jac_ext = fft.ifft2(fft.fftshift(self.Sq)*jac_ext)

        jac = fft.fft2(((self.mu(ns))*(self.dx*self.dy)).reshape((self.Nx,self.Ny)))
        jac = fft.ifft2(fft.fftshift(self.Sq)*jac)
        jac = jac[::-1,::-1]
        jac += jac_G + jac_ext

        jac = 4*jac[self.Nx//4:3*self.Nx//4,self.Ny//4:3*self.Ny//4]
        jac = jac.reshape((-1,))

        return np.ascontiguousarray(np.real(jac))/(2*self.L)**2*self.energy_scale

    def init_n(self, eta = 0.15, uniform = False, int_dot = False):
        """
            Helper function to prepare initial density configurations.
            If uniform, create a uniform \nu=1 state with noise eta
            Otherwise we initialize a noise \nu=0 and \nu=1 state under appropriate gates.
        """

        if uniform:
            n = (1 - eta) * (np.ones((self.Nx//2,self.Ny//2)) + eta * np.random.rand(self.Nx//2,self.Ny//2)).reshape((-1,))
        else:
            x = self.TFdata.X + 1e-8
            y = self.TFdata.Y + 1e-8
            n = 0.5 + 0.5*np.sign(x*y)[self.Nx//4:3*self.Nx//4, self.Ny//4:3*self.Ny//4]
            if int_dot:
                n *= ((x**2 + y**2) > 16)[self.Nx//4:3*self.Nx//4, self.Ny//4:3*self.Ny//4]
                n +=  ((x**2 + y**2) < 9)[self.Nx//4:3*self.Nx//4, self.Ny//4:3*self.Ny//4]
            n = n.reshape((-1,))
            n = (1 - eta) * n + eta * np.random.rand(len(n))

        return n

    def find_opt(self, n0 = [], n_iter = None, opt_factor = 1.):
        """
            Global optimization.
            Runs a (bounded) basinhopping optimizer for n_iter reps.
            Internally the global optimizer uses the L-BFGS-B local optimizer.
        """

        class MyBounds:

            def __init__(self, xmax=[1.1,1.1], xmin=[-1.1,-1.1] ):
                self.xmax = np.array(xmax)
                self.xmin = np.array(xmin)
            def __call__(self, **kwargs):
                x = kwargs["x_new"]
                tmax = bool(np.all(x <= self.xmax))
                tmin = bool(np.all(x >= self.xmin))
                return tmax and tmin

        if n_iter == None:
            n_iter = self.n_iter

        if len(n0) == 0:
            n = self.init_n()
        else:
            n = np.copy(n0)

        my_bounds = MyBounds(xmax=[self.n_upper for _ in n], xmin=[self.n_lower for _ in n])

        my_kwargs = {"method":"L-BFGS-B", "jac":self.jac_E_tot, "bounds":tuple([(self.n_lower,self.n_upper) for _ in n])}

        start_time = time.time()

        self.opt_engine = optimize.basinhopping(self.E_tot, n, minimizer_kwargs = my_kwargs, niter = n_iter, T = self.T, accept_test = my_bounds)

        end_time = time.time()

        n = self.opt_engine['x']

        print(f"opt time = {np.round(end_time - start_time)} s")

        return n

    def find_local_opt(self, n0=[]):
        """
            Local optimization.
            Runs a (bounded) L-BFGS-B optimizer.
        """
        if len(n0) == 0:
            n = self.init_n()
        else:
            n = np.copy(n0)

        my_bounds = tuple([(self.n_lower, self.n_upper) for _ in n])

        start_time = time.time()

        self.opt_engine = optimize.minimize(self.E_tot, n, method='L-BFGS-B', jac=self.jac_E_tot, bounds=my_bounds)

        end_time = time.time()

        n = self.opt_engine['x']

        print(f"opt time = {np.round(end_time - start_time)} s")

        return n