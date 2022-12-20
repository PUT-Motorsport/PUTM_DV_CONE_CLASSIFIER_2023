import shapely
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import numpy as np
from shapely import affinity
import math
import time
from scipy.spatial import Delaunay
from iter_through_points import*

'''
Checking if the triangle is locked:
    i can go only to the other vertex of the next triangle
        get possible points to go to                        findTriangles
        get distances to all possible points                findTriangles
        go to the closest point and save rest in memory
        mark point as taken
    other side
        get possible points to go to
        if both points are taken go to previous side and change point to the second closest

        get possible points to go to
        get distances to all possible points
        go to the closest point and save rest in memory
        mark point as taken
'''

#numpy_points = np.array([[-239.28590431227303, 121.98321404586304], [-190.71542073733096, 140.63352377547224], [-138.33644801159795, 137.91706071832806], [-88.71535492871936, 160.60442135514262], [-35.925593893357494, 151.4802087335676], [-5.4383184555142705, 106.75686308185043], [12.692113868883062, 55.09782223305757], [14.99999930125987, 0.004578449893607691], [-14.99999930125987, -0.004578449893606847], [-18.691676190262022, 62.082153394862786], [-44.267023422459474, 118.67472829694223], [-101.2771911667341, 125.92273809878164], [-157.15955484391569, 101.58456411729983], [-215.39198132989281, 103.84263950942452]])
#numpy_points = np.array([[ 31.,    5. ], [ 22.3,  17. ], [ 14.7,   3. ], [-15. ,  -3. ], [-15. ,   8. ], [-13. ,  19. ], [ -8. ,  28. ], [ -0. ,  37. ], [  9. ,  43. ], [ 19. ,  47. ], [ 30. ,  47. ], [ 40. ,  42. ], [ 48. ,  35. ], [ 54. ,  26. ], [ 59. ,  16. ]])
#numpy_points = np.array([[-239.28590431227303, 121.98321404586304], [-190.71542073733096, 140.63352377547224], [-138.33644801159795, 137.91706071832806], [-88.71535492871936, 160.60442135514262]])
numpy_points = np.array([[-136.3,  256. ],
 [-125.8,  255. ],
 [-115.5,  253. ],
 [-105.6,  249. ],
 [ -96.2,  245. ],
 [ -87.4,  239. ],
 [ -79.5,  232. ],
 [ -72.5,  224. ],
 [ -65.2,  217. ],
 [ -57.3,  210. ],
 [ -48.7,  204. ],
 [ -39.6,  198. ],
 [ -30.8,  193. ],
 [ -22.3,  187. ],
 [ -14.1,  180. ],
 [  -6.4,  173. ],
 [  -0.3,  164. ],
 [   3.4,  154. ],
 [   4.8,  144. ],
 [   5.9,  134. ],
 [   7.3,  123. ],
 [   9. ,  113. ],
 [  11.4,  103. ],
 [  14.4,   93. ],
 [  17.3,   82. ],
 [  19.8,   72. ],
 [  21.9,   62. ],
 [  23.1,   52. ],
 [  22.9,   41. ],
 [  21.5,   31. ],
 [  18.9,   20. ],
 [  15.9,   10. ],
 [  15. ,   -0. ],
 [ -15. ,    0. ],
 [ -14. ,   10. ],
 [ -13. ,   21. ],
 [  -9. ,   30. ],
 [  -7. ,   41. ],
 [  -7. ,   51. ],
 [  -8. ,   61. ],
 [ -11. ,   71. ],
 [ -13. ,   81. ],
 [ -17. ,   91. ],
 [ -19. ,  101. ],
 [ -21. ,  111. ],
 [ -23. ,  122. ],
 [ -24. ,  132. ],
 [ -25. ,  142. ],
 [ -28. ,  152. ],
 [ -36. ,  159. ],
 [ -44. ,  165. ],
 [ -52. ,  171. ],
 [ -61. ,  176. ],
 [ -70. ,  182. ],
 [ -78. ,  188. ],
 [ -86. ,  195. ],
 [ -93. ,  202. ],
 [-100. ,  210. ],
 [-108. ,  217. ],
 [-117. ,  222. ],
 [-127. ,  225. ],
 [-138. ,  226. ]])

plt.scatter(*zip(*numpy_points), color='Black')
plt.scatter(numpy_points[1][0],numpy_points[1][1],color='Red')
plt.show()

tri = Delaunay(numpy_points)
triangle = numpy_points[tri.simplices]

point = numpy_points[1]
exclude_point = numpy_points[0]

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
                distance = np.linalg.norm(point - p)
                distances.append(distance)
                points.append(p)
    return triangles, distances, points

triangles, distances, points = findTriangles(tri, point, exclude_point, 100)

print(triangles)
print(distances)
print(points)

for triangle in triangles:
    x = [numpy_points[i][0] for i in triangle]
    y = [numpy_points[i][1] for i in triangle]
    plt.fill(x, y, color='red')

plt.triplot(numpy_points[:,0], numpy_points[:,1], tri.simplices)
plt.plot(numpy_points[:,0], numpy_points[:,1], 'o')
plt.show()

