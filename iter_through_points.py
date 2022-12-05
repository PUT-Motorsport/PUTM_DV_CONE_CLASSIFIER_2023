import shapely
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import numpy as np
from shapely import affinity
import math
import time
#shape
polygon = Polygon([[0.0, 0], [5,0], [40, 30], [30, 42], [20, 47], [10, 50], 
                [0, 51], [-10, 50], [-20, 47], [-30, 42], [-40, 30], [-5,0]])

numpy_points = np.array([[20,0],
 [192.7, 139. ],
 [183.1 ,144. ],
 [173.  ,146. ],
 [162.5 ,147. ],
 [152.1 ,146. ],
 [141.8 ,144. ],
 [131.6 ,141. ],
 [121.7 ,138. ],
 [112.2 ,134. ],
 [102.8 ,129. ],
 [ 92.9 ,125. ],
 [ 82.7 ,123. ],
 [ 72.2 ,123. ],
 [ 61.7 ,123. ],
 [ 51.3 ,122. ],
 [ 42.1 ,118. ],
 [ 34.8 ,110. ],
 [ 28.7 ,102. ],
 [ 23.7 , 92. ],
 [ 19.9 , 83. ],
 [ 17.  , 72. ],
 [ 14.4 , 62. ],
 [ 12.2 , 52. ],
 [ 10.8 , 42. ],
 [ 11.1 , 31. ],
 [ 13.1 , 21. ],
 [ 14.6 , 10. ],
 [ 15.  ,  0. ],
 [-15.  , -0. ],
 [-16.  , 10. ],
 [-18.  , 21. ],
 [-19.  , 31. ],
 [-19.  , 41. ],
 [-18.  , 52. ],
 [-16.  , 62. ],
 [-14.  , 72. ],
 [-11.  , 82. ],
 [ -8.  , 92. ],
 [ -5.  ,102. ],
 [ -0.  ,112. ],
 [  5.  ,121. ],
 [ 12.  ,129. ],
 [ 18.  ,137. ],
 [ 27.  ,143. ],
 [ 36.  ,149. ],
 [ 45.  ,152. ],
 [ 56.  ,153. ],
 [ 66.  ,153. ],
 [ 77.  ,153. ],
 [ 87.  ,155. ],
 [ 96.  ,159. ],
 [106.  ,164. ],
 [116.  ,168. ],
 [125.  ,171. ],
 [136.  ,173. ],
 [146.  ,175. ],
 [156.  ,177. ],
 [167.  ,177. ],
 [177.  ,176. ],
 [187.  ,174. ],
 [197.  ,170. ],
 [207.  ,166. ]])

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
    radians = math.pi - radians
    angle = radians*(180/math.pi)
    #print(angle)
    #checking angle side
    if ((points[-2][0] - points[-1][0])*(points[-3][1] - points[-1][1]) - (points[-2][1] - points[-1][1])*(points[-3][0] - points[-1][0])) > 0:
        radians = -radians
    return radians



#test points
points = nparray_to_pointarray(numpy_points)
# ex_points = extract_points_shapely(points_inside(polygon, points))
# pi = points_inside(polygon, points)

# start sequence:  get the first cone on the right and rotate 90 degrees to get the second point, after that we can get angle between 3 points (one being imaginary, right behind the first cone) and go on from there


    # right
start = time.time()

right_cones = [(15,-1)]
vector = (0,0)
deg90 = -3.14/2

right_shape = translate_poly(polygon, vector)
right_shape = rotate_poly(right_shape, deg90, vector)
points_in, closest = points_inside(right_shape, points)
ex_points = extract_points_shapely(points_in)
closest_point = (closest.x, closest.y)  #next point to go to
right_cones.append(closest_point)

print(closest_point) 

plt.scatter(ex_points[0],ex_points[1])
plt.plot(right_shape.exterior.xy[0], right_shape.exterior.xy[1])
plt.show()

vector = closest_point
second_right_shape = translate_poly(right_shape, vector)
second_right_shape = rotate_poly(second_right_shape, 0, vector)
points_in, closest = points_inside(second_right_shape, points)
ex_points = extract_points_shapely(points_in)
closest_point = (closest.x, closest.y)  #next point to go to
right_cones.append(closest_point)

print(closest_point) 
print(right_cones)
print(calculate_angle(right_cones))



plt.scatter(ex_points[0],ex_points[1])
plt.plot(second_right_shape.exterior.xy[0], second_right_shape.exterior.xy[1])
plt.show()

# now form this point it can be done in a loop

for i in range(9):
    rads = calculate_angle(right_cones)
    vector = closest_point

    third_right_shape = translate_poly(second_right_shape, vector)
    third_right_shape = rotate_poly(third_right_shape, rads, vector)
    points_in, closest = points_inside(third_right_shape, points)
    ex_points = extract_points_shapely(points_in)
    closest_point = (closest.x, closest.y)  #next point to go to
    right_cones.append(closest_point)
    print(right_cones)

    plt.scatter(ex_points[0],ex_points[1])
    plt.plot(third_right_shape.exterior.xy[0], third_right_shape.exterior.xy[1])
    plt.show()

plt.scatter(*zip(*numpy_points))
plt.show()

plt.scatter(*zip(*right_cones))
plt.show()