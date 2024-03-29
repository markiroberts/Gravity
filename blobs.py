# on a PC:
# python -m venv gravity
# Set-ExecutionPolicy RemoteSigned -Scope CurrentUser  
# .\Gravity\Scripts\activate
# source ./advent/bin/activate
# python.exe -m pip install --upgrade pip
# pip install -r .\Gravity\requirements.txt
# pip install matplotlib
# pip install numpy

#import os
#import sys
#import json
#from pathlib import Path
import re
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import time

#from numpy.core.umath_tests import inner1d

def init_objects():
    objects             = MAX_OBJECTS
    obj_position        = np.zeros(POSITION_SHAPE, dtype=float)
    obj_radius          = np.zeros(MASS_SHAPE, dtype=float)
    obj_mass            = np.zeros(MASS_SHAPE, dtype=float)
    obj_velocity        = np.zeros(VELOCITY_SHAPE, dtype=float)
    obj_acceleration    = np.zeros(VELOCITY_SHAPE, dtype=float)
    for i in range(objects):
        orbit_radius = 100 + (100 * np.random.rand() ) 
        angle = 2*3.1465 * np.random.rand()
        vel = 10 * np.random.rand()
        obj_velocity[i][0] = vel * np.sin(angle)
        obj_velocity[i][1] = -vel * np.cos(angle)
        
        obj_position[i][0] = orbit_radius * np.cos(angle)
        obj_position[i][1] = orbit_radius * np.sin(angle)

        obj_radius[i] = (1 * np.random.rand()) + 1.0
        obj_mass[i] = obj_radius[i] * obj_radius[i]
#        obj_velocity[i] = np.random.rand()
        
    obj_position[0][0] = 0.0
    obj_position[0][1] = 0.0
    obj_radius[0] = 40
    obj_mass[0] = obj_radius[0] * obj_radius[0]
    obj_velocity[0][0] = 0.0
    obj_velocity[0][1] = 0.0
    return obj_position, obj_radius, obj_mass, obj_velocity, obj_acceleration

def determine_acceleration():
    for i in range(MAX_OBJECTS):
        force = force_on_object_i(i)
        acceleration = force / object_mass[i]
        object_acceleration[i] = acceleration

def determine_new_velocity():
    for i in range(MAX_OBJECTS):
        object_new_velocity[i] = object_velocity[i] + (object_acceleration[i] * TIMESTEP)

def determine_new_position():
    for i in range(MAX_OBJECTS):
        object_new_position[i] = object_new_position[i] + (object_velocity[i] * TIMESTEP)

def force_on_object_i(i):
    force = np.zeros(2, dtype=float)
    direction = np.zeros(2, dtype=float)
    for j in range(MAX_OBJECTS):
        if j != i:
            direction = object_position[j] - object_position[i]
            direction_magnitude = np.sqrt(direction[0]**2 + direction[1]**2)
            if ( direction_magnitude < ( object_radius[i] + object_radius[j] )  ):
                if i==0:
                    print("the sun")
                print(f"Join {i} {j} {direction_magnitude} {direction} radius before: {object_radius[i]}, {object_radius[j]} velocity before {object_velocity[i]} {object_velocity[j]}")
                object_radius[i] = np.sqrt(object_radius[i]**2 + object_radius[j]**2)
                if (object_radius[i] > object_mass[j]):
                    addto = i
                    delete = j
                else:
                    addto = j
                    delete = i

                object_velocity[addto] = object_velocity[addto] + ( object_velocity[delete] / (  object_mass[addto] + object_mass[delete] )  )
                object_mass[addto] = object_mass[addto] + object_mass[delete]
                object_radius[delete] = -1
                object_mass[delete] = 0.000001
                object_position[delete][0] = 99999 + ( 9999 * np.random.rand() )
                object_position[delete][1] = 99999 + ( 9999 * np.random.rand() )
                object_velocity[delete][0] = 0
                object_velocity[delete][1] = 0
                print(f"Join {i} {j} radius after: {object_radius[i]}, {object_radius[j]} velocity after {object_velocity[i]}")
            else:
                direction_normalised = direction / direction_magnitude
                force = force + ( ( GRAVITY * object_mass[j] * object_mass[i] ) / direction_magnitude**2 ) * direction_normalised
    return force


TIMESTEP = 0.01
PLOT_EVERY_X_STEPS = 10
MAX_TIME = 100.0
MAX_OBJECTS = 50
DIMENSIONS = 2
POSITION_SHAPE = (MAX_OBJECTS,2)
VELOCITY_SHAPE = (MAX_OBJECTS,2)
MASS_SHAPE = (MAX_OBJECTS,1)
GRAVITY = 1.0

fig = plt.figure(figsize=[5, 5])
ax = plt.axes([0.1, 0.1, 0.8, 0.8], xlim=(-200, 200), ylim=(-200, 200))
points_whole_ax = 5 * 0.8 * 72

time = 0.0
object_position, object_radius, object_mass, object_velocity, object_acceleration = init_objects()
frames = 0

xt = []

while time < MAX_TIME:
    object_new_velocity = object_velocity
    object_new_position = object_position
    determine_acceleration()
    determine_new_velocity()
    determine_new_position()
    object_velocity = object_new_velocity
    object_position = object_new_position

    if ((frames % 30) == 0):
        x = []
        y = []
        s = []#object_mass[i]
        colors = []
        for i in range(MAX_OBJECTS):
            if object_radius[i] > 0: 
                x.append(object_new_position[i][0])
                y.append(object_new_position[i][1])
                radius = 40
                radius = object_radius[i]
   #             radius = 40
                radius = 1
                points_radius = 2 * radius / 1.0 * points_whole_ax 
                points_radius = object_radius[i] * 1.4
                s.append(points_radius**2)
                colors.append(i)

        xt.append(object_new_position[0][0])
 
        plt.scatter(x,y,s=s,c=colors)
        plt.xlim(-200, 200)
        plt.ylim(-200, 200)
        plt.title(f"Time:{time:.2f} Frames: {frames}")

    #    plt.scatter(object_new_position[:][0], object_new_position[:][1], s=area, c=colors, alpha=0.5)
        plt.draw()
        plt.pause(0.1)
        plt.clf()
    time += TIMESTEP
    frames += 1
#    print(time)
##

#plt.scatter(x,y)
#plt.show()
#print(xt)