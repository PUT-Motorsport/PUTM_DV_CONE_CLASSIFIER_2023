from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import numpy as np
from shapely import affinity
import math
from scipy.spatial import Delaunay


# returning points in polygon and the closest one
def points_inside(polygon, points):
    mid = Point(0, 0)
    points_inside_polygon = []
    distances = []

    for i, val in enumerate(points):
        if polygon.contains(points[i]) is True:
            points_inside_polygon.append(points[i])
            distances.append(mid.distance(points[i]))

    if distances == []:
        print('finished')
        closest_point = 0
        return points_inside_polygon, closest_point
    closest = distances.index(min(distances))
    print('point', closest)
    print(points_inside_polygon[closest])
    closest_point = points_inside_polygon[closest]

    return points_inside_polygon, closest_point


# converting from point to values
def extract_points_shapely(point_list):
    xs = [point.x for point in point_list]
    ys = [point.y for point in point_list]
    return xs, ys


# rotating function
def rotate_poly(poly, radians, rotate_around):
    r_poly = affinity.rotate(poly, radians, use_radians=True, origin=rotate_around)
    return r_poly


# translating function
def translate_poly(poly, vector):
    trans_x, trans_y = vector
    t_poly = affinity.translate(polygon, trans_x, trans_y)
    return t_poly


# converting from np.array to list
def nparray_to_pointarray(points):
    point_arr = []
    for i, val in enumerate(points):
        point_arr.append(Point((points[i][0]), (points[i][1])))
    return point_arr


# calculating angle between 3 last points
def calculate_angle(points):
    p1 = points[-1]
    p2 = points[-3]
    p3 = points[-2]

    p12 = math.sqrt((p3[0]-p1[0])**2 + (p3[1]-p1[1])**2)
    p23 = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
    p13 = math.sqrt((p3[0]-p2[0])**2 + (p3[1]-p2[1])**2)

    radians = np.arccos((p12**2 + p13**2 - p23**2)/(2 * p12 * p13))

    print(p12, p13, p23)
    radians = math.pi - radians
    angle = radians*(180/math.pi)

    # checking angle side
    if ((points[-2][0] - points[-1][0])*(points[-3][1] - points[-1][1]) -
            (points[-2][1] - points[-1][1])*(points[-3][0] - points[-1][0])) > 0:
        radians = -radians
    return radians


# removing point from list
def remove_point(arr1, point_to_remove):
    arr2 = np.array([[point_to_remove[0], point_to_remove[1]]])
    delta = set(map(tuple, arr2))
    return np.fromiter((x for xs in arr1 if tuple(xs) not in delta for x in xs),
                       dtype=arr1.dtype).reshape(-1, arr1.shape[-1])

u_points = []
# finding possible next points from triangulation
def findTriangles(triangulation, point, exclude_point, max_side_length):
    triangles = []
    distances = []
    points = []
    for triangle in triangulation.simplices:
        if point in numpy_points[triangle] and exclude_point not in numpy_points[triangle]:

            sides = [(numpy_points[triangle[0]], numpy_points[triangle[1]]),
                     (numpy_points[triangle[1]], numpy_points[triangle[2]]),
                     (numpy_points[triangle[2]], numpy_points[triangle[0]])]
            skip_triangle = False
            for side in sides:
                distance = np.linalg.norm(side[0] - side[1])
                if distance > max_side_length:
                    skip_triangle = True
                    break
            if skip_triangle:
                continue
            triangles.append(triangle)
            for p in numpy_points[triangle]:
                # distance = np.linalg.norm(point - p)
                # distances.append(distance)
                points.append(p)

            u_points = np.unique(points, axis=0)
            print(u_points, 'asdjoaijdoasijdoa')

    for p in u_points:
        distance = np.linalg.norm(point - p)
        distances.append(distance)

    return triangles, distances, np.unique(points, axis=0)


