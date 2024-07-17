import sys
import numpy as np
from PyQt6 import QtWidgets, QtCore
from vispy import scene
from vispy.color import Colormap

class ImageViewerWithColorBar(scene.SceneCanvas):
    def __init__(self):
        super().__init__(keys='interactive', bgcolor='transparent')
        
        self.unfreeze()
        
        grid = self.central_widget.add_grid(spacing=0, margin=0)
        
        # Image
        view = grid.add_view(row=0, col=0)
        
        size = 100
        image_data = np.random.rand(size, size).astype(np.float32)

        self.image = scene.visuals.Image(image_data, parent=view.scene, cmap='viridis')

        view.camera = scene.PanZoomCamera(rect=(0, 0, size, size), aspect=1)
        view.camera.set_range()
        view.camera.interactive = False
        
        # Colorbar
        cmap = Colormap(['#000000', '#FF0000', '#FFFF00', '#FFFFFF'])
        colorbar_widget = grid.add_widget(row=0, col=1)
        self.colorbar = scene.ColorBarWidget(cmap, orientation='right', label='Intensity', 
                                             label_color='white')
        colorbar_widget.add_widget(self.colorbar)
        self.colorbar.clim = (0, 1)
        
        self.freeze()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Image Viewer with Color Bar')
        
        self.setStyleSheet("background-color: #2D2D2D;")
        
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.viewer = ImageViewerWithColorBar()
        viewer_widget = self.viewer.native
        # viewer_widget.setFixedSize(500, 400)  # Adjust size as needed
        layout.addWidget(viewer_widget)
        
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()