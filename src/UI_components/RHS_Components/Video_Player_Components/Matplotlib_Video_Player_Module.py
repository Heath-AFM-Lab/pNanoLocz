import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSizePolicy, QLayout
from PyQt6.QtCore import QTimer, pyqtSignal, QSize, QRect, QPoint
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
from matplotlib.offsetbox import AnchoredText
import matplotlib.font_manager as fm
from core.Colormaps import CMAPS, DEFAULT_CMAP_NAME

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

class MatplotlibVideoPlayerWidget(QWidget):
    update_widgets = pyqtSignal()

    def __init__(self, video_frames, parent=None):
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
    
        # Store video frames
        self.video_frames = video_frames
        self.current_frame_index = 0

        # Create a layout for the widget
        self.layout = AspectRatioLayout(self)
        self.setLayout(self.layout)

        # Create a Matplotlib Figure and Canvas
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.fig.patch.set_alpha(0)  # Set the figure background to transparent
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setStyleSheet("background-color: transparent;")  # Set the canvas background to transparent
        self.layout.addWidget(self.canvas)

        # Create an Axes for displaying the image
        self.ax = self.fig.add_subplot(111)
        self.ax.axis('off')

        # Display the first frame
        self.image = self.ax.imshow(video_frames[0], cmap=CMAPS[DEFAULT_CMAP_NAME])

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

        # Setup a timer to update the frames
        self.timer = QTimer()
        self.timer.timeout.connect(self._go_to_next_frame)
        self.set_fps(DEFAULT_FPS)
        self.timer.stop()

        # Connect the resize event
        self.canvas.mpl_connect('resize_event', self.on_resize)

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

    def hasHeightForWidth(self):
        return self.aspect_ratio > 1

    ### Matplotlib video player functions ###
    def _update_frame(self):
        self.image.set_data(self.video_frames[self.current_frame_index])
        # TODO: implement the timestamp and scale bar update functionality
        # self.timestamp.txt.set_text(f"{self.current_frame_index / self.fps:.1f}s")
        self.canvas.draw()
        self.update_widgets.emit()

    def _go_to_next_frame(self):
        # Update the image with the next frame
        self.current_frame_index = (self.current_frame_index + 1) % len(self.video_frames)
        self._update_frame()

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
        self.hide_scale_bar()

    def _add_timestamp(self):
        fontprops = fm.FontProperties(size=10, weight='bold')
        self.timestamp = AnchoredText("100.0s", loc='upper left', prop={'size': 10, 'weight': 'bold'}, frameon=False)
        self.ax.add_artist(self.timestamp)
        self.hide_timescale()
    
    def set_cmap(self, cmap_name: str):
        self.image.set_cmap(CMAPS[cmap_name])
        self.canvas.draw()

    def show_scale_bar(self):
        if not hasattr(self, 'scale_bar'):
            self._add_scale_bar()  # Add scale bar if it does not exist
        self.scale_bar.set_visible(True)
        self.canvas.draw()

    def hide_scale_bar(self):
        if hasattr(self, 'scale_bar'):
            self.scale_bar.set_visible(False)
            self.canvas.draw()

    def show_timescale(self):
        if not hasattr(self, 'timestamp'):
            self._add_timestamp()  # Add timestamp if it does not exist
        self.timestamp.set_visible(True)
        self.canvas.draw()

    def hide_timescale(self):
        if hasattr(self, 'timestamp'):
            self.timestamp.set_visible(False)
            self.canvas.draw()



if __name__ == '__main__':
    # Generate a random video using NumPy (100 frames of 100x100 RGB images)
    video_frames = np.random.rand(100, 100, 100, 3).astype(np.float32)

    # Create the PyQt6 application
    app = QApplication(sys.argv)

    # Create the main window
    main_window = QWidget()
    main_window.setWindowTitle('Matplotlib Video Display')

    # Create and add the Matplotlib widget to the main window
    matplotlib_widget = MatplotlibVideoPlayerWidget(video_frames)
    layout = QVBoxLayout()
    main_window.setLayout(layout)
    layout.addWidget(matplotlib_widget)

    # Show the main window
    main_window.show()

    # Start the PyQt6 event loop
    sys.exit(app.exec())
