import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
from sdtoolbox.postshock import CJspeed

# Initial conditions
P1 = 100000
Pmax = 1000000
T1 = 300
Tmax = 1000
p_steps = 10
T_steps = 8
q = 'CH4:1.0 O2:2.0 N2:7.52'  # Composition of the mixture

mech = 'gri30.cti'
gas = ct.Solution(mech)

P = np.linspace(P1, Pmax, p_steps)  # Pressure range
pbar = P / 100000  # Pressure in bars

T_array = np.linspace(T1, Tmax, T_steps)  # Temperature range
cj_speed = np.zeros((p_steps, T_steps))  # Array to store CJ speeds

# Loop over pressure and temperature values
for i, p in enumerate(P):
    for j, T in enumerate(T_array):
        gas.TPX = T, p, q  # Set the gas state
        cj_speed[i, j] = CJspeed(p, T, q, mech)  # Compute CJ speed

print('CJ computation for ' + mech + ' with composition ' + q)
print('CJ speed:\n', np.round(cj_speed, 1), '(m/s)')

# Plot CJ detonation speed vs pressure
plt.figure(figsize=(20, 10))
for i in range(T_steps // 2):
    plt.plot(pbar, cj_speed[:, 2 * i], label='T = %.0f K' % T_array[2 * i])
plt.xlabel('Pressure [bar]')
plt.ylabel('CJ detonation speed [m/s]')
plt.title('CJ Detonation Speed vs Pressure')
plt.legend()
plt.show()

# Plot CJ detonation speed vs temperature
plt.figure(figsize=(20, 10))
for i in range(p_steps // 2):
    plt.plot(T_array, cj_speed[2 * i, :], label='p = %.1f bar' % pbar[2 * i])
plt.xlabel('Temperature [K]')
plt.ylabel('CJ detonation speed [m/s]')
plt.title('CJ Detonation Speed vs Temperature')
plt.legend()
plt.show()
