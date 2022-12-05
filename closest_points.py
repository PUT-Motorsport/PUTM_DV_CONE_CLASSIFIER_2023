# import numpy as np
# from shapely.geometry import Point, Polygon
# import matplotlib.pyplot as plt
# from shapely import affinity
# from shapely.geometry import LineString
# import math


import numpy as np
# points_2d = np.array([[ 31.,    5. ],
#  [ 22.3,  17. ],
#  [ 14.7,   3. ],
#  [-15. ,  -3. ],
#  [-15. ,   8. ],
#  [-13. ,  19. ],
#  [ -8. ,  28. ],
#  [ -0. ,  37. ],
#  [  9. ,  43. ],
#  [ 19. ,  47. ],
#  [ 30. ,  47. ],
#  [ 40. ,  42. ],
#  [ 48. ,  35. ],
#  [ 54. ,  26. ],
#  [ 59. ,  16. ]])

points_2d = np.array([[192.7, 139. ],
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

points_2d = np.array([[-136.3,  256. ],
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

points_2d = np.array([[ 30.3,   3. ],
 [ 29.3,  10. ],
 [ 25.1,  15. ],
 [ 19.8,  15. ],
 [ 15.7,  10. ],
 [ 14.7,   3. ],
 [-15. ,  -3. ],
 [-15. ,   2. ],
 [-15. ,   7. ],
 [-15. ,  13. ],
 [-13. ,  18. ],
 [-11. ,  22. ],
 [ -9. ,  27. ],
 [ -6. ,  31. ],
 [ -3. ,  35. ],
 [  1. ,  39. ],
 [  5. ,  42. ],
 [ 10. ,  45. ],
 [ 15. ,  46. ],
 [ 20. ,  47. ],
 [ 25. ,  47. ],
 [ 30. ,  46. ],
 [ 35. ,  45. ],
 [ 40. ,  42. ],
 [ 44. ,  39. ],
 [ 48. ,  35. ],
 [ 51. ,  31. ],
 [ 54. ,  27. ],
 [ 56. ,  22. ],
 [ 58. ,  18. ],
 [ 60. ,  13. ],
 [ 60. ,   7. ],
 [ 60. ,   2. ],
 [ 60. ,  -3. ]])
 

def Random_Points_in_Polygon(polygon, number):
    rand_points = []
    minx, miny, maxx, maxy = polygon.bounds
    while len(rand_points) < number:
        pnt = Point(np.random.uniform(minx, maxx), np.random.uniform(miny, maxy))
        #print(pnt.x)
        if polygon.contains(pnt):
            rand_points.append(pnt)
    return rand_points

def rotate(p1, p2, p3):
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

    if ((points[-2].x - points[-1].x)*(points[-3].y - points[-1].y) - (points[-2].y - points[-1].y)*(points[-3].x - points[-1].x)) > 0:
        radians = -radians
    
    trans_x = points[-1].x - points[-2].x
    trans_y = points[-1].y - points[-2].y

    translated_polygon = affinity.translate(polygon, trans_x, trans_y)
    rotated_polygon = affinity.rotate(translated_polygon, radians, use_radians=True, origin=(points[-1]))
    polygon = rotated_polygon

    points.append(*Random_Points_in_Polygon(rotated_polygon, 1))
    return polygon

'''create leftPonts and rightPoints lists
create shape
set 2 points on both sides of the car
check for 2 closest cones
devide it into leftPont and rightPoint
loop over :
	rotate shape to be in same orientation as 2 previous points
	create shape from the points at right angle to the car
	get points in shape	
		closest point to leftPoint append to leftPoints	
		closest point to rightPoint append to rightPoints
	go newest point in the list
'''


def distance(pt_1, pt_2):
    pt_1 = np.array((pt_1[0], pt_1[1]))
    pt_2 = np.array((pt_2[0], pt_2[1]))
    return np.linalg.norm(pt_1-pt_2)

def closest_node(node, nodes):
    pt = []
    dist = 999
    for n in nodes:
        if distance(node, n) <= dist:
            dist = distance(node, n)
            pt = n
    return pt



polygon = Polygon([[0.0, 2.0], [3.0, 13.25], [6.0, 17.0], [9.0, 20.0], [12.0, 21.5], [15.0, 23.0], 
                [18.0, 23.0], [24.0, 26.0], [31.5, 33.5], [30.0, 35.0], [21.0, 41.75], [12.0, 45.5], 
                [0.0, 47.0], [-12.0, 45.5], [-21.0, 41.75], [-30.0, 35.0], [-31.5, 33.5], [-24.0, 26.0], 
                [-18.0, 23.0], [-15.0, 23.0], [-12.0, 21.5], [-9.0, 20.0], [-6.0, 17.0], [-3.0, 13.25]])

leftPoints = []
rightPoints = []

carPoint = (0.0, 0.0)

polygon = rotate(polygon, -90)
xp,yp = polygon.exterior.xy
plt.plot(xp,yp)

# xs = [point.x for point in points]
# ys = [point.y for point in points]
# plt.scatter(xs, ys, color="red")
plt.show()
