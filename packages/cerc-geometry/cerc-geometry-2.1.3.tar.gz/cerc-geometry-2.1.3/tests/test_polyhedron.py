"""
Unit tests for polyhedron
"""

from unittest import TestCase
import numpy as np
from geometry import Polyhedron
from geometry import Polygon


class TestPolyhedron(TestCase):
    """
    Polyhedron test class
    """

    def setUp(self) -> None:
        """
        Set up for tests
        :return: None
        """
        self._vertices = [
            [0, 0, 1000], [1000, 0, 1000],
            [5000, 1000, 1000], [0, 1000, 1000],
            [0, 0, 0], [1000, 0, 0],
            [1000, 1000, 0], [0, 1000, 2500]
        ]
        polygon_2 = Polygon(np.array(self._vertices))
        self.polyhedron = Polyhedron([polygon_2])

    def test_polyhedron_properties(self):
        """
        Test polyhedron properties
        :return:
        """
        self.assertEqual(self.polyhedron.max_x, 5000)
        self.assertEqual(self.polyhedron.min_x, 0)
        self.assertEqual(self.polyhedron.min_y, 0)
        self.assertEqual(self.polyhedron.max_y, 1000)
        self.assertEqual(self.polyhedron.max_z, 2500)
        self.assertEqual(self.polyhedron.min_z, 0)
        self.assertIsNone(self.polyhedron.centroid)
        self.assertEqual(self.polyhedron.volume, float('inf'))
        self.assertEqual(self.polyhedron.trimesh.area, 0.0)
        self.assertEqual(len(self.polyhedron.trimesh.triangles), 0)
        self.assertEqual(self.polyhedron.trimesh.vertices[0][2], 1000.0)
