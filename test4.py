import sys
import numpy as np
from PyQt6 import QtWidgets
from vispy import scene
from vispy.color import Colormap


class FixedPanZoomCamera(scene.cameras.PanZoomCamera):
    def viewbox_mouse_event(self, event):
        # Ignore all mouse events to lock the video in place
        return
    
class MyCanvas(scene.SceneCanvas):
    def __init__(self, parent=None):
        super().__init__(keys='interactive', parent=parent, bgcolor='white')
        self.unfreeze()
        
        # Create a grid layout to hold the image and colorbar
        grid = self.central_widget.add_grid()

        # Generate a random image
        image_data = np.random.rand(100, 100).astype(np.float32)

        # Create the Image visual
        self.image_view = grid.add_view(row=0, col=0)
        self.image = scene.visuals.Image(image_data, parent=self.image_view.scene, cmap='viridis')
        self.image_view.camera = FixedPanZoomCamera()
        self.image_view.camera.set_range()

        # Create the ColorBar visual
        self.colorbar_view = grid.add_view(row=0, col=1)
        cmap = Colormap(['blue', 'green', 'yellow', 'red'])
        self.colorbar = scene.visuals.ColorBar(cmap=cmap, orientation='right',
                                               size=(100, 10), parent=self.colorbar_view.scene)
        self.colorbar_view.camera = FixedPanZoomCamera()



        self.freeze()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('NumPy Array with Color Bar')
        self.canvas = MyCanvas()
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas.native)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()
