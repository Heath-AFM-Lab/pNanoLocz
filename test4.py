import sys
import numpy as np
from PyQt6 import QtWidgets, QtCore, QtGui
from vispy import scene
from vispy.color import Colormap

class ImageViewer(scene.SceneCanvas):
    def __init__(self):
        super().__init__(keys='interactive', bgcolor='transparent', always_on_top=True)
        
        self.unfreeze()
        
        view = self.central_widget.add_view(margin=0)
        
        size = 100
        image_data = np.random.rand(size, size).astype(np.float32)

        self.image = scene.visuals.Image(image_data, parent=view.scene, cmap='viridis')

        view.camera = scene.PanZoomCamera(rect=(0, 0, size, size), aspect=1)
        view.camera.set_range()
        view.camera.interactive = False
        
        self.freeze()

class ColorBarWidget(scene.SceneCanvas):
    def __init__(self):
        super().__init__(bgcolor='transparent')
        
        self.unfreeze()
        
        grid = self.central_widget.add_grid(margin=0)
        
        cmap = Colormap(['#000000', '#FF0000', '#FFFF00', '#FFFFFF'])
        self.colorbar = scene.ColorBarWidget(cmap, orientation='right', label='Intensity', 
                                             label_color='white')
        grid.add_widget(self.colorbar)
        self.colorbar.clim = (0, 1)
        
        self.freeze()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Image Viewer with Color Bar')
        
        # Set the background color to match system's dark mode grey
        # self.setStyleSheet("background-color: #2D2D2D;")
        
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.image_viewer = ImageViewer()
        self.image_viewer.native.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint, True)

        image_widget = self.image_viewer.native

        image_widget.setFixedSize(400, 400)
        layout.addWidget(image_widget)
        
        self.colorbar = ColorBarWidget()
        colorbar_widget = self.colorbar.native
        colorbar_widget.setFixedSize(100, 400)
        layout.addWidget(colorbar_widget)
        
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()