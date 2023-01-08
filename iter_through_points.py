from shapely import affinity
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.spatial import Delaunay


# converting from np.array to list
def nparray_to_array(np_points):
    point_arr = []
    for i, val in enumerate(np_points):
        point_arr.append(Point((np_points[i][0]), (np_points[i][1])))
    return point_arr


# converting from point to values
def extract_point_shapely(point):
    return [point.x, point.y]


def calculate_vector(points):
    p1 = points[-1]
    p2 = points[-2]

    vx = p1.x - p2.x
    vy = p1.y - p2.y
    return [vx, vy]


# coloring triangles that satisfy the conditions
def color_triangles(triangles, points):
    for triangle in triangles:
        x = [points[i][0] for i in triangle]
        y = [points[i][1] for i in triangle]
        plt.fill(x, y, color='red')


# calculating angle between 3 last points
def calculate_angle(points):
    p1 = points[-1]
    p2 = points[-3]
    p3 = points[-2]

    p12 = math.sqrt((p3.x-p1.x)**2 + (p3.y-p1.y)**2)
    p23 = math.sqrt((p1.x-p2.x)**2 + (p1.y-p2.y)**2)
    p13 = math.sqrt((p3.x-p2.x)**2 + (p3.y-p2.y)**2)

    radians = np.arccos((p12**2 + p13**2 - p23**2)/(2 * p12 * p13))

    # print(p12, p13, p23)
    radians = math.pi - radians
    # angle = radians*(180/math.pi)

    # checking angle side
    if ((p3.x - p1.x)*(p2.y - p1.y) -
            (p3.y - p1.y)*(p2.x - p1.x)) > 0:
        radians = -radians
    return radians


def find_triangles(all_points, point_instance, exclude_point, max_side_length):
    point = [point_instance.x, point_instance.y]

    triangulation = Delaunay(all_points)
    triangles = []
    distances = []
    points = []
    u_points = []
    xs, ys = [], []
    for triangle in triangulation.simplices:
        if point in all_points[triangle] and exclude_point not in all_points[triangle]:
            sides = [(all_points[triangle[0]], all_points[triangle[1]]),
                     (all_points[triangle[1]], all_points[triangle[2]]),
                     (all_points[triangle[2]], all_points[triangle[0]])]
            skip_triangle = False
            for side in sides:
                distance = np.linalg.norm(side[0] - side[1])
                if distance > max_side_length:
                    skip_triangle = True
                    break
            if skip_triangle:
                continue
            triangles.append(triangle)
            for p in all_points[triangle]:
                distance = np.linalg.norm(point - p)
                distances.append(distance)
                points.append(p)
            u_points = np.unique(points, axis=0)

    for p, val in enumerate(u_points):
        distance = np.linalg.norm(point - val)
        distances.append(distance)
        xs.append(u_points[p][0])
        ys.append(u_points[p][1])

    point_instance.tri_x = xs
    point_instance.tri_y = ys
    point_instance.distances = distances

    color_triangles(triangles, all_points)
    plt.triplot(all_points[:, 0], all_points[:, 1], triangulation.simplices)
    return triangles, distances, u_points


# this class defines a structure that holds a position, possible next cones from triangulation, and distances
class Cone:
    def __init__(self, x, y, tri_x=None, tri_y=None, tri_distances=None, index=None):
        self.x = x
        self.y = y
        self.tri_x = tri_x
        self.tri_y = tri_y
        self.tri_distances = tri_distances
        self.index = index


# this class is responsible for classification of one side. it can be invoked for both sides.
class Classification:
    def __init__(self, in_points, in_side, max_side, cones_list):
        self.in_points = in_points
        self.in_side = in_side
        self.max_side = max_side
        self.cones_list = cones_list
        # shape
        self.zone = Polygon([[0.0, 1], [5, 1], [30, 30], [30, 42], [20, 47], [10, 50],
                             [0, 51], [-10, 50], [-20, 47], [-30, 42], [-30, 30], [-5, 1]])
        self.zone = affinity.scale(self.zone, xfact=0.1, yfact=0.1, origin=(0, 0))
        self.cones = []

    # adding points in the beginning to simplify moving across points
    def side_check(self, side):
        if side is 'RIGHT':
            start_right_1 = Cone(1.5, -1.0)
            start_right_2 = Cone(1.5, -.8)
            start_right_3 = Cone(1.5, -.6)
            self.cones.append(start_right_1)
            self.cones.append(start_right_2)
            self.cones.append(start_right_3)
        elif side is 'LEFT':
            start_left_1 = Cone(-1.5, -1.0)
            start_left_2 = Cone(-1.5, -.8)
            start_left_3 = Cone(-1.5, -.6)
            self.cones.append(start_left_1)
            self.cones.append(start_left_2)
            self.cones.append(start_left_3)

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

        # print(distances)
        closest = distances.index(min(distances))
        closest_point = points_inside_polygon[closest]
        x, y = extract_point_shapely(closest_point)
        next_cone = Cone(x, y)
        self.cones.append(next_cone)
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

    def detect_first(self):
        # self.plot(self.in_points)
        self.side_check(self.in_side)
        self.move_poly([self.cones[-1].x, self.cones[-1].y], 0, [self.cones[-3].x, self.cones[-3].y])
        # print(self.in_side)

    def run(self):
        try:
            # self.plot(self.in_points)
            vector = calculate_vector(self.cones)
            rads = calculate_angle(self.cones)

            self.move_poly(vector, rads, [self.cones[-1].x, self.cones[-1].y])
            self.points_inside(self.in_points)
            find_triangles(self.in_points, self.cones[-1], [self.cones[-2].x, self.cones[-2].y], self.max_side)

            # self.plot(self.in_points)
            # print(self.in_side)
            return False
        except ValueError:
            print('end of sequence')
            return True


CONES_RIGHT = []
CONES_LEFT = []

POINTS_TEST_1 = np.array([[13.099135578175783, 17.721805070425326], [10.516033859075476, 21.199963420584364],
                          [14.961893804916489, 22.727814637806297], [7.822690731937084, 18.133058987854778],
                          [9.971461358072586, 15.35586889780742], [4.7083579870335726, 15.56139968809873],
                          [6.969509498121127, 12.925172489258221], [1.7121513788600975, 12.292570239941853],
                          [4.535207314707911, 10.361157497135585], [2.7561998824527514, 7.061895071080194],
                          [-0.1852417858437594, 8.300137553811966], [-1.8610559324936222, 4.429225562891993],
                          [1.5143610646256143, 3.7245553594928786], [1.2516181776130075, 0.2805800147314983],
                          [-2.25711740307967, 0.4176005415923676]])

right = Classification(POINTS_TEST_1, 'RIGHT', 6, CONES_RIGHT)
left = Classification(POINTS_TEST_1, 'LEFT', 6, CONES_LEFT)
left.detect_first()
right.detect_first()

while True:
    if right.run() is True: break
    if left.run() is True: break
