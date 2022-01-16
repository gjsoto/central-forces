# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 19:59:56 2022

@author: gjsot
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons, CheckButtons, Slider
from Orbiter import Orbiter

class Launcher(object):
    
    def __init__(self):
        
        self.e = 0
        self.tol = 1.5
        self.orbiter = Orbiter()
        # create figure with adjusted graph
        self.createFigure()
        self.createParameterButton()
        plt.show()
    
    def createFigure(self):
        
        # define and save figure to self
        self.fig = plt.figure()
        self.ax = self.fig.subplots()
        self.fig.subplots_adjust(left = 0.3, bottom = 0.25)
        self.line = self.plotRadialOrbit( )
    
    def createParameterButton(self):
        
        def param( label ):
            if label == 'e = 0':
                self.e = 0
            elif label ==  'e < 1':
                self.e = 0.5
            elif label == 'e = 1':
                self.e = 1
            elif label == 'e > 1':
                self.e = 1.1
            self.orbiter.setOrbit( self.e )
            self.plotRadialOrbit( )
        
        ax_param = self.fig.add_axes([0.02, 0.5, 0.2, 0.3])
        self.param_button = RadioButtons(ax_param, ['e = 0', 'e < 1', 'e = 1', 'e > 1'],
                            [True, False, False, False], activecolor= 'r')
        self.param_button.on_clicked(param)
        plt.show()
    
    def plotRadialOrbit(self):
        
        r   = self.orbiter.orbit
        phi = self.orbiter.phi
        tol = self.tol
        
        x_ = r*np.cos(phi)
        y_ = r*np.sin(phi)
        
        self.ax.plot( x_, y_ )
        self.ax.set_xlim( np.min(x_)*(1+tol) , np.max(x_)*(1+tol) )
        self.ax.set_ylim( np.min(y_)*(1+tol) , np.max(y_)*(1+tol) )
        