import vtkmodules.all as vtk
import os
import lidar3d.utils as utils
import numpy as np
import Stage


class Lidar:
    def __init__(self, tar, pos=[0, 0, 0]):
        self.tar_direction = None
        self.actor = None
        self.initSetting()
        self.position = np.array(pos, dtype=np.float32)
        self.obj_tree = vtk.vtkOBBTree()
        self.obj_tree.SetDataSet(tar)
        self.obj_tree.BuildLocator()
        self.target_model = tar
        self.laser_len = 150

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
        self.actor = utils.makeActor(utils.makeSphere([0, 0, 0], 3), color=[0,1,0])

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


    def scan(self):
        m_p = self.getCurrentTargetPoints()

        res = []
        for p in m_p:
            f, r = self.interset_with_line_first(self.position, p)
            if f:
                res.append(r)
        if len(res) != 0:
            res = np.vstack(res)
        else:
            res = np.array([])
        print(res.shape)
        collisions = utils.makeActor(utils.makePointCloud(res, 1), color=[0, 1, 0])
        tar_points = utils.makeActor(utils.makePointCloud(m_p, 0.4), color=[1, 0, 0])

        tar_actor = utils.makeActor(self.target_model, opacity=1)

        utils.show_in_vtk([tar_points, collisions, self.actor, tar_actor])


    def interset_with_line_first(self, p0, p1):
        intersectPoints = vtk.vtkPoints()
        self.obj_tree.IntersectWithLine(p0, p1, intersectPoints, None)
        pts = []
        if intersectPoints.GetNumberOfPoints() == 0:
            return False, np.array([])
        intersection = [0, 0, 0]
        intersectPoints.GetPoint(0, intersection)
        return True, np.array(intersection)

    def interset_with_line_all(self, p0, p1):
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


if __name__ == '__main__':
    s = Stage.Stage3d.make_default_stage3d()

    li = Lidar(s.mesh)
    li.setLidarPosition([100, 100, 10])
    li.scan()

