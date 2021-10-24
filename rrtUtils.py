import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QColor

import numpy as np
import cv2
from skimage import draw


def toQImage(img):
    if img is None:
        return QImage()
    if len(img.shape) == 2:
        qimg = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format_Grayscale8)
        # qim.setColorTable(self.gray_color_table)
        return qimg

    elif len(img.shape) == 3:
        if img.shape[2] == 3:
            qimg = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888)
            return qimg
        elif img.shape[2] == 4:
            qimg = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format_ARGB32)
            return qimg


def voxelization_traj(traj):
    movs = []
    #print('ready to move', len(traj)-1)
    if len(traj) == 0:
        return[]
    for i in range(len(traj)-1):
        p1, p2 = traj[i], traj[i+1]
        #print(p1, p2)
        rr, cc = draw.line(p1[1], p1[0], p2[1], p2[0])
        for r, c in zip(rr, cc):
            movs.append([c, r])
    movs = np.array(movs)
    return movs

def moveDirectly(pos, tar):
    if(pos[0] == tar[0]) and (pos[1] == tar[1]):
        return []
    rr, cc = draw.line(pos[1], pos[0], tar[1], tar[0])
    return np.array(list(zip(cc, rr)))


def traj2acts(traj):
    pos = voxelization_traj(traj)
    diff = np.diff(pos, axis=0)
    return diff


def collision_judge(map, pos, ep, ok=0):
    if(pos[0] == ep[0]) and (pos[1] == ep[1]):
        print('that false', pos, ep, "????")
        return True, pos
    rr, cc = draw.line(pos[1], pos[0], ep[1], ep[0])
    pre_ep = ep[:]
    ep = pos
    for r, c in zip(rr, cc):
        if (r == pos[0]) and (c == pos[1]):
            continue
        # print(r, c, "the res is:", map[r, c], (map[r, c] == 0),
        #         (r >= 0) , (c >=0) , (r<map.shape[0]) , (c<map.shape[1]))
        rf = (r >= 0) and (c >=0) and (r < map.shape[0]) and (c < map.shape[1])
        #print(r, c, map.shape)
        if rf and (map[r, c] == ok):
            ep = [c, r]
        else:
            print(r, c, map.shape, (r >= 0) , (c >=0) , (r < map.shape[0]) , (c < map.shape[1]))
            if rf:
                print(map[r, c], 'collision')
            return False, ep
    if (ep[0] == pos[0]) and(ep[1] == pos[1]):
        return False, pre_ep
    return True, ep


def collision_judge_step_fast(map, tar, action, ok=0):
    ep = tar + action
    r, c = ep[1], ep[0]
    rf = (r >= 0) and (c >= 0) and (r < map.shape[0]) and (c < map.shape[1])
    if rf and (map[r, c] == ok):
        return True, ep
    else:
        return False, tar


def getRangeMap(pos, rad, shape):
    x0 = pos[0] - rad
    x0 = x0 if x0 > 0 else 0

    x1 = pos[0] + rad
    x1 = x1 if x1 < shape[0] else shape[0] - 1

    y0 = pos[1] - rad
    y0 = y0 if y0 > 0 else 0

    y1 = pos[1] + rad
    y1 = y1 if y1 < shape[1] else shape[1] - 1

    return y0, y1, x0, x1


def getSampleLine(obs, pos, rad):
    #print(' i am in ', pos, obs.shape)
    nts = np.zeros_like(obs)
    pos = np.array(pos)
    #rr, cc = draw.circle_perimeter(pos[1], pos[0], radius=rad, shape=obs.shape)
    #
    start = (pos-rad//2)
    end = (pos + rad//2)
    if start[0] <= 0:
        start[0] = 2
    if start[1] <= 0:
        start[1] = 2
    if end[0] >= obs.shape[0]:
        end[0] = obs.shape[0]-2
    if end[1] >= obs.shape[1]:
        end[1] = obs.shape[1]-2
    rr, cc = draw.rectangle_perimeter(start, end, shape=obs.shape)
    w, h = obs.shape[1], obs.shape[0]
    wallPnts = []
    for r, c in zip(rr, cc):
        aa, bb = draw.line(pos[1], pos[0], c, r)
        #nts[r, c] = 255
        for a, b in zip(aa, bb):
            #print(a, b, '????', r, c)
            if (a == pos[1]) and (b == pos[0]):
                continue
            if (a >= w) or (b >= h):
                continue
            if obs[b, a] == 255:
                wallPnts.append([b, a])
                break
            nts[b, a] = 255
    return nts, np.array(wallPnts, dtype=np.int32)


def getFrontier2(view, wall):
    # not used anymore
    frontier, _ = cv2.findContours(view,
                        cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(frontier) == 0:
        return []
    print('front num', len(frontier))
    frontier = np.vstack(frontier).reshape(-1,2)
    nf = []
    for f in frontier:
        #if wall[f[0], f[1]] != 255:
            nf.append(f)
    nf = np.array(nf)
    print(nf.shape,' ????')
    return nf


def getFrontier(view, wall):
    frontier = cv2.Laplacian(view, cv2.CV_8U, 3)
    frontier = np.flip(np.argwhere(frontier == 255))
    nf = []
    for f in frontier:
        if (wall[f[1], f[0]] != 255)\
                and (f[0] != 0) and(f[1] != 0) \
                and (f[0] != wall.shape[0]-1) and(f[1] != wall.shape[1]-1):
            nf.append(f)
    nf = np.array(nf)
    return nf


def drawUserView(view, wall, front, pnts=None):
    # profiler = Profiler()
    # profiler.start()
    img = cv2.cvtColor(view, cv2.COLOR_GRAY2BGR)
    wall, _ = cv2.findContours(wall, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, wall, -1, color=(255,0,0), thickness=3)
    if pnts is not None:
        for p in pnts:
            cv2.circle(img, p, 5, (0,0,255), 3)
    if len(front) != 0:
        img[front[:,1], front[:,0],:] = (0,255,0)
    # profiler.stop()
    # profiler.print()
    return toQImage(img)


if __name__ == '__main__':
    # for test
    import matplotlib.pyplot as plt

    img = np.zeros(shape=(20, 41), dtype=np.int32)
    img[15] = 255
    p = np.array([17, 15])
    img, w = getSampleLine(img, p, 20)
    print(img.dtype, img.shape)
    img[15] = 128
    img[p[0], p[1]] = 50
    plt.imshow(img)
    plt.show()
    
    