# adding new points after initial 2
def next_right_point(right_closest_point):
    right_rads = calculate_angle(right_cones)
    right_vector = right_closest_point

    third_right_shape = translate_poly(second_right_shape, right_vector)
    third_right_shape = rotate_poly(third_right_shape, right_rads, right_vector)
    right_points_in, right_closest = points_inside(third_right_shape, points)
    if right_closest == 0:
        return 1
    right_ex_points = extract_points_shapely(right_points_in)
    right_closest_point = (right_closest.x, right_closest.y)  # next point to go to
    right_cones.append(right_closest_point)

    print(right_cones, ' right')

    # right_triangles, right_triangles_distances, right_triangles_points = \
    #     findTriangles(tri, right_cones[-1], right_cones[-2], 60)
    # right_memory_1 = [right_triangles, right_triangles_distances, right_triangles_points]

    plt.scatter(*zip(*numpy_points), color='Black')
    # color_triangles(right_triangles)
    plt.scatter(right_ex_points[0], right_ex_points[1])
    plt.plot(third_right_shape.exterior.xy[0], third_right_shape.exterior.xy[1])
    plt.show()


def next_left_point(left_closest_point):

    left_rads = calculate_angle(left_cones)
    left_vector = left_closest_point

    third_left_shape = translate_poly(second_left_shape, left_vector)
    third_left_shape = rotate_poly(third_left_shape, left_rads, left_vector)
    left_points_in, left_closest = points_inside(third_left_shape, points)
    if left_closest == 0:
        return 1
    left_ex_points = extract_points_shapely(left_points_in)
    left_closest_point = (left_closest.x, left_closest.y)  # next point to go to
    left_cones.append(left_closest_point)
    print(left_cones, ' left')


def color_triangles(triangles):
    for triangle in triangles:
        x = [numpy_points[i][0] for i in triangle]
        y = [numpy_points[i][1] for i in triangle]
        plt.fill(x, y, color='red')


# shape
polygon = Polygon([[0.0, 1], [5, 1], [40, 30], [30, 42], [20, 47], [10, 50],
                   [0, 51], [-10, 50], [-20, 47], [-30, 42], [-40, 30], [-5, 1]])
polygon = affinity.scale(polygon, xfact=1, yfact=1, origin=(0,0))


# numpy_points = np.array([[-239.2, 121.9],
#                          [-190.7, 140.6],
#                          [-138.3, 137.9],
#                          [-88.7, 160.6],
#                          [-35.9, 151.4],
#                          [-5.4, 106.7],
#                          [12.6, 55.0],
#                          [14.9, 0.],
#                          [-14.9, -0.],
#                          [-18.6, 62.],
#                          [-44.2, 118.6],
#                          [-101.2, 125.9],
#                          [-157.1, 101.5],
#                          [-215.3, 103.82]])
numpy_points = np.array([[-136.3,  256.],
                         [-125.8,  255.],
                         [-115.5,  253.],
                         [-105.6,  249.],
                         [-96.2,  245.],
                         [-87.4,  239.],
                         [-79.5,  232.],
                         [-72.5,  224.],
                         [-65.2,  217.],
                         [-57.3,  210.],
                         [-48.7,  204.],
                         [-39.6,  198.],
                         [-30.8,  193.],
                         [-22.3,  187.],
                         [-14.1,  180.],
                         [-6.4,  173.],
                         [-0.3,  164.],
                         [3.4,  154.],
                         [4.8,  144.],
                         [5.9,  134.],
                         [7.3,  123.],
                         [9.,  113.],
                         [11.4,  103.],
                         [14.4,   93.],
                         [17.3,   82.],
                         [19.8,   72.],
                         [21.9,   62.],
                         [23.1,   52.],
                         [22.9,   41.],
                         [21.5,   31.],
                         [18.9,   20.],
                         [15.9,   10.],
                         [15.,   -0.],
                         [-15.,    0.],
                         [-14.,   10.],
                         [-13.,   21.],
                         [-9.,   30.],
                         [-7.,   41.],
                         [-7.,   51.],
                         [-8.,   61.],
                         [-11.,   71.],
                         [-13.,   81.],
                         [-17.,   91.],
                         [-19.,  101.],
                         [-21.,  111.],
                         [-23.,  122.],
                         [-24.,  132.],
                         [-25.,  142.],
                         [-28.,  152.],
                         [-36.,  159.],
                         [-44.,  165.],
                         [-52.,  171.],
                         [-61.,  176.],
                         [-70.,  182.],
                         [-78.,  188.],
                         [-86.,  195.],
                         [-93.,  202.],
                         [-100.,  210.],
                         [-108.,  217.],
                         [-117.,  222.],
                         [-127.,  225.],
                         [-138.,  226.]])

points = nparray_to_pointarray(numpy_points)

plt.scatter(*zip(*numpy_points), color='Black')
plt.show()
start_point = (0, 0)


