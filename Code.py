import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
from sdtoolbox.postshock import CJspeed

P1 = 100000
Pmax = 1000000
T1 = 300
Tmax = 1000
p_steps = 10;
T_steps = 8;
q = 'CH4:1.0 O2:2.0 N2:7.52'

mech = 'gri30.cti'
gas = ct.Solution(mech)

P = np.zeros(p_steps);
pbar = np.zeros(p_steps);
T = np.zeros(T_steps);
cj_speed = np.zeros((p_steps, T_steps));

T_index = 0;
p_index = 0;

while p_index < p_steps:

    P[p_index] = P1+ p_index * (Pmax- P1) / (p_steps - 1);
    pbar[p_index] = P[p_index] / 100000;

    while T_index < T_steps:

        T[T_index] = T1 + T_index * (Tmax - T1) / (T_steps - 1)

        cj_speed[p_index, T_index] = CJspeed(P[p_index], T[T_index], q, mech);
        T_index += 1;

    p_index += 1;
    T_index = 0;

print('CJ computation for ' + mech + ' with composition ' + q)
print('CJ speed ' + str(np.round(cj_speed, 1)) + ' (m/s)')

font = {'family': 'DejaVu Sans',
        'weight': 'normal',
        'size': 18}

plt.rc('font', **font)

plt.figure(figsize=(20, 10))
for i in range(T_steps // 2):
    plt.plot(pbar, cj_speed[:, 2 * i ], label='T = %.0f K' % T[2 * i])
plt.xlabel('Preassure [bar]')
plt.ylabel('CJ detonation speed [m/s]')
plt.title("")
plt.legend()
plt.show()
# plt.savefig('CJU_p_T1var.png')

plt.figure(figsize=(20, 10))
for i in range(p_steps // 2):
    plt.plot(T, cj_speed[2 * i, :], label='p = %.1f bar' % pbar[2 * i])
plt.xlabel('Temperature [K]')
plt.ylabel('CJ detonation speed [m/s]')
plt.title("")
plt.legend()
plt.show()
# plt.savefig('CJU_T1_p1var.png')