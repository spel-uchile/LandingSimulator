
from .InitGyro import InitGyro
from .InitThruster import InitThruster


class InitComponents(object):
    def __init__(self, properties,  prop_step):

        init_gyro = None
        init_obc = None
        init_power = None
        init_thruster = None

        components_init = {'gyro_flag': init_gyro,
                           'obc_flag': init_obc,
                           'power_flag': init_power,
                           'thruster_flag': init_thruster}

        self.gyro_properties    = None
        self.obc_properties     = None
        self.power_properties   = None
        self.thruster_properties = None
        self.gps_properties     = None
        self.temperature_properties = None
        self.thermal_actuator_properties = None
        self.camera_properties = None
        self.antenna_properties = None

        path = properties['path_com']

        if properties['gyro_flag']:
            self.gyro_properties = InitGyro(path).gyro_properties
        if properties['obc_flag']:
            k = 0
        if properties['power_flag']:
            k = 0
        if properties['thruster_flag']:
            self.thruster_properties = InitThruster(path, prop_step).thruster_properties
