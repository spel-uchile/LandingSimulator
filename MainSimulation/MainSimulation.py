"""
Created on Wed Jan 15 11:19:53 2020

@author: EO
"""

from Spacecraft.Spacecraft import Spacecraft
from Dynamics.SimTime import SimTime
from Interface.Initializer import InitialConfig
from Interface.Logger import Logger
from Environments.Environment import Environment
from Disturbance.Disturbances import Disturbances

import numpy as np
import pandas as pd
import datetime

twopi   = 2.0 * np.pi
deg2rad = np.pi / 180.0
rad2deg = 1 / deg2rad


class MainSimulation(InitialConfig, Logger):
    def __init__(self):
        InitialConfig.__init__(self)
        Logger.__init__(self, self.logger_properties)

        self.simtime = SimTime(self.time_properties)
        self.spacecraft = Spacecraft(self.spacecraft_properties, self.components_properties, self.simtime)

        self.environment = Environment(self.environment_properties)
        self.disturbance = Disturbances(self.disturbance_properties, self.environment, self.spacecraft)

        # Auxiliary variables
        date = datetime.datetime.now()
        self.filename = date.strftime('%Y-%m-%d %H-%M-%S')

    def run_simulation(self, save_data=True):
        self.spacecraft.dynamics.trajectory.set_propagator()
        # Loop
        self.simtime.reset_countTime()
        print('Simulation running...')
        while self.simtime.maincountTime <= self.simtime.endsimTime:
            # spacecraft update
            self.spacecraft.update()

            # current Environment and disturbances
            self.environment.update(self.simtime.current_decyaer, self.spacecraft.dynamics)
            self.disturbance.update()

            # Add the force and torque generated by the disturbance for the next dynamics propagation
            #self.spacecraft.dynamics.add_force_b(self.disturbance.get_dis_force_b())
            #self.spacecraft.dynamics.attitude.add_ext_torque_b(self.disturbance.get_dist_torque_b())

            # Add the force and torque generated by the satellite for the next dynamics propagation
            self.spacecraft.dynamics.add_force_i(self.spacecraft.generate_force_i())
            #self.spacecraft.dynamics.attitude.add_int_torque_b(self.spacecraft.generate_torque_b())

            if self.simtime.log_flag:
                self.spacecraft.update_data()
                self.environment.update_data()
                self.disturbance.update_data()
                self.simtime.progressionsimTime()
                self.simtime.log_flag = False

            # update time
            self.simtime.updateSimtime()
            if self.spacecraft.dynamics.trajectory.reference_frame != 3:
                if self.spacecraft.dynamics.trajectory.current_alt <= 0:
                    print('Ground reached')
                    break
            else:
                if self.spacecraft.dynamics.trajectory.current_position[2] <= 0:
                    print('Ground reached')
                    break

        # Data report to create dictionary
        self.spacecraft.add_report(self.environment.create_report())
        self.spacecraft.add_report(self.disturbance.create_report())
        self.spacecraft.create_report()

        # Save Dataframe pandas in csv file
        if save_data:
            self.save_data()
            print('Data saved')
        print('Finished')

    def save_data(self):
        master_data = self.spacecraft.master_data_satellite
        database = pd.DataFrame(master_data, columns=master_data.keys())

        database.to_csv("./Data/logs/"+self.filename+".csv", index=False, header=True)
        print("Data created")
