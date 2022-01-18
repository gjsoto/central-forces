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
        self.color='C4'
        
        # create figure with adjusted graph
        self.createFigure()
        self.createParameterButton()
        self.createAngleSlider()
        
        # make active plot
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
        self.plotRadialOrbit( 'e = 0' )
        self.plotPotentialEnergy( 'e = 0' )
        
        plt.show()
    
    
    def createParameterButton(self):
        
        def param( label ):
            if label == 'e = 0':
                self.e = 0
                self.orbiter.setOrbit( self.e )
                self.color = 'C4'
            elif label ==  'e < 1':
                self.e = 0.5
                self.orbiter.setOrbit( self.e )
                self.color = 'C1'
            elif label == 'e = 1':
                self.e = 1
                self.orbiter.setOrbit( self.e, phi0=-2.42, phiF=2.42 )
                self.color = 'C3'
            elif label == 'e > 1':
                self.e = 1.1
                self.orbiter.setOrbit( self.e, phi0=-2.335, phiF=2.335 )
                self.color = 'C0'
            
            self.resetPlots()
            self.plotRadialOrbit( label )
            self.plotPotentialEnergy( label )
        
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
            valmax=1,
            valinit=0,
        )
        self.angle_slider.on_changed(self.updateSlider)
        plt.show()

    
    def plotRadialOrbit(self, label):
        
        r   = self.orbiter.orbit
        phi = self.orbiter.phi
        phi_norm = phi - phi.min() 
        phi_norm /= phi_norm.max()
        self.r_interp = interp1d( phi_norm, r, kind='cubic')
        
        x_ = r*np.cos(phi)
        y_ = r*np.sin(phi)
        self.x_interp = interp1d( phi_norm, x_, kind='cubic')
        self.y_interp = interp1d( phi_norm, y_, kind='cubic')
        
        color = self.color
        
        self.axR.plot( x_, y_, color=color )
        self.axR.plot( [0], [0], 'kx', markersize=5  )
        self.axR.plot( [0], [0], 'wx', markersize=2  )
        self.point, = self.axR.plot( [self.x_interp(0)], [self.y_interp(0)], 'ko', markersize=5  )
        
        self.axR.set_xlabel('X-Component')
        self.axR.set_ylabel('Y-Component')
        
        self.axR.set_xlim( -3 , 3 )
        self.axR.set_ylim( -3 , 3 )


    def plotPotentialEnergy(self, label):
        
        phi = self.orbiter.phi
        Ubar = self.orbiter.energy
        
        phi_norm = phi - phi.min()
        phi_norm /= phi_norm.max()
        Ubar_max  = self.orbiter.energy_max
        Ubar_prof = self.orbiter.energy_profile
        r_prof    = self.orbiter.r_profile
        zero_line = np.zeros( len(r_prof) )
        
        self.u_interp = interp1d( phi_norm, Ubar, kind='cubic')
        
        color = self.color 
        
        self.axU.plot( r_prof, zero_line, '--', color='k' )
        self.axU.plot( r_prof, Ubar_max, '--', color=color )
        self.axU.plot( r_prof, Ubar_prof, color='k' )
        
        self.axU.set_xlabel('Orbital Radius')
        self.axU.set_ylabel('Effective Potential Energy')
        
        self.Upoint, = self.axU.plot( [self.r_interp(0)], [self.u_interp(0)], 'o', color=color, markersize=5  )


    def resetPlots(self):
        
        self.axR.cla()
        self.axU.cla()
        
        
    def updateSlider(self, phival):
        self.point.set_xdata(self.x_interp(phival))
        self.point.set_ydata(self.y_interp(phival))

        self.Upoint.set_xdata(self.r_interp(phival))
        self.Upoint.set_ydata(self.u_interp(phival))
        
        self.fig.canvas.draw_idle()
        