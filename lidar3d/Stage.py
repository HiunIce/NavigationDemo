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
        return stage


if __name__ == '__main__':
    s = Stage3d.make_default_stage3d()
    pnts = utils.getPoints(utils.makeSphere(center=[30, 30, 30], radius=20))
    print(pnts)
    utils.show_in_vtk([s.actor])
