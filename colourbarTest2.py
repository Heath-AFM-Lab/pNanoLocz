import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout
from vispy import app, scene
from vispy.scene.visuals import Image, ColorBar
from vispy.color import get_colormaps

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Vispy Colourbar Widget Example')

        # Create a central widget and set layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # Create a layout for the image and colourbar
        image_layout = QHBoxLayout()
        layout.addLayout(image_layout)

        # Create a Vispy canvas for the image
        self.image_canvas = scene.SceneCanvas(keys='interactive', bgcolor='white')
        self.image_view = self.image_canvas.central_widget.add_view()
        image_layout.addWidget(self.image_canvas.native)

        # Create a Vispy canvas for the colourbar
        self.colorbar_canvas = scene.SceneCanvas(keys='interactive', bgcolor='white', size=(200, 20))
        self.colorbar_view = self.colorbar_canvas.central_widget.add_view()
        image_layout.addWidget(self.colorbar_canvas.native)

        # Create and display the colourbar and image
        self.create_colorbar_and_image()

    def create_colorbar_and_image(self):
        # Create some data
        data = np.random.rand(10, 10)

        # Create an Image visual with a predefined colormap
        colormap = get_colormaps()['viridis']
        img = Image(data, cmap=colormap, interpolation='bilinear')
        self.image_view.add(img)

        # Add a colourbar
        colorbar = ColorBar(cmap=colormap, size=(200, 20), orientation='bottom')
        self.colorbar_view.add(colorbar)

        # Adjust the views
        self.image_view.camera = 'panzoom'
        self.image_view.camera.aspect = 1.0
        self.colorbar_view.camera = 'panzoom'
        self.colorbar_view.camera.aspect = 10.0  # Flatten the colorbar

if __name__ == '__main__':
    app.use_app('pyqt6')
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
