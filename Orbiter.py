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
        self.m = 1
        self.l = 1
        self.a = 1
        
        # start and end for theta values
        phi_ini = 0
        phi_fin = 2*np.pi
        phi_N   = 1000
        
        # theta array for plotting
        self.phi = np.linspace( phi_ini, phi_fin, phi_N+1 )[1:]
        self.setOrbit( 0 )
    
    def setOrbit( self, e=0 ):
        self.orbit  = self.inverseSquareOrbit( e )
        self.energy = self.inverseSquareEnergy( e )
    
    def inverseSquareOrbit(self, e):
        
        l = self.l
        a = self.a
        
        r = (l**2/a) / (1 + e*np.cos(self.phi) )
        
        return r
        
    
    def inverseSquareEnergy(self, e):
        
        r = self.inverseSquareOrbit( e )
        
        m = self.m
        l = self.l
        a = self.a
        
        Ubar = 0.5*m*l**2/r**2 - m*a/r
        
        return Ubar
        
        