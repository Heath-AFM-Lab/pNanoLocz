import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSizePolicy, QLayout
from PyQt6.QtCore import QTimer, pyqtSignal, QSize, QRect, QPoint, QThread
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
from matplotlib.offsetbox import AnchoredText
import matplotlib.font_manager as fm
from core.Colormaps_Module.Colormaps import CMAPS, DEFAULT_CMAP_NAME
import warnings
from core.Image_Storage_Module.Depth_Control_Manager import DepthControlManager

# Try to import cupy for GPU acceleration
try:
    import cupy as cp
    HAS_GPU = True
except ImportError:
    HAS_GPU = False
    warnings.warn("CuPy not available. GPU acceleration will not be used.")

DEFAULT_FPS = 30

class AspectRatioLayout(QLayout):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.item = None
        self.aspect_ratio = 1.0

    def setAspectRatio(self, aspect_ratio):
        self.aspect_ratio = aspect_ratio

    def addItem(self, item):
        if self.item is not None:
            raise ValueError("AspectRatioLayout can only manage one item")
        self.item = item

    def count(self):
        return 1 if self.item else 0

    def itemAt(self, index):
        return self.item if index == 0 else None

    def takeAt(self, index):
        if index == 0:
            item = self.item
            self.item = None
            return item
        return None

    def setGeometry(self, rect):
        super().setGeometry(rect)
        if self.item:
            available_width = rect.width()
            available_height = rect.height()
            
            if available_height <= 0:
                # Handle the case where height is zero or negative
                height = 1  # Set a minimum height
                width = int(height * self.aspect_ratio)
            elif available_width / available_height > self.aspect_ratio:
                # Width is larger, constrain to height
                height = available_height
                width = int(height * self.aspect_ratio)
            else:
                # Height is larger, constrain to width
                width = available_width
                height = int(width / self.aspect_ratio)
            
            x = (available_width - width) // 2
            y = (available_height - height) // 2
            
            self.item.setGeometry(QRect(QPoint(x, y), QSize(width, height)))

    def sizeHint(self):
        if self.item:
            return self.item.sizeHint()
        return QSize()

    def minimumSize(self):
        if self.item:
            return self.item.minimumSize()
        return QSize()
    

class FrameProcessor(QThread):
    frame_ready = pyqtSignal(object, int, float, float, float)  # Add timestamp to the signal

    def __init__(self, video_frames, video_frames_metadata, depth_control_manager: DepthControlManager):
        super().__init__()
        self.depth_control_manager = depth_control_manager
        if HAS_GPU:
            self.video_frames = cp.asarray(video_frames)
        else:
            self.video_frames = video_frames
        self.video_frames_metadata = video_frames_metadata
        self.current_frame_index = 0
        self.running = False
        self.fps = DEFAULT_FPS

    def run(self):
        while self.running:
            frame = self.video_frames[self.current_frame_index]
            if HAS_GPU:
                processed_frame = cp.asnumpy(frame)
            else:
                processed_frame = frame
            vmin, vmax = self.depth_control_manager.get_min_max_depths_per_frame(self.current_frame_index)
            timestamp = self.video_frames_metadata[self.current_frame_index].get("Timestamp", 0.0)  # Get timestamp from metadata
            self.frame_ready.emit(processed_frame, self.current_frame_index, vmin, vmax, timestamp)
            self.current_frame_index = (self.current_frame_index + 1) % len(self.video_frames)
            QThread.msleep(int(1000 / self.fps))

    def seek_to_frame(self, frame_no):
        if 0 <= frame_no < len(self.video_frames):
            self.current_frame_index = frame_no
            frame = self.video_frames[self.current_frame_index]
            if HAS_GPU:
                processed_frame = cp.asnumpy(frame)
            else:
                processed_frame = frame
            vmin, vmax = self.depth_control_manager.get_min_max_depths_per_frame(self.current_frame_index)
            timestamp = self.video_frames_metadata[self.current_frame_index].get("Timestamp", 0.0)  # Get timestamp from metadata
            self.frame_ready.emit(processed_frame, self.current_frame_index, vmin, vmax, timestamp)

    def stop(self):
        self.running = False

    def set_fps(self, fps: int):
        self.fps = fps


