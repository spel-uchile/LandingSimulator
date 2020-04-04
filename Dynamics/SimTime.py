# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 05:17:52 2020

@author: EO
"""
from datetime import datetime
from Library.sgp4 import ext
from Library.math_sup.tools_reference_frame import JdToDecyear


class SimTime(object):

    def __init__(self,
                 time_properties):
        start_string        = time_properties['StartTime']
        datetime_array      = datetime.strptime(start_string, '%Y/%m/%d %H:%M:%S')
        self.startsimTime   = datetime_array.timestamp()
        self.currentsimTime = self.startsimTime
        self.current_array, _ = self.get_array_time()
        self.endsimTime     = time_properties['EndTime']
        self.simspeedTime   = time_properties['SimulationSpeed']
        self.current_jd      = ext.jday(self.current_array[0],
                                        self.current_array[1],
                                        self.current_array[2],
                                        self.current_array[3],
                                        self.current_array[4],
                                        self.current_array[5])
        self.current_decyaer = JdToDecyear(self.current_jd)
        # Principal Time variable
        self.stepsimTime    = time_properties['StepTime']   # principal Step
        self.maincountTime  = 0     # Count for Principal Step
        self.logperiod      = time_properties['LogPeriod']
        self.log_count      = 0     # Log output Period in function of principal time
        self.log_flag       = True  # It is true to save the first data (initial)

        # Auxiliary variable for orbit, attitude and thermal update
        self.orbitstep              = time_properties['OrbStepTime']  # Orbit Step
        self.attitudestep           = time_properties['PropStepSec']  # Attitude step
        self.orbit_update_flag      = True  # Flag for Orbit Step
        self.attitudecountTime      = 0  # Count for Attitude Step
        self.orbitcountTime         = 0  # Count for Orbit Step

        self.historical_DateTime    = []
        self.historical_satStepTime        = []
        print("-----------------------------")
        print('Simulation start Time: ' + start_string)

    def get_array_time(self):
        datetime_array = datetime.fromtimestamp(self.currentsimTime)
        currenttime_array = [datetime_array.year,
                             datetime_array.month,
                             datetime_array.day,
                             datetime_array.hour,
                             datetime_array.minute,
                             datetime_array.second + datetime_array.microsecond/1e6]
        return currenttime_array, datetime_array.strftime('%Y-%m-%d %H:%M:%S')

    def updateSimtime(self):
        self.currentsimTime     += self.stepsimTime
        self.maincountTime      += self.stepsimTime
        self.current_array, _    = self.get_array_time()
        self.current_jd      = ext.jday(self.current_array[0],
                                        self.current_array[1],
                                        self.current_array[2],
                                        self.current_array[3],
                                        self.current_array[4],
                                        self.current_array[5])
        self.current_decyaer = JdToDecyear(self.current_jd)
        self.orbitcountTime     += self.stepsimTime

        if abs(self.orbitcountTime - self.orbitstep) < 1e-6:
            self.orbit_update_flag = True
            self.orbitcountTime = 0

        self.update_log_count()

    def progressionsimTime(self):
        val = round(100*self.maincountTime/self.endsimTime, 2)
        if val % 5 == 0:
            print(val, '%')

    def reset_countTime(self):
        self.maincountTime      = 0
        self.attitudecountTime  = 0
        self.orbitcountTime     = 0

    def update_log_count(self):
        self.log_count += 1
        if self.log_count == self.logperiod:
            self.log_flag = True
            self.log_count = 0

    def save_simtime_data(self):
        self.historical_DateTime.append(self.get_array_time()[1])
        self.historical_satStepTime.append(self.maincountTime)

    def get_log_values(self):
        report_timelog = {'Date time': self.historical_DateTime,
                          'time[sec]': self.historical_satStepTime}
        return report_timelog
