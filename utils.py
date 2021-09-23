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


def collision_judge(map, pos, mov):
    ep = pos + mov
    rr, cc = draw.line(pos[1], pos[0], ep[1], ep[0])
    ep = pos
    for r, c in zip(rr, cc):
        if (r == pos[1]) and (c == pos[0]):
            continue
        # print(r, c, "the res is:", map[r, c],
        #       (map[r, c] == 0) , (r >= 0) , (c >=0) , (r<map.shape[0]) , (c<map.shape[1]))
        rf = (r >= 0) and (c >=0) and (r<map.shape[0]) and (c<map.shape[1])
        if (map[r, c] == 0) and rf:
            ep = [c, r]
        else:
            return False, ep
    return True, ep


def getRangeMap(pos, rad, shape):
    x0 = pos[0] - rad
    x0 = x0 if x0 > 0 else 0

    x1 = pos[0] + rad + 1
    x1 = x1 if x1 < shape[0] else shape[0] - 1

    y0 = pos[1] - rad
    y0 = y0 if y0 > 0 else 0

    y1 = pos[1] + rad + 1
    y1 = y1 if y1 < shape[1] else shape[1] - 1

    return y0, y1, x0, x1


def getSampleLine(obs, pos, rad):
    print(' i am in ', pos, obs.shape)
    nts = np.zeros_like(obs)
    rr, cc = draw.circle_perimeter(pos[1], pos[0], radius=rad, shape=obs.shape)
    #print(rr, cc)
    for r, c in zip(rr, cc):
        print('~~~', pos[1], pos[0], r, c, ':::',r, c)
        aa, bb = draw.line(pos[1], pos[0], r, c)
        #nts[r, c] = 255
        for a, b in zip(aa, bb):
            if (a == pos[1]) and (b == pos[0]):
                continue
            if obs[a, b] != 0:
                break
            nts[a, b] = 255
    return nts
