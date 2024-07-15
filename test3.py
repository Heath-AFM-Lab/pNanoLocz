from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSignal
from vispy import app, scene
import numpy as np

class VispyCanvasWidget(QWidget):
    frame_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # Create a Vispy canvas
        self.canvas = scene.SceneCanvas(keys='interactive', show=True)
        layout.addWidget(self.canvas.native)

        # Create a 3D array of random data (100 frames of 200x200 arrays)
        self.frames = np.random.rand(100, 200, 200)

        # Initialize Vispy visuals with a colormap
        self.image = scene.visuals.Image(self.frames[0], parent=self.canvas.scene, cmap='inferno')

        # Timer to animate frames
        self.timer = app.Timer('auto', connect=self.update_frame, start=True)

    def update_frame(self, event):
        # Update the frame displayed
        current_frame = event.iteration % len(self.frames)
        self.image.set_data(self.frames[current_frame])

        # Emit signal with current frame number
        self.frame_changed.emit(current_frame)

        # Trigger canvas update
        self.canvas.update()



from PyQt6.QtWidgets import QWidget, QVBoxLayout
from vispy import scene

class ColorBarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # Create a ColorBarWidget from Vispy
        self.colorbar = scene.ColorBarWidget(orientation='right', cmap='inferno')
        layout.addWidget(self.colorbar)

        # Optionally, adjust the size policy or other properties as needed
        self.setMinimumWidth(100)  # Example: adjust minimum width

    def update_colorbar(self, frame_data):
        # Update color bar with new data or limits
        self.colorbar.update_colorbar(frame_data)






import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from vispy import app, scene
from vispy.visuals.transforms import STTransform


class PlayerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Frame Player")
        self.setGeometry(100, 100, 900, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Create VispyCanvasWidget
        self.vispy_widget = VispyCanvasWidget()
        layout.addWidget(self.vispy_widget)

        # Create ColorBarWidget
        self.colorbar_widget = ColorBarWidget()
        layout.addWidget(self.colorbar_widget)

        # Connect signals for synchronization
        self.vispy_widget.frame_changed.connect(self.colorbar_widget.update_colorbar)

        # Initialize the application
        self.init_application()

    def init_application(self):
        # Any initialization logic can go here
        pass


if __name__ == '__main__':
    appQt = QApplication(sys.argv)
    player = PlayerWindow()
    player.show()
    sys.exit(appQt.exec())



