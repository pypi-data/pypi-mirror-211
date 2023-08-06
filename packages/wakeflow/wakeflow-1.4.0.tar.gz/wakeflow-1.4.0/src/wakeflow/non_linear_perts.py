# non_linear_perts.py
# Written by Thomas Hilder, Daniele Fasano and Francesco Bollati

"""
Contains the NonLinearPerts class responsible for handling the non-linear regime of the models.
"""

# type hinting without circular imports
from typing import          TYPE_CHECKING

import time
import numpy                    as np
import matplotlib.pyplot        as plt
from scipy.interpolate      import griddata
from copy                   import copy
from tqdm                   import tqdm
from .burgers               import _solve_burgers
from .transformations       import _Eta, _t, _get_chi, _get_dens_vel, _plot_r_t, _t_vector, _get_chi_vector

if TYPE_CHECKING:
    from .model_setup       import _Parameters
    from .grid              import _Grid
    from .linear_perts      import _LinearPerts

# NOTE: contents are intended for internal use and should not be directly accessed by users

# class for non-linear regime results
class _NonLinearPerts():
    """
    Class to store the results from the non-linear wake propagation away from the planet.
    """

    # intialise object, give params and grid
    def __init__(self, parameters: '_Parameters', Grid: '_Grid') -> None:
        """Setup _NonLinearPerts object by grabbing _Parameters and _Grid objects.
        """
        
        # grab parameters object
        self.p = parameters

        # should be handed an empty grid with the correct dimensions and grid setup used in the run
        self.g = Grid

    # get initial conditions for burgers eqn
    def _extract_ICs(self, LinearPerts: '_LinearPerts') -> None:
        """Extract the initial conditions for the non-linear evolution from the linear regime.
        """
        
        # grab linear perturbations object
        lp = LinearPerts

        # grid
        x = lp.X[0,:]
        y = lp.Y[:,0]

        # set maximum eta - semi-width of the support of the azimuthal profile of the linear density perturbation
        eta_max = 25 

        # inner and outer wake x position
        x_box_outer =  lp.x_box_r
        x_box_inner = -lp.x_box_l

        # find the index in the x grid corresponding to the edge of the box
        index_outer = np.argmin(np.abs(x - x_box_outer))
        index_inner = np.argmin(np.abs(x - x_box_inner))

        # extract profile of constant x along edge of box for initial condition
        profile_outer = lp.pert_rho[:,index_outer] / np.sqrt(np.abs(x_box_outer))
        profile_inner = lp.pert_rho[:,index_inner] / np.sqrt(np.abs(x_box_inner))

        # restrict y range --- I'm not sure why this is necessary but it is. Larger values will cause issues
        y_max = 30
        y_rest = y[(y > -y_max) & (y < y_max)]

        # restrict inner and outer IC
        profile_rest_outer = profile_outer[(y > -y_max) & (y < y_max)]
        profile_rest_inner = profile_inner[(y > -y_max) & (y < y_max)]

        # ## find eta points for IC profile using full transformation
        # find local cart. coords in real units
        x_IC_outer = self.p.l * np.repeat(x_box_outer, len(y_rest))
        y_IC_outer = self.p.l * y_rest
        x_IC_inner = self.p.l * np.repeat(x_box_inner, len(y_rest))
        y_IC_inner = self.p.l * y_rest

        # find corresponding global polar coords
        r_IC_outer   = x_IC_outer + self.p.r_planet
        r_IC_inner   = x_IC_inner + self.p.r_planet
        phi_IC_outer = y_IC_outer / self.p.r_planet
        phi_IC_inner = y_IC_inner / self.p.r_planet

        if False:
            plt.plot(phi_IC_outer, profile_rest_outer, label="outer")
            plt.plot(phi_IC_inner, profile_rest_inner, label="inner")
            plt.legend(loc="best")
            plt.show()

        # initialise arrays for corresponding t,eta points
        eta_IC_outer = np.zeros(len(y_rest))
        eta_IC_inner = np.zeros(len(y_rest))
        t_IC_outer   = np.zeros(len(y_rest))
        t_IC_inner   = np.zeros(len(y_rest))

        # perform transformation
        for i in range(len(y_rest)):

            # eta for outer and inner
            eta_IC_outer[i] = _Eta(r_IC_outer[i], phi_IC_outer[i], self.p.r_planet, self.p.hr_planet, self.p.q, -1)
            eta_IC_inner[i] = _Eta(r_IC_inner[i], phi_IC_inner[i], self.p.r_planet, self.p.hr_planet, self.p.q, -1)

            # t for outer and inner
            t_IC_outer[i] = _t(r_IC_outer[i], self.p.r_planet, self.p.hr_planet, self.p.q, self.p.p)
            t_IC_inner[i] = _t(r_IC_inner[i], self.p.r_planet, self.p.hr_planet, self.p.q, self.p.p)

        # restrict eta range using eta_max
        self.eta_outer = eta_IC_outer[(eta_IC_outer > -eta_max) & (eta_IC_outer < eta_max)]
        self.eta_inner = eta_IC_inner[(eta_IC_inner > -eta_max) & (eta_IC_inner < eta_max)]
        self.profile_outer = profile_rest_outer[(eta_IC_outer > -eta_max) & (eta_IC_outer < eta_max)]
        self.profile_inner = profile_rest_inner[(eta_IC_inner > -eta_max) & (eta_IC_inner < eta_max)]

        # set t0
        self.t0_outer = t_IC_outer[0]
        self.t0_inner = t_IC_inner[0]

        # old, approximate IC extraction procedure
        if False:
            y_match = -np.sign(lp.x_box) * 0.5 * lp.x_box**2
            y_cut = y[(y - y_match > -eta_max) & (y - y_match < eta_max)]
            self.profile = profile[(y - y_match > -eta_max) & (y - y_match < eta_max)]
            self.eta = y_cut - y_match*np.ones(len(y_cut))
            self.t0 = _t(self.p.r_planet + self.p.l * lp.x_box, self.p.r_planet, self.p.hr, self.p.q, self.p.p)

        # set eta_tilde for outer wake:
        for i in range(len(self.eta_outer)):
            if self.profile_outer[i] == 0 and self.eta_outer[i] > -10 and self.eta_outer[i] < 0:
                zero_outer = self.eta_outer[i]
            elif i!= (len(self.eta_outer) - 1) and self.profile_outer[i] * self.profile_outer[i + 1] < 0 and self.eta_outer[i] > -10 and self.eta_outer[i] < 0:
                zero_outer = 0.5 * (self.eta_outer[i] + self.eta_outer[i + 1])
        self.eta_tilde_outer = -zero_outer

        # set eta_tilde for inner wake:
        for i in range(len(self.eta_inner)):
            if self.profile_inner[i] == 0 and self.eta_inner[i] > -10 and self.eta_inner[i] < 0:
                zero_inner = self.eta_inner[i]
            elif i!= (len(self.eta_inner) - 1) and self.profile_inner[i] * self.profile_inner[i + 1] < 0 and self.eta_inner[i] > -10 and self.eta_inner[i] < 0:
                zero_inner = 0.5 * (self.eta_inner[i] + self.eta_inner[i + 1])
        self.eta_tilde_inner = -zero_inner

        # set C for outer wake:
        deta_outer = self.eta_outer[1] - self.eta_outer[0]
        profile0_outer = self.profile_outer[self.eta_outer < -self.eta_tilde_outer]
        C0_outer = -np.trapz(profile0_outer, dx = deta_outer)
        self.C_outer = (self.p.gamma + 1) * (self.p.m_planet / self.p.m_thermal) * C0_outer / 2**(3/4)

        # set C for inner wake:
        deta_inner = self.eta_inner[1] - self.eta_inner[0]
        profile0_inner = self.profile_inner[self.eta_inner < -self.eta_tilde_inner]
        C0_inner = -np.trapz(profile0_inner, dx = deta_inner)
        self.C_inner = (self.p.gamma + 1) * (self.p.m_planet / self.p.m_thermal) * C0_inner / 2**(3/4)

        #print('     Outer Wake:')
        #print('         eta_tilde = ', self.eta_tilde_outer)
        #print('         C0 = ', C0_outer)
        #print('         t0 = ', self.t0_outer)
        #print('     Inner Wake:')
        #print('         eta_tilde = ', self.eta_tilde_inner)
        #print('         C0 = ', C0_inner)
        #print('         t0 = ', self.t0_inner)

        # ======================================
        # === put linear solution into t,eta ===

        # you will need to run cut_box_square on the linear perts object before doing this.
        # it is okay to run it as well as the annulus cut, they don't overwrite each other

        beta_p = self.p.m_planet / self.p.m_thermal
        gamma  = self.p.gamma

