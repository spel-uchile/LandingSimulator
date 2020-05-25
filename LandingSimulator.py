# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 11:19:53 2020

@author: Elias Obreque
els.obrq@gmail.com
"""

from MainSimulation.MainSimulation import MainSimulation
from Visualization.Viewer import Viewer
from matplotlib import pyplot as plt

mainSim = MainSimulation()
mainSim.run_simulation(save_data=False)    # Datalog => *.Json
#filename = mainSim.filename + ".csv"
#
# Viewer()

#%%
time = mainSim.spacecraft.master_data_satellite['time[sec]']
rx = mainSim.spacecraft.master_data_satellite['sat_position_i(X)[m]']
ry = mainSim.spacecraft.master_data_satellite['sat_position_i(Y)[m]']
rz = mainSim.spacecraft.master_data_satellite['sat_position_i(Z)[m]']

vx = mainSim.spacecraft.master_data_satellite['sat_velocity_i(X)[m/s]']
vy = mainSim.spacecraft.master_data_satellite['sat_velocity_i(Y)[m/s]']
vz = mainSim.spacecraft.master_data_satellite['sat_velocity_i(Z)[m/s]']

ctrhx = mainSim.spacecraft.master_data_satellite['Control_X_i [N]']
ctrhy = mainSim.spacecraft.master_data_satellite['Control_Y_i [N]']
ctrhz = mainSim.spacecraft.master_data_satellite['Control_Z_i [N]']

mass = mainSim.spacecraft.master_data_satellite['Mass [kg]']

trhx = mainSim.spacecraft.master_data_satellite['Thruster_X_i [N]']
trhy = mainSim.spacecraft.master_data_satellite['Thruster_Y_i [N]']
trhz = mainSim.spacecraft.master_data_satellite['Thruster_Z_i [N]']

mag_thrust = []
for i in range(1, 9):
    mag_thrust.append(mainSim.spacecraft.master_data_satellite['Mag_Thrust_' + str(i) + ' [N]'])

#%%
fig_thr, axs_thr = plt.subplots(4, 2)
for i in range(4):
    for j in range(2):
        axs_thr[i, j].grid()
        axs_thr[i, j].plot(time, mag_thrust[i*2 + j])
        axs_thr[i, j].set_ylabel('Thrust ' + str(i*2 + j + 1) + '[N]')
        axs_thr[i, j].set_xlabel('Time [s]')

#%%
#PLOT
plt.figure()
plt.plot('Mass [kg]')
plt.plot(time, mass)

plt.figure()
plt.title('Control Thrust')
plt.grid()
plt.ylabel('Thrust [N]')
plt.xlabel('time [s]')
plt.plot(time, ctrhx)
plt.plot(time, ctrhy)
plt.plot(time, ctrhz)
plt.legend(['T_x', 'T_y', 'T_z'])

plt.figure()
plt.title('Enginne Thrust')
plt.grid()
plt.ylabel('Thrust [N]')
plt.xlabel('time [s]')
plt.plot(time, trhx)
plt.plot(time, trhy)
plt.plot(time, trhz)
plt.legend(['T_x', 'T_y', 'T_z'])

plt.figure()
plt.title('Error Target')
plt.grid()
plt.xlabel('X-Position')
plt.ylabel('Y-Position')
plt.plot(rx, ry)

plt.figure()
plt.title('Error Pointing Target')
plt.grid()
plt.xlabel('X-Position')
plt.ylabel('Y-Position')
plt.plot(rx[-1], ry[-1], '*')

fig, axs = plt.subplots(2, 2)
axs[0, 0].grid()
axs[0, 0].plot(rx, ry)
axs[0, 0].set_ylabel('Y-Position [m]')
axs[0, 0].set_xlabel('X-Position [m]')
# %%

axs[0, 1].grid()
axs[0, 1].plot(time, rz)
axs[0, 1].set_xlabel('Time [s]')
axs[0, 1].set_ylabel('Z-Position')

axs[1, 0].grid()
axs[1, 0].plot(vx, vy)
axs[1, 0].set_ylabel('Y-Velocity [m/s]')
axs[1, 0].set_xlabel('X-Velocity [m/s]')
# %%

axs[1, 1].grid()
axs[1, 1].plot(time, vz)
axs[1, 1].set_xlabel('Time [s]')
axs[1, 1].set_ylabel('Z-Velocity')
plt.show()