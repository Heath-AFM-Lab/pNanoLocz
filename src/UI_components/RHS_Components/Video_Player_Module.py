import sys
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal
from UI_components.RHS_Components.Video_Player_Components import VideoControlWidget, VideoDepthControlWidget, VisualRepresentationWidget, ExportAndVideoScaleWidget, MatplotlibVideoPlayerWidget, MatplotlibColourBarWidget
from utils.constants import PATH_TO_ICON_DIRECTORY
from core.Image_Storage_Module.Image_Storage_Class import MediaDataManager
from core.Image_Storage_Module.Depth_Control_Manager import DepthControlManager

class VideoPlayerWidget(QWidget):
    update_external_widgets = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.buildVideoPlayerWidgets()

    def buildVideoPlayerWidgets(self):
        self.media_data_manager = MediaDataManager()
        self.depth_control_manager = DepthControlManager()
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

        # Set and add a layout to store video player and colour bar
        self.videoPlayerLayout = QHBoxLayout()
        self.mediaLayout.addLayout(self.videoPlayerLayout)
        
        self.videoPlayerWidget = MatplotlibVideoPlayerWidget(self.depth_control_manager)
        self.videoPlayerWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.videoPlayerLayout.addWidget(self.videoPlayerWidget, stretch=1)
        self.videoPlayerWidget.setMinimumSize(10, 10)

        self.colorbarWidget = MatplotlibColourBarWidget()
        self.videoPlayerLayout.addWidget(self.colorbarWidget)
        self.colorbarWidget.setMinimumWidth(100)
        self.colorbarWidget.hide()

        # Initialize the rest of the widgets
        self.videoControlWidget = VideoControlWidget()
        self.visualRepresentationWidget = VisualRepresentationWidget()
        self.videoDepthControlWidget = VideoDepthControlWidget()
        self.exportAndVideoScaleWidget = ExportAndVideoScaleWidget()

        # Connect signals to slots
        # Video player control widgets
        self.videoControlWidget.playClicked.connect(self.playPauseVideo)
        self.videoControlWidget.skipBackClicked.connect(self.skipBackward)
        self.videoControlWidget.skipForwardClicked.connect(self.skipForward)
        self.videoControlWidget.fpsChanged.connect(self.changePlaybackRate)
        self.videoControlWidget.specificVideoFrameGiven.connect(self.goToFrameNo)
        self.videoControlWidget.videoSeekSlider.valueChanged.connect(self.setVideoPosition)
        self.videoControlWidget.videoSeekSlider.sliderReleased.connect(self.sliderReleased)

        self.videoPlayerWidget.update_widgets.connect(self.update_widgets)
        self.videoPlayerWidget.reset_widgets.connect(self.reset_widgets)

        # Visual representation widgets
        self.visualRepresentationWidget.zScaleCheckboxChecked.connect(self.toggle_colorbar)
        self.visualRepresentationWidget.scaleBarCheckboxChecked.connect(self.toggle_scale_bar)
        self.visualRepresentationWidget.timescaleCheckboxChecked.connect(self.toggle_timescale)

        # Depth control widgets
        self.videoDepthControlWidget.new_depth_values.connect(self.depth_control_manager.set_min_max_manual_values)
        self.videoDepthControlWidget.depthTypeDropdown.currentTextChanged.connect(self.depth_control_manager.set_depth_control_type)
        self.depth_control_manager.request_current_min_max_values.connect(self.videoDepthControlWidget.get_min_max_values)


        # Media manager class to load data
        self.media_data_manager.new_file_loaded.connect(self.load_frames_data)

        # Depth control widget to update widgets if changes are detected
        self.depth_control_manager.update_widgets.connect(self.update_widgets)


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

    # TODO: create proper load frames func that triggers after user selects a file to open
    def load_frames_data(self):
        self.frames = self.media_data_manager.get_frames()
        self.number_of_frames = len(self.frames)

        self.videoPlayerWidget.load_video_frames(self.frames, self.media_data_manager.get_frames_metadata())

        # Update slider with max frames
        self.videoControlWidget.videoSeekSlider.setRange(0, self.number_of_frames - 1)

        # Update frame selector with max frames
        self.videoControlWidget.frameSpinBox.setRange(1, self.number_of_frames)

        # Update FPS box with base FPS
        self.videoControlWidget.fpsTextBox.setText(str(self.videoPlayerWidget.get_fps()))

        # Update widgets
        self.update_widgets()

        # set either image viewer mode or video player mode
        if self.number_of_frames == 1:
            self.hide_video_player_widgets()
        else:
            self.show_video_player_widgets()

        # Enable widgets
        self.enableWidgets()

    def disableWidgets(self):
        self.videoControlWidget.setDisabled(True)
        self.visualRepresentationWidget.setDisabled(True)
        self.videoDepthControlWidget.setDisabled(True)
        self.exportAndVideoScaleWidget.setDisabled(True)

    def enableWidgets(self):
        self.videoControlWidget.setEnabled(True)
        self.visualRepresentationWidget.setEnabled(True)
        self.videoDepthControlWidget.setEnabled(True)
        self.exportAndVideoScaleWidget.setEnabled(True)

    def hide_video_player_widgets(self):
        self.videoControlWidget.setVisible(False)
        self.visualRepresentationWidget.timescaleCheckbox.setVisible(False)
        self.toggle_timescale(False)
        
    def show_video_player_widgets(self):
        self.videoControlWidget.setVisible(True)
        self.visualRepresentationWidget.timescaleCheckbox.setVisible(True)
        self.toggle_timescale(self.visualRepresentationWidget.timescaleCheckbox.isChecked())
        

    def reset_widgets(self):
        self.blockSignals(True)
        self.videoPlayerWidget.stop_timer()
        self.videoControlWidget.playIcon.setToolTip("Play")
        self.videoControlWidget.videoSeekSlider.setValue(0)
        self.videoControlWidget.frameSpinBox.setValue(1)
        self.videoControlWidget.playIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "play.png")))
        self.videoControlWidget.fpsTextBox.setText(str(self.videoPlayerWidget.get_fps()))
        self.blockSignals(False)

    ### VIDEO CONTROL FUNCTIONALITY ###
    def update_widgets(self):
        frame_no = self.videoPlayerWidget.get_frame_number()
        frame_metadata = self.media_data_manager.get_frames_metadata_per_frame(frame_no)
        # Update the slider position
        self.videoControlWidget.videoSeekSlider.blockSignals(True)
        self.videoControlWidget.videoSeekSlider.setValue(frame_no)
        self.videoControlWidget.videoSeekSlider.blockSignals(False)

        # Update frame number
        self.videoControlWidget.frameSpinBox.blockSignals(True)
        self.videoControlWidget.frameSpinBox.setValue(frame_no + 1)
        self.videoControlWidget.frameSpinBox.blockSignals(False)

        # Update colourbar with frame cmap limits
        min_frame_limit, max_frame_limit = self.depth_control_manager.get_min_max_depths_per_frame(frame_no)
        self.colorbarWidget.set_min_max_limits(min_frame_limit, max_frame_limit)

        self.videoDepthControlWidget.minSpinBox.blockSignals(True)
        self.videoDepthControlWidget.maxSpinBox.blockSignals(True)
        self.videoDepthControlWidget.minSpinBox.setValue(min_frame_limit)
        self.videoDepthControlWidget.maxSpinBox.setValue(max_frame_limit)
        self.videoDepthControlWidget.minSpinBox.blockSignals(False)
        self.videoDepthControlWidget.maxSpinBox.blockSignals(False)

        self.update_external_widgets.emit(frame_no)

    def playPauseVideo(self):
        if self.videoPlayerWidget.timer_is_running():
            self.videoPlayerWidget.stop_timer()
            self.videoControlWidget.playIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "play.png")))
            self.videoControlWidget.playIcon.setToolTip("Play")
        else:
            self.videoPlayerWidget.start_timer()
            self.videoControlWidget.playIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "pause.png")))
            self.videoControlWidget.playIcon.setToolTip("Pause")

    def skipForward(self):
        self.videoPlayerWidget.skip_forward()
        self.update_widgets()

    def skipBackward(self):
        self.videoPlayerWidget.skip_backward()
        self.update_widgets()

    def changePlaybackRate(self, fps):
        self.videoPlayerWidget.set_fps(fps)

    def goToFrameNo(self, frameNo):
        self.videoPlayerWidget.go_to_frame_no(frameNo - 1)

    def setVideoPosition(self, position):
        self.videoPlayerWidget.go_to_frame_no(position)

    def sliderReleased(self):
        self.update_widgets()

    ### VISUAL REPRESENTATION FUNCTIONALITY ###
    def toggle_colorbar(self, z_scale_box_is_checked):
        if z_scale_box_is_checked:
            self.colorbarWidget.show()
        else:
            self.colorbarWidget.hide()

    def toggle_scale_bar(self, scale_bar_is_checked):
        if scale_bar_is_checked:
            self.videoPlayerWidget.show_scale_bar()
        else:
            self.videoPlayerWidget.hide_scale_bar()

    def toggle_timescale(self, timescale_is_checked):
        if timescale_is_checked:
            self.videoPlayerWidget.show_timescale()
        else:
            self.videoPlayerWidget.hide_timescale()

    ### COLOR BAR FUNCTIONALITY ###
    def change_colour_bar(self, cmap_name):
        self.videoPlayerWidget.set_cmap(cmap_name)
        self.colorbarWidget.set_cmap(cmap_name)
            

# TODO: remove later
if __name__ == "__main__":
    # Path to icon directory
    ICON_DIRECTORY = "../../../assets/icons"
    PATH_TO_ICON_DIRECTORY = os.path.abspath(os.path.join(os.getcwd(), ICON_DIRECTORY))
    app = QApplication(sys.argv)
    videoPlayerWidget = VideoPlayerWidget()
    videoPlayerWidget.show()
    sys.exit(app.exec())
