# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 20:10:34 2022

@author: gjsot
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons, CheckButtons

class Orbiter(object):
    
    def __init__(self):
        # orbit parameters
        self.m = 1
        self.l = 1
        self.a = 1
        
        # create generic orbit
        self.setOrbit( 0 )
    
    def setOrbit( self, e=0, phi0=0, phiF=2*np.pi, phiN=1000 ):
        # define angles of orbit
        self.phi    = np.linspace( phi0, phiF, phiN+1 )[1:]
        # generate orbit
        self.orbit  = self.inverseSquareOrbit( e )
        # calculate potential energy
        self.energy = self.inverseSquareEnergy( e )
    
    def inverseSquareOrbit(self, e):
        # get orbit parameters
        l = self.l
        a = self.a
        
        # calculate radial component of orbit
        r = (l**2/a) / (1 + e*np.cos(self.phi) )
        return r
        
    
    def inverseSquareEnergy(self, e):
        # calculate orbit
        r = self.inverseSquareOrbit( e )
        
        # get orbit parameters
        m = self.m
        l = self.l
        a = self.a
        
        # calculate effective potential energy of orbit
        Ubar = 0.5*m*l**2/r**2 - m*a/r
        return Ubar
        
        