import shapely
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import numpy as np
from shapely import affinity
import math
import time


def setdiff2d_iter(arr1, point_to_remove):
    arr2 = np.array([[point_to_remove[0], point_to_remove[1]]])
    delta = set(map(tuple, arr2))
    return np.fromiter((x for xs in arr1 if tuple(xs) not in delta for x in xs), dtype=arr1.dtype).reshape(-1, arr1.shape[-1])



numpy_points = np.array([[-136.3,  256. ],
 [-125.8,  255. ],
 [-115.5,  253. ],
 [-105.6,  249. ],
 [ -96.2,  245. ],
 [ -87.4,  239. ],
 [ -79.5,  232. ],
 [ -72.5,  224. ],
 [ -65.2,  217. ],
 [ -57.3,  210. ]])

print(setdiff2d_iter(numpy_points, (-136.3,  256.)))