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


def points2Image(pnts):
    import cv2
    # transpose is to make
    # [[xyz];[xyz];[xyz]]
    # into [xxx; yyy; zzz]
    allPnts = np.vstack(pnts).T
    xmin = np.min(allPnts[0])
    xmax = np.max(allPnts[0])
    ymin = np.min(allPnts[1])
    ymax = np.max(allPnts[0])

    origin = np.array([xmin, ymin], dtype=np.int64)
    bounds = [int(xmax-xmin) + 1, int(ymax-ymin) + 1]
    data = np.zeros(shape=(*bounds, 3), dtype=np.uint8)

    for p in pnts: 
        color = np.random.randint(0, 255, size=3)

        p = p[:, :2].astype(np.int64) - origin
        #data[p[:0], p[:1]] = color
        for a in p:
            data[a[0], a[1]] = color

    obj_map = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
    obj_map[obj_map > 0] = 255

    cv2.imshow('imgs', data)
    cv2.waitKey(0)
    cv2.imshow('obj_map', obj_map)
    cv2.waitKey(0)
    cv2.imwrite('obj_map.bmp', obj_map)


if __name__ == '__main__':

    x = np.load('test_pnt.npy')
    x_seg = segmentation(x, 'rule')
    # x_seg = segmentation(x, 'kmeans')
    # x_seg = segmentation(x, 'dbscan')
    actors = make_pnts_actor(x_seg)
    points2Image(x_seg)
    #utils.show_in_vtk(actors)
