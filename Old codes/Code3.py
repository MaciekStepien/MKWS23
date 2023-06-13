from SDToolbox import *
import matplotlib.pyplot as plt
import sys

T1=298
p1=101325
T2=400
p2=1.5*p1
T3=600
p3=3*p1


q1 ='CH4:1, O2:2';
mech = 'gri30_highT.cti';   

q2 = 'C3H8:1, O2:5'
mech = 'gri30_highT.cti'

q3 = 'H2:2 O2:1'
mech = 'gri30_highT.cti'


def speed (q, T, p):
   
    P1atm = p/one_atm;
    
     
    [cj_speed,R2] = CJspeed(p, T, q, mech, 0);   

    gas = PostShock_eq(cj_speed, p, T, q, mech)
    Ps = gas.P/one_atm

    
    Ps = gas.P/one_atm

    
    print 'For ' + q + ' with p = %.2f [bar] T = %.2f K ' % (P1atm,T)
    print 'CJ Speed is %.2f m/s \n' % cj_speed
    
speed(q1,T1,p1)
speed(q1,T2,p2)
speed(q1,T3,p3)

speed(q2,T1,p1)
speed(q2,T2,p2)
speed(q2,T3,p3)

speed(q3,T1,p1)
speed(q3,T2,p2)
speed(q3,T3,p3)

def temp (m):                                 ## Funkcja wyliczająca temperature spalania w czasie 
    wyniki = open('wyniki_mkws2.txt', 'w')
    wyniki.write('%5s\t%10s\t%10s\n' % ('L.p.', 'p[Pa]', 'T [K]'))
    s=[]
    s=[p1,p2,p3]
    t=[T1,T2,T3]
    
    wyniki.close()
    
    plt.figure()
    plt.plot(s, t)
    plt.xlabel('Pressure [Pa]')
    plt.ylabel('Temperature [K]')
    plt.title('Temperature')
    
temp(q1)