import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from vispy import app, scene, color

class PlayerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Frame Player")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

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

        # Trigger canvas update
        self.canvas.update()

if __name__ == '__main__':
    appQt = QApplication(sys.argv)
    player = PlayerWindow()
    player.show()
    sys.exit(appQt.exec())
