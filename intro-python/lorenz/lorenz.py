from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy import integrate
import multiprocessing as mp
from functools import partial

SIGMA    = 10.0
BETA     = 8/3
RHO      = 28
max_time = 20.0
N        = 20
PROCS    = 1

def lorenz_deriv(t0,x_y_z,sigma,beta,rho):
    """Compute the time-derivative of a Lorenz system."""
    x, y, z = x_y_z
    return np.r_[sigma * (y - x), x * (rho - z) - y, x * y - beta * z]

def mysolve(t,x0,sigma=SIGMA,beta=BETA,rho=RHO):
    RHS = lambda t,x: lorenz_deriv(t,x,sigma,beta,rho)
    ts  = np.r_[t[[0,-1]]]
    x=integrate.solve_ivp(RHS,ts,x0,method='RK23',t_eval=t)
    return x 

#def solve_lorenz(sigma=SIGMA, beta=BETA, rho=RHO, procs=PROCS):
def solve_lorenz(sigma=SIGMA, beta=BETA, rho=RHO): #, procs=PROCS):
    """Plot a solution to the Lorenz differential equations."""
    ts = np.r_[0,max_time]

    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1], projection='3d')
    ax.axis('off')

    # prepare the axes limits
    ax.set_xlim((-25, 25))
    ax.set_ylim((-35, 35))
    ax.set_zlim((5, 55))
    
    # Choose random starting points, uniformly distributed from -15 to 15
    np.random.seed(1)
    x0 = 15 * ( 2 * np.random.random((N, 3)) - 1 )

    # Solve for the trajectories
    t = np.linspace(0, max_time, int(250*max_time))

    Pool= mp.Pool(processes=PROCS)
    iXt = Pool.starmap(
        partial(mysolve,sigma=sigma,beta=beta,rho=rho),
        [(t,x0k) for x0k in x0]
    )
    Pool.terminate()
    
    # choose a different color for each trajectory
    colors = plt.cm.viridis(np.linspace(0, 1, N))
     
    X_t = []
    for k,ixt in enumerate(iXt):
        x_t = ixt.y
        lines = ax.plot(*x_t, '-', c=colors[k],lw=1.5)
        X_t.append(x_t)
    X_t = np.array(X_t)
    angle = 104
    ax.view_init(30, angle)
    plt.show()

    return t, X_t
