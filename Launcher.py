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
        self.fig = plt.figure(figsize=(12,5.5))
        
        # generate axes for radial orbit and potential energy
        axR, axU = self.fig.subplots(nrows=1, ncols=2)
        self.axR = axR
        self.axU = axU
        
        # create line for radial orbit
        self.fig.subplots_adjust(left = 0.19, bottom = 0.25)
        self.plotRadialOrbit( 'e = 0' )
        self.plotPotentialEnergy( 'e = 0' )
        
        plt.show()
    
    
    def createParameterButton(self):
        
        # call function when switching radio buttons for parameters
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
        
        # create axis object for parameter button
        ax_param = self.fig.add_axes([0.02, 0.4, 0.1, 0.25])
        
        # create parameter button with labels
        self.param_button = RadioButtons(ax_param, ['e = 0', 'e < 1', 'e = 1', 'e > 1'],
                            [True, False, False, False], activecolor= 'r')
        
        # keep parameter button at the ready and define call function
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
        
        # turning on the slider and keeping it ready for updates
        self.angle_slider.on_changed(self.updateSlider)
        plt.show()

    
    def plotRadialOrbit(self, label):
        
        # get orbit and angles for orbit + color for orbit
        r   = self.orbiter.orbit
        phi = self.orbiter.phi
        color = self.color
        
        # normalize angles for interpolation
        phi_norm = phi - phi.min() 
        phi_norm /= phi_norm.max()
        
        # create radial interpolant
        self.r_interp = interp1d( phi_norm, r, kind='cubic')
        
        # calculate x- and y-components for orbit + interpolants
        x_ = r*np.cos(phi)
        y_ = r*np.sin(phi)
        self.x_interp = interp1d( phi_norm, x_, kind='cubic')
        self.y_interp = interp1d( phi_norm, y_, kind='cubic')
        
        # plot orbit
        self.axR.plot( x_, y_, color=color )
        
        # plot origin of coordinates
        self.axR.plot( [0], [0], 'kx', markersize=5  )
        self.axR.plot( [0], [0], 'wx', markersize=2  )
        
        # create orbiter point
        self.point, = self.axR.plot( [self.x_interp(0)], [self.y_interp(0)], 'ko', markersize=5  )
        
        # set axis labels and limits
        self.axR.set_xlabel('X-Component')
        self.axR.set_ylabel('Y-Component')
        self.axR.set_xlim( -3 , 3 )
        self.axR.set_ylim( -3 , 3 )


    def plotPotentialEnergy(self, label):
        
        # get orbit, angles, and energy for orbit + color for orbit
        r   = self.orbiter.orbit
        phi = self.orbiter.phi
        Ubar = self.orbiter.energy
        color = self.color 
        
        # normalize angles for interpolation
        phi_norm = phi - phi.min()
        phi_norm /= phi_norm.max()
        
        # get max and profile energy curves for plotting
        r_prof    = self.orbiter.r_profile
        Ubar_max  = self.orbiter.energy_max
        Ubar_prof = self.orbiter.energy_profile
        
        # create zero energy line demarcating bound vs unbound orbits
        zero_line = np.zeros( len(r_prof) )
        
        # calculate energy interpolant
        self.u_interp = interp1d( phi_norm, Ubar, kind='cubic')
        
        # plotting general energy profiles
        self.axU.plot( r_prof, zero_line, '--', color='k' )
        self.axU.plot( r_prof, Ubar_max, '--', color=color )
        self.axU.plot( r_prof, Ubar_prof, color='k' )
        
        # text demarcating bound and unbound orbits
        self.axU.text( 2.5,  0.025, "UNBOUND ORBIT")
        self.axU.text( 2.5, -0.05,  "BOUND ORBIT")
        
        # plot actual orbit energy
        self.axU.plot( r, Ubar, color=color )
        
        # set axis labels
        self.axU.set_xlabel('Orbital Radius')
        self.axU.set_ylabel('Effective Potential Energy')
        
        # create orbiter point for energy plot
        self.Upoint, = self.axU.plot( [self.r_interp(0)], [self.u_interp(0)], 'o', color=color, markersize=5  )


    def resetPlots(self):
        
        # clearing axes
        self.axR.cla()
        self.axU.cla()
        
        
    def updateSlider(self, phival):
        
        # update location of orbiter
        self.point.set_xdata(self.x_interp(phival))
        self.point.set_ydata(self.y_interp(phival))
        
        # update location of potential energy point
        self.Upoint.set_xdata(self.r_interp(phival))
        self.Upoint.set_ydata(self.u_interp(phival))
        
        self.fig.canvas.draw_idle()
        