#        if self.p.show_teta_debug_plots:
#
#            index = index_outer
#
#            # run square box cut
#            lp._cut_box_square()
#
#            # plot r, t
#            _plot_r_t(self.p)
#
#            # Local Cartesian grid which the linear solution was calculated on, meshgrid version
#            X, Y = np.meshgrid(lp.x_cut,lp.y_cut)
#
#            print("Y MIN MAX", np.min(Y),np.max(Y))
#
#            # grab positive x side of linear solution
#            x_len = len(lp.x_cut) // 2
#
#            # restrict box to area considered
#            X_rest = X[:,x_len:index]
#            Y_rest = Y[:,x_len:index]
#
#            print("Y MIN MAX", np.min(Y_rest),np.max(Y_rest))
#
#            # Find chi for linear solution, only taking positive values of x
#            # The "index" value also makes it so we do not go outside the linear box
#            linear_profile = lp.cut_rho[:,x_len:index] / np.sqrt(np.abs(X_rest)) ###
#            chi0_rho = linear_profile[:,-1]  * (gamma+1) * beta_p / 2**(3/4) 
#
#            # extract chi from velocity perturbations
#            v_unit = (self.p.c_s_planet*(self.p.m_planet/self.p.m_thermal))
#            Rp     = self.p.r_planet
#            cw     = -self.p.a_cw
#            hr     = self.p.hr_planet
#            q      = self.p.q
#            gamma  = self.p.gamma
#            csp    = self.p.c_s_planet
#            p      = self.p.p
#            l      = self.p.l
#            linear_profile_v_r   = v_unit * (lp.cut_v_r[:,x_len:index]   / np.sqrt(np.abs(X_rest))) ###
#            linear_profile_v_phi = v_unit * (lp.cut_v_phi[:,x_len:index] / np.sqrt(np.abs(X_rest))) ###
#            R0  = np.sqrt((Rp + l*X_rest[:,-1])**2 + (l*Y_rest[:,-1])**2)
#            Lfu = _Lambda_fu(R0, Rp, csp, hr, gamma, q, p)
#            Lfv = _Lambda_fv(R0, Rp, csp, hr, gamma, q, p)
#            chi0_v_r = linear_profile_v_r[:,-1] / (np.sign(R0 - Rp) * Lfu)
#            chi0_v_phi = linear_profile_v_phi[:,-1] / (np.sign(R0 - Rp) * Lfv * (-cw))
#
#            # Find etas for the box using IC method
#            linear_eta = Y_rest + np.sign(X_rest) * 0.5 * X_rest**2
#
#            # Find etas using proper transformations
#            #hp = self.p.hr * self.p.r_planet
#            hp = self.p.hr_planet * self.p.r_planet
#            x_glob = 2 * hp * X_rest / 3.
#            y_glob = 2 * hp * Y_rest / 3.
#            r_glob = x_glob + self.p.r_planet
#            phi_glob = y_glob / self.p.r_planet
#            eta_lin = np.zeros(linear_profile.shape)
#            t_lin = np.zeros(linear_profile.shape)
#            for i in range(eta_lin.shape[0]):
#                #print(str(i))
#                for j in range(eta_lin.shape[1]):
#                    eta_lin[i,j] = _Eta(r_glob[i,j], phi_glob[i,j], self.p.r_planet, self.p.hr_planet, self.p.q, -self.p.a_cw)
#                    t_lin[i,j] = _t(r_glob[i,j], self.p.r_planet, self.p.hr_planet, self.p.q, self.p.p)
#
#            # Plot Chi vs eta when using eta transformation used for IC cut out
#
#            #for i in range(0, len(linear_eta[0,:]), 10):
#            #    plt.plot(linear_eta[:,i], linear_profile[:,i])
#            #    plt.plot(eta_lin[:,i], linear_profile[:,i])
#            #    plt.show()
#
#            plt.plot(eta_lin[:,-1], chi0_rho, label="chi rho")
#            plt.plot(eta_lin[:,-1], chi0_v_r, label="chi vr")
#            plt.plot(eta_lin[:,-1], chi0_v_phi, label="chi vphi")
#            plt.legend(loc="lower left")
#            plt.xlim(-10,10)
#            plt.xlabel('$\eta$')
#            plt.ylabel('$\chi$')
#            plt.show()
#
#            if True: # save results to file for plotting
#
#                name = "sim_further"
#                eta_save = eta_lin[:,-1]
#                chi_save = np.array([chi0_rho, chi0_v_r, chi0_v_phi])
#                np.save(f"{name}_eta.npy", eta_save)
#                np.save(f"{name}_chi.npy", chi_save)
#
#            plt.plot(linear_eta[:,-1], linear_profile[:,-1], label="Approximate $\eta$ transformation")
#            plt.plot(eta_lin[:,-1], linear_profile[:,-1], label="Full $\eta$ transformation")
#            plt.plot(self.eta, self.profile, ls='--', label="Actual IC used")
#            plt.legend(loc="lower left")
#            plt.xlim(-10,10)
#            plt.xlabel('$\eta$')
#            plt.ylabel('$\chi$')
#            plt.show()
#
#            plt.scatter(t_lin, eta_lin)
#            plt.show()
#
#            #eta_lin = linear_eta    ### TURN THIS ON AND OFF TO CHANGE ETA TRANSFORMATION --> COMMENT OUT TO USE INTEGRAL TRANSFORM
#
#            # get grid regular in (t,eta) to interpolate onto
#            dt_lin = np.diff(np.sort(t_lin.flatten())).mean()       # find time step interval to use on regular grid from t_lin
#                                                                    # takes minimum separation between points in original t_lin grid
#            t_lin_reg = np.arange(0, self.t0, dt_lin)
#            eta_lin_reg = copy(self.eta)
#            T_lin_reg, ETA_lin_reg = np.meshgrid(t_lin_reg, eta_lin_reg)
#
#            # interpolate solution over irregular grid onto regular grid
#            print("Interpolating Linear solution into (t, eta) space")
#            lin_solution = griddata(
#                (t_lin.flatten(), eta_lin.flatten()), 
#                linear_profile.flatten(),
#                (T_lin_reg, ETA_lin_reg),
#                method='linear'
#            )
#
#            #plt.plot(linear_eta[:,-1], linear_profile[:,-1])       # approx
#            plt.plot(eta_lin[:,-1], linear_profile[:,-1])           # integral trans
#            plt.plot(eta_lin_reg, lin_solution[:,-1])               # interpolated integral trans
#            #plt.plot(self.eta, self.profile, c='k')                # IC
#            plt.show()
#
#            # plotting (for debugging)
#            _, ax = plt.subplots()
#            myplot = ax.contourf(t_lin_reg, eta_lin_reg, np.nan_to_num(lin_solution), levels=np.arange(-4,4,0.1), cmap='RdBu', extend='both')
#            plt.colorbar(myplot)
#            plt.show()
#
#            # stick this into the solutions array, update later code so that solutions array builds on this one
#            self.linear_solution = np.nan_to_num(lin_solution)
#            self.linear_t = t_lin_reg
#
#        else:
            
        self.linear_solution = 0
        self.linear_t = 0

    # alternative IC extraction using edge of box
    def _extract_ICs_ann(self, LinearPerts: '_LinearPerts') -> None:
        """Alternate initial condition extraction where the IC is read from the edges of the box as included in the final
        solution. Usually, far more y-extent of the linear regime is used than this. Using this method will invalidate the
        solution and is meant for developer use only.
        """
        
        # grab linear perturbations object
        lp = LinearPerts

        # mass unit
        beta_p = self.p.m_planet / self.p.m_thermal

        # grab radius and phi values for edge of box
        phi_IC_outer = lp.PHI_ann[:,-1]
        phi_IC_inner = lp.PHI_ann[:,0]
        r_IC_outer   = lp.r_ann[-1]
        r_IC_inner   = lp.r_ann[ 0]

        # edge of box in local coords
        x_box_outer = (r_IC_outer - self.p.r_planet) / self.p.l
        x_box_inner = (r_IC_inner - self.p.r_planet) / self.p.l

        self.profile_outer = (lp.pert_rho_ann[:,-1] / beta_p) / np.sqrt(np.abs(x_box_outer))
        self.profile_inner = (lp.pert_rho_ann[:, 0] / beta_p) / np.sqrt(np.abs(x_box_inner))

        if False:
         plt.plot(phi_IC_outer, self.profile_outer, label="outer")
         plt.plot(phi_IC_inner, self.profile_inner, label="inner")
         plt.legend(loc="best")
         plt.show()

        # find t points
        t_IC_outer = _t(r_IC_outer, self.p.r_planet, self.p.hr_planet, self.p.q, self.p.p)
        t_IC_inner = _t(r_IC_inner, self.p.r_planet, self.p.hr_planet, self.p.q, self.p.p)

        # initialise arrays for corresponding eta points
        self.eta_outer = np.zeros(len(phi_IC_outer))
        self.eta_inner = np.zeros(len(phi_IC_outer))

        # perform transformation
        for i in range(len(phi_IC_outer)):
            self.eta_outer[i] = _Eta(r_IC_outer, phi_IC_outer[i], self.p.r_planet, self.p.hr_planet, self.p.q, -1)
            self.eta_inner[i] = _Eta(r_IC_inner, phi_IC_inner[i], self.p.r_planet, self.p.hr_planet, self.p.q, -1)

        # set t0
        self.t0_outer = t_IC_outer
        self.t0_inner = t_IC_inner

        # set eta_tilde for outer wake:
        for i in range(len(self.eta_outer)):
            if self.profile_outer[i] == 0 and self.eta_outer[i] > -10 and self.eta_outer[i] < 0:
                zero_outer = self.eta_outer[i]
            elif i!= (len(self.eta_outer) - 1) and self.profile_outer[i] * self.profile_outer[i + 1] < 0 and self.eta_outer[i] > -10 and self.eta_outer[i] < 0:
                zero_outer = 0.5 * (self.eta_outer[i] + self.eta_outer[i + 1])
        self.eta_tilde_outer = -zero_outer

        # set eta_tilde for inner wake:
        for i in range(len(self.eta_inner)):
            if self.profile_inner[i] == 0 and self.eta_inner[i] > -10 and self.eta_inner[i] < 0:
                zero_inner = self.eta_inner[i]
            elif i!= (len(self.eta_inner) - 1) and self.profile_inner[i] * self.profile_inner[i + 1] < 0 and self.eta_inner[i] > -10 and self.eta_inner[i] < 0:
                zero_inner = 0.5 * (self.eta_inner[i] + self.eta_inner[i + 1])
        self.eta_tilde_inner = -zero_inner

        # set C for outer wake:
        deta_outer = self.eta_outer[1] - self.eta_outer[0]
        profile0_outer = self.profile_outer[self.eta_outer < -self.eta_tilde_outer]
        C0_outer = -np.trapz(profile0_outer, dx = deta_outer)
        self.C_outer = (self.p.gamma + 1) * (self.p.m_planet / self.p.m_thermal) * C0_outer / 2**(3/4)

        # set C for inner wake:
        deta_inner = self.eta_inner[1] - self.eta_inner[0]
        profile0_inner = self.profile_inner[self.eta_inner < -self.eta_tilde_inner]
        C0_inner = -np.trapz(profile0_inner, dx = deta_inner)
        self.C_inner = (self.p.gamma + 1) * (self.p.m_planet / self.p.m_thermal) * C0_inner / 2**(3/4)

        #print('     Outer Wake:')
        #print('         eta_tilde = ', self.eta_tilde_outer)
        #print('         C0 = ', C0_outer)
        #print('         t0 = ', self.t0_outer)
        #print('     Inner Wake:')
        #print('         eta_tilde = ', self.eta_tilde_inner)
        #print('         C0 = ', C0_inner)
        #print('         t0 = ', self.t0_inner)

        # hard to explain, but they're not needed so set to zero
        self.linear_solution = 0
        self.linear_t = 0

    # propagate the wake using IC
    def _get_non_linear_perts(self) -> None:
        """Calculate the perturbations in the non-linear regime by propagating the wake away from the planet
        by solving Burger's eqn and then transforming the results to physical coordinates.
        """

        beta_p = self.p.m_planet / self.p.m_thermal

        print('Propagating outer wake... ')

        timer_0 = time.perf_counter()

        time_outer, eta_outer, solution_outer = _solve_burgers(
            self.eta_outer, 
            self.profile_outer, 
            self.p.gamma, 
            beta_p, 
            self.C_outer, 
            self.p.CFL, 
            self.eta_tilde_outer, 
            self.t0_outer, 
            self.linear_solution, 
            self.linear_t, 
            self.p.show_teta_debug_plots,
            self.p.tf_fac,
        )

        timer_1 = time.perf_counter()

        print(f'Completed in {timer_1-timer_0:0.2f} s')

        print('Propagating inner wake... ')

        timer_0 = time.perf_counter()

        time_inner, eta_inner, solution_inner = _solve_burgers(
            self.eta_inner, 
            -self.profile_inner,     # this minus sign is intended
            self.p.gamma, 
            beta_p, 
            self.C_inner, 
            self.p.CFL, 
            self.eta_tilde_inner, 
            self.t0_inner, 
            self.linear_solution, 
            self.linear_t, 
            self.p.show_teta_debug_plots,
            self.p.tf_fac
        )

        timer_1 = time.perf_counter()

        print(f'Completed in {timer_1-timer_0:0.2f} s')

        # final time of solutions before N-wave behaviour
        tf_outer = time_outer[-1]
        tf_inner = time_inner[-1]

        # needed constants from solutions, inner and outer
        eta_tilde_outer = self.eta_tilde_outer
        eta_tilde_inner = self.eta_tilde_inner
        C_outer         = self.C_outer
        C_inner         = self.C_inner
        t0_outer        = self.t0_outer
        t0_inner        = self.t0_inner

        # parameters of run
        Rp      = self.p.r_planet
        x_match_l = 2*self.p.scale_box_l
        x_match_r = 2*self.p.scale_box_r
        l       = self.p.l
        cw      = -self.p.a_cw
        hr      = self.p.hr_planet
        q       = self.p.q
        csp     = self.p.c_s_planet
        p       = self.p.p

        # physical parameters
        gamma = self.p.gamma


        # if using a Cartesian grid

        timer_0 = time.perf_counter()

        if self.g.info["Type"] == "cartesian":
            print("Mapping to Physical Coords")

            x = self.g.x 
            y = self.g.y

            [x_grid, y_grid] = np.meshgrid(x, y)
            r_grid = np.sqrt(x_grid**2 + y_grid**2)
            pphi_grid = np.arctan2(y_grid, x_grid) - self.p.phi_planet

            tt = _t_vector(r_grid, Rp, hr, q, p)

            CChi = _get_chi_vector(
                pphi_grid, 
                r_grid,
                tt,
                time_outer,
                time_inner, 
                eta_outer, 
                eta_inner, 
                eta_tilde_outer,
                eta_tilde_inner, 
                C_outer,
                C_inner, 
                solution_outer, 
                solution_inner, 
                t0_outer,
                t0_inner, 
                tf_outer,
                tf_inner, 
                Rp, 
                x_match_l,
                x_match_r,
                l, 
                cw, 
                hr, 
                q, 
                p,
            )

            # COMPUTE DENSITY AND VELOCITY PERTURBATIONS
            dnl, unl, vnl = _get_dens_vel(
                np.transpose(r_grid), 
                np.transpose(CChi), 
                gamma, 
                Rp, 
                cw, 
                csp, 
                hr, 
                q, 
                p,
                self.p.use_old_vel
            )

        # if using a cylindrical grid
        else:
            r = self.g.r
            phi = self.g.phi - self.p.phi_planet

            r_grid, pphi_grid = np.meshgrid(r, phi)

            tt = _t_vector(r_grid, Rp, hr, q, p)

            Chi = _get_chi_vector(
                pphi_grid, 
                r_grid, 
                tt,
                time_outer,
                time_inner, 
                eta_outer, 
                eta_inner, 
                eta_tilde_outer,
                eta_tilde_inner, 
                C_outer,
                C_inner, 
                solution_outer, 
                solution_inner, 
                t0_outer,
                t0_inner, 
                tf_outer,
                tf_inner, 
                Rp, 
                x_match_l,
                x_match_r,
                l, 
                cw, 
                hr, 
                q, 
                p
            )

            # COMPUTE DENSITY AND VELOCITY PERTURBATIONS
            dnl, unl, vnl = _get_dens_vel(
                r_grid, 
                Chi, 
                gamma, 
                Rp, 
                cw, 
                csp, 
                hr, 
                q, 
                p,
                self.p.use_old_vel
            )
        
        timer_1 = time.perf_counter()
        print(f'Completed in {timer_1-timer_0:0.2f} s')

        self.rho = dnl
        self.vr = 1e-5*unl
        self.vphi = 1e-5*vnl
