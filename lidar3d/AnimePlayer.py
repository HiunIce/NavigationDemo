from lidar3d.Stage import Stage3d
from lidar3d.LidarCore import Lidar
import lidar3d.utils as utils
import numpy as np


class AnimePlayer:
    def __init__(self, turns, time_speed=5, model=None):
        s = Stage3d.make_default_stage3d()
        self.li = Lidar(s.mesh, model=model)

        self.iterations = turns
        self.renderer, self.win, self.iren = utils.makeVtkRenderWindow()
        actors = [self.li.actor,
                  utils.makeActor(self.li.target_model, opacity=1),
                  self.li.sampled_filter.actor
                  ]
        for a in actors:
            self.renderer.AddActor(a)
        self.renderer.ResetCamera(actors[1].GetBounds())
        self.iren.Initialize()
        self.iren.AddObserver('TimerEvent', self.execute)
        self.timerId = self.iren.CreateRepeatingTimer(time_speed)
        self.win.SetSize(800, 800)
        self.iren.Start()

    def execute(self, iren, event):
        if self.iterations == 0:
            iren.DestroyTimer(self.timerId)

        self.li.scan()
        mov = -10#self.iterations * 10

        self.li.moveInXYPlane(mov, mov)
        #self.li.setLidarPosition([150 + mov, 150 + mov, 10])
        self.renderer.Render()
        iren.GetRenderWindow().Render()
        iren.Render()
        self.iterations -= 1


def test_anime():
    AnimePlayer(turns=20)

def test_anime_your_model():
    # TODO: make your sensor looks cooler
    # find a 3d model in https://free3d.com/
    # search a car, machine, or anything you like
    # remember, your model should be end with '.obj'
    # if your model is small or need to be rotated
    # use function utils.transModel.

    model = 'C:/Users/psw-e/PycharmProjects/NavigationDemo/lidar3d/model/UFO_Empty.obj'
    model = utils.getPolyfromFile(model)
    model = utils.transModel(model, rot=[90,0,0], scale=4)
    ani = AnimePlayer(turns=20, model=model)

    # to save the points you sampled
    # it will be saved after you closed the window
    np.save('test_pnt.npy', ani.li.sampled_pnts)


def showWhatYouSampled():
    # take a screen shot of your sampled feature
    # remember take a photo for the result
    # because the function is time consuming

    pts = np.load('test_pnt.npy')
    cloud = utils.makeActor(utils.makePointCloud(pts, radius=0.3), color=[0, 1, 0])
    pts = utils.numpyArray2vtkPoints(pts)
    # this function is time consuming, please wait
    mesh = utils.reconstructionFromPoints(pts)

    actor = utils.makeActor(mesh, color=[1, 1, 1])
    mapper = actor.GetMapper()
    mapper.ScalarVisibilityOff()
    mapper.Update()

    origin_stage = utils.makeActor(Stage3d.make_default_stage3d().mesh, color=[0, 1, 1], opacity=0.1)
    utils.show_in_vtk([actor, cloud, origin_stage])

if __name__ == "__main__":
    pass
    # test_anime() # step1 run this function
    # test_anime()
    # test_anime_your_model() # step 2 run this function
    showWhatYouSampled() # step 3 run this function