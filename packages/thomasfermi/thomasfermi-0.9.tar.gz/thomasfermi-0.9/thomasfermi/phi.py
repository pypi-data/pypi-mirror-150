import numpy as np
from scipy import fft

class make_Phi(object):

    def __init__(self, pars):
        """
            Parent class to construct the potential Phi_ext felt by the 2DEG due to the gates.
            Input is a TFdata that contains the calculation setup and device geometry.
        """

        self.TFdata = pars["TFdata"]

        self.L = self.TFdata.L

        self.Nx = self.TFdata.Nx
        self.Ny = self.TFdata.Ny

        if self.TFdata.l_B != None:
            self.l_B = self.TFdata.l_B
        else:
            self.l_B = 1

        self.X = self.TFdata.X
        self.Y = self.TFdata.Y

        self.d_t = self.TFdata.d_t
        self.d_b = self.TFdata.d_b

        self.Gq_g = self.TFdata.Gq_g

    def gate_to_ext(self, Phi_gate):
        """
            Converts the gate potential to the external potential.
        """

        if self.Phi_back == None:
            self.Phi_back = 0

        self.Phi_ext = self.Phi_back/(self.d_t+self.d_b)*self.d_t + np.real((fft.ifft2(fft.fftshift(self.Gq_g)*fft.fft2(self.Phi_gate))).reshape((-1,)))

        return True


class make_QPC_Phi(make_Phi):

    def __init__(self, pars):
        """
            Construct the potential Phi_ext felt by the 2DEG due to QPC gates.
            Input is a TFdata and additional parameters listed below:

            w_EW, w_NS - displacement from the center of the E/W and N/S gates.
            dn_NS, dn_EW - detuning of the potential on the corresponding pair of gates
            Phi_EW, Phi_NS - potential at which the corresponding gates are held
            Phi_back - potential at which the back gate is held
        """

        super().__init__(pars)

        self.w_EW = pars.setdefault('w_EW', 35)
        self.w_NS = pars.setdefault('w_NS', 35)
        self.w_EW = self.w_EW/self.l_B
        self.w_NS = self.w_NS/self.l_B

        self.dn_NS = pars.setdefault('dn_NS', 0)
        self.dn_EW = pars.setdefault('dn_EW', 0)

        self.Phi_EW = pars.setdefault('Phi_EW', -0.8)
        self.Phi_NS = pars.setdefault('Phi_NS', 0.2)
        self.Phi_back = pars.setdefault('Phi_back', -0.2)

        self.Phi_EW_ext = pars.setdefault('Phi_EW_ext', None)
        self.Phi_NS_ext = pars.setdefault('Phi_NS_ext', None)

        if self.Phi_EW_ext != None:
            self.Phi_EW = (self.Phi_EW_ext - self.d_t/(self.d_t + self.d_b)*self.Phi_back)/(self.d_b/(self.d_t + self.d_b))
            self.Phi_NS = (self.Phi_NS_ext - self.d_t/(self.d_t + self.d_b)*self.Phi_back)/(self.d_b/(self.d_t + self.d_b))

        self.Phi_gate = self.Phi_EW*(1+self.dn_EW)*(self.X < -self.w_EW)*(self.Y < -self.w_EW)*(self.X > -self.L + self.w_EW)*(self.Y > -self.L + self.w_EW) \
                + self.Phi_NS*(1+self.dn_NS)*(self.X > self.w_NS)*(self.Y < -self.w_NS)*(self.X < self.L - self.w_NS)*(self.Y > -self.L + self.w_NS) \
                + self.Phi_NS*(1-self.dn_NS)*(self.X < -self.w_NS)*(self.Y > self.w_NS)*(self.X > -self.L + self.w_NS)*(self.Y < self.L - self.w_NS) \
                + self.Phi_EW*(1-self.dn_EW)*(self.X > self.w_EW)*(self.Y > self.w_EW)*(self.X < self.L - self.w_EW)*(self.Y < self.L - self.w_EW)

        self.gate_to_ext(self.Phi_gate)

class make_uniform_Phi(make_Phi):

    def __init__(self, pars):
        """
            Construct the potential Phi_ext felt by the 2DEG due to a uniform gate.
            Input is a TFdata and additional parameters listed below:

            Phi_top - potential at which the top gate is held
            Phi_back - potential at which the back gate is held
        """

        super().__init__(pars)

        self.Phi_back = pars.setdefault('Phi_back', -0.2)
        self.Phi_top = pars.setdefault('Phi_top', 0)

        self.Phi_ext = self.Phi_back/(self.d_t+self.d_b)*self.d_t + self.Phi_top/(self.d_t+self.d_b)*self.d_b + 0*(self.X).reshape((-1,))

class make_gradient_Phi(make_Phi):

    def __init__(self, pars):
        """
            Construct the potential Phi_ext felt by the 2DEG due to a uniform gate.
            Input is a TFdata and additional parameters listed below:

            Phi_top - potential at which the top gate is held
            Phi_back - potential at which the back gate is held
        """
        super().__init__(pars)

        self.Phi_low = pars.setdefault('Phi_low', -0.8)
        self.Phi_high = pars.setdefault('Phi_high', 0.2)
        self.Phi_back = pars.setdefault('Phi_back', -0.2)

        self.Phi_low_ext = pars.setdefault('Phi_low_ext', None)
        self.Phi_high_ext = pars.setdefault('Phi_high_ext', None)

        if self.Phi_low_ext != None:
            self.Phi_low = (self.Phi_low_ext - self.d_t/(self.d_t + self.d_b)*self.Phi_back)/(self.d_b/(self.d_t + self.d_b))
            self.Phi_high = (self.Phi_high_ext - self.d_t/(self.d_t + self.d_b)*self.Phi_back)/(self.d_b/(self.d_t + self.d_b))

        self.Phi_ave = (self.Phi_low + self.Phi_high)/2
        self.Phi_diff = (self.Phi_high - self.Phi_low)/2
        
        self.Phi_gate = self.Phi_ave + self.Phi_diff*np.arange(-1,1,2/(self.Nx//2))*np.ones((self.Nx//2,1))

        self.Phi_gate = self.symmetrize_Phi(self.Phi_gate)

        self.gate_to_ext(self.Phi_gate)

    def symmetrize_Phi(self, Phi):

        Phi = np.concatenate((Phi,Phi[::-1,:]), axis=0)
        Phi = np.concatenate((Phi,Phi[:,::-1]), axis=1)

        Phi = np.roll(np.roll(Phi, self.Nx//4, axis = 0), self.Ny//4, axis = 1)

        return Phi