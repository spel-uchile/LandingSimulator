# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 03:58:00 2020

@author: EO
"""
import configparser
import numpy as np
from datetime import datetime
import pyvista as pv


class InitialConfig(object):
    def __init__(self):
        self.time_properties = TimeSim()
        spacecraft_properties, self.components_properties = SatSim()
        trajectory_properties = TrajecSim()
        self.environment_properties = EnvSim()
        self.disturbance_properties = DistSim()
        self.spacecraft_properties = {'Attitude': spacecraft_properties,
                                      'Orbit': trajectory_properties}
        ephemeris_properties = {'Ephemerides': EphSim()}
        self.spacecraft_properties = {**self.spacecraft_properties, **ephemeris_properties}
        self.logger_properties = self.LogSim()

    def LogSim(self):
        properties = {'env_mag_log': self.environment_properties['MAG']['mag_logging'],
                      'env_atm_log': self.environment_properties['ATM']['atm_logging'],
                      'dis_atm_log': self.disturbance_properties['ADRAG']['atm_logging'],
                      'dis_gra_log': self.disturbance_properties['GRA']['gra_logging']}
        return properties


def EphSim():
    config = configparser.ConfigParser()
    config.read("Data/ini/PlanetSelect.ini", encoding="utf8")
    properties = {'inertial_frame': config['PLANET_SELECTION']['inertial_frame'],
                  'aberration_correction': config['PLANET_SELECTION']['aberration_correction'],
                  'center_object': config['PLANET_SELECTION']['center_object'],
                  'num_of_selected_body': config['PLANET_SELECTION']['num_of_selected_body']}
    return properties


def TimeSim():
    config = configparser.ConfigParser()
    config.read("Data/ini/Spacecraft.ini", encoding="utf8")
    StartYMDHMS = config['TIME']['StartYMDHMS']
    if StartYMDHMS == ('Today' or 'TODAY' or 'today'):
        today = datetime.utcnow()
        StartYMDHMS = today.strftime("%Y/%m/%d %H:%M:%S")

    EndTimeSec = float(config['TIME']['EndTimeSec'])
    StepTimeSec = float(config['TIME']['StepTimeSec'])
    OrbitPropagateStepTimeSec = float(config['TIME']['OrbitPropagateStepTimeSec'])
    LogPeriod = float(config['TIME']['LogPeriod'])
    SimulationSpeed = float(config['TIME']['SimulationSpeed'])
    PropStepSec = float(config['ATTITUDE']['PropStepSec'])
    PropStepSec_Thermal = float(config['THERMAL']['PropStepSec_Thermal'])
    timesim = {'StartTime': StartYMDHMS,
               'EndTime': EndTimeSec,
               'StepTime': StepTimeSec,
               'OrbStepTime': OrbitPropagateStepTimeSec,
               'LogPeriod': LogPeriod,
               'SimulationSpeed': SimulationSpeed,
               'PropStepSec': PropStepSec,
               'PropStepSec_Thermal': PropStepSec_Thermal}
    return timesim


def SatSim():
    config = configparser.ConfigParser()
    config.read("Data/ini/Spacecraft.ini", encoding="utf8")
    spacecraft_name = config['NAME']['spacecraft_name']
    spacecraft_model_name = config['NAME']['model_name']
    # Load geometry mesh. Folder Model
    spacecraft_model = pv.read('./Visualization/Model/' + spacecraft_model_name)

    # Rotational speed [rad/s]
    Omega_b = np.zeros(3)
    Omega_b[0] = config['ATTITUDE']['Omega_b(0)']
    Omega_b[1] = config['ATTITUDE']['Omega_b(1)']
    Omega_b[2] = config['ATTITUDE']['Omega_b(2)']
    # QuaternionCi2bC
    Quaternion_i2b = np.zeros(4)
    Quaternion_i2b[0] = config['ATTITUDE']['Quaternion_i2b(0)']
    Quaternion_i2b[1] = config['ATTITUDE']['Quaternion_i2b(1)']
    Quaternion_i2b[2] = config['ATTITUDE']['Quaternion_i2b(2)']
    Quaternion_i2b[3] = config['ATTITUDE']['Quaternion_i2b(3)']

    # Inertial
    Iner = np.zeros((3, 3))
    Iner[0, 0] = config['ATTITUDE']['Iner(0)']
    Iner[0, 1] = config['ATTITUDE']['Iner(1)']
    Iner[0, 2] = config['ATTITUDE']['Iner(2)']
    Iner[1, 0] = config['ATTITUDE']['Iner(3)']
    Iner[1, 1] = config['ATTITUDE']['Iner(4)']
    Iner[1, 2] = config['ATTITUDE']['Iner(5)']
    Iner[2, 0] = config['ATTITUDE']['Iner(6)']
    Iner[2, 1] = config['ATTITUDE']['Iner(7)']
    Iner[2, 2] = config['ATTITUDE']['Iner(8)']
    # mass
    mass = float(config['ATTITUDE']['mass'])
    satset = {'Omega_b': Omega_b,
              'Quaternion_i2b': Quaternion_i2b,
              'Inertia': Iner,
              'Mass': mass,
              'spacecraft_name': spacecraft_name,
              'spacecraft_model': spacecraft_model}

    file_components = config['COMPONENTS']['file_components']
    section = 'SUBSYSTEMS'
    comset = {'path_com': file_components,
              'create_cdh': config[section]['create_cdh'] == 'True',
              'cdh_setting': config[section]['cdh_setting'],
              'create_odcs': config[section]['create_odcs'] == 'True',
              'odcs_setting': config[section]['odcs_setting'],
              'create_adcs': config[section]['create_adcs'] == 'True',
              'adcs_setting': config[section]['adcs_setting'],
              'create_power': config[section]['create_power'] == 'True',
              'power_setting': config[section]['power_setting'],
              'create_com': config[section]['create_com'] == 'True',
              'com_setting': config[section]['com_setting'],
              'create_str': config[section]['create_str'] == 'True',
              'str_setting': config[section]['str_setting'],
              'create_payload': config[section]['create_payload'] == 'True',
              'payload_setting': config[section]['payload_setting'],
              'create_tcs': config[section]['create_tcs'] == 'True',
              'tcs_setting': config[section]['tcs_setting']}

    return satset, comset


def TrajecSim():
    config = configparser.ConfigParser()
    config.read("Data/ini/Trajectory.ini", encoding="utf8")

    propagate_mode = float(config['PROPAGATION']['propagate_mode'])
    reference_frame_data = float(config['ORBIT']['reference_frame_data'])
    if reference_frame_data == 2:
        r = np.zeros(3)
        r[0] = float(config['ORBIT']['long'])
        r[1] = float(config['ORBIT']['lat'])
        r[2] = float(config['ORBIT']['alt'])

        v = np.zeros(3)
        v[0] = float(config['ORBIT']['v_north'])
        v[1] = float(config['ORBIT']['v_east'])
        v[2] = float(config['ORBIT']['v_down'])

        orbitset = {'Orbit_info': [r, v],
                    'propagate': propagate_mode,
                    'reference_frame': reference_frame_data}
    else:
        # position
        r = np.zeros(3)
        r[0] = float(config['ORBIT']['rx'])
        r[1] = float(config['ORBIT']['ry'])
        r[2] = float(config['ORBIT']['rz'])
        # velocity
        v = np.zeros(3)
        v[0] = float(config['ORBIT']['vx'])
        v[1] = float(config['ORBIT']['vy'])
        v[2] = float(config['ORBIT']['vz'])

        orbitset = {'Orbit_info': [r, v],
                    'propagate': propagate_mode,
                    'reference_frame': reference_frame_data}
    return orbitset


def EnvSim():
    config = configparser.ConfigParser()
    config.read("Data/ini/Environment.ini", encoding="utf8")
    mag_calculation = config['MAG_ENVIRONMENT']['calculation']
    mag_logging = config['MAG_ENVIRONMENT']['logging']
    mag_rwdev = float(config['MAG_ENVIRONMENT']['mag_rwdev'])
    mag_rwlimit = float(config['MAG_ENVIRONMENT']['mag_rwlimit'])
    mag_wnvar = float(config['MAG_ENVIRONMENT']['mag_wnvar'])

    atm_calculation = config['ATMOSPHERE']['calculation']
    atm_logging = config['ATMOSPHERE']['logging']
    mag_properties = {'mag_calculation': mag_calculation == 'True',
                      'mag_logging': mag_logging == 'True',
                      'mag_rwdev': mag_rwdev,
                      'mag_rwlimit': mag_rwlimit,
                      'mag_wnvar': mag_wnvar}
    atm_properties = {'atm_calculation': atm_calculation == 'True',
                      'atm_logging': atm_logging == 'True'}
    environment_properties = {'MAG': mag_properties,
                              'ATM': atm_properties}
    return environment_properties


def DistSim():
    config = configparser.ConfigParser()
    config.read("Data/ini/Disturbance.ini", encoding="utf8")
    grav_properties = {'gra_calculation': config['GRAVITY_GRADIENT']['calculation'] == 'True',
                       'gra_logging': config['GRAVITY_GRADIENT']['logging'] == 'True'}

    specularity = np.zeros(6)
    specularity[0] = config['AIRDRAG']['specularity(0)']
    specularity[1] = config['AIRDRAG']['specularity(1)']
    specularity[2] = config['AIRDRAG']['specularity(2)']
    specularity[3] = config['AIRDRAG']['specularity(3)']
    specularity[4] = config['AIRDRAG']['specularity(4)']
    specularity[5] = config['AIRDRAG']['specularity(5)']
    atmdrag_properties = {'atm_calculation': config['AIRDRAG']['calculation'] == 'True',
                          'atm_logging': config['AIRDRAG']['logging'] == 'True',
                          'Temp_wall': float(config['AIRDRAG']['Temp_wall']),
                          'specularity': specularity}

    position_vector_surface = np.zeros((6, 3))
    position_vector_surface[0] = [config['SURFACEFORCE']['px_arm(0)'],
                                  config['SURFACEFORCE']['px_arm(1)'],
                                  config['SURFACEFORCE']['px_arm(2)']]
    position_vector_surface[1] = [config['SURFACEFORCE']['mx_arm(0)'],
                                  config['SURFACEFORCE']['mx_arm(1)'],
                                  config['SURFACEFORCE']['mx_arm(2)']]
    position_vector_surface[2] = [config['SURFACEFORCE']['py_arm(0)'],
                                  config['SURFACEFORCE']['py_arm(1)'],
                                  config['SURFACEFORCE']['py_arm(2)']]
    position_vector_surface[3] = [config['SURFACEFORCE']['my_arm(0)'],
                                  config['SURFACEFORCE']['my_arm(1)'],
                                  config['SURFACEFORCE']['my_arm(2)']]
    position_vector_surface[4] = [config['SURFACEFORCE']['pz_arm(0)'],
                                  config['SURFACEFORCE']['pz_arm(1)'],
                                  config['SURFACEFORCE']['pz_arm(2)']]
    position_vector_surface[5] = [config['SURFACEFORCE']['mz_arm(0)'],
                                  config['SURFACEFORCE']['mz_arm(1)'],
                                  config['SURFACEFORCE']['mz_arm(2)']]
    sff_area = np.zeros(6)
    sff_area[:] = [config['SURFACEFORCE']['area(0)'],
                   config['SURFACEFORCE']['area(1)'],
                   config['SURFACEFORCE']['area(2)'],
                   config['SURFACEFORCE']['area(3)'],
                   config['SURFACEFORCE']['area(4)'],
                   config['SURFACEFORCE']['area(5)']]

    sff_vector = np.zeros((6, 3))
    sff_vector[0] = [config['SURFACEFORCE']['px_normal(0)'],
                     config['SURFACEFORCE']['px_normal(1)'],
                     config['SURFACEFORCE']['px_normal(2)']]
    sff_vector[1] = [config['SURFACEFORCE']['mx_normal(0)'],
                     config['SURFACEFORCE']['mx_normal(1)'],
                     config['SURFACEFORCE']['mx_normal(2)']]
    sff_vector[2] = [config['SURFACEFORCE']['py_normal(0)'],
                     config['SURFACEFORCE']['py_normal(1)'],
                     config['SURFACEFORCE']['py_normal(2)']]
    sff_vector[3] = [config['SURFACEFORCE']['my_normal(0)'],
                     config['SURFACEFORCE']['my_normal(1)'],
                     config['SURFACEFORCE']['my_normal(2)']]
    sff_vector[4] = [config['SURFACEFORCE']['pz_normal(0)'],
                     config['SURFACEFORCE']['pz_normal(1)'],
                     config['SURFACEFORCE']['pz_normal(2)']]
    sff_vector[5] = [config['SURFACEFORCE']['mz_normal(0)'],
                     config['SURFACEFORCE']['mz_normal(1)'],
                     config['SURFACEFORCE']['mz_normal(2)']]

    sff_center = np.zeros(3)
    sff_center[0] = config['SURFACEFORCE']['center(0)']
    sff_center[1] = config['SURFACEFORCE']['center(1)']
    sff_center[2] = config['SURFACEFORCE']['center(2)']

    sff_properties = {'sff_position': position_vector_surface,
                      'sff_area': sff_area,
                      'sff_vector': sff_vector,
                      'sff_center': sff_center}

    disturbance_properties = {'GRA': grav_properties,
                              'ADRAG': atmdrag_properties,
                              'SFF': sff_properties}
    return disturbance_properties
