import matplotlib.pyplot as plt
import numpy as np
import math
import random
from scipy import interpolate
from numpy import ones,vstack
from numpy.linalg import lstsq
from shapely.geometry import LineString
from generate import generate_track
import alphashape
from csv import writer
import multiprocessing as mp
from descartes import PolygonPatch
from scipy.spatial import ConvexHull, convex_hull_plot_2d

'''FS rules states that the track is:
minimum 3m wide
max cone distance is 5m
minium radius of a turn is 3m from the inner circle
1 pixel is 10 cm
'''

#data per process (5 processes)
DATASET_SIZE = 1

#track settings
TRACK_WIDTH = 30
INTERPOLATION_RESOLUTION = 30
CLOSE_LOOP = 0
dist_bt_cones = 5 #random.randint(13, 50)


'''
#function to plot a shape from coords
def plot_coords(coords):
    pts = list(coords)
    x, y = zip(*pts)
    plt.plot(x,y)

#drawing shape by dragging function
def onclick(event):
    try:
        print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' % 
          (event.button, event.x, event.y, event.xdata, event.ydata))   #idk why it has to be with print() to draw only when lmb is pressed 
        ax.scatter(event.xdata, event.ydata)
        fig.canvas.draw()
        middle.append([event.x, event.y])
    except:
        pass
    '''
class DatasetGen:
    dataframe = []

    #intersection of 2 lists
    def intersection(self, lst1, lst2):
        lst3 = [value for value in lst1 if value in lst2]
        return lst3

    #interpolation of a spline
    def ip_curve(self, points, ip_res):
    #interpolated curve, based on given points
        nodes = np.array(points)  #nodes for spline
        x = nodes[:,0]
        y = nodes[:,1]
        tck,u     = interpolate.splprep( [x,y], s=0, k=2)
        xnew,ynew = interpolate.splev( np.linspace( 0, 1, ip_res ), tck,der = 0)
        return xnew, ynew

    #calculate distance of lines
    def distance(self, points):
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

    #plot with cones
    def create_plot(self, xrnew,yrnew, xlnew,ylnew):
        plt.axes().set_facecolor("lightgrey")

        plt.plot(xrnew,yrnew, marker="o", markersize=2, markeredgecolor="blue", linestyle="None")
        plt.plot(xlnew,ylnew, marker="o", markersize=2, markeredgecolor="yellow", linestyle="None")
        plt.plot(0,0,marker="o", markersize=5, markeredgecolor="green")
        plt.text(-300, 320, "odległość między pachołkami wynosi {}0 cm".format(dist_bt_cones))
        plt.axis([-300, 300, -50, 300])
        plt.show()

    
    def dataset(self, xrnew, yrnew, xlnew, ylnew):
        y1 = 0 #left
        y2 = 1
        
        Xl1 = [xlnew[0], ylnew[0]]
        Xl2 = [xlnew[1], ylnew[1]]
        Xl3 = [xlnew[2], ylnew[2]]

        Xr1 = [xrnew[-1], yrnew[-1]]
        Xr2 = [xrnew[-2], yrnew[-2]]
        Xr3 = [xrnew[-3], yrnew[-3]]

        data = [(Xl1, y1), (Xl2, y1), (Xl3, y1), (Xr1, y2), (Xr2, y2), (Xr3, y2)]

        random.shuffle(data)    
                                    #normalizing data
        dataX1x = ((data[0][0][0]) + 80) /160
        dataX2x = ((data[1][0][0]) + 80) /160
        dataX3x = ((data[2][0][0]) + 80) /160
        dataX4x = ((data[3][0][0]) + 80) /160
        dataX5x = ((data[4][0][0]) + 80) /160
        dataX6x = ((data[5][0][0]) + 80) /160

        dataX1y = ((data[0][0][1]) + 10) /160
        dataX2y = ((data[1][0][1]) + 10) /160
        dataX3y = ((data[2][0][1]) + 10) /160
        dataX4y = ((data[3][0][1]) + 10) /160
        dataX5y = ((data[4][0][1]) + 10) /160
        dataX6y = ((data[5][0][1]) + 10) /160

        datay1 = (data[0][1])
        datay2 = (data[1][1])
        datay3 = (data[2][1])
        datay4 = (data[3][1])
        datay5 = (data[4][1])
        datay6 = (data[5][1])
        
        dataset_values = [dataX1x, dataX2x, dataX3x, dataX4x, dataX5x, dataX6x,  dataX1y, dataX2y, dataX3y, dataX4y, dataX5y, dataX6y,  datay1, datay2, datay3, datay4, datay5, datay6]
        return dataset_values

    def set_cones(self):
        middle = [[0,0],[0,10],[22.5,32.5],[45, 10],[45,0]]#generate_track(), [[0,0],[0,10],[22.5,32.5],[45, 10],[45,0]] = worst case
        xnew,ynew = self.ip_curve(middle, 1000)

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
        right_side = self.intersection(both_list, right_list)
        left_side  = self.intersection(left_list, both_list)

        #print(dist_bt_cones)

        #interpolating to get right distance between cones
        right_cones_amount = int(self.distance(right_side) / dist_bt_cones)
        left_cones_amount = int(self.distance(left_side) / dist_bt_cones)

        xrnew, yrnew = self.ip_curve(right_side, right_cones_amount)
        xlnew, ylnew = self.ip_curve(left_side, left_cones_amount)

        #self.create_plot(xrnew,yrnew, xlnew,ylnew)
        return  np.round(xrnew,1),np.round( yrnew), np.round(xlnew), np.round(ylnew)

    def thread(self):
        for i in range(DATASET_SIZE):
            points = []
            xrnew, yrnew, xlnew, ylnew = self.set_cones()
            for i, val in enumerate(xrnew):
                points.append([xrnew[i], yrnew[i]])
            for i, val in enumerate(xlnew):
                points.append([xlnew[i], ylnew[i]])
            
            points = np.array(points)

            print(points)
            # hull = ConvexHull(points)

            # fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 3))

            # for ax in (ax1, ax2):
            #     ax.plot(points[:, 0], points[:, 1], '.', color='k')
            #     if ax == ax1:
            #         ax.set_title('Given points')
            #     else:
            #         ax.set_title('Convex hull')
            #         for simplex in hull.simplices:
            #             ax.plot(points[simplex, 0], points[simplex, 1], 'c')
            #         ax.plot(points[hull.vertices, 0], points[hull.vertices, 1], 'o', mec='r', color='none', lw=1, markersize=10)
            #     ax.set_xticks(range(10))
            #     ax.set_yticks(range(10))
            # plt.show()
            
            # row = self.dataset(xrnew, yrnew, xlnew, ylnew)
            # with open("cones.csv", "a", newline="") as f_object:
            #     writer_object = writer(f_object)
            #     writer_object.writerow(row)
            #     f_object.close()
        #alpha_shape = alphashape.alphashape(points, 0.02)

        fig, ax = plt.subplots()
        ax.scatter(*zip(*points))
        #ax.add_patch(PolygonPatch(alpha_shape, alpha=0.2))
        plt.show()

    def __init__(self):
        self.thread()


DatasetGen()

# if __name__ == "__main__":
# #     p1 = mp.Process(target=DatasetGen)
#     p2 = mp.Process(target=DatasetGen)
#     p3 = mp.Process(target=DatasetGen)
#     p4 = mp.Process(target=DatasetGen)
#     p5 = mp.Process(target=DatasetGen)
#     p1.start()
#     p2.start()
#     p3.start()
#     p4.start()
#     p5.start()
