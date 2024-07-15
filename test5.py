import sys
import numpy as np
from PyQt6 import QtWidgets
from vispy import scene, visuals
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class VispyCanvas(scene.SceneCanvas):
    def __init__(self, parent=None):
        super().__init__(keys='interactive', parent=parent, bgcolor='white')
        self.unfreeze()

        # Create a grid layout to hold the image
        grid = self.central_widget.add_grid()

        # Generate a random image
        self.image_data = np.random.rand(100, 100).astype(np.float32)

        # Create the Image visual
        self.image_view = grid.add_view(row=0, col=0)
        self.image = scene.visuals.Image(self.image_data, parent=self.image_view.scene, cmap='viridis')
        self.image_view.camera = scene.PanZoomCamera(aspect=1)
        self.image_view.camera.set_range()

        # Add a scale bar
        self.add_scale_bar()

        self.freeze()

    def add_scale_bar(self):
        # Define scale bar parameters
        bar_length = 20  # Length of the scale bar in pixels
        bar_height = 5   # Height of the scale bar in pixels
        bar_color = 'white'  # Color of the scale bar
        text_color = 'white'  # Color of the text

        # Define positions
        canvas_size = self.size
        x_pos = 10  # 10 pixels padding from the left edge
        y_pos = canvas_size[1] - bar_height - 10  # 10 pixels padding from the bottom edge

        # Create the scale bar
        bar = visuals.rectangle(center=(x_pos + bar_length / 2, y_pos + bar_height / 2), 
                                width=bar_length, height=bar_height, 
                                color=bar_color, parent=self.image_view.scene)
        
        # Add text label for the scale bar
        text = visuals.text(f'{bar_length}px', color=text_color, 
                            pos=(x_pos + bar_length / 2, y_pos - 10), 
                            parent=self.image_view.scene, font_size=10, 
                            anchor_x='center', anchor_y='top')

class MatplotlibColorBar(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(figsize=(1, 5))
        self.fig.subplots_adjust(left=0.5, right=0.8, top=0.9, bottom=0.1)
        
        # Create a colorbar
        self.cbar = self.fig.colorbar(plt.cm.ScalarMappable(cmap='viridis'), cax=self.ax)
        
        super().__init__(self.fig)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('NumPy Array with Matplotlib Color Bar and Scale Bar')
        
        # Create central widget
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(central_widget)
        
        # Create and add Vispy canvas
        self.canvas = VispyCanvas()
        layout.addWidget(self.canvas.native)
        
        # Create and add Matplotlib color bar
        self.colorbar = MatplotlibColorBar()
        layout.addWidget(self.colorbar)
        
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()
