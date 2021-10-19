"""
# Li Ang <psw.liang@link.cuhk.edu.hk>
# Write for ELEG4701 CUHK term 1
# Please read the guideline before you run this script.
"""

#<<<<<<<< Guide Line>>>>>>>>>>>>#
# This is a Simple Lidar simulator, you can know about "what is lidar feature looks like"
# you can find a lidar feature image in google,
# or link below
# https://eak2mvmpt4a.exactdn.com/wp-content/uploads/2020/07/A-Guide-to-Lidar-Wavelengths-Velodyne-Lidar-AlphaPrime-1.jpg?strip=all&lossy=1&ssl=1

# if you are a freshman for navigation, you will have problems below

# Q1. why the feature captured by Lidar system is point cloud?
#  A: Lidar(light detection and ranging), which means that what he emits is rays.
# Imagine what is the intersection of a ray and a 3d object?
# Yes, it is a point. Lidar has countless such lasers, so the output of the system is a point cloud.

# Q2. why some points are blue, some points are green?
#  A: It is the intensity of signal which related to
#  the incident angle of the laser, the material of the object, distance, environment etc.
#  In other words, our system should be able to infer these parameters from the lidar intensity.
#  of course, in our course, you do not needs to care about it.

# Q3. why lidar knows point are in 'that' position.
#  A: Google ToF(time-of-flight) (You do not need to care about it at all).

# Q4. why some concentric circles shows in lidar system output?
#  A: it looks like graph below, you can see the * is going faraway, when angle increases
#   * (light source)
#   |\`
#   *-*--*----  (ground)


#####
# The following class contains many function,
# You don't need to read the functions that I have not specifically annotated.
# It has nothing to do with the subject or the assignment.
# But it would be better if you can read and understand the principles behind the functions.
# (And this is why I don’t use the ros system directly, but wrote a demo for you guys instead.
#####


import vtkmodules.all as vtk
import os
import lidar3d.utils as utils
import numpy as np
import Stage
from lidar3d.LidarCloud import LidarCloud as LidarCloud
from time import *


class Lidar:
    def __init__(self, tar, pos=[100, 100, 10], model=None):
        self.tar_direction = None
        self.actor = model
        self.sampled_pnts = np.array([])
        self.sampled_filter = LidarCloud()
        self.initSetting()
        self.position = np.array(pos, dtype=np.float32)
        self.obj_tree = vtk.vtkOBBTree()
        self.obj_tree.SetDataSet(tar)
        self.obj_tree.BuildLocator()
        self.target_model = tar
        self.laser_len = 150  # the args controls the range of lidar

    def initSetting(self):
        """      z
                |
              * | *
            *   |___*___ y
            *   /   *
              */* *
              x
        """

        singal_num_xy = int(360)
        ceil = 0.2  # almost no clip
        sphere = utils.makeSphere(center=[0, 0, 0], radius=1,
                                  res_theta=singal_num_xy, res_phi=100)
        points = []
        for p in utils.getPoints(sphere):
            #print(p)
            if abs(p[2]) < ceil:
                points.append(p)
        points = np.array(points)
        self.tar_direction = points
        if self.actor is None:
            self.actor = utils.makeActor(utils.makeSphere([0, 0, 0], 3), color=[0, 1, 0])
        if isinstance(self.actor, vtk.vtkPolyData):
            self.actor = utils.makeActor(self.actor)

    def moveInXYPlane(self, x, y):
        self.position[0] += x
        self.position[1] += y
        utils.translateActor(self.actor, self.position)

    def setLidarPosition(self, pos):
        self.position = np.array(pos)
        utils.translateActor(self.actor, self.position)

    def getCurrentTargetPoints(self):
        # scale
        p = self.tar_direction * self.laser_len
        # rot, not used in current demo
        # you can try scipy.spatial.transform.Rotation
        # if you want to try (do not forget to change shape of target points)

        # translate
        p = p + self.position
        return p

    def scan(self, renderStep=False):
        m_p = self.getCurrentTargetPoints()
        res = []
        for p in m_p:
            f, r = self.intersect_with_line_first(self.position, p)
            if f:
                res.append(r)
        if len(res) != 0:
            res = np.vstack(res)
        else:
            res = np.array([])

        if self.sampled_pnts.shape[0] == 0:
            self.sampled_pnts = res
        else:
            self.sampled_pnts = np.append(self.sampled_pnts, res, axis=0)

        #update_time = time()
        self.sampled_filter.setPoints(self.sampled_pnts)
        # print('update time', time() - update_time, 's')
        # make_time = time()
        # all_pnts = utils.makeActor(utils.makePointCloud(self.sampled_pnts, 0.3), color=[0, 0, 1])  # blue
        # print('make time', time() - make_time, 's')

        print(self.sampled_pnts.shape, '?')
        if renderStep: # if the arg is ture, show somethings to user
            collisions = utils.makeActor(utils.makePointCloud(res, 1), color=[0, 1, 0]) #green
            tar_points = utils.makeActor(utils.makePointCloud(m_p, 0.4), color=[1, 0, 0]) #read
            make_time = time()
            all_pnts = utils.makeActor(utils.makePointCloud(self.sampled_pnts, 0.3), color=[0, 0, 1]) # blue
            print('make time', time() - make_time, 's')
            tar_actor = utils.makeActor(self.target_model, opacity=1) # the background
            utils.show_in_vtk([tar_points, collisions, self.actor, tar_actor, self.sampled_filter.actor])

    def intersect_with_line_first(self, p0, p1):
        intersectPoints = vtk.vtkPoints()
        self.obj_tree.IntersectWithLine(p0, p1, intersectPoints, None)
        pts = []
        if intersectPoints.GetNumberOfPoints() == 0:
            return False, np.array([])
        intersection = [0, 0, 0]
        intersectPoints.GetPoint(0, intersection)
        return True, np.array(intersection)

    def intersect_with_line_all(self, p0, p1):
        intersectPoints = vtk.vtkPoints()
        self.obj_tree.IntersectWithLine(p0, p1, intersectPoints, None)
        pts = []
        for i in range(intersectPoints.GetNumberOfPoints()):
            intersection = [0, 0, 0]
            intersectPoints.GetPoint(i, intersection)
            pts.append(intersection)
        pts = np.array(pts)
        if pts.shape[0] == 0:
            return False, pts
        return True, pts


def try_lidar():
    s = Stage.Stage3d.make_default_stage3d()
    li = Lidar(s.mesh)
    li.setLidarPosition([100, 100, 10])
    li.scan(renderStep=True)
    li.setLidarPosition([50, 50, 10])
    li.scan(renderStep=True)

    for i in range(50, 30, -1):
        li.setLidarPosition([i, i, 10])
        li.scan()
    li.scan(renderStep=True)

if __name__ == "__main__":
    try_lidar()

    # then run anime player for see what happens when