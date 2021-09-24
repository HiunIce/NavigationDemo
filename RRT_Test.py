import numpy as np
import cv2
from RRTBase import RRT
import matplotlib.pyplot as plt

test_rrt_seed = -1

def test_RRT(displayCallback=None):
    import cv2
    def makeTestGrid(shape=(300, 300)):
        bm = np.zeros(shape=shape, dtype=np.uint8)
        if test_rrt_seed >= 0:
            np.random.seed(test_rrt_seed)
        for i in range(10):
            p1 = np.random.randint(0, bm.shape[0], 2)
            p2 = np.copy(p1)
            p2[np.random.randint(0, 2)] = np.random.randint(0, 100)
            cv2.line(bm, p1, p2, 255, thickness=3, lineType=4, shift=0)
        return bm
    bm = makeTestGrid()

    pos = [100, 100]
    tar = [250, 250]
    rs = RRT.fast_search(bm, pos, tar, displayCallback=displayCallback)

    cv2.circle(bm, pos, 10, 255, 1)
    cv2.circle(bm, tar, 10, 255, 1)

    for p in rs:
        cv2.circle(bm, p, 3, 255, -1)

    for idx in range(len(rs) - 1):
        cv2.line(bm, rs[idx], rs[idx + 1], 255, 1, 4, 0)

    if not displayCallback:
        plt.imshow(bm)
        plt.show()
    else:
        pass
        displayCallback(bm, add=rs)


def testWithAnimation():
    from PyQt5.QtGui import QPainter, QImage, QColor
    from PyQt5.QtWidgets import QWidget, QApplication
    import sys
    import utils
    class showWidget(QWidget):
        def __init__(self, parent=None):
            QWidget.__init__(self, parent=parent)
            self.img = None

        def paintEvent(self, a0):
            pt = QPainter(win)
            if self.img is not None:
                pt.drawImage(self.rect(), utils.toQImage(self.img))

        def setInputImg(self, img):
            self.img = img
            self.update()

        def drawFinishLine(self, rs):
            self.img = cv2.cvtColor(self.img, cv2.COLOR_GRAY2BGR)
            for idx in range(len(rs) - 1):
                p0 = rs[idx]
                p1 = rs[idx + 1]
                #print(p0, '--->', p1)
                cv2.line(self.img, rs[idx], rs[idx + 1], (255,0,0), 1, 4, 0)
            print('draw line fin')
            self.update()

        def start(self):
            def callback(a, **kargs):
                if 'add' in kargs.keys():
                    win.drawFinishLine(kargs['add'])
                else:
                    win.setInputImg(a)
                QApplication.processEvents()
            test_RRT(callback)


    app = QApplication(sys.argv)
    win = showWidget()
    win.show()
    win.start()

    sys.exit(app.exec_())


if __name__ == "__main__":
    testWithAnimation()