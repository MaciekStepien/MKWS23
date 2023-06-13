#"GOOD_T_P_Multicore"
import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
from sdtoolbox.postshock import CJspeed
from multiprocessing import Pool, cpu_count

# Define a function to calculate CJ speed for a given set of parameters
def calculate_cj_speed(args):
    p, T, q, mech = args
    gas = ct.Solution(mech)
    gas.TPX = T, p, q
    cj_speed = CJspeed(p, T, q, mech)
    return cj_speed

# Define input parameters
P1 = 100000  # Initial pressure [Pa]
Pmax = 1000000  # Maximum pressure [Pa]
T1 = 300  # Initial temperature [K]
Tmax = 1000  # Maximum temperature [K]
p_steps = 10  # Number of pressure steps
T_steps = 8  # Number of temperature steps
q = 'CH4:1.0 O2:2.0 N2:7.52'  # Composition
mech = 'gri30.cti'  # Mechanism file

# Generate the list of arguments for the multiprocessing calculation
args = [(p, T, q, mech) for p in np.linspace(P1, Pmax, p_steps) for T in np.linspace(T1, Tmax, T_steps)]

if __name__ == '__main__':
    # Create a multiprocessing pool with the number of available CPU cores
    pool = Pool(processes=cpu_count())

    # Use multiprocessing to calculate CJ speeds for each set of parameters
    cj_speed = np.array(pool.map(calculate_cj_speed, args)).reshape((p_steps, T_steps))

    # Close the pool of processes
    pool.close()
    pool.join()

    # Output CJ speeds
    print('CJ computation for ' + mech + ' with composition ' + q)
    print('CJ speed:\n', np.round(cj_speed, 1), '(m/s)')

    # Set the font for the plots
    font = {'family': 'DejaVu Sans', 'weight': 'normal', 'size': 18}
    plt.rc('font', **font)

    # Plot CJ detonation speed vs. pressure
    plt.figure(figsize=(20, 10))
    for i in range(T_steps // 2):
        T_array = np.linspace(T1, Tmax, T_steps)
        plt.plot(np.linspace(P1, Pmax, p_steps), cj_speed[:, 2 * i], label='T = %.0f K' % T_array[2 * i])
    plt.xlabel('Pressure [Pa]')
    plt.ylabel('CJ detonation speed [m/s]')
    plt.title('CJ Detonation Speed vs Pressure')
    plt.legend()
    plt.show()

    # Plot CJ detonation speed vs. temperature
    plt.figure(figsize=(20, 10))
    for i in range(p_steps // 2):
        pbar = np.linspace(P1, Pmax, p_steps)
        plt.plot(T_array, cj_speed[2 * i, :], label='p = %.1f bar' % pbar[2 * i])
    plt.xlabel('Temperature [K]')
    plt.ylabel('CJ detonation speed [m/s]')
    plt.title('CJ Detonation Speed vs Temperature')
    plt.legend()
    plt.show()
