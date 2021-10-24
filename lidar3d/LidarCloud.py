# If you are do not want to learn visualization by yourself,
# do not reading this script, it will makes you confused.


import vtkmodules.all as vtk
import lidar3d.utils as utils
from vtkmodules.util import numpy_support


class LidarCloud:
    def __init__(self):
        self.poly = vtk.vtkPolyData()
        self.points = vtk.vtkPoints()
        self.poly.SetPoints(self.points)
        self.poly.Modified()

        sphere = vtk.vtkSphereSource()
        sphere.SetRadius(0.2)
        sphere.Update()

        self.glyph = vtk.vtkGlyph3D()
        self.glyph.SetSourceData(sphere.GetOutput())
        self.glyph.SetInputData(self.poly)
        self.glyph.SetScaleFactor(1)
        self.glyph.Update()
        self.actor = utils.makeActor(self.glyph.GetOutput(), color=[0, 0, 1])
        self.mapper = self.actor.GetMapper()

    def setRadius(self, rad):
        self.glyph.SetScaleFactor(rad)
        self.Update()

    def setPoints(self, pts):
        self.points.SetData(numpy_support.numpy_to_vtk(pts))
        self.points.Modified()
        #self.poly.Modified()
        self.Update()

    def Update(self):
        # the upper case of 'Update' is to keep the coding style with vtk
        self.glyph.Update()
