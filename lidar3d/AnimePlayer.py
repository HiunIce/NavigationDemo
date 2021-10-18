from lidar3d.Stage import Stage3d
from lidar3d.LidarCore import Lidar
import lidar3d.utils as utils
class AnimePlayer:
    def __init__(self, turns, time_speed=5):
        s = Stage3d.make_default_stage3d()
        self.li = Lidar(s.mesh)

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


if __name__ == "__main__":
    AnimePlayer(20)