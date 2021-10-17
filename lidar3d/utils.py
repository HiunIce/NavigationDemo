import vtkmodules.all as vtk
import os
import numpy as np
from vtkmodules.util import numpy_support

def getPolyfromFile(path):
    suffix = os.path.splitext(path)[-1]
    d = dict({
        ".vtk": vtk.vtkPolyDataReader(),
        ".obj": vtk.vtkOBJReader(),
        ".stl": vtk.vtkSTLReader(),
    })
    reader = d[suffix]
    reader.SetFileName(path)
    reader.Update()
    return reader.GetOutput()

def makeActor(mesh, color=[1, 1, 1], opacity=1.0):
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(mesh)
    mapper.Update()

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetDiffuseColor(color)
    actor.GetProperty().SetOpacity(opacity)
    return actor


def makeCube(center=None, shape=None, bounds=None):
    src = vtk.vtkCubeSource()
    if bounds is not None:
        if np.array(bounds).size != 6:
            raise TypeError('Bounds must be given as length 6 tuple: (xMin,xMax, yMin,yMax, zMin,zMax)')
        src.SetBounds(bounds)
    else:
        src.SetCenter(center)
        src.SetXLength(shape[0])
        src.SetYLength(shape[1])
        src.SetZLength(shape[2])
    src.Update()
    return src.GetOutput()

def makeSphere(center, radius, res_theta=10, res_phi=10):
    src = vtk.vtkSphereSource()
    src.SetCenter(center[0], center[1], center[2])
    src.SetRadius(radius)
    src.SetThetaResolution(res_theta)
    src.SetPhiResolution(res_phi)
    src.Update()

    bkdata = vtk.vtkPolyData()
    bkdata.DeepCopy(src.GetOutput())
    return bkdata


def getPoints(mesh):
    if isinstance(mesh, vtk.vtkActor):
        mesh = mesh.GetMapper().GetInput()
    points = mesh.GetPoints()
    as_numpy = numpy_support.vtk_to_numpy(points.GetData())
    return as_numpy

def anyDisplayFilter(data):
    if isinstance(data, vtk.vtkActor) \
        or isinstance(data, vtk.vtkVolume) \
        or isinstance(data, vtk.vtkActor2D):
        return data
    elif isinstance(data, vtk.vtkPolyData):
        data = makeActor(data)
    return data

def show_in_vtk(things=[], moveAxis=None, screenShoot=None, camera=None):
    win = vtk.vtkRenderWindow()
    ren = vtk.vtkRenderer()
    ren.SetBackground(1.0, 1.0, 1.0)
    ren.SetBackground2(0.529, 0.8078, 0.92157)
    ren.SetGradientBackground(True)
    win.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
    iren.SetRenderWindow(win)
    things = [anyDisplayFilter(sth) for sth in things]
    for sth in things:
        ren.AddViewProp(sth)

    ren.ResetCamera(things[0].GetBounds())
    if camera is not None:
        ren.SetCamera(camera)
    win.Render()
    iren.Start()


def numpyArray2vtkPoints(pts):
    points = vtk.vtkPoints()
    points.SetData(numpy_support.numpy_to_vtk(pts))
    return points


def makePointCloud(points, radius=1, colorVec=None):
    poly = vtk.vtkPolyData()
    if isinstance(points, np.ndarray):
        if points.shape[0] == 0:
            return vtk.vtkPolyData()
        points = numpyArray2vtkPoints(points)
    poly.SetPoints(points)

    if colorVec is not None:
        color = vtk.vtkDoubleArray()
        color.SetNumberOfValues(colorVec.shape[0])
        color.SetName("Colors")
        for i in range(colorVec.shape[0]):
            color.SetValue(i, colorVec[i])
        poly.GetPointData().AddArray(color)

    poly.Modified()
    sphere = vtk.vtkSphereSource()
    sphere.SetRadius(radius)
    sphere.Update()

    glyph = vtk.vtkGlyph3D()
    glyph.SetSourceData(sphere.GetOutput())
    glyph.SetInputData(poly)
    glyph.SetScaleFactor(1)
    glyph.Update()

    return glyph.GetOutput()


def translateActor(obj, pos):
    mat = obj.GetUserMatrix()
    if mat is None:
        mat = vtk.vtkMatrix4x4()
        obj.SetUserMatrix(mat)
    mat.SetElement(0, 3, pos[0])
    mat.SetElement(1, 3, pos[1])
    mat.SetElement(2, 3, pos[2])
    obj.SetUserMatrix(mat)
