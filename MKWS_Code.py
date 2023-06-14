import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
from sdtoolbox.postshock import CJspeed
from multiprocessing import Pool, cpu_count
import os

# Define a function to calculate CJ speed for a given set of parameters
def calculate_cj_speed(args):
    p, T, q, mech = args
    gas = ct.Solution(mech)
    gas.TPX = T, p, q
    cj_speed = CJspeed(p, T, q, mech)
    return cj_speed


# Specify the directory to save the plots
save_dir = 'D:\Studia\Semestr VII\MKWS\MKWS23\Results'

# Define input parameters
P1 = 100000  # Initial pressure [Pa]
Pmax = 1000000  # Maximum pressure [Pa]
T1 = 300  # Initial temperature [K]
Tmax = 1000  # Maximum temperature [K]
p_steps = 10  # Number of pressure steps
T_steps = 8  # Number of temperature steps
q = 'CH4:1.5 O2:2.0 N2:7.52'  # Composition
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
        plt.plot(np.linspace(P1/100000, Pmax/100000, p_steps), cj_speed[:, 2 * i], label='T = %.0f K' % T_array[2 * i])
    plt.xlabel('Pressure [bar]')
    plt.ylabel('CJ detonation speed [m/s]')
    plt.title('CJ Detonation Speed vs Pressure (Methane slightly rich)')
    plt.legend()

    # Save the plot as an image in the specified directory
    plt.savefig(os.path.join(save_dir, 'cj_speed_CH4_slightly_rich_pressure.png'))
    plt.close()

    # Plot CJ detonation speed vs. temperature
    plt.figure(figsize=(20, 10))
    for i in range(p_steps // 2):
        pbar = np.linspace(P1, Pmax, p_steps)
        plt.plot(T_array, cj_speed[2 * i, :], label='p = %.1f bar' % (pbar[2 * i]/100000))
    plt.xlabel('Temperature [K]')
    plt.ylabel('CJ detonation speed [m/s]')
    plt.title('CJ Detonation Speed vs Temperature (Methane slightly rich)')
    plt.legend()

    # Save the plot as an image in the specified directory
    plt.savefig(os.path.join(save_dir, 'cj_speed_CH4_slightly_rich_temperature.png'))
    plt.close()

    # HYDROGEN CALCULATIONS

    # Define hydrogen input parameters
    P1_h2 = 100000  # Initial pressure for hydrogen [Pa]
    Pmax_h2 = 1000000  # Maximum pressure for hydrogen [Pa]
    T1_h2 = 300  # Initial temperature for hydrogen [K]
    Tmax_h2 = 1000  # Maximum temperature for hydrogen [K]
    p_steps_h2 = 10  # Number of pressure steps for hydrogen
    T_steps_h2 = 8  # Number of temperature steps for hydrogen
    q_h2 = 'H2:3.0 O2:1.0 N2:3.76'  # Composition for hydrogen
    mech = 'gri30.cti'  # Mechanism file

    # Generate a new list of arguments for the hydrogen-air case
    args_h2 = [(p, T, q_h2, mech) for p in np.linspace(P1_h2, Pmax_h2, p_steps_h2) for T in np.linspace(T1_h2, Tmax_h2, T_steps_h2)]

    # Create a new multiprocessing pool for hydrogen calculations
    pool_h2 = Pool(processes=cpu_count())

    # Calculate CJ speeds for each set of parameters for hydrogen-air
    cj_speed_h2 = np.array(pool_h2.map(calculate_cj_speed, args_h2)).reshape((p_steps_h2, T_steps_h2))

    # Close the pool of processes for hydrogen calculations
    pool_h2.close()
    pool_h2.join()

    # Output CJ speeds for hydrogen-air
    print('CJ computation for Hydrogen with composition ' + q_h2)
    print('CJ speed:\n', np.round(cj_speed_h2, 1), '(m/s)')

    # Plot CJ detonation speed vs. pressure for hydrogen-air
    plt.figure(figsize=(20, 10))
    for i in range(T_steps_h2 // 2):
        T_array_h2 = np.linspace(T1_h2, Tmax_h2, T_steps_h2)
        plt.plot(np.linspace(P1_h2/100000, Pmax_h2/100000, p_steps_h2), cj_speed_h2[:, 2 * i], label='T = %.0f K' % T_array_h2[2 * i])
    plt.xlabel('Pressure [bar]')
    plt.ylabel('CJ detonation speed [m/s]')
    plt.title('CJ Detonation Speed vs Pressure (Hydrogen slightly rich)')
    plt.legend()

    # Save the plot as an image in the specified directory
    plt.savefig(os.path.join(save_dir, 'cj_speed_H2_slightly_rich_pressure.png'))
    plt.close()

    # Plot CJ detonation speed vs. temperature for hydrogen-air
    plt.figure(figsize=(20, 10))
    for i in range(p_steps_h2 // 2):
        pbar_h2 = np.linspace(P1_h2, Pmax_h2, p_steps_h2)
        plt.plot(T_array_h2, cj_speed_h2[2 * i, :], label='p = %.1f bar' % (pbar[2 * i]/100000))
    plt.xlabel('Temperature [K]')
    plt.ylabel('CJ detonation speed [m/s]')
    plt.title('CJ Detonation Speed vs Temperature (Hydrogen slightly rich)')
    plt.legend()

    # Save the plot as an image in the specified directory
    plt.savefig(os.path.join(save_dir, 'cj_speed_H2_slightly_rich_temperature.png'))
    plt.close()

