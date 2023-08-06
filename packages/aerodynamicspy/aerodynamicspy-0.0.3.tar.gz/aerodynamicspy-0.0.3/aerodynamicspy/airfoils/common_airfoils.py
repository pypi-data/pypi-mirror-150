import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import aerodynamicspy as aero

# Create an array in X
def create_x_array(num_points):

    phi = np.linspace(0, np.pi, num_points)
    x = np.zeros(num_points)

    for i in range(num_points):
        x[i] = 1/2 * (1-np.cos(phi[i]))

    return x


# Create a NACA 4-series airfoil
def naca(c,p,t,N):
        
    c = c/100
    p = p/10
    t = t/100

    x = create_x_array(N)
    array = np.zeros([N,3])
    coordinates = np.zeros([2*N,2])

    for i in range(N):
        array[i,0] = x[i]
        array[i,1] = _camber(x[i],p,c) + _thickness(t,x[i])/2
        array[i,2] = _camber(x[i],p,c) - _thickness(t,x[i])/2

    xpositions = array[:,0]
    zu = array[:,1]
    zl = array[:,2]

    coordinates[0:len(x),0] = xpositions
    coordinates[len(x) + 0:2*len(x),0] = np.flip(xpositions)
    coordinates[0:len(x),1] = zu
    coordinates[len(x) + 0:2*len(x),1] = np.flip(zl)

    # XFOIL wants the trailing edge first, then wrap around to the leading edge
    # and then back to the trailing edge
    # Currently, we have it:
    # leading edge -> trailing edge over the top
    # leading edge -> trailing edge over the bottom
    # So all we need to do is reverse the top, or the first half of the coordinates

    coordinates[0:len(x),0] = np.flip(coordinates[0:len(x),0])
    coordinates[0:len(x),1] = np.flip(coordinates[0:len(x),1])

    coordinates[len(x) + 0:2*len(x),0] = np.flip(coordinates[len(x) + 0:2*len(x),0])
    coordinates[len(x) + 0:2*len(x),1] = np.flip(coordinates[len(x) + 0:2*len(x),1])

    NACA = aero.Airfoil("NACA " + str(int(c*100)) + str(int(p*10)) + str(int(t*100)),coordinates[:,0],coordinates[:,1])

    return NACA

def _camber(x,p,c):

    # camber(x,p,c)

    # Determines the proper amount of camber.
    
    # x = position along the chord
    # p = position of maximum camber
    # c = value of maximum camber

    if x <= p:
        z = c * (2*p*x - x**2)/p**2
    else:
        z = c * (1 - 2*p + 2*p*x -x**2)/(1-p)**2

    if p == 0:
        z = 0

    return z

def _thickness(m,x):

    # thickness(maximum thickness,position)

    # Outputs the thickness of a NACA 4-series airfoil.
    
    # This function the maximum thickness (as a percentage of the chord) 
    # and the position along the chord to generate the thickness along
    # the chord.

    t = 10 * m * (0.2969*np.sqrt(x) - 0.1260*x - 0.3537*x**2 + 0.2843*x**3 - 0.1015*x**4)

    return t