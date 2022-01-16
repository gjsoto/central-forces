# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 19:59:56 2022

@author: gjsot
"""

import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons, CheckButtons, Slider
from Orbiter import Orbiter

class Launcher(object):
    
    def __init__(self):
        
        self.e = 0
        self.orbiter = Orbiter()
        
        # create figure with adjusted graph
        self.createFigure()
        self.createParameterButton()
#        self.createAngleSlider()
        plt.show()
    
    
    def createFigure(self):
        
        # define and save figure to self
        self.fig = plt.figure(figsize=(10,5))
        
        # generate axes for radial orbit and potential energy
        axR, axU = self.fig.subplots(nrows=1, ncols=2)
        self.axR = axR
        self.axU = axU
        
        # create line for radial orbit
        self.fig.subplots_adjust(left = 0.2, bottom = 0.25)
        self.radial = self.plotRadialOrbit( 'e = 0' )
        
        plt.show()
    
    
    def createParameterButton(self):
        
        def param( label ):
            if label == 'e = 0':
                self.e = 0
                self.orbiter.setOrbit( self.e )
            elif label ==  'e < 1':
                self.e = 0.5
                self.orbiter.setOrbit( self.e )
            elif label == 'e = 1':
                self.e = 1
                self.orbiter.setOrbit( self.e, phiF=2*np.pi*0.99 )
            elif label == 'e > 1':
                self.e = 1.1
                self.orbiter.setOrbit( self.e, phi0=-2.35, phiF=2.35 )
            
            self.plotRadialOrbit( label )
        
        ax_param = self.fig.add_axes([0.02, 0.4, 0.1, 0.25])
        self.param_button = RadioButtons(ax_param, ['e = 0', 'e < 1', 'e = 1', 'e > 1'],
                            [True, False, False, False], activecolor= 'r')
        self.param_button.on_clicked(param)
        plt.show()
    
    
    def createAngleSlider(self):
        
        # Make a horizontal slider to control the frequency.
        ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03])
        self.angle_slider = Slider(
            ax=ax_slider,
            label='Phi',
            valmin=0,
            valmax=2*np.pi,
            valinit=0,
        )
        self.angle_slider.on_changed(self.updateSlider)
        plt.show()

    
    def plotRadialOrbit(self, label):
        
        r   = self.orbiter.orbit
        phi = self.orbiter.phi
        phi_norm = (phi - phi.min() ) / phi.max()
        self.r_interp = interp1d( phi_norm, r, kind='cubic')
        
        x_ = r*np.cos(phi)
        y_ = r*np.sin(phi)
        self.x_interp = interp1d( phi_norm, x_, kind='cubic')
        self.y_interp = interp1d( phi_norm, y_, kind='cubic')
        
        labels = np.array(['e = 0', 'e < 1',  'e = 1', 'e > 1'])
        colors = np.array(['C4', 'C1', 'C3', 'C0'])
        color = [colors[n] for n,l in enumerate(labels) if label==l]
        
        self.axR.plot( x_, y_, color=color[0] )
        self.point, = self.axR.plot( [self.x_interp(0)], [self.y_interp(0)], 'ko', markersize=5  )
        self.axR.set_xlim( -3 , 3 )
        self.axR.set_ylim( -3 , 3 )
        
        
#    def plotRadialOrbitPoint(self, phival):
#        
#        r_int = self.r_interp(phival)
#        
        
#    def updateSlider(self, val):
#
#        line.set_ydata(f(t, amp_slider.val, freq_slider.val))
#        fig.canvas.draw_idle()