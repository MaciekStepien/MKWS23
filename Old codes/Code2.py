from SDToolbox import *
import cantera as ct
import numpy as np
from cantera import *
import matplotlib.pyplot as plt     # requirement for plots 
#%matplotlib inline
# without above line plots dont show up


P1 = 100000; P1atm = P1/one_atm;
T1 = 300;
q = 'H2:2 O2:1'
mech = 'h2air_highT.cti'

#Methane-Air
P1=one_atm; P1atm=P1/one_atm;
T1=300;
q='CH4:1 O2:1 N2:3.76';
mech = 'gri30_highT.cti';

 
[cj_speed,R2] = CJspeed(P1, T1, q, mech, 0);   

gas = PostShock_eq(cj_speed, P1, T1, q, mech)
Ps = gas.P/one_atm

print ' '
print 'CJ State'
gas()
Ps = gas.P/one_atm

print ' '
print 'For ' + q + ' with P1 = %.2f atm & T1 = %.2f K using ' % (P1atm,T1) + mech 
print 'CJ Speed is %.2f m/s' % cj_speed

print 'The CJ State is %.2f atm & %.2f K' % (Ps,gas.T)

[ae,af] = equilSoundSpeeds(gas)

print 'The sound speeds are: af = %.2f m/s & ae = %.2f m/s' % (af,ae)
print ' '
print 
print



T1=300;
q='CH4:1 O2:1 N2:3.76';
mech = 'gri30_highT.cti';

press = 100000
presses = np.zeros(15)
data = np.zeros(15)
dataiip = np.zeros(15)
dataiit = np.zeros(15)

for n in range(15):
    presses[n] = press/one_atm
    [cj_speed,R2] = CJspeed(press, T1, q, mech, 0);
    gas = PostShock_eq(cj_speed, press, T1, q, mech)
    data[n] = cj_speed
    dataiip[n] = gas.P
    dataiit[n] = gas.T
    press+=100000

    
print('%15s    %15s' % ('Pressure [atm]', 'CJ speed [m/s]'))
for i in range(15):
    print('%10.1f   %15.1f') % (presses[i], data[i])
#print data
print 

plt.plot(presses,data)
plt.ylabel('CJ speed [m/s]')
plt.xlabel('Pressure [atm]')
plt.ylim(0, 2200)
plt.show()

print
print

print('%15s    %15s    %15s' % ('Pressure [atm]', 'CJ state pressure [atm]', 'CJ state temperature [K]'))
for i in range(15):
    print('%10.1f   %15.1f              %15.1f') % (presses[i], dataiip[i]/one_atm, dataiit[i])

#print dataii
print
#print dataiit

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Pressure (atm)')
ax1.set_ylabel('CJ state pressure [atm]', color=color)
ax1.plot(presses, dataiip/one_atm, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('CJ state temperature [K]', color=color)  # we already handled the x-label with ax1
ax2.plot(presses, dataiit, color=color)
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_ylim(2100, 2200)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()


print

P1=100000
temp = 300
temps = np.zeros(15)
data = np.zeros(15)
dataiip = np.zeros(15)
dataiit = np.zeros(15)

for n in range(15):
    temps[n] = temp
    [cj_speed,R2] = CJspeed(P1, temp, q, mech, 0);
    gas = PostShock_eq(cj_speed, P1, temp, q, mech)
    data[n] = cj_speed
    dataiip[n] = gas.P
    dataiit[n] = gas.T
    temp+=100

    
print('%15s    %15s' % ('Temperature [K]', 'CJ speed [m/s]'))
for i in range(15):
    print('%10.1f   %15.1f') % (temps[i], data[i])    
    
    
#print data
print 

plt.plot(temps,data)
plt.ylabel('CJ speed [m/s]')
plt.xlabel('Temperature [K]')
plt.show()



print 
print
print

print('%15s    %15s    %15s' % ('Temperature [K]', 'CJ state pressure [atm]', 'CJ state temperature [K]'))
for i in range(15):
    print('%10.1f   %15.1f              %15.1f') % (temps[i], dataiip[i]/one_atm, dataiit[i])

print 
print

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Temperature (K)')
ax1.set_ylabel('CJ state pressure [atm]', color=color)
ax1.plot(temps, dataiip/one_atm, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('CJ state temperature [K]', color=color)  # we already handled the x-label with ax1
ax2.plot(temps, dataiit, color=color)
ax2.tick_params(axis='y', labelcolor=color)
#ax2.set_ylim(2100, 2200)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()
