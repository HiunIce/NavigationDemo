import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from RRT_Test import testWithAnimation
import cv2
import numpy as np


start = [0,0]

obj_img = cv2.imread('obj_map.bmp')
obj_img = cv2.cvtColor(obj_img, cv2.COLOR_BGR2GRAY)
print(obj_img.shape)

end = [0.9*obj_img.shape[0], 0.9*obj_img.shape[1]]

start, end = np.array(start), np.array(end)
testWithAnimation([obj_img, start, end])
