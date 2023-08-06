"""
Geometry helper
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
Code contributors: Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
import math
from pathlib import Path

import numpy as np
from PIL import Image
from trimesh import Trimesh
from trimesh import intersections
from geometry.polygon import Polygon
from geometry.polyhedron import Polyhedron
from geometry.location import Location
from geometry.map_point import MapPoint


class Library:
    """
    Geometry helper class
    """
    # todo: complete dictionary
    srs_transformations = {
        'urn:adv:crs:ETRS89_UTM32*DE_DHHN92_NH': 'epsg:25832'
    }

    @staticmethod
    def factor():
        """
      Returns factor
      :return:
      """
        return 0.5

    def __init__(self, delta=0, area_delta=0):
        self._delta = delta
        self._area_delta = area_delta

    @staticmethod
    def coordinate_to_map_point(coordinate, city):
        """
        Convert coordinate to map points
        :param coordinate: list of coordinates
        :param city: city object
        :return: MapPoint
        """
        factor = Library.factor()
        return MapPoint(((coordinate[0] - city.lower_corner[0]) * factor),
                        ((coordinate[1] - city.lower_corner[1]) * factor))

    @staticmethod
    def city_mapping(city, building_names=None, plot=False):

        """
        Returns a shared_information dictionary like
        {
         "building_name" : [{line: 0 coordinate_1: [x,y,z], coordinate_2:[x, y, z], points: 0}]
        }
        """
        lines_information = {}
        if building_names is None:
            building_names = [b.name for b in city.buildings]
        factor = Library.factor()
        x_value = math.ceil((city.upper_corner[0] - city.lower_corner[0]) * factor) + 1
        y_value = math.ceil((city.upper_corner[1] - city.lower_corner[1]) * factor) + 1
        city_map = [['' for _ in range(y_value + 1)] for _ in range(x_value + 1)]
        map_info = [[{} for _ in range(y_value + 1)] for _ in range(x_value + 1)]
        img = Image.new('RGB', (x_value + 1, y_value + 1), "black")  # create a new black image
        city_image = img.load()  # create the pixel map
        for building_name in building_names:
            building = city.city_object(building_name)
            line = 0
            for ground in building.grounds:
                length = len(ground.perimeter_polygon.coordinates) - 1
                for i, coordinate in enumerate(ground.perimeter_polygon.coordinates):

                    j = i + 1
                    if i == length:
                        j = 0
                    next_coordinate = ground.perimeter_polygon.coordinates[j]
                    distance = Library.distance_between_points(coordinate, next_coordinate)
                    steps = int(distance * factor * 2)
                    if steps == 0:
                        continue
                    delta_x = (next_coordinate[0] - coordinate[0]) / steps
                    delta_y = (next_coordinate[1] - coordinate[1]) / steps

                    for k in range(0, steps):
                        new_coordinate = (coordinate[0] + (delta_x * k),
                                          coordinate[1] + (delta_y * k))
                        point = Library.coordinate_to_map_point(new_coordinate, city)
                        x_value = point.x
                        y_value = point.y
                        if city_map[x_value][y_value] == '':
                            city_map[x_value][y_value] = building.name
                            map_info[x_value][y_value] = {
                                'line_start': (coordinate[0], coordinate[1]),
                                'line_end': (next_coordinate[0], next_coordinate[1]),
                            }
                            city_image[x_value, y_value] = (100, 0, 0)
                        elif city_map[x_value][y_value] != building.name:
                            neighbour = city.city_object(city_map[x_value][y_value])
                            neighbour_info = map_info[x_value][y_value]

                            # prepare the keys
                            neighbour_start_coordinate = \
                              f'{Library.coordinate_to_map_point(neighbour_info["line_start"], city)}'
                            building_start_coordinate = \
                              f'{Library.coordinate_to_map_point(coordinate, city)}'
                            neighbour_key = f'{neighbour.name}_{neighbour_start_coordinate}' \
                                            f'_{building_start_coordinate}'
                            building_key = f'{building.name}_{building_start_coordinate}' \
                                           f'_{neighbour_start_coordinate}'

                            # Add my neighbour info to my shared lines
                            if building.name in lines_information.keys() and neighbour_key in \
                                lines_information[building.name]:
                                shared_points = \
                                  int(lines_information[building.name][neighbour_key]['shared_points'])
                                lines_information[building.name][neighbour_key]['shared_points'] = \
                                  shared_points + 1
                            else:
                                if building.name not in lines_information.keys():
                                    lines_information[building.name] = {}
                                lines_information[building.name][neighbour_key] = {
                                    'neighbour_name': neighbour.name,
                                    'line_start': (coordinate[0], coordinate[1]),
                                    'line_end': (next_coordinate[0], next_coordinate[1]),
                                    'neighbour_line_start': neighbour_info['line_start'],
                                    'neighbour_line_end': neighbour_info['line_end'],
                                    'coordinate_start':
                                      f"{Library.coordinate_to_map_point(coordinate, city)}",
                                    'coordinate_end':
                                      f"{Library.coordinate_to_map_point(next_coordinate, city)}",
                                    'neighbour_start':
                                      f"{Library.coordinate_to_map_point(neighbour_info['line_start'], city)}",
                                    'neighbour_end':
                                      f"{Library.coordinate_to_map_point(neighbour_info['line_end'], city)}",
                                    'shared_points': 1
                                }

                            # Add my info to my neighbour shared lines
                            if neighbour.name in lines_information.keys() and building_key in \
                                lines_information[neighbour.name]:
                                shared_points = \
                                  int(lines_information[neighbour.name][building_key]['shared_points'])
                                lines_information[neighbour.name][building_key]['shared_points'] = \
                                  shared_points + 1
                            else:
                                if neighbour.name not in lines_information.keys():
                                    lines_information[neighbour.name] = {}
                                lines_information[neighbour.name][building_key] = {
                                    'neighbour_name': building.name,
                                    'line_start': neighbour_info['line_start'],
                                    'line_end': neighbour_info['line_end'],
                                    'neighbour_line_start': (coordinate[0], coordinate[1]),
                                    'neighbour_line_end': (next_coordinate[0], next_coordinate[1]),
                                    'neighbour_start':
                                      f"{Library.coordinate_to_map_point(coordinate, city)}",
                                    'neighbour_end':
                                      f"{Library.coordinate_to_map_point(next_coordinate, city)}",
                                    'coordinate_start':
                                      f"{Library.coordinate_to_map_point(neighbour_info['line_start'], city)}",
                                    'coordinate_end':
                                      f"{Library.coordinate_to_map_point(neighbour_info['line_end'], city)}",
                                    'shared_points': 1
                                }

                            if building.neighbours is None:
                                building.neighbours = [neighbour]
                            elif neighbour not in building.neighbours:
                                building.neighbours.append(neighbour)
                            if neighbour.neighbours is None:
                                neighbour.neighbours = [building]
                            elif building not in neighbour.neighbours:
                                neighbour.neighbours.append(building)
                    line += 1

        if plot:
            img.show()
        return lines_information

    @staticmethod
    def segment_list_to_trimesh(lines) -> Trimesh:
        """
        Transform a list of segments into a Trimesh
        """
        # todo: trimesh has a method for this
        line_points = [lines[0][0], lines[0][1]]
        lines.remove(lines[0])
        while len(lines) > 1:
            i = 0
            for line in lines:
                i += 1
                if Library.distance_between_points(
                    line[0], line_points[len(line_points) - 1]) < 1e-8:
                    line_points.append(line[1])
                    lines.pop(i - 1)
                    break
                if Library.distance_between_points(
                    line[1], line_points[len(line_points) - 1]) < 1e-8:
                    line_points.append(line[0])
                    lines.pop(i - 1)
                    break
        polyhedron = Polyhedron(Polygon(line_points).triangles)
        trimesh = Trimesh(polyhedron.vertices, polyhedron.faces)
        return trimesh

    @staticmethod
    def _merge_meshes(mesh1, mesh2):
        v_1 = mesh1.vertices
        f_1 = mesh1.faces
        v_2 = mesh2.vertices
        f_2 = mesh2.faces
        length = len(v_1)
        v_merge = np.concatenate((v_1, v_2))
        f_merge = np.asarray(f_1)

        for item in f_2:
            point1 = item.item(0) + length
            point2 = item.item(1) + length
            point3 = item.item(2) + length
            surface = np.asarray([point1, point2, point3])
            f_merge = np.concatenate((f_merge, [surface]))

        mesh_merge = Trimesh(vertices=v_merge, faces=f_merge)
        mesh_merge.fix_normals()

        return mesh_merge

    @staticmethod
    def divide_mesh_by_plane(trimesh, normal_plane, point_plane):
        """
        Divide a mesh by a plane
        :param trimesh: Trimesh
        :param normal_plane: [x, y, z]
        :param point_plane: [x, y, z]
        :return: [Trimesh]
        """
        # The first mesh returns the positive side of the plane and the second the negative side.
        # If the plane does not divide the mesh
        # (i.e. it does not touch it or it is coplanar with one or more faces),
        # then it returns only the original mesh.
        # todo: review split method in https://github.com/mikedh/trimesh/issues/235,
        #  once triangulate_polygon in Polygon class is solved

        normal_plane_opp = [None] * len(normal_plane)
        for i, plane in enumerate(normal_plane):
            normal_plane_opp[i] = - plane

        section_1 = intersections.slice_mesh_plane(trimesh, normal_plane, point_plane)
        if section_1 is None:
            return [trimesh]
        lines = list(intersections.mesh_plane(trimesh, normal_plane, point_plane))
        cap = Library.segment_list_to_trimesh(lines)
        trimesh_1 = Library._merge_meshes(section_1, cap)

        section_2 = intersections.slice_mesh_plane(trimesh, normal_plane_opp, point_plane)
        if section_2 is None:
            return [trimesh_1]
        trimesh_2 = Library._merge_meshes(section_2, cap)

        return [trimesh_1, trimesh_2]

    @staticmethod
    def get_location(latitude, longitude) -> Location:
        """
        Get Location from latitude and longitude
        """
        _data_path = Path(Path(__file__).parent / 'data/geolocation/cities15000.txt').resolve()
        latitude = float(latitude)
        longitude = float(longitude)
        distance = math.inf
        country = 'Unknown'
        city = 'Unknown'
        with open(_data_path, 'r', encoding='utf-8') as data_file:
            for _, line in enumerate(data_file):
                fields = line.split('\t')
                file_city_name = fields[2]
                file_latitude = float(fields[4])
                file_longitude = float(fields[5])
                file_country_code = fields[8]
                new_distance = math.sqrt(pow((latitude - file_latitude), 2)
                                         + pow((longitude - file_longitude), 2))
                if distance > new_distance:
                    distance = new_distance
                    country = file_country_code
                    city = file_city_name
        return Location(country, city)

    @staticmethod
    def distance_between_points(vertex1, vertex2):
        """
        distance between points in an n-D Euclidean space
        :param vertex1: point or vertex
        :param vertex2: point or vertex
        :return: float
        """
        power = 0
        for dimension, vertex in enumerate(vertex1):
            power += math.pow(vertex2[dimension] - vertex, 2)
        distance = math.sqrt(power)
        return distance