class MatplotlibVideoPlayerWidget(QWidget):
    update_widgets = pyqtSignal()
    reset_widgets = pyqtSignal()

    def __init__(self, depth_control_manager: DepthControlManager, parent=None):
        super().__init__(parent)
        self.depth_control_manager = depth_control_manager
        self.layout = None
        self.fig = None
        self.canvas = None
        self.ax = None
        self.image = None
        self.video_frames = None
        self.video_frames_metadata = None
        self.current_frame_index = 0
        self.aspect_ratio = 1.0
        self.fps = DEFAULT_FPS
        self.cmap_name = DEFAULT_CMAP_NAME
        self.scale_bar = None
        self.scale_bar_shown = False
        self.timestamp = None
        self.timestamp_shown = False
        self.has_content = False
        self.frame_processor = None
        self.is_playing = False
        self.timestamp_format = "{:.1f}s"  # Format for timestamp display

    def load_video_frames(self, video_frames: np.ndarray, video_frames_metadata: dict):
        self.setContentsMargins(0, 0, 0, 0)
        self.reset()

        self.has_content = True

        self.depth_control_manager.load_depth_control_data(video_frames, video_frames_metadata)

        # Create and start the frame processor
        self.frame_processor = FrameProcessor(video_frames, video_frames_metadata, self.depth_control_manager)
        self.frame_processor.frame_ready.connect(self._update_frame)

        # Create a layout for the widget
        if self.layout is None:
            self.layout = AspectRatioLayout(self)
            self.setLayout(self.layout)

        # Create a Matplotlib Figure and Canvas
        if self.fig is None:
            self.fig = Figure(figsize=(5, 5), dpi=100)
            self.fig.patch.set_alpha(0)  # Set the figure background to transparent
            self.canvas = FigureCanvas(self.fig)
            self.canvas.setStyleSheet("background-color: transparent;")  # Set the canvas background to transparent
            self.layout.addWidget(self.canvas)

        # Create an Axes for displaying the image
        if self.ax is None:
            self.ax = self.fig.add_subplot(111)
        self.ax.axis('off')

        # Display the first frame
        self.image = self.ax.imshow(video_frames[0], cmap=CMAPS[self.cmap_name])
        # self.enable_cbar_autoscale(True)

        # Get image dimensions and calculate aspect ratio
        self.image_height, self.image_width = video_frames[0].shape[:2]
        self.aspect_ratio = self.image_width / self.image_height
        self.layout.setAspectRatio(self.aspect_ratio)

        # Add a scale bar to the image
        self._add_scale_bar()

        # Add a timestamp to the image
        self._add_timestamp()

        # Set size policy
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Connect the resize event
        self.canvas.mpl_connect('resize_event', self.on_resize)

        # Load first frame
        self.go_to_frame_no(0)

        # Connect the depth control manager to update image if needed.
        self.depth_control_manager.update_widgets.connect(lambda: self.go_to_frame_no(frame_no=self.current_frame_index))
        self.reset_widgets.connect(self.depth_control_manager.reset)

        self.updateGeometry()


    def reset(self):
        if not self.has_content:
            return
        if self.frame_processor:
            self.frame_processor.stop()
            self.frame_processor.wait()
            self.frame_processor = None
        self.layout.setAspectRatio(1.0)
        self.ax.clear()
        self.ax.axis('off')
        self.canvas.draw()
        self.fps = DEFAULT_FPS

        self.reset_widgets.emit()

    def on_resize(self, event):
        # Update the figure size to match the new canvas size
        self.fig.set_size_inches(event.width / 100, event.height / 100)
        
        # Adjust the subplot to fill the figure
        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
        
        # Update the image aspect ratio
        self.ax.set_aspect('auto')
        
        # Redraw the canvas
        self.canvas.draw()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateGeometry()

    def heightForWidth(self, width):
        return int(width / self.aspect_ratio)

    def widthForHeight(self, height):
        return int(height * self.aspect_ratio)

    ### Matplotlib video player functions ###
    def _update_frame(self, frame, current_frame_index, vmin, vmax, timestamp):
        self.current_frame_index = current_frame_index
        self.image.set_data(frame)
        self.image.set_clim(vmin, vmax)

        # Update timestamp
        if self.timestamp_shown:
            self._update_timestamp(timestamp)

        # TODO: Update scale bar if active
        
        self.canvas.draw()
        self.update_widgets.emit()

    def _go_to_next_frame(self):
        if self.frame_processor:
            self.frame_processor.current_frame_index = (self.frame_processor.current_frame_index + 1) % len(self.frame_processor.video_frames)

    def set_fps(self, fps):
        self.fps = fps
        if self.frame_processor:
            self.frame_processor.fps = fps

    def stop_timer(self):
        if self.frame_processor and self.is_playing:
            self.frame_processor.running = False
            self.frame_processor.stop()
            self.is_playing = False

    def start_timer(self):
        if self.frame_processor and not self.is_playing:
            self.frame_processor.running = True
            self.frame_processor.start()
            self.is_playing = True

    def get_fps(self):
        return self.fps

    def skip_forward(self):
        if self.frame_processor:
            self.frame_processor.current_frame_index = min(
                self.frame_processor.current_frame_index + 30, 
                len(self.frame_processor.video_frames) - 1
            )

    def skip_backward(self):
        if self.frame_processor:
            self.frame_processor.current_frame_index = max(
                self.frame_processor.current_frame_index - 30, 
                0
            )

    def timer_is_running(self):
        return self.is_playing

    def go_to_frame_no(self, frame_no):
        if self.frame_processor:
            self.frame_processor.seek_to_frame(frame_no)
            self.current_frame_index = frame_no

    def get_frame_number(self):
        return self.frame_processor.current_frame_index if self.frame_processor else 0
    

    ### Visual control functions ###
    def _add_scale_bar(self):
        fontprops = fm.FontProperties(size=10, weight='bold')
        self.scale_bar = AnchoredSizeBar(self.ax.transData,
                                    50, '50 nm', 'lower right', 
                                    pad=0.1,
                                    color='black',
                                    frameon=False,
                                    size_vertical=1,
                                    fontproperties=fontprops)
        self.ax.add_artist(self.scale_bar)
        if self.scale_bar_shown:
            self.show_scale_bar()
        else:
            self.hide_scale_bar()

    def _add_timestamp(self):
        self.timestamp = AnchoredText(self.timestamp_format.format(0.0), loc='upper left', prop={'size': 10, 'weight': 'bold'}, frameon=False)
        self.ax.add_artist(self.timestamp)
        if self.scale_bar_shown:
            self.show_timescale()
        else:
            self.hide_timescale()

    def _update_timestamp(self, timestamp):
        if self.timestamp:
            self.timestamp.txt.set_text(self.timestamp_format.format(timestamp))
    
    def set_cmap(self, cmap_name: str):
        if self.image:
            self.image.set_cmap(CMAPS[cmap_name])
            self.canvas.draw()

        self.cmap_name = cmap_name

    def show_scale_bar(self):
        self.scale_bar.set_visible(True)
        self.scale_bar_shown = True
        self.canvas.draw()

    def hide_scale_bar(self):
        self.scale_bar.set_visible(False)
        self.scale_bar_shown = False
        self.canvas.draw()

    def show_timescale(self):
        self.timestamp.set_visible(True)
        self.timestamp_shown = True
        self.canvas.draw()

    def hide_timescale(self):
        self.timestamp.set_visible(False)
        self.timestamp_shown = True
        self.canvas.draw()

    ### Autoscale color bar controls ###
    def enable_cbar_autoscale(self, enable_autoscale: bool):
        # TODO: refresh by accessing frame metadata for vmin and vmax values
        pass


if __name__ == '__main__':
    # Generate a random video using NumPy (100 frames of 100x100 RGB images)
    video_frames = np.random.rand(100, 100, 100, 3).astype(np.float32)

    # Create the PyQt6 application
    app = QApplication(sys.argv)

    # Create the main window
    main_window = QWidget()
    main_window.setWindowTitle('Matplotlib Video Display')

    # Create and add the Matplotlib widget to the main window
    matplotlib_widget = MatplotlibVideoPlayerWidget()
    layout = QVBoxLayout()
    main_window.setLayout(layout)
    layout.addWidget(matplotlib_widget)

    # Load video frames into the Matplotlib widget
    matplotlib_widget.load_video_frames(video_frames)

    # Show the main window
    main_window.show()

    # Start the PyQt6 event loop
    sys.exit(app.exec())
