import cantera as ct
import SDToolbox as sd
import matplotlib.pyplot as plt
import numpy as np

mech = 'gri30_highT.cti';
pressure_array = np.linspace(0.5,8,20)
temperature_array = np.linspace(300,1000,20)
conc = []

#initial conditions fos variable concentrations
P1=one_atm; P1atm=P1/one_atm;
T1=300;



T2 = []
P2 = []
speed = []

j = 0
#loop that iterate thrue concentrations
while j < 60:
    nH2 = 0.21 + float(j)/100
    nO2 = (1-nH2) /4.76
    nN2 = (1-nH2) *3.76/4.76
    X  =  'H2:'+str(nH2)+ ' ' + 'O2:'+str(nO2) + ' ' + 'N2:'+str(nN2)
    conc.append(nH2)
    [cj_speed,R2] = sd.CJspeed(P1, T1, X, mech, 0);
    gas = sd.PostShock_eq(cj_speed, P1, T1, X, mech)
    T2.append(gas.T)
    P2.append(gas.P/one_atm)
    speed.append(cj_speed)
    print "%f" % (conc[j])
    #print "%s; temperature: %f, pressure: %f, CJspeed: %f" % (X, T2[j], P2[j], speed[j])
    j = j + 1
    
plt.plot(conc,speed)
plt.xlabel('Concentration [%]')
plt.ylabel('C-J Speed [m/s]')
plt.show()

plt.plot(conc,P2)
plt.xlabel('Concentration [%]')
plt.ylabel('post-shock pressure [atm]')
plt.show()

plt.plot(conc,T2)
plt.xlabel('Concentration [%]')
plt.ylabel('post-shock temperature [K]')
plt.show()

#intial condidtions for variable initial pressure
T1 = 300
nH2 = 0.34
nO2 = (1-nH2) /4.76
nN2 = (1-nH2) *3.76/4.76
X  =  'H2:'+str(nH2)+ ' ' + 'O2:'+str(nO2) + ' ' + 'N2:'+str(nN2)

T2 = []
P2 = []
speed = []
for P1 in pressure_array:
    [cj_speed,R2] = sd.CJspeed(P1*one_atm, T1, X, mech, 0);
    gas = sd.PostShock_eq(cj_speed, P1*one_atm, T1, X, mech)
    T2.append(gas.T)
    P2.append(gas.P/one_atm)
    speed.append(cj_speed)

i = 0

#for i in range(len(pressure_array)):
#    print "temperature: %f, pressure: %f, CJspeed: %f" % (T2[i], P2[i], speed[i])

plt.plot(pressure_array,speed)
plt.xlabel('Initial pressure [%]')
plt.ylabel('C-J Speed [m/s]')
plt.show()

plt.plot(pressure_array,P2)
plt.xlabel('Initial pressure [%]')
plt.ylabel('post-shock pressure [atm]')
plt.show()

plt.plot(pressure_array,T2)
plt.xlabel('Initial pressure [%]')
plt.ylabel('post-shock temperature [K]')
plt.show()    

#intial condidtions for variable initial temperature
P1 = one_atm
nH2 = 0.34
nO2 = (1-nH2) /4.76
nN2 = (1-nH2) *3.76/4.76
X  =  'H2:'+str(nH2)+ ' ' + 'O2:'+str(nO2) + ' ' + 'N2:'+str(nN2)

T2 = []
P2 = []
speed = []
for T1 in temperature_array:
    [cj_speed,R2] = sd.CJspeed(P1, T1, X, mech, 0);
    gas = sd.PostShock_eq(cj_speed, P1, T1, X, mech)
    T2.append(gas.T)
    P2.append(gas.P/one_atm)
    speed.append(cj_speed)

i = 0

#for i in range(len(temperature_array)):
    #print "For: initial temperature: %f; temperature: %f, pressure: %f, CJspeed: %f" % (temperature_array[i], T2[i], P2[i], speed[i])

plt.plot(temperature_array,speed)
plt.xlabel('Initial temperature [%]')
plt.ylabel('C-J Speed [m/s]')
plt.show()

plt.plot(temperature_array,P2)
plt.xlabel('Initial temperature [%]')
plt.ylabel('post-shock pressure [atm]')
plt.show()

plt.plot(temperature_array,T2)
plt.xlabel('Initial temperature [%]')
plt.ylabel('post-shock temperature [K]')
plt.show()    