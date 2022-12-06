import shapely
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import numpy as np
from shapely import affinity
import math
import time
#shape
polygon = Polygon([[0.0, 1], [5,1], [40, 30], [30, 42], [20, 47], [10, 50], 
                [0, 51], [-10, 50], [-20, 47], [-30, 42], [-40, 30], [-5,1]])

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

start_point = Point(0,0)



def points_inside(polygon, points):
    mid = Point(0,0)
    points_inside_polygon = []
    distances = []
    x,y = polygon.exterior.xy
    xs, ys = extract_points_shapely(points)
    for i, val in enumerate(points):
        if polygon.contains(points[i]) is True:
            #print(mid.distance(points[i]), points[i])
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

def extract_points_shapely(point_list):
    xs = [point.x for point in point_list]
    ys = [point.y for point in point_list]
    return xs, ys

def rotate_poly(poly, radians, rotate_around):
    r_poly = affinity.rotate(poly, radians, use_radians=True, origin=rotate_around)
    return r_poly

def translate_poly(poly, vector):
    trans_x, trans_y = vector
    t_poly = affinity.translate(polygon, trans_x, trans_y)
    return t_poly

def nparray_to_pointarray(points):
    point_arr = []
    for i, val in enumerate(points):
        point_arr.append(Point((points[i][0]), (points[i][1])))
    return point_arr

def calculate_angle(points):
    p1 = points[-2]
    p2 = points[-1]
    p3 = points[-3]
    
    p12 = math.sqrt((points[-2][0]-points[-1][0])**2 + (points[-2][1]-points[-1][1])**2)
    p23 = math.sqrt((points[-1][0]-points[-3][0])**2 + (points[-1][1]-points[-3][1])**2)
    p13 = math.sqrt((points[-2][0]-points[-3][0])**2 + (points[-2][1]-points[-3][1])**2)


    radians = np.arccos((p12**2 + p13**2 - p23**2)/(2 * p12 * p13))
   
    print(p12, p13, p23)
    radians = math.pi - radians
    angle = radians*(180/math.pi)
    #print(angle)
    #checking angle side
    if ((points[-2][0] - points[-1][0])*(points[-3][1] - points[-1][1]) - (points[-2][1] - points[-1][1])*(points[-3][0] - points[-1][0])) > 0:
        radians = -radians
    return radians

def remove_point(arr1, point_to_remove):
    arr2 = np.array([[point_to_remove[0], point_to_remove[1]]])
    delta = set(map(tuple, arr2))
    return np.fromiter((x for xs in arr1 if tuple(xs) not in delta for x in xs), dtype=arr1.dtype).reshape(-1, arr1.shape[-1])


#test points
points = nparray_to_pointarray(numpy_points)
# ex_points = extract_points_shapely(points_inside(polygon, points))
# pi = points_inside(polygon, points)

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


while 1:
    right_rads = calculate_angle(right_cones)
    right_vector = right_closest_point

    third_right_shape = translate_poly(second_right_shape, right_vector)
    third_right_shape = rotate_poly(third_right_shape, right_rads, right_vector)
    right_points_in, right_closest = points_inside(third_right_shape, points)
    if right_closest  == 0:
        break   # powinno byc go to left
    right_ex_points = extract_points_shapely(right_points_in)
    right_closest_point = (right_closest.x, right_closest.y)  #next point to go to
    right_cones.append(right_closest_point)
    #points = remove_point(points, right_closest_point)
    print(right_cones,' right')
    
    # plt.scatter(right_ex_points[0], right_ex_points[1])
    # plt.plot(third_right_shape.exterior.xy[0], third_right_shape.exterior.xy[1])
    # plt.show()


    left_rads = calculate_angle(left_cones)
    left_vector = left_closest_point

    third_left_shape = translate_poly(second_left_shape, left_vector)
    third_left_shape = rotate_poly(third_left_shape, left_rads, left_vector)
    left_points_in, left_closest = points_inside(third_left_shape, points)
    if left_closest  == 0:
        break
    left_ex_points = extract_points_shapely(left_points_in)
    left_closest_point = (left_closest.x, left_closest.y)  #next point to go to
    left_cones.append(left_closest_point)
    #points = remove_point(points, left_closest_point)
    print(left_cones, ' left')

    # plt.scatter(left_ex_points[0],left_ex_points[1], edgecolors='Yellow')
    # plt.plot(third_left_shape.exterior.xy[0], third_left_shape.exterior.xy[1])
    # plt.show()

plt.scatter(*zip(*numpy_points), edgecolors='Black')
plt.show()

plt.scatter(*zip(*right_cones))

plt.scatter(*zip(*left_cones), edgecolors='Yellow')
plt.show()