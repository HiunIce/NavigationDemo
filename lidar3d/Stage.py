"""
# Li Ang <psw.liang@link.cuhk.edu.hk>
# Write for ELEG4701 CUHK term 1
# Please read the guideline before you run this script.
"""

import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import vtkmodules.all as vtk
import os
import lidar3d.utils as utils
import numpy as np


class Stage3d:
    def __init__(self):
        self.mesh = vtk.vtkPolyData()
        self.appendPolyFilter = vtk.vtkAppendPolyData()
        self.actor = vtk.vtkAssembly()

    def addObject(self, mesh):
        if isinstance(mesh, str):
            mesh = self.getPolyfromFile(mesh)

        if isinstance(mesh, vtk.vtkPolyData):
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputData(mesh)
            mesh = utils.makeActor(mesh)
            self.actor.AddPart(mesh)
        mesh = mesh.GetMapper().GetInput()
        self.appendPolyFilter.AddInputData(mesh)
        self.appendPolyFilter.Update()
        self.mesh = self.appendPolyFilter.GetOutput()

    @staticmethod
    def make_default_stage3d():
        stage = Stage3d()
        stage.addObject(utils.makeCube(center=[0, 0, 0], shape=[10, 100, 100]))
        stage.addObject(utils.makeCube(center=[0, 0, 0], shape=[100, 10, 10]))
        stage.addObject(utils.makeCube(center=[0, 0, 0], shape=[500, 500, 1]))
        stage.addObject(utils.makeSphere(center=[30, 30, 30], radius=20))
        return Stage3d.make_your_stage3d()
        return stage

    @staticmethod
    def make_your_stage3d():
        # TODO: modify this function
        # to make your own stage
        # then, let make_default_stage3d return make_your_statge3d()
        # example is in above
        stage = Stage3d()
        np.random.seed(5)
        cube = utils.makeCube(center=[0, 0, 0], shape=[10, 100, 100])
        for i in range(10):
            cube1 = utils.transModel(cube, rot=np.random.randint(0,45, 3), pos=[i*15, 10 + i*3, 0])
            stage.addObject(cube1)
        stage.addObject(utils.makeCube(center=[0, 0, 0], shape=[500, 500, 1]))
        stage.addObject(utils.makeSphere(center=[30, 30, 30], radius=20))
        return stage

if __name__ == '__main__':
    s = Stage3d.make_default_stage3d()

    #s = Stage3d.make_your_stage3d()
    utils.show_in_vtk([s.actor])