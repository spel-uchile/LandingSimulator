# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 11:19:53 2020

@author: EO
"""

from MainSimulation.MainSimulation import MainSimulation


mainSim = MainSimulation()
mainSim.run_simulation()    # Datalog => *.Json
filename = mainSim.filename + ".csv"






