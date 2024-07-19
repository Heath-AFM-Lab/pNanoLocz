import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSizePolicy, QSpacerItem, QHBoxLayout
from PyQt6.QtCore import QTimer, pyqtSignal, Qt, QSize
from vispy import scene
from vispy.scene import visuals

DEFAULT_FPS = 30


class VispyVideoPlayerWidget(QWidget):
    update_widgets = pyqtSignal()

    def __init__(self, video_frames, parent=None):
        super().__init__(parent)
        
        # Store video frames
        self.video_frames = video_frames
        self.current_frame_index = 0
        self.resizing = False  # Flag to prevent recursive resize
        
        # Create a layout for the widget
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create a Vispy canvas
        self.canvas = scene.SceneCanvas(keys='interactive', show=True)
        
        # Add the Vispy canvas to the layout, centre widget
        layout.addSpacing(1)
        layout.addWidget(self.canvas.native)
        layout.addSpacing(1)

        # Create a viewbox to display the image
        self.view = self.canvas.central_widget.add_view()
        
        # Create an Image visual
        self.image = visuals.Image(video_frames[0], parent=self.view.scene, method='auto')
        
        # Adjust camera to fit the image without padding
        self.view.camera = scene.cameras.PanZoomCamera(aspect=1)
        self.view.camera.rect = (0, 0, video_frames[0].shape[1], video_frames[0].shape[0])

        # Adjust size policy
        # if video_frames[0].shape[1] > video_frames[0].shape[0]:
        #     self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        # else:
        #     self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Lock the camera
        self.view.camera.interactive = False

        # Setup a timer to update the frames
        self.timer = QTimer()
        self.timer.timeout.connect(self._go_to_next_frame)
        self.set_fps(DEFAULT_FPS)  # Baseline FPS, default is DEFAULT_FPS
        self.timer.stop()

    ### Override methods for dimensions
    def resizeEvent(self, event):
        if self.resizing:
            return
        self.resizing = True
        super().resizeEvent(event)
        widget_width = self.width()
        widget_height = self.height()

        video_aspect_ratio = self.video_frames[0].shape[1] / self.video_frames[0].shape[0]
        widget_aspect_ratio = widget_width / widget_height

        if widget_aspect_ratio > video_aspect_ratio:
            new_width = int(widget_height * video_aspect_ratio)
            new_height = widget_height
            # self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        else:
            new_width = widget_width
            new_height = int(widget_width / video_aspect_ratio)
            # self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # print("image dims", self.video_frames[0].shape[1], self.video_frames[0].shape[0])
        # print("new dims", new_height, new_width)
        # print("widget dims", widget_height, widget_width)

        self.canvas.native.resize(new_width, new_height)
        self.resize(new_width, new_height)
        self.update()
        # print("new widget size", self.size())
        self.view.camera.aspect = 1  # Keep the aspect ratio 1 for camera to avoid distortion
        self.view.camera.set_range(x=(0, self.video_frames[0].shape[1]), y=(0, self.video_frames[0].shape[0]), margin=0)
        self.view.camera.rect = (0, 0, self.video_frames[0].shape[1], self.video_frames[0].shape[0])
        self.resizing = False

    def get_dims(self):
        return self.dims

    ### Vispy video player functions
    def _update_frame(self):
        self.image.set_data(self.video_frames[self.current_frame_index])
        self.update_widgets.emit()
        self.canvas.update()
        
    def _go_to_next_frame(self):
        # Update the image with the next frame
        self.current_frame_index = (self.current_frame_index + 1) % len(self.video_frames)
        self.image.set_data(self.video_frames[self.current_frame_index])

        self.update_widgets.emit()
        self.canvas.update()

    def set_fps(self, fps):
        self.fps = fps
        interval = 1000 // self.fps  # Calculate interval in milliseconds
        self.timer.setInterval(interval)

    def get_fps(self):
        return self.fps

    def skip_forward(self):
        self.current_frame_index = min(self.current_frame_index + 30, len(self.video_frames) - 1)  # Skip 30 frames forward
        self._update_frame()

    def skip_backward(self):
        self.current_frame_index = max(self.current_frame_index - 30, 0)  # Skip 30 frames backward
        self._update_frame()

    def update_frame(self, current_frame_index):
        self.current_frame_index = current_frame_index
        self._update_frame()

    def timer_is_running(self):
        return self.timer.isActive()

    def stop_timer(self):
        self.timer.stop()

    def start_timer(self):
        self.timer.start()

    def go_to_frame_no(self, frame_no):
        self.current_frame_index = frame_no
        self._update_frame()  # Update the frame immediately

    def get_frame_number(self):
        return self.current_frame_index


if __name__ == '__main__':
    # Generate a random video using NumPy (100 frames of 100x100 RGB images)
    video_frames = np.random.rand(100, 100, 100, 3).astype(np.float32)
    
    # Create the PyQt6 application
    app = QApplication(sys.argv)
    
    # Create the main window
    main_window = QWidget()
    main_window.setWindowTitle('Vispy Video Display')
    
    # Create and add the Vispy widget to the main window
    vispy_widget = VispyVideoPlayerWidget(video_frames)
    layout = QVBoxLayout()
    main_window.setLayout(layout)
    layout.addWidget(vispy_widget)
    
    # Show the main window
    main_window.show()
    
    # Start the PyQt6 event loop
    sys.exit(app.exec())
