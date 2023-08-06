"""
Unit tests for point
"""
from unittest import TestCase
import numpy as np
from geometry import Point


class TestPoint(TestCase):
    """
     Polygon test class
     """

    def test_positive_distance_to_point(self):
        """
        Test distance to point
        :return:
        """
        point = Point(np.array([10, 5]))
        distance = point.distance_to_point(Point(np.array([20, 15])))
        self.assertEqual(distance, 14.142135623730951)

    def test_negative_distance_to_point(self):
        """
        Test negative distance to point
        :return:
        """
        point = Point(np.array([-10, -5]))
        distance = point.distance_to_point(Point(np.array([20, -15])))
        self.assertEqual(distance, 31.622776601683793)

    def test_wrong_distance_to_point(self):
        """
        Test invoking distance to point with wrong data
        :return:
        """
        point = Point(np.array([11, 5]))
        distance = point.distance_to_point(np.array([20, 15]))
        self.assertEqual(distance, None)

    def test_list_distance_to_point(self):
        """
        Test invoking distance to point with wrong data
        :return:
        """
        point = Point([11, 5])
        distance = point.distance_to_point(np.array([20, 15]))
        self.assertIsNone(distance)