# iteration part
polygon = Polygon([[0.0, 1], [5,1], [40, 30], [30, 42], [20, 47], [10, 50],
                [0, 51], [-10, 50], [-20, 47], [-30, 42], [-40, 30], [-5,1]])
start_point = Point(0,0)

# start sequence:  get the first cone on the right and rotate 90 degrees to get the second point, after that we can get angle between 3 points (one being imaginary, right behind the first cone) and go on from there


    # right


right_cones = [(15,-1)]
right_vector = (0,0)
right_deg90 = -3.14/2

right_shape = translate_poly(polygon, right_vector)
right_shape = rotate_poly(right_shape, right_deg90, right_vector)
right_points_in, right_closest = points_inside(right_shape, points)
right_ex_points = extract_points_shapely(right_points_in)
right_closest_point = (right_closest.x, right_closest.y)  #next point to go to
right_cones.append(right_closest_point)

print(right_closest_point,' right')

plt.scatter(right_ex_points[0],right_ex_points[1])
plt.plot(right_shape.exterior.xy[0], right_shape.exterior.xy[1])
plt.show()

right_vector = right_closest_point
second_right_shape = translate_poly(right_shape, right_vector)
second_right_shape = rotate_poly(second_right_shape, 0, right_vector)
right_points_in, right_closest = points_inside(second_right_shape, points)
right_ex_points = extract_points_shapely(right_points_in)
right_closest_point = (right_closest.x, right_closest.y)  #next point to go to
right_cones.append(right_closest_point)

print(right_closest_point, ' right')
print(right_cones)
print(calculate_angle(right_cones))

plt.scatter(right_ex_points[0],right_ex_points[1])
plt.plot(second_right_shape.exterior.xy[0], second_right_shape.exterior.xy[1])
plt.show()
#####################################################################################

    # left


left_cones = [(-15,-1)]
left_vector = (0,0)
left_deg90 = 3.14/2

left_shape = translate_poly(polygon, left_vector)
left_shape = rotate_poly(left_shape, left_deg90, left_vector)
left_points_in, left_closest = points_inside(left_shape, points)
left_ex_points = extract_points_shapely(left_points_in)
left_closest_point = (left_closest.x, left_closest.y)  #next point to go to
left_cones.append(left_closest_point)

print(left_closest_point, ' left')

plt.scatter(left_ex_points[0],left_ex_points[1], edgecolors='Yellow')
plt.plot(left_shape.exterior.xy[0], left_shape.exterior.xy[1])
plt.show()

left_vector = left_closest_point
second_left_shape = translate_poly(left_shape, left_vector)
second_left_shape = rotate_poly(second_left_shape, 0, left_vector)
left_points_in, left_closest = points_inside(second_left_shape, points)
left_ex_points = extract_points_shapely(left_points_in)
left_closest_point = (left_closest.x, left_closest.y)  #next point to go to
left_cones.append(left_closest_point)

print(left_closest_point, ' left')
print(left_cones)
print(calculate_angle(left_cones))

plt.scatter(left_ex_points[0], left_ex_points[1], edgecolors='Yellow')

plt.plot(second_left_shape.exterior.xy[0], second_left_shape.exterior.xy[1])
plt.show()

####################################################################################

while 1:
    right_rads = calculate_angle(right_cones)
    right_vector = right_closest_point

    third_right_shape = translate_poly(second_right_shape, right_vector)
    third_right_shape = rotate_poly(third_right_shape, right_rads, right_vector)
    right_points_in, right_closest = points_inside(third_right_shape, points)
    if right_closest == 0:
        break  # powinno byc go to left
    right_ex_points = extract_points_shapely(right_points_in)
    right_closest_point = (right_closest.x, right_closest.y)  # next point to go to
    right_cones.append(right_closest_point)
    # points = remove_point(points, right_closest_point)
    print(right_cones, ' right')

    # plt.scatter(right_ex_points[0], right_ex_points[1])
    # plt.plot(third_right_shape.exterior.xy[0], third_right_shape.exterior.xy[1])
    # plt.show()

    left_rads = calculate_angle(left_cones)
    left_vector = left_closest_point

    third_left_shape = translate_poly(second_left_shape, left_vector)
    third_left_shape = rotate_poly(third_left_shape, left_rads, left_vector)
    left_points_in, left_closest = points_inside(third_left_shape, points)
    if left_closest == 0:
        break
    left_ex_points = extract_points_shapely(left_points_in)
    left_closest_point = (left_closest.x, left_closest.y)  # next point to go to
    left_cones.append(left_closest_point)
    # points = remove_point(points, left_closest_point)
    print(left_cones, ' left')

    # plt.scatter(left_ex_points[0],left_ex_points[1], edgecolors='Yellow')
    # plt.plot(third_left_shape.exterior.xy[0], third_left_shape.exterior.xy[1])
    # plt.show()

plt.scatter(*zip(*numpy_points), edgecolors='Black')
plt.show()

plt.scatter(*zip(*right_cones))

plt.scatter(*zip(*left_cones), edgecolors='Yellow')
plt.show()