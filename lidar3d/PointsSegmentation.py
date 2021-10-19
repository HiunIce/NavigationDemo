from sklearn.cluster import DBSCAN, KMeans
import numpy as np
import lidar3d.utils as utils

x = np.load('test_pnt.npy')
y_pred = (x[:,2] > 1)
# y_pred = DBSCAN().fit_predict(x)
# y_pred = KMeans().fit_predict(x)
print(np.unique(y_pred))

pnts = []
for l in np.unique(y_pred):
    pnts.append(x[y_pred == l])
    print(l, pnts[-1].shape[0])

actors = []
for p in pnts:
    a = utils.makeActor(utils.makePointCloud(p, radius=0.2), color=[np.random.random(1),
                                                                    np.random.random(1),
                                                                    np.random.random(1)])
    actors.append(a)
utils.show_in_vtk(actors)
