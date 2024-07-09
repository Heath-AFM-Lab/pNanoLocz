import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from vispy import app, scene

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Vispy Video with PyQt6 Example")
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget for the main window
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        layout = QVBoxLayout(central_widget)

        # Create a Vispy canvas widget
        self.canvas = scene.SceneCanvas(keys='interactive', parent=central_widget)
        layout.addWidget(self.canvas.native)

        # Create a Vispy view
        self.view = self.canvas.central_widget.add_view()

        # Set up camera and view
        self.view.camera = 'panzoom'
        self.view.camera.rect = (0, 0, 1600, 1200)

        # Initialize frame counter and maximum frames
        self.frame_count = 0
        self.max_frames = 10000  # Number of frames for the video (increased to 10000)

        # Start the update timer
        self.timer = app.Timer('auto', connect=self.update_video, start=True)

    def update_video(self, event):
        # Generate RGB random noise for the current frame
        width, height = 1600, 1200
        rgb_noise = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)

        # Update the image visual with the new frame
        if self.frame_count < self.max_frames:
            if self.frame_count == 0:
                # Create the initial Image visual
                self.image_visual = scene.visuals.Image(rgb_noise, parent=self.view.scene, interpolation='nearest')
            else:
                # Update the existing Image visual
                self.image_visual.set_data(rgb_noise)

            # Increment frame count
            self.frame_count += 1
        else:
            # Reset frame count for infinite loop
            self.frame_count = 0

        # Ensure canvas updates
        self.canvas.update()

if __name__ == "__main__":
    appQt = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(appQt.exec())
