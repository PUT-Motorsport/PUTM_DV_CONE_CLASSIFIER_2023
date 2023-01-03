from shapely import affinity
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import numpy as np
import math
# from scipy.spatial import Delaunay


# converting from np.array to list
def nparray_to_array(np_points):
    point_arr = []
    for i, val in enumerate(np_points):
        point_arr.append(Point((np_points[i][0]), (np_points[i][1])))
    return point_arr


# converting from point to values
def extract_point_shapely(point):
    return (point.x, point.y)


def calculate_vector(points):
    p1 = points[-1]
    p2 = points[-2]

    x = p1[0] - p2[0]
    y = p1[1] - p2[1]
    return (x, y)


# calculating angle between 3 last points
def calculate_angle(points):
    p1 = points[-1]
    p2 = points[-3]
    p3 = points[-2]

    p12 = math.sqrt((p3[0]-p1[0])**2 + (p3[1]-p1[1])**2)
    p23 = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
    p13 = math.sqrt((p3[0]-p2[0])**2 + (p3[1]-p2[1])**2)

    radians = np.arccos((p12**2 + p13**2 - p23**2)/(2 * p12 * p13))

    # print(p12, p13, p23)
    radians = math.pi - radians
    # angle = radians*(180/math.pi)

    # checking angle side
    if ((points[-2][0] - points[-1][0])*(points[-3][1] - points[-1][1]) -
            (points[-2][1] - points[-1][1])*(points[-3][0] - points[-1][0])) > 0:
        radians = -radians
    return radians


class Cone:
    def __init__(self):
        pass


class Classification:
    # shape
    zone = Polygon([[0.0, 1], [5, 1], [30, 30], [30, 42], [20, 47], [10, 50],
                    [0, 51], [-10, 50], [-20, 47], [-30, 42], [-30, 30], [-5, 1]])
    zone = affinity.scale(zone, xfact=0.1, yfact=0.1, origin=(0, 0))

    cones = []

    # adding points in the beginning to simplify moving across points
    def side_check(self, side):
        if side is 'RIGHT':
            self.cones.append((1.5, -1.0))
            self.cones.append((1.5, -.8))
            self.cones.append((1.5, -.6))
        elif side is 'LEFT':
            self.cones.append((-1.5, -1.0))
            self.cones.append((-1.5, -.8))
            self.cones.append((-1.5, -.6))

    # returning points in polygon and the closest one
    def points_inside(self, points):
        points = nparray_to_array(points)

        mid = Point(0, 0)
        points_inside_polygon = []
        distances = []

        for i, val in enumerate(points):
            if self.zone.contains(points[i]) is True:
                points_inside_polygon.append(points[i])
                distances.append(mid.distance(points[i]))
        closest = distances.index(min(distances))
        closest_point = points_inside_polygon[closest]

        self.cones.append(extract_point_shapely(closest_point))

        return points_inside_polygon

    def move_poly(self, vector, radians, origin):
        trans_x, trans_y = vector
        self.zone = affinity.translate(self.zone, trans_x, trans_y)
        self.zone = affinity.rotate(self.zone, radians, use_radians=True, origin=origin)
        return self.zone

    def plot(self, points):
        plt.plot(self.zone.exterior.xy[0], self.zone.exterior.xy[1])
        plt.scatter(*zip(*points), color='Black')
        plt.show()

    def __init__(self, in_points, in_side):
        self.plot(in_points)
        self.side_check(in_side)
        print(self.cones)
        self.move_poly(self.cones[-1], 0, self.cones[-3])

        for i in range(100):
            vector = calculate_vector(self.cones)
            rads = calculate_angle(self.cones)

            self.move_poly(vector, rads, self.cones[-1])
            print(self.points_inside(in_points))
            # print(self.cones)

            self.plot(in_points)


POINTS_TEST = np.array([[13.099135578175783, 17.721805070425326], [10.516033859075476, 21.199963420584364],
                        [14.961893804916489, 22.727814637806297], [7.822690731937084, 18.133058987854778],
                        [9.971461358072586, 15.35586889780742], [4.7083579870335726, 15.56139968809873],
                        [6.969509498121127, 12.925172489258221], [1.7121513788600975, 12.292570239941853],
                        [4.535207314707911, 10.361157497135585], [2.7561998824527514, 7.061895071080194],
                        [-0.1852417858437594, 8.300137553811966], [-1.8610559324936222, 4.429225562891993],
                        [1.5143610646256143, 3.7245553594928786], [1.2516181776130075, 0.2805800147314983],
                        [-2.25711740307967, 0.4176005415923676]])

right = Classification(POINTS_TEST, 'RIGHT')
left = Classification(POINTS_TEST, 'LEFT')
