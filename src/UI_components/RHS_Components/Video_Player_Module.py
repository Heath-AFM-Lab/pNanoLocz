import sys
import os
import numpy as np
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from vispy import app, scene
from vispy.scene import visuals
from UI_components.RHS_Components.Video_Player_Components import VideoControlWidget, VideoDepthControlWidget, VisualRepresentationWidget, ExportAndVideoScaleWidget, VispyVideoPlayerWidget, MatplotlibColourBarWidget
from utils.constants import PATH_TO_ICON_DIRECTORY

class FixedPanZoomCamera(scene.cameras.PanZoomCamera):
    def viewbox_mouse_event(self, event):
        # Ignore all mouse events to lock the video in place
        return
    

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



class VideoPlayerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.buildVideoPlayerWidgets()
        self.framesLoaded = False
        # TODO: reconfigure to actually load a file
        self.loadFrames()


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

        self.mediaLayout.addStretch(1)


        # Set and add a layout to store video player and colour bar
        self.videoPlayerLayout = QHBoxLayout()

        self.videoPlayerLayout.addStretch(1)

        # Placeholder widget for the video player to make the layout look better
        # self.videoPlaceholderWidget = QWidget()
        # self.videoPlaceholderWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # self.videoPlayerLayout.addWidget(self.videoPlaceholderWidget)


        # Set up second SceneCanvas to show the colorbar
        self.colorbarCanvas = scene.SceneCanvas(keys="interactive", bgcolor="transparent")
        self.colorbarGrid = self.colorbarCanvas.central_widget.add_grid(margin=0)

        # self.videoPlayerLayout.addWidget(self.colorbarCanvas.native)
        self.colorbarView = self.colorbarCanvas.central_widget.add_view()
        self.colorbarView.camera = FixedPanZoomCamera()
        self.colorbarView.camera.zoom_factor = 1.0  # Set initial zoom factor

        self.videoPlayerLayout.addStretch(1)

        self.mediaLayout.addLayout(self.videoPlayerLayout)

        self.mediaLayout.addStretch(1)

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
        
        # Disable widgets until loadFrames is called
        self.disableWidgets()

        self.setLayout(self.mediaLayout)




    # TODO: create proper load frames func that 
    # triggers after user selects a file to open
    def loadFrames(self):
        width, height = 512, 512
        # Example: Generate random frames
        self.frames = [np.random.randint(0, 256, (height, width), dtype=np.uint8) for _ in range(100)]

        # Remove placeholder widget
        # self.videoPlaceholderWidget.hide()

        # Set up vispy video player
        # self.videoPlayerLayout.addStretch(1)
        self.vispyVideoPlayerWidget = VispyVideoPlayerWidget(self.frames)
        self.videoPlayerLayout.addWidget(self.vispyVideoPlayerWidget)
        self.vispyVideoPlayerWidget.update_widgets.connect(self.update_widgets)
        # self.videoPlayerLayout.addStretch(1)
        # self.mediaLayout.update()


 
        # TODO: refactor this to become a class 
        self.colorbarWidget = MatplotlibColourBarWidget()
        # self.colorbarWidget.setFixedSize(100, 400)
        self.videoPlayerLayout.addWidget(self.colorbarWidget)
        print(self.colorbarWidget.size())



        # self.colorbar = scene.ColorBarWidget(cmap="grays", orientation='right', label='Intensity', 
        #                                      label_color='white')
        # self.colorbarGrid.add_widget(self.colorbar)
        # self.colorbarCanvas.native.setFixedWidth(100)

        # self.videoPlayerLayout.addSpacing(5)
        # self.videoPlayerLayout.addWidget(self.colorbarCanvas.native)
        # self.colorbarWidget.setFixedSize(100, 400)

        # self.colorbarCanvas.native.hide()
        

        # Create a ColorBarWidget (managed independently)
        # self.colorbar = scene.ColorBarWidget(orientation='right', cmap="plasma")
        # self.colorbar.pos = (750, 50)  # Position of the color bar within the canvas
        # self.colorbar.size = (100, 500)  # Size of the color bar
        # self.colorbar.parent = self.vispyCanvas.scene

        # self.grid.add_widget(self.colorbar)

        # Update slider with max frames
        self.videoControlWidget.videoSeekSlider.setRange(0, len(self.frames) - 1)

        # Update frame selector with max frames
        self.videoControlWidget.frameSpinBox.setRange(1, len(self.frames))

        # Update FPS box with base FPS
        self.videoControlWidget.fpsTextBox.setText(str(self.vispyVideoPlayerWidget.get_fps()))

        # Enable widgets
        self.enableWidgets()
        self.framesLoaded = True

    def disableWidgets(self):
        self.videoControlWidget.setDisabled(True)
    
    def enableWidgets(self):
        self.videoControlWidget.setEnabled(True)


###     VIDEO CONTROL FUNCTIONALITY     ###
# Following functions are for the video control widget, to play and control the video
    def update_widgets(self):
        # Update the slider position
        self.videoControlWidget.videoSeekSlider.blockSignals(True)
        self.videoControlWidget.videoSeekSlider.setValue(self.vispyVideoPlayerWidget.get_frame_number())
        self.videoControlWidget.videoSeekSlider.blockSignals(False)

        # Update frame number
        self.videoControlWidget.frameSpinBox.blockSignals(True)
        self.videoControlWidget.frameSpinBox.setValue(self.vispyVideoPlayerWidget.get_frame_number() + 1)
        self.videoControlWidget.frameSpinBox.blockSignals(False)

        # Update the image visual with the new frame
        # self.vispyVideoPlayerWidget.image.set_data(self.frames[self.frame_index])
        # self.frame_index = (self.frame_index + 1) % len(self.frames)
        # self.videoPlayerCanvas.update()
        # self.vispyVideoPlayerWidget.update_widgets(self.frame_index)


    def playPauseVideo(self):
        if self.vispyVideoPlayerWidget.timer_is_running():
            self.vispyVideoPlayerWidget.stop_timer()
            self.videoControlWidget.playIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "play.png")))
            self.videoControlWidget.playIcon.setToolTip("Play")
        else:
            self.vispyVideoPlayerWidget.start_timer()
            self.videoControlWidget.playIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "pause.png")))
            self.videoControlWidget.playIcon.setToolTip("Pause")

    def skipForward(self):
        self.vispyVideoPlayerWidget.skip_forward()
        self.update_widgets()

    def skipBackward(self):
        self.vispyVideoPlayerWidget.skip_backward()
        self.update_widgets()

    def changePlaybackRate(self, fps):
        self.vispyVideoPlayerWidget.set_fps(fps)

    def goToFrameNo(self, frameNo):
        self.vispyVideoPlayerWidget.go_to_frame_no(frameNo - 1)

    def setVideoPosition(self, position):
        self.vispyVideoPlayerWidget.go_to_frame_no(position)

    def sliderReleased(self):
        self.update_widgets()

    # TODO: complete this func
    def deleteFrames(self, min, max):
        pass





# TODO: remove later
if __name__ == "__main__":
    # Path to icon directory
    ICON_DIRECTORY = "../../../assets/icons"
    PATH_TO_ICON_DIRECTORY = os.path.abspath(os.path.join(os.getcwd(), ICON_DIRECTORY))
    app = QApplication(sys.argv)
    videoPlayerWidget = VideoPlayerWidget()
    videoPlayerWidget.show()
    sys.exit(app.exec())
