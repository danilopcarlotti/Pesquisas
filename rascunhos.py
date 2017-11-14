import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.ticker as ticker
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
var_a = [1,2,1,2,0,2,0,2,1,1,2,2,0,2,1,2,1,2,1,0,1,0,0,1,1,1,0,1,1,0,0,0,1,2,1,0,1,2,1,0,0,0,0,1,0,0,2,1,0,2,0]
var_c = [1,2,2,3,2,2,1,2,2,2,0,0,3,1,2,1,3,1,0,2,3,1,1,1,0,1,0,0,2,3,2,1,1,1,1,1,2,1,1,3,0,0,2,3,3,1,0,2,1,2,0]
var_d = [2,2,2,2,1,1,0,1,2,1,3,2,1,2,1,2,2,3,2,2,2,3,1,2,1,4,1,2,2,2,1,0,2,3,3,2,3,1,1,2,4,0,2,2,1,0,1,2,0,3,2]

ax.scatter(np.array(var_a),np.array(var_c),np.array(var_d),zdir='z', s=20, c=None, depthshade=True)
ax.xaxis.set_major_locator(ticker.MultipleLocator(base=1.0))
ax.yaxis.set_major_locator(ticker.MultipleLocator(base=1.0))
ax.zaxis.set_major_locator(ticker.MultipleLocator(base=1.0))
ax.set_xlabel('Variável A')
ax.set_ylabel('Variável C')
ax.set_zlabel('Variável D')
plt.show()
