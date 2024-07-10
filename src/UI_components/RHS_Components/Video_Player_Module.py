import sys
import os
import numpy as np
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from vispy import app, scene
from vispy.gloo import set_clear_color
from UI_components.RHS_Components.Video_Player_Components import VideoControlWidget, VideoDepthControlWidget, VisualRepresentationWidget, ExportAndVideoScaleWidget
from constants import PATH_TO_ICON_DIRECTORY

class FixedPanZoomCamera(scene.cameras.PanZoomCamera):
    def viewbox_mouse_event(self, event):
        # Ignore all mouse events to lock the video in place
        return

class VideoPlayerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.buildVideoPlayerWidgets()
        # TODO: reconfigure to actually load a file
        self.loadFrames()
        self.frame_index = 0

        # Timer to update the frames
        self.timer = app.Timer('auto', connect=self.update_frame, start=False)

    def buildVideoPlayerWidgets(self):
        # Set up video player layout 
        self.mediaLayout = QVBoxLayout()
        self.mediaLayout.setContentsMargins(0, 0, 0, 0)
        self.mediaLayout.setSpacing(0)

        self.iconLayout = QHBoxLayout()
        self.iconLayout.addStretch(1)

        # Add screenshot icon
        self.screenshotIcon = QPushButton()
        self.screenshotIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "pop.png")))
        self.screenshotIcon.setIconSize(self.screenshotIcon.sizeHint())
        self.screenshotIcon.setToolTip("Screenshot video")
        self.screenshotIcon.setFixedSize(16, 16)
        self.iconLayout.addWidget(self.screenshotIcon)
        self.mediaLayout.addLayout(self.iconLayout)

        # Set up Vispy canvas
        self.videoPlayerContainer = QWidget()
        self.vispyCanvas = scene.SceneCanvas(keys='interactive', parent=self.videoPlayerContainer, bgcolor=None)
        # self.vispyCanvas.native.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # Expand to fill space
        self.mediaLayout.addWidget(self.vispyCanvas.native)

        self.view = self.vispyCanvas.central_widget.add_view()
        self.view.camera = FixedPanZoomCamera()
        self.view.camera.zoom_factor = 1.0  # Set initial zoom factor

        self.setLayout(self.mediaLayout)

        # Initialize the rest of the widgets
        self.videoControlWidget = VideoControlWidget()
        self.visualRepresentationWidget = VisualRepresentationWidget()
        self.videoDepthControlWidget = VideoDepthControlWidget()
        self.exportAndVideoScaleWidget = ExportAndVideoScaleWidget()

        # Connect signals to slots
        self.videoControlWidget.playClicked.connect(self.playPauseVideo)
        self.videoControlWidget.skipBackClicked.connect(self.skipBackward)
        self.videoControlWidget.skipForwardClicked.connect(self.skipForward)
        self.videoControlWidget.fpsChanged.connect(self.changePlaybackRate)
        self.videoControlWidget.specificVideoFrameGiven.connect(self.goToFrameNo)
        self.videoControlWidget.videoSeekSlider.valueChanged.connect(self.setVideoPosition)
        self.videoControlWidget.videoSeekSlider.sliderReleased.connect(self.sliderReleased)

        # Fix all sizes
        self.videoControlWidget.setFixedSize(self.videoControlWidget.sizeHint())
        self.visualRepresentationWidget.setFixedSize(self.visualRepresentationWidget.sizeHint())
        self.videoDepthControlWidget.setFixedSize(self.videoDepthControlWidget.sizeHint())
        self.exportAndVideoScaleWidget.setFixedSize(self.exportAndVideoScaleWidget.sizeHint())

        # Compose all widgets
        videoControlLayout = QHBoxLayout()
        videoControlLayout.addWidget(self.videoControlWidget)
        videoControlLayout.addWidget(self.visualRepresentationWidget)
        videoControlLayout.addStretch(1)
        videoControlLayout.addWidget(self.videoDepthControlWidget)

        self.mediaLayout.addLayout(videoControlLayout)
        self.mediaLayout.addWidget(self.exportAndVideoScaleWidget)

        # Adapt the video player widget to match the size of the lower control widgets
        self.adjustSizeToFitBottomWidgets()
        
        # Disable widgets until loadFrames is called
        self.disableWidgets()

    def adjustSizeToFitBottomWidgets(self):
        widthOfControlWidgets = self.videoControlWidget.width() + self.visualRepresentationWidget.width() + self.videoDepthControlWidget.width()
        self.videoPlayerContainer.setFixedSize(widthOfControlWidgets, widthOfControlWidgets)


    # TODO: create proper load frames func that 
    # triggers after user selects a file to open
    def loadFrames(self):
        # Example: Generate random frames
        self.frames = [np.random.randint(0, 256, (512, 512), dtype=np.uint8) for _ in range(100)]
        self.image_visual = scene.visuals.Image(self.frames[0], parent=self.view.scene, interpolation='nearest')

        # Update slider with max frames
        self.videoControlWidget.videoSeekSlider.setRange(0, len(self.frames) - 1)

        # Update frame selector with max frames
        self.videoControlWidget.frameSpinBox.setRange(1, len(self.frames))

        # Enable widgets
        self.enableWidgets()
        
        # Update the view camera to fit the entire image
        self.update_view_camera()

    def disableWidgets(self):
        self.videoControlWidget.setDisabled(True)
    
    def enableWidgets(self):
        self.videoControlWidget.setEnabled(True)

    # Following functions are for the video control widget, to play and control the video
    def update_frame(self, event):
        # Update the slider position
        self.videoControlWidget.videoSeekSlider.blockSignals(True)
        self.videoControlWidget.videoSeekSlider.setValue(self.frame_index)
        self.videoControlWidget.videoSeekSlider.blockSignals(False)

        # Update frame number
        self.videoControlWidget.frameSpinBox.blockSignals(True)
        self.videoControlWidget.frameSpinBox.setValue(self.frame_index + 1)
        self.videoControlWidget.frameSpinBox.blockSignals(False)

        # Update the image visual with the new frame
        self.image_visual.set_data(self.frames[self.frame_index])
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.vispyCanvas.update()

    def update_view_camera(self):
        # Adjust the camera to fit the entire image
        img_height, img_width = self.frames[0].shape
        self.view.camera.set_range(x=(0, img_width), y=(0, img_height))
        self.view.camera.aspect = 1.0 * img_width / img_height

    def playPauseVideo(self):
        if self.timer.running:
            self.timer.stop()
            self.videoControlWidget.playIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "play.png")))
            self.videoControlWidget.playIcon.setToolTip("Play")
        else:
            self.timer.start()
            self.videoControlWidget.playIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "pause.png")))
            self.videoControlWidget.playIcon.setToolTip("Pause")

    def skipForward(self):
        self.frame_index = min(self.frame_index + 29, len(self.frames) - 1)  # Skip 30 frames forward
        self.update_frame(None)

    def skipBackward(self):
        self.frame_index = max(self.frame_index - 31, 0)  # Skip 30 frames backward
        self.update_frame(None)

    def changePlaybackRate(self, fps):
        self.timer.interval = 1.0 / fps

    def goToFrameNo(self, frameNo):
        if 1 <= frameNo <= len(self.frames):
            self.frame_index = frameNo - 1
            self.update_frame(None)  # Update the frame immediately

    def setVideoPosition(self, position):
        self.frame_index = position

    def sliderReleased(self):
        self.update_frame(None)

    def deleteFrames(self, min, max):
        pass

if __name__ == "__main__":
    # Path to icon directory
    ICON_DIRECTORY = "../../../assets/icons"
    PATH_TO_ICON_DIRECTORY = os.path.abspath(os.path.join(os.getcwd(), ICON_DIRECTORY))
    app = QApplication(sys.argv)
    videoPlayerWidget = VideoPlayerWidget()
    videoPlayerWidget.show()
    sys.exit(app.exec())
