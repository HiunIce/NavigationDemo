import numpy as np


class MobileRobot:
    def __init__(self, idx, pos=np.zeros(2, dtype=np.int32)):
        self.pos = pos
        self.type = idx



