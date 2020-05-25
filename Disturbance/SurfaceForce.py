"""
Created by:

@author: Elias Obreque
els.obrq@gmail.com

ref:
 -
"""


import numpy as np


class SurfaceForce(object):
    def __init__(self, surface_properties):
        self.position_vector_face = surface_properties['sff_position']
        self.surface_area = surface_properties['sff_area']
        self.normal_vector_face = surface_properties['sff_vector']
        self.mass_center = surface_properties['sff_center']
        self.cos_theta = np.zeros(6)
        self.sen_theta = np.zeros(6)
        self.force_vector_b = np.zeros(3)
        self.torque_vector_b = np.zeros(3)
        self.condition_ = None

    def calc_force_torque_vector_b(self, parameter_b_norm, Cp, Ct):
        # Tangent force:
        # Normal vector from the plane between velocity and vector area
        vector_to_plane = np.cross(parameter_b_norm,
                                   self.normal_vector_face[self.condition_, :])
        if np.all(vector_to_plane == 0):
            norm_vector_to_plane = np.zeros(3)
        else:
            norm_vector_to_plane = 1/np.linalg.norm(vector_to_plane, axis=1)
            norm_vector_to_plane = norm_vector_to_plane.reshape((norm_vector_to_plane.size, 1))
        unit_vector_to_plane = vector_to_plane * norm_vector_to_plane
        unit_tang_vector = np.cross(unit_vector_to_plane, self.normal_vector_face[self.condition_, :])
        unit_normal_vector = - self.normal_vector_face[self.condition_, :]
        normal_vector_b = unit_normal_vector * self.surface_area[self.condition_].reshape(Cp.size,
                                                                                          1) * Cp.reshape((Cp.size, 1))
        tang_vector_b = unit_tang_vector * self.surface_area[self.condition_].reshape(Cp.size,
                                                                                      1)  * Ct.reshape((Ct.size, 1))
        forces_vectors = (normal_vector_b + tang_vector_b)
        unit_torque_b = np.cross(self.position_vector_face[self.condition_] - self.mass_center, forces_vectors)
        self.force_vector_b = np.sum(forces_vectors, axis=0)
        self.torque_vector_b = np.sum(unit_torque_b, axis=0)

    def calc_ang_parameters(self, input_b_norm):
        self.cos_theta = np.inner(self.normal_vector_face, input_b_norm)
        self.sen_theta = np.sqrt(1 - self.cos_theta ** 2)
        self.condition_ = np.array(self.cos_theta > 0.0)

