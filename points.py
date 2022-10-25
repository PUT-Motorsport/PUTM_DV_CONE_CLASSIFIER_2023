import matplotlib.pyplot as plt
import numpy as np
import math
import random
from scipy import interpolate
from numpy import ones,vstack
from numpy.linalg import lstsq
from shapely.geometry import LineString
from shapely.geometry import Point
#from generate import generate_track

'''FS rules states that the track is:
minimum 3m wide
max cone distance is 5m
minium radius of a turn is 3m from the inner circle
1 pixel is 10 cm
'''

#track settings
TRACK_WIDTH = 30
INTERPOLATION_RESOLUTION = 30
CLOSE_LOOP = 0
dist_bt_cones = random.randint(20, 50)

#plot 1 for drawing
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim([0, 600])
ax.set_ylim([0, 500])

#function to plot a shape from coords
def plot_coords(coords):
    pts = list(coords)
    x, y = zip(*pts)
    plt.plot(x,y)

#drawing shape by dragging function
#middle = generate_track()
middle = []
def onclick(event):
    try:
        print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' % 
          (event.button, event.x, event.y, event.xdata, event.ydata))   #idk why it has to be with print() to draw only when lmb is pressed 
        ax.scatter(event.xdata, event.ydata)
        fig.canvas.draw()
        middle.append([event.x, event.y])
    except:
        pass

#intersection of 2 lists
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

#interpolation of a spline
def ip_curve(points, ip_res):
#interpolated curve, based on given points
    nodes = np.array(points)  #nodes for spline
    x = nodes[:,0]
    y = nodes[:,1]
    tck,u     = interpolate.splprep( [x,y] ,s = 0 )
    xnew,ynew = interpolate.splev( np.linspace( 0, 1, ip_res ), tck,der = 0)
    return xnew, ynew

#calculate distance of lines
def distance(points):
    dist = []
    try:
        for i, val in enumerate(points):
            x1_tmp = points[i][0]
            y1_tmp = points[i][1]
            x2_tmp = points[i+1][0]
            y2_tmp = points[i+1][1]
            dbp = math.sqrt((x2_tmp - x1_tmp)**2 + (y2_tmp - y1_tmp)**2)
            dist.append(dbp)
    except: pass
    return sum(dist)

#append shape on plot 1
cid = fig.canvas.mpl_connect('motion_notify_event', onclick)
plt.show()
print(middle)

# for i in range(10):
#     x = random.randint(0,900)
#     y = random.randint(0,750)
#     middle.append([x,y])


if CLOSE_LOOP == True: middle.append(middle[0])    #close the shape
xnew,ynew = ip_curve(middle, 1000)

#access coords with shapely
coords = []
for i, val in enumerate(ynew):
    coords.append((xnew[i],ynew[i]))
track = LineString(coords)

#draw polygons including cone lines
left_hand_side  = track.buffer(TRACK_WIDTH/2 , single_sided=True)
right_hand_side = track.buffer(-TRACK_WIDTH/2, single_sided=True)
both_sides      = track.buffer(TRACK_WIDTH/2, single_sided=False)

xl,yl = left_hand_side.exterior.xy
xr,yr = right_hand_side.exterior.xy
xb,yb = both_sides.exterior.xy

#getting points from polygons
left_list = []
right_list = []
both_list = []
for i, val in enumerate(yl): left_list.append((xl[i],yl[i]))
for i, val in enumerate(yr): right_list.append((xr[i],yr[i]))
for i, val in enumerate(yb): both_list.append((xb[i],yb[i]))

#polygons above include middle of the road, so to get only the outter side
#i want only the ones that intersect points with a list containing both sides
#that way i already have seperate left and right lists of points
right_side = intersection(both_list, right_list)
left_side  = intersection(left_list, both_list)

print(dist_bt_cones)

#interpolating to get right distance between cones
right_cones = int(distance(right_side) / dist_bt_cones)
left_cones = int(distance(left_side) / dist_bt_cones)

xrnew, yrnew = ip_curve(right_side, right_cones)
xlnew, ylnew = ip_curve(left_side, left_cones)

#plot 2 with cones
plt.plot(xrnew,yrnew, marker="o", markersize=2, markeredgecolor="blue")
plt.plot(xlnew,ylnew, marker="o", markersize=2, markeredgecolor="yellow")

#plot 2 with cones
plt.text(0, 800, "odległość między pachołkami wynosi {}0 cm".format(dist_bt_cones))
plt.axis([0, 900, 0, 750])
plt.show()
