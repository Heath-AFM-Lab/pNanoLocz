from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QSpinBox, QCheckBox, QPushButton, 
    QSlider, QGridLayout, QRadioButton, QButtonGroup, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial import Polynomial
from core.Image_Storage_Module.Media_Data_Manager_Class import MediaDataManager

AUTO_LIST = ["Off", "Iterative 1nm High", "Iterative -1nm Low", "Iterative High Low", "High-Low x2 (Fit)", "Iterative Fit Holes", "Iterative Fit Peaks"]
FILTER_LIST = ["Off", "Gaussian", "Median", "Mean", "Non-local mean", "High-pass", "Top Hat", "Sliding Mean Frames", "Sphere Deconvolution", "Mean All", "Median all", "Fill Mask", "Scar Fill"]
MASK_METHOD_LIST = ["histogram", "otsu", "2 level otsu", "step detection", "adaptive"]

class LevelingWidget(QWidget):

    bold_font = QFont()
    bold_font.setBold(True)

    def __init__(self):
        super().__init__()
        self.media_data_manager = MediaDataManager()  # Initialize the MediaDataManager
        self.build_leveling_module()
        self.current_image = None  # Initialize with None
        self.imgt = None

    class CustomSpinBox(QSpinBox):
        def wheelEvent(self, event):
            # Override to disable scroll wheel changes
            event.ignore()

    def build_leveling_module(self):
        # Do not reinitialize media_data_manager here
        self.leveling_layout = self.build_leveling_layout()
        self.filtering_layout = self.build_filtering_layout()
        self.graph_widget = self.build_graph_widget()

        # Zero All and Restore Buttons
        button_layout = QHBoxLayout()
        self.zero_all_button = QPushButton("Zero all")
        self.restore_button = QPushButton("Restore")
        self.zero_all_button.setFixedSize(self.zero_all_button.sizeHint())
        self.restore_button.setFixedSize(self.restore_button.sizeHint())
        button_layout.addWidget(self.zero_all_button)
        button_layout.addWidget(self.restore_button)

        lhs_layout = QVBoxLayout()
        container_layout = QHBoxLayout()
        
        lhs_layout.addLayout(self.leveling_layout)
        lhs_layout.addSpacing(10)
        lhs_layout.addLayout(self.filtering_layout)
        lhs_layout.addStretch(1)
        lhs_layout.addLayout(button_layout)

        container_layout.addLayout(lhs_layout)
        container_layout.addWidget(self.graph_widget)

        container_widget = QWidget()
        container_widget.setLayout(container_layout)
        container_widget.setFixedSize(container_widget.sizeHint())

        scroll_area = QScrollArea()
        scroll_area.setWidget(container_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def build_leveling_layout(self):
        leveling_layout = QVBoxLayout()
        
        # Add title in bold
        self.levelling_title = QLabel("Leveling")
        self.levelling_title.setFont(self.bold_font)
        leveling_layout.addWidget(self.levelling_title)

        # Auto Dropdown
        auto_dropdown_layout = QHBoxLayout()
        self.auto_label = QLabel("Auto:")
        self.auto_dropdown = QComboBox()
        self.auto_dropdown.addItems(AUTO_LIST)
        auto_dropdown_layout.addWidget(self.auto_label)
        auto_dropdown_layout.addWidget(self.auto_dropdown)
        leveling_layout.addLayout(auto_dropdown_layout)

        # Plane and Line Layouts
        plane_line_layout = QHBoxLayout()
        plane_layout = QVBoxLayout()
        line_layout = QVBoxLayout()

        # Plane Layout
        self.plane_label = QLabel("Plane")

        x_plane_layout = QHBoxLayout()
        self.x_plane_label = QLabel("X")
        self.x_plane_spinbox = self.CustomSpinBox()
        self.x_plane_spinbox.valueChanged.connect(self.update_image)  # Connect to update_image
        self.x_plane_spinbox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        x_plane_layout.addWidget(self.x_plane_label)
        x_plane_layout.addWidget(self.x_plane_spinbox)

        y_plane_layout = QHBoxLayout()
        self.y_plane_label = QLabel("Y")
        self.y_plane_spinbox = self.CustomSpinBox()
        self.y_plane_spinbox.valueChanged.connect(self.update_image)  # Connect to update_image
        self.y_plane_spinbox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        y_plane_layout.addWidget(self.y_plane_label)
        y_plane_layout.addWidget(self.y_plane_spinbox)

        mean_checkbox_layout = QHBoxLayout()
        self.mean_label = QLabel("-Mean")
        self.mean_checkbox = QCheckBox()
        mean_checkbox_layout.addWidget(self.mean_label)
        mean_checkbox_layout.addWidget(self.mean_checkbox)

        plane_layout.addWidget(self.plane_label)
        plane_layout.addLayout(x_plane_layout)
        plane_layout.addLayout(y_plane_layout)
        plane_layout.addLayout(mean_checkbox_layout)


        # Line Layout
        self.line_label = QLabel("Line")

        x_line_layout = QHBoxLayout()
        self.x_line_label = QLabel("X")
        self.x_line_spinbox = self.CustomSpinBox()
        self.x_line_spinbox.valueChanged.connect(self.update_image)  # Connect to update_image
        self.x_line_spinbox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        x_line_layout.addWidget(self.x_line_label)
        x_line_layout.addWidget(self.x_line_spinbox)

        y_line_layout = QHBoxLayout()
        self.y_line_label = QLabel("Y")
        self.y_line_spinbox = self.CustomSpinBox()
        self.y_line_spinbox.valueChanged.connect(self.update_image)  # Connect to update_image
        self.y_line_spinbox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        y_line_layout.addWidget(self.y_line_label)
        y_line_layout.addWidget(self.y_line_spinbox)

        median_checkbox_layout = QHBoxLayout()
        self.median_label = QLabel("-Median")
        self.median_checkbox = QCheckBox()
        median_checkbox_layout.addWidget(self.median_label)
        median_checkbox_layout.addWidget(self.median_checkbox)

        line_layout.addWidget(self.line_label)
        line_layout.addLayout(x_line_layout)
        line_layout.addLayout(y_line_layout)
        line_layout.addLayout(median_checkbox_layout)

        # Assemble all widgets
        plane_line_layout.addLayout(plane_layout)
        plane_line_layout.addLayout(line_layout)
        leveling_layout.addLayout(plane_line_layout)

        return leveling_layout

    def update_image(self):
        polyx = self.x_plane_spinbox.value()
        polyy = self.y_plane_spinbox.value()
        line_plane = "plane" if self.plane_label.text() == "Plane" else "line"  # Change as per your requirement

        # Retrieve the frames
        frames = self.media_data_manager.get_frames()

        # Check if frames are loaded correctly
        if frames is None:
            print("Error: No frames loaded in MediaDataManager.")
            return

        # Apply leveling to the image using the actual frames
        leveled_image = apply_levelling(frames, polyx, polyy, line_plane, self.imgt)

        # Display the updated image in a new Matplotlib window
        plt.close('all')  # Close any existing windows
        plt.imshow(leveled_image, cmap='gray')
        plt.title(f"Updated Image: {line_plane.capitalize()} X: {polyx}, Y: {polyy}")
        plt.show()


    def build_filtering_layout(self):
        filtering_layout = QVBoxLayout()

        # Add title in bold
        self.filtering_title = QLabel("Filtering")
        self.filtering_title.setFont(self.bold_font)
        filtering_layout.addWidget(self.filtering_title)

        # Filter Dropdown
        filter_dropdown_layout = QHBoxLayout()
        self.filter_label = QLabel("Filter:")
        self.filter_dropdown = QComboBox()
        self.filter_dropdown.addItems(FILTER_LIST)
        filter_dropdown_layout.addWidget(self.filter_label)
        filter_dropdown_layout.addWidget(self.filter_dropdown)
        filtering_layout.addLayout(filter_dropdown_layout)

        # Filter Spinbox
        filter_spinbox_layout = QHBoxLayout()
        self.filter_spinbox_label = QLabel("Spinbox:")
        self.filter_spinbox = self.CustomSpinBox()
        self.filter_spinbox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        filter_spinbox_layout.addWidget(self.filter_spinbox_label)
        filter_spinbox_layout.addWidget(self.filter_spinbox)
        filtering_layout.addLayout(filter_spinbox_layout)

        # Subtract Mode Checkbox
        self.subtract_mode_checkbox = QCheckBox("Subtract mode")
        filtering_layout.addWidget(self.subtract_mode_checkbox)

        return filtering_layout

    def build_graph_widget(self):
        graph_layout = QVBoxLayout()

        # Mask and Z-scale Radio Buttons
        self.mask_radio = QRadioButton("Mask")
        self.zscale_radio = QRadioButton("Z-scale")
        self.radio_button_group = QButtonGroup()
        self.radio_button_group.addButton(self.mask_radio)
        self.radio_button_group.addButton(self.zscale_radio)
        mask_toggle_layout = QHBoxLayout()
        mask_toggle_layout.addWidget(self.mask_radio)
        mask_toggle_layout.addWidget(self.zscale_radio)
        graph_layout.addLayout(mask_toggle_layout)

        # Method Dropdown with Clear Button
        method_clear_layout = QHBoxLayout()
        self.method_label = QLabel("Method:")
        self.method_dropdown = QComboBox()
        self.method_dropdown.addItems(MASK_METHOD_LIST)
        self.clear_button = QPushButton("Clear")
        self.clear_button.setFixedSize(self.clear_button.sizeHint())
        method_clear_layout.addWidget(self.method_label)
        method_clear_layout.addWidget(self.method_dropdown)
        method_clear_layout.addStretch(1)
        method_clear_layout.addWidget(self.clear_button)
        graph_layout.addLayout(method_clear_layout)

        # Mask Controls - First Row (3 buttons per row)
        mask_controls_layout1 = QHBoxLayout()

        # Mask Controls - First Row (3 buttons per row)
        mask_controls_layout1 = QHBoxLayout()

        # Create individual buttons with unique variable names and set size based on size hint
        self.log_y_button = QPushButton("Log y")
        self.log_y_button.setFixedSize(self.log_y_button.sizeHint())
        mask_controls_layout1.addWidget(self.log_y_button)

        self.zoom_button = QPushButton("Zoom")
        self.zoom_button.setFixedSize(self.zoom_button.sizeHint())
        mask_controls_layout1.addWidget(self.zoom_button)

        self.fit_button = QPushButton("Fit")
        self.fit_button.setFixedSize(self.fit_button.sizeHint())
        mask_controls_layout1.addWidget(self.fit_button)

        # Add the layout to the main graph layout
        graph_layout.addLayout(mask_controls_layout1)


        # Mask Controls - Second Row
        mask_controls_layout2 = QHBoxLayout()

        # Create individual buttons with unique variable names and set size based on size hint
        self.draw_mask_button = QPushButton("Draw Mask")
        self.draw_mask_button.setFixedSize(self.draw_mask_button.sizeHint())
        mask_controls_layout2.addWidget(self.draw_mask_button)

        self.invert_button = QPushButton("Invert")
        self.invert_button.setFixedSize(self.invert_button.sizeHint())
        mask_controls_layout2.addWidget(self.invert_button)

        self.view_mask_button = QPushButton("View Mask")
        self.view_mask_button.setFixedSize(self.view_mask_button.sizeHint())
        mask_controls_layout2.addWidget(self.view_mask_button)

        # Add the layout to the main graph layout
        graph_layout.addLayout(mask_controls_layout2)


        # Add an empty graph using Matplotlib
        self.figure, self.ax = plt.subplots(figsize=(3, 1.5))
        self.canvas = FigureCanvas(self.figure)
        self.ax.plot([], [])
        graph_layout.addWidget(self.canvas)

        # Sliders for Limits
        self.lower_limit_slider = QSlider(Qt.Orientation.Horizontal)
        self.upper_limit_slider = QSlider(Qt.Orientation.Horizontal)
        graph_layout.addWidget(QLabel("lower limit"))
        graph_layout.addWidget(self.lower_limit_slider)
        graph_layout.addWidget(QLabel("upper limit"))
        graph_layout.addWidget(self.upper_limit_slider)

        # Mask with Z-scale Checkbox
        self.mask_with_zscale_checkbox = QCheckBox("Mask with z-scale")
        graph_layout.addWidget(self.mask_with_zscale_checkbox)

        # Analyze Mask Button
        self.analyze_mask_button = QPushButton("Analyze Mask")
        self.analyze_mask_button.setFixedSize(self.analyze_mask_button.sizeHint())
        graph_layout.addWidget(self.analyze_mask_button)

        graph_widget = QWidget()
        graph_widget.setLayout(graph_layout)
        return graph_widget
    

def apply_levelling(img, polyx, polyy, line_plane, imgt):
    # Convert the image to float64 to ensure the operations are compatible
    r = img.astype(np.float64).copy()

    if imgt is None:
        imgt = img > -np.inf

    if line_plane == 'plane':
        xp = np.nanmean(imgt * img, axis=1)
        print(f"[DEBUG] Shape of xp after np.nanmean: {xp.shape}")

        # Ensure xp is 1D by squeezing the array
        xp = np.squeeze(xp)
        print(f"[DEBUG] Shape of xp after squeezing: {xp.shape}")

        # Ensure xp is 1D
        if xp.ndim != 1:
            raise ValueError(f"Unexpected array shape for xp, expected 1D array but got {xp.shape}.")

        valid_xp = ~np.isnan(xp)
        xf = xp[valid_xp]
        xl = np.arange(len(xp))[valid_xp]

        if polyx > 0 and len(xl) > 0:
            p = np.polyfit(xl, xf, polyx)
            r -= np.polyval(p, np.arange(r.shape[0]))[:, None]  # Correct broadcasting without changing dimensions
            print(f"[DEBUG] Shape of r after polyx subtraction: {r.shape}")

        yp = np.nanmean(r, axis=0)  # Calculate mean across the rows (axis=0) to get a 1D array
        print(f"[DEBUG] Shape of yp after np.nanmean: {yp.shape}")

        # Ensure yp is 1D by squeezing the array
        yp = np.squeeze(yp)
        print(f"[DEBUG] Shape of yp after squeezing: {yp.shape}")

        # Ensure yp is 1D
        if yp.ndim != 1:
            raise ValueError(f"Unexpected array shape for yp, expected 1D array but got {yp.shape}.")

        valid_yp = ~np.isnan(yp)
        yf = yp[valid_yp]
        yl = np.arange(len(yp))[valid_yp]

        if polyy > 0 and len(yl) > 0:
            p = np.polyfit(yl, yf, polyy)
            r -= np.polyval(p, np.arange(r.shape[1]))  # Subtract the polynomial fit from the result
            print(f"[DEBUG] Shape of r after polyy subtraction: {r.shape}")

    elif line_plane == 'line':
        if polyx > 0:
            xl = np.arange(img.shape[1])
            y2 = np.zeros_like(r)
            mask_line = []

            for i in range(img.shape[0]):
                pos = imgt[i, :] > 0
                if np.sum(pos) > polyx + 8:
                    y1 = img[i, pos]
                    x1 = xl[pos]
                    p = np.polyfit(x1, y1, polyx)
                    y2[i, :] = np.polyval(p, np.arange(img.shape[1]))
                    r[i, :] -= y2[i, :]
                else:
                    mask_line.append(i)

            for i in mask_line:
                r[i, :] = img[i, :] - np.nanmedian(y2)

        if polyy > 0:
            for i in range(img.shape[1]):
                yp = np.nanmean(r[:, i])  # Calculate mean across the columns (axis=1) to get a 1D array
                print(f"[DEBUG] Shape of yp before squeezing in line: {yp.shape}")

                # Ensure yp is 1D by squeezing the array
                yp = np.squeeze(yp)
                print(f"[DEBUG] Shape of yp after squeezing in line: {yp.shape}")

                # Ensure yp is 1D
                if yp.ndim != 1:
                    print(f"yp in line is not 1D, shape is: {yp.shape}")
                    raise ValueError("Unexpected array shape for yp in line, expected 1D array.")

                valid_yp = ~np.isnan(yp)
                yf = yp[valid_yp]
                yl = np.arange(img.shape[0])[valid_yp]

                if len(yl) >= polyy:
                    p = np.polyfit(yl, yf, polyy)
                    r[:, i] -= np.polyval(p, np.arange(img.shape[0]))

    return r





from PyQt6.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout(window)
    tab = LevelingWidget()
    layout.addWidget(tab)
    window.setLayout(layout)
    window.show()
    sys.exit(app.exec())
