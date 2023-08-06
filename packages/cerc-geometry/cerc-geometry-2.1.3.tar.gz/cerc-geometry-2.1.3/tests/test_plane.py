"""
Unit tests for plane
"""
from unittest import TestCase
import numpy as np
from geometry import Plane
from geometry import Point


class TestPlane(TestCase):
    """
    Plane test class
    """

    def setUp(self) -> None:
        """
        Set up for tests
        :return: None
        """
        self.plane = Plane(Point(np.array([10, 5, 6])), [2, 3, 5])

    def test_opposite_normal(self):
        """
        test for plan normal
        :return:
        """
        self.assertEqual(self.plane.opposite_normal[0], -2)
        self.assertEqual(self.plane.opposite_normal[2], -5)
        self.assertEqual(self.plane.origin.coordinates[1], 5)
        self.assertNotEqual(self.plane.opposite_normal[1], 3)

    def test_equation(self):
        """
        Test plane equations
        :return:
        """
        self.assertTupleEqual(self.plane.equation, tuple([2, 3, 5, -65]))

    def test_equation_with_wrong_coordinates(self):
        """
        test equation with wrong coordinate values
        :return:
        """
        plane = Plane(Point(np.array([5, 6])), [2, 3, 5])
        self.assertIsNone(plane.equation)
