import alphashape
import matplotlib.pyplot as plt
from descartes import PolygonPatch
import time
# Define input points

a=time.time()
points = [[ 30.3,   3. ],
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
 [ 60. ,  -3. ]]


# Determine the optimized alpha parameter
alpha = alphashape.optimizealpha(points)
# Generate the alpha shape
alpha_shape = alphashape.alphashape(points, alpha)
print(time.time()-a)
# Initialize plot
fig, ax = plt.subplots()
# Plot input points
ax.scatter(*zip(*points))
# Plot alpha shape
ax.add_patch(PolygonPatch(alpha_shape, alpha=.2))
plt.show()