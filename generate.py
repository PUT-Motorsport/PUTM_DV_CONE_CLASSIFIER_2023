import numpy as np
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
from shapely import affinity
from shapely.geometry import LineString
import math

def generate_track():
    points = [Point(0,0), Point(0,1), Point(0,2)]
    point_list = []
    polygon = Polygon([[0.0, 2.0], [3.0, 13.25], [6.0, 17.0], [9.0, 20.0], [12.0, 21.5], [15.0, 23.0], 
                    [18.0, 23.0], [24.0, 26.0], [31.5, 33.5], [30.0, 35.0], [21.0, 41.75], [12.0, 45.5], 
                    [0.0, 47.0], [-12.0, 45.5], [-21.0, 41.75], [-30.0, 35.0], [-31.5, 33.5], [-24.0, 26.0], 
                    [-18.0, 23.0], [-15.0, 23.0], [-12.0, 21.5], [-9.0, 20.0], [-6.0, 17.0], [-3.0, 13.25]])

    def Random_Points_in_Polygon(polygon, number):
        rand_points = []
        minx, miny, maxx, maxy = polygon.bounds
        while len(rand_points) < number:
            pnt = Point(np.random.uniform(minx, maxx), np.random.uniform(miny, maxy))
            #print(pnt.x)
            if polygon.contains(pnt):
                rand_points.append(pnt)
        return rand_points

    for i in range(7):
        #calculating angle
        p1 = points[-2]
        p2 = points[-1]
        p3 = points[-3]
        
        p12 = math.sqrt((points[-2].x-points[-1].x)**2 + (points[-2].y-points[-1].y)**2)
        p23 = math.sqrt((points[-1].x-points[-3].x)**2 + (points[-1].y-points[-3].y)**2)
        p13 = math.sqrt((points[-2].x-points[-3].x)**2 + (points[-2].y-points[-3].y)**2)

        radians = np.arccos((p12**2 + p13**2 - p23**2)/(2 * p12 * p13))
        radians = math.pi - radians
        angle = radians*(180/math.pi)
        #print(angle)
        #checking angle side
        if ((points[-2].x - points[-1].x)*(points[-3].y - points[-1].y) - (points[-2].y - points[-1].y)*(points[-3].x - points[-1].x)) > 0:
            radians = -radians
        
        trans_x = points[-1].x - points[-2].x
        trans_y = points[-1].y - points[-2].y

        translated_polygon = affinity.translate(polygon, trans_x, trans_y)
        rotated_polygon = affinity.rotate(translated_polygon, radians, use_radians=True, origin=(points[-1]))
        polygon = rotated_polygon

        points.append(*Random_Points_in_Polygon(rotated_polygon, 1))
        

    for i, val in enumerate(points):
        point_list.append([points[i].x, points[i].y])
    #print(point_list)
    return point_list

#print(generate_track())

# xp,yp = rotated_polygon.exterior.xy
# plt.plot(xp,yp)

# xs = [point.x for point in points]
# ys = [point.y for point in points]
# plt.scatter(xs, ys, color="red")
# plt.show()


