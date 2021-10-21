"""
# Li Ang <psw.liang@link.cuhk.edu.hk>
# Write for ELEG4701 CUHK term 1
# This script is to simply illustrate how you design your lidar sensor in this lab
# Please read the guideline before you run this script.
"""

import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import lidar3d.utils as utils
import numpy as np



# sparse
pnts = utils.getPoints(utils.makeSphere(center=[0, 0, 0], radius=20))
pnts = utils.makePointCloud(pnts)
utils.show_in_vtk([pnts])


# dense
pnts = utils.getPoints(utils.makeSphere(center=[0, 0, 0], radius=20, res_theta=100, res_phi=100))
pnts = utils.makePointCloud(pnts, radius=0.1)
utils.show_in_vtk([pnts])

# cut off
pnts = []
ceil = 0.3
for p in utils.getPoints(utils.makeSphere(center=[0, 0, 0], radius=1, res_theta=100, res_phi=100)):
    if abs(p[2]) < ceil:
        pnts.append(p)
pnts = np.array(pnts) * 20
pnts = utils.makePointCloud(pnts, radius=0.1)
utils.show_in_vtk([pnts])
