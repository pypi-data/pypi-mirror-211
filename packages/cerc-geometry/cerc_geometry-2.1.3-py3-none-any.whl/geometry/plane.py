"""
Plane module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from typing import TypeVar
import sys
import numpy as np


Point = TypeVar('Point')


class Plane:
    """
    Plane class
    """

    def __init__(self, origin, normal):
        self._origin = origin
        self._normal = normal
        self._equation = None
        self._opposite_normal = None

    @property
    def origin(self) -> Point:
        """
        Get plane origin point
        :return: Point
        """
        return self._origin

    @property
    def normal(self):
        """
        Get plane normal [x, y, z]
        :return: np.ndarray
        """
        return self._normal

    @property
    def equation(self) -> (float, float, float, float):
        """
        Get the plane equation components Ax + By + Cz + D = 0
        :return: (A, B, C, D)
        """
        try:
            if self._equation is None:
                a_value = self.normal[0]
                b_value = self.normal[1]
                c_value = self.normal[2]
                d_value = -1 * self.origin.coordinates[0] * self.normal[0]
                d_value += -1 * self.origin.coordinates[1] * self.normal[1]
                d_value += -1 * self.origin.coordinates[2] * self.normal[2]
                self._equation = (a_value, b_value, c_value, d_value)
            return self._equation
        except IndexError as error:
            sys.stderr.write(f'You provided incorrect coordinates: {error}')
            return None

    def distance_to_point(self, point):
        """
        Distance between the given point and the plane
        :return: float
        """
        point_copy = point
        equation = self.equation
        denominator = np.abs((point_copy[0] * equation[0]) +
                             (point_copy[1] * equation[1]) + (point_copy[2] * equation[2]) + equation[3])
        numerator = np.sqrt((equation[0] ** 2) + (equation[1] ** 2) + (equation[2] ** 2))
        return float(denominator / numerator)

    @property
    def opposite_normal(self):
        """
        get plane normal in the opposite direction [x, y, z]
        :return: np.ndarray
        """
        if self._opposite_normal is None:
            coordinates = []
            for coordinate in self.normal:
                coordinates.append(-coordinate)
            self._opposite_normal = np.array(coordinates)
        return self._opposite_normal
