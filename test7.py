import sys
import numpy as np
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSizePolicy
from vispy import scene, app
from vispy.scene import visuals

class VispyWidget(QWidget):
    def __init__(self, video_frames, parent=None):
        super().__init__(parent)
        
        # Store video frames
        self.video_frames = video_frames
        self.current_frame_index = 0
        
        # Create a layout for the widget
        layout = QVBoxLayout(self)
        
        # Create a Vispy canvas
        self.canvas = scene.SceneCanvas(keys='interactive', show=True)
        layout.addWidget(self.canvas.native)
        
        # Create a viewbox to display the image
        self.view = self.canvas.central_widget.add_view()
        
        # Create an Image visual
        self.image = visuals.Image(video_frames[0], parent=self.view.scene, method='auto')
        
        # Adjust camera to fit the image without padding
        self.view.camera = scene.cameras.PanZoomCamera(aspect=1)
        self.view.camera.rect = (0, 0, video_frames[0].shape[1], video_frames[0].shape[0])

        # Set the size policy to expand and fill the space
        self.canvas.native.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.canvas.native.setMinimumSize(400, 400)  # Set a minimum size to prevent resizing issues

        # Setup a timer to update the frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update frame every 30 ms (approx 33 FPS)
        
    def update_frame(self):
        # Update the image with the next frame
        self.image.set_data(self.video_frames[self.current_frame_index])
        self.current_frame_index = (self.current_frame_index + 1) % len(self.video_frames)
        self.canvas.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = self.canvas.native.size()
        new_size = min(size.width(), size.height())
        self.canvas.native.resize(new_size, new_size)
        self.view.camera.aspect = 1
        

    def stopTimer(self):
        self.timer.stop()

    def startTimer(self):
        self.timer.start()

if __name__ == '__main__':
    # Generate a random video using NumPy (100 frames of 100x100 RGB images)
    video_frames = np.random.rand(100, 100, 100, 3).astype(np.float32)
    
    # Create the PyQt6 application
    app = QApplication(sys.argv)
    
    # Create the main window
    main_window = QWidget()
    main_window.setWindowTitle('Vispy Video Display')
    
    # Create and add the Vispy widget to the main window
    vispy_widget = VispyWidget(video_frames)
    layout = QVBoxLayout()
    main_window.setLayout(layout)
    layout.addWidget(vispy_widget)
    
    # Show the main window
    main_window.show()
    
    # Start the PyQt6 event loop
    sys.exit(app.exec())
