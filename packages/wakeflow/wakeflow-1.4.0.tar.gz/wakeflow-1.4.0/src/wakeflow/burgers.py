# burgers.py
# Written by Thomas Hilder and Francesco Bollati

"""
Contains the solve_burgers function used in the wake non-linear propagation calculations.
"""

import numpy                as np
import matplotlib.pyplot    as plt

# NOTE: contents are intended for internal use and should not be directly accessed by users

# function to solve burgers equation as part of the non-linear propagation of the planet wake
def _solve_burgers(
    eta, 
    profile, 
    gamma, 
    beta_p, 
    C, 
    CFL, 
    eta_tilde, 
    t0, 
    linear_solution, 
    linear_t, 
    show_teta, 
    tf_fac
): 
    """Propagate the wake in (t,eta,chi) space by solving Eq. 10 from Bollati et al. 2021 using Godunov scheme.
    """

    # Eq. (15) Bollati et al. 2021
    profile = profile * (gamma + 1) * beta_p / 2**(3 / 4)
    deta    = eta[1] - eta[0]

    # time required to develop N-wave for betap = 1
    tf_th = 300 

    # time required to display N-wave for generic betap, Eq. (39) Rafikov 2002
    tf  = tf_th / beta_p 
    tf *= tf_fac

    # Eq. (18) Bollati et al. 2021
    eta_min = -eta_tilde - np.sqrt(2 * C * tf) - 3 
    eta_max = -eta_tilde + np.sqrt(2 * C * tf) + 3

    # extend the profile domain due to profile broadening during evolution 
    extr = eta[-1]

    while extr < eta_max:

        eta     = np.append(eta, eta[-1] + deta)
        profile = np.append(profile, 0)
        extr    = eta[-1]

        #if show_teta:
        #    linear_solution = np.append(profile, 0, axis=0)

    extr = eta[0]

    while extr > eta_min:

        eta     = np.insert(eta, 0, eta[0] - deta)
        profile = np.insert(profile, 0, 0)
        extr    = eta[0]

        #if show_teta:
        #    linear_solution = np.insert(linear_solution, 0, 0, axis=0)

    # number of centers
    Neta = len(eta)

    a = eta[0] - deta/2

    # cells edges
    x = np.zeros(Neta + 1) 
    for i in range(0, Neta + 1):
        x[i] = a + i * deta

    solution = [np.zeros((Neta), dtype=float)]
    time = [0]

    # linear solution as initial condition
    solution[0] = profile

    # define flux vector
    F = np.zeros(Neta + 1) #there is a flux at each cell edge

    # calculate flux according to Godunov scheme, vectorised
    def _NumericalFluxVector(uL, uR):
        """Calculate flux according to the Godunov scheme.
        """

        FL = 0.5 * uL**2
        FR = 0.5 * uR**2

        # compute the shock speed
        s = 0.5 * (uL + uR)

        # See "GodunovNumericalFlux".
        # This returns the same value without branching
        # through the if statements.
        return  (uL >= uR) * (
            (s > 0.0) * FL + (s <= 0.0) * FR
            ) + (uL < uR) * (
                (uL > 0.0) * (FL) +
                (uL <= 0.0) * (uR < 0.0) * FR
            )

    # initialise
    lapsed_time = 0
    counter     = 0

    # time integration
    while lapsed_time < tf:

        # increment
        counter += 1

        # time step calculation
        dt = min(deta * CFL / (max(abs(solution[-1])) + 1e-8), 0.02)

        # update time
        time.append(time[-1] + dt)
        lapsed_time += dt

        # compute the interior fluxes
        F[1:Neta] = _NumericalFluxVector(solution[-1][0:-1], solution[-1][1:])

        # compute the left boundary flux
        if solution[-1][0] < 0.0:
            uL = 2.0 * solution[-1][0] - solution[-1][1]
        else:
            uL = solution[0][0]

        uR   = solution[-1][0]
        F[0] = _NumericalFluxVector(uL, uR)

        # compute the right boundary flux
        if solution[-1][Neta - 1] > 0.0:
            uR = 2.0 * solution[-1][Neta - 1] - solution[-1][Neta - 2]
        else:
            uR = solution[0][Neta - 1]

        uL      = solution[-1][Neta - 1]
        F[Neta] = _NumericalFluxVector(uL, uR)

        solution.append(solution[-1][0:Neta] - dt / deta * (F[1:Neta+1] - F[0:Neta]))

    solution = np.array(solution).transpose()
    time     = np.array(time)

    # plot Fig. 3 Bollati et al. 2021
    #plt.plot(eta, solution[:,0], label = "$t=t_0+$ ")#+str(0*dt))
    #plt.plot(eta, solution[:,100], label = "$t=t_0+$ ")#+str(round(dt*Nt/10,2)))
    #plt.plot(eta, solution[:,200], label = "$t=t_0+$ ")#+str(round(dt*Nt/6,2)))
    #plt.plot(eta, solution[:,300], label = "$t=t_0+$ ")#+str(round(dt*Nt/3,2)))
    #plt.plot(eta, solution[:,400], label = "$t=t_0+$ ")#+str(round(T,2)))
    #plt.legend()
    #plt.xlabel(r"$\eta$")
    #plt.ylabel(r"$\chi(t,\eta)$")
    #plt.grid(True)
    #plt.title(r'$\chi$ "evolution" $r > r_p$')
    #plt.show()

    #if show_teta: # combining linear and non-linear solution and plotting
    #    
    #    # scale linear solution
    #    linear_solution = linear_solution * (gamma + 1) * beta_p / 2**(3 / 4)
    #
    #    # add linear solution in (t,eta) to non-linear solution array
    #    total_solution = np.concatenate((linear_solution, solution), axis=1)
    #    total_time     = np.concatenate((linear_t,        time + t0))
    #
    #    fig, ax = plt.subplots(1)
    #    cont = ax.contourf(total_time, eta, total_solution, levels=np.arange(-4, 4, 0.05), cmap='RdBu')
    #    for c in cont.collections:
    #        c.set_rasterized(True)
    #    plt.colorbar(cont, label='$\chi$')
    #    ax.set_xlim(0,10)
    #    ax.set_xlabel('$t$')
    #    ax.set_ylabel('$\eta$')
    #    #plt.savefig("teta_badjoin.pdf")
    #    plt.show()

    # The following will put the linear solution into returned solution for Chi
    #if False:
    #    Nt = np.shape(total_solution)[1]
    #
    #    solution_inner = np.zeros(total_solution.shape) # solution for r < Rp (and disc rotating counterclockwise)
    #    for i in range(Neta):
    #        for j in range(Nt):
    #            solution_inner[i,j] = total_solution[int(Neta-1-i),j]
    #
    #    eta_inner = - eta[::-1]
    #    return total_time, eta, total_solution, eta_inner, solution_inner

    return time, eta, solution
    