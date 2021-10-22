import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from sklearn.cluster import DBSCAN, KMeans
import numpy as np
import lidar3d.utils as utils

def segmentation(x, mode='rule'):
    if mode == 'rule':
        y_pred = (x[:,2] > 1)
    if mode == 'dbscan':
        y_pred = DBSCAN().fit_predict(x)
    if mode == 'kmeans':
        y_pred = KMeans().fit_predict(x)
    print(np.unique(y_pred))
    pnts = []
    for l in np.unique(y_pred):
        pnts.append(x[y_pred == l])
        print(l, pnts[-1].shape[0])
    return pnts


def make_pnts_actor(pnts):
    actors = []
    for p in pnts:
        a = utils.makeActor(utils.makePointCloud(p, radius=0.2), color=[np.random.random(1),
                                                                        np.random.random(1),
                                                                        np.random.random(1)])
        actors.append(a)
    return actors

if __name__ == '__main__':
    

    x = np.load('test_pnt.npy')
    x_seg = segmentation(x, 'rule')
    # x_seg = segmentation(x, 'kmeans')
    # x_seg = segmentation(x, 'dbscan')
    actors = make_pnts_actor(x_seg)

    utils.show_in_vtk(actors)