# start sequence:  get the first cone on the right and rotate 90 degrees to get the second point,
# after that we can get angle between 3 points (one being imaginary, right behind the first cone) and go on from there
# right
# triangulation
# tri = Delaunay(numpy_ponts)

# first cone variables
right_cones = [(15, -5)]
right_vector = start_point
right_deg90 = -math.pi/2

# moving shape
right_shape = translate_poly(polygon, right_vector)
right_shape = rotate_poly(right_shape, right_deg90, right_vector)

# choosing next point with shape
right_points_in, right_closest = points_inside(right_shape, points)
print(right_closest)

right_ex_points = extract_points_shapely(right_points_in)

right_closest_point = (right_closest.x, right_closest.y)  # next point to go to
right_cones.append(right_closest_point)

# # triangulation memory
# right_triangles, right_triangles_distances, right_triangles_points = \
#     findTriangles(tri, right_cones[-1], numpy_points[4], 60)
# right_memory_1 = [right_triangles, right_triangles_distances, right_triangles_points]

print(right_closest_point, ' right')
# color_triangles(right_triangles)

# plot
plt.scatter(right_ex_points[0], right_ex_points[1])
plt.plot(right_shape.exterior.xy[0], right_shape.exterior.xy[1])
plt.show()

#  moving shape
right_vector = right_closest_point
second_right_shape = translate_poly(right_shape, right_vector)
second_right_shape = rotate_poly(second_right_shape, 0, right_vector)
plt.scatter(*zip(*numpy_points), color='Black')
plt.plot(second_right_shape.exterior.xy[0], second_right_shape.exterior.xy[1])
plt.show()

# choosing next point with shape
right_points_in, right_closest = points_inside(second_right_shape, points)
right_ex_points = extract_points_shapely(right_points_in)
print(right_closest,'aaa')
right_closest_point = (right_closest.x, right_closest.y)  # next point to go to

# # triangulation memory
# right_triangles, right_triangles_distances, right_triangles_points = \
#     findTriangles(tri, right_cones[-1], numpy_points[-2], 60)
# right_memory_1 = [right_triangles, right_triangles_distances, right_triangles_points]

# appending cones
right_cones.append(right_closest_point)

print(right_closest_point, ' right')
print(right_cones, '##################################################################################################')
# print(calculate_angle(right_cones))

# plot
# color_triangles(right_triangles)
plt.scatter(right_ex_points[0], right_ex_points[1])
plt.plot(second_right_shape.exterior.xy[0], second_right_shape.exterior.xy[1])
plt.show()

# left

# first cone variables
left_cones = [(-15, -1)]
left_vector = start_point
left_deg90 = math.pi/2

# moving shape
left_shape = translate_poly(polygon, left_vector)
left_shape = rotate_poly(left_shape, left_deg90, left_vector)
left_points_in, left_closest = points_inside(left_shape, points)
left_ex_points = extract_points_shapely(left_points_in)

# choosing next point with shape
left_closest_point = (left_closest.x, left_closest.y)  # next point to go to
left_cones.append(left_closest_point)

# print(left_closest_point, ' left')
# # plot
# plt.scatter(left_ex_points[0], left_ex_points[1], color='Yellow')
# plt.plot(left_shape.exterior.xy[0], left_shape.exterior.xy[1])
# plt.show()

#  moving shape
left_vector = left_closest_point
second_left_shape = translate_poly(left_shape, left_vector)
second_left_shape = rotate_poly(second_left_shape, 0, left_vector)

# choosing next point with shape
left_points_in, left_closest = points_inside(second_left_shape, points)
left_ex_points = extract_points_shapely(left_points_in)
left_closest_point = (left_closest.x, left_closest.y)  # next point to go to

# appending cones
left_cones.append(left_closest_point)

# print(left_closest_point, ' left')
# print(left_cones)
# print(calculate_angle(left_cones))
#
# # plot
# plt.scatter(left_ex_points[0], left_ex_points[1], color='Yellow')
# plt.plot(second_left_shape.exterior.xy[0], second_left_shape.exterior.xy[1])
# plt.show()

while True:
    if next_right_point(right_cones[-1]) == 1:
        break
    if next_left_point(left_cones[-1]) == 1:
        break

# all points
plt.scatter(*zip(*numpy_points), color='Black')
plt.show()

# divided points
plt.scatter(*zip(*right_cones))
plt.scatter(*zip(*left_cones), color='Yellow')
plt.show()
