from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QSpinBox, QCheckBox, QPushButton, QSlider, QGridLayout, QRadioButton, QButtonGroup, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

AUTO_LIST = ["Off", "Iterative 1nm High", "Iterative -1nm Low", "Iterative High Low", "High-Low x2 (Fit)", "Iterative Fit Holes", "Iterative Fit Peaks"]
FILTER_LIST = ["Off", "Gaussian", "Median", "Mean", "Non-local mean", "High-pass", "Top Hat", "Sliding Mean Frames", "Sphere Deconvolution", "Mean All", "Median all", "Fill Mask", "Scar Fill"]
MASK_METHOD_LIST = ["histogram", "otsu", "2 level otsu", "step detection", "adaptive"]

class LevelingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.build_leveling_module()

    def build_leveling_module(self):
        self.leveling_widget = self.build_leveling_widget()
        self.filtering_widget = self.build_filtering_widget()
        self.graph_widget = self.build_graph_widget()

        # Create a container widget and scroll area
        container_widget = QWidget()
        container_layout = QGridLayout(container_widget)
        container_layout.setSpacing(5)
        container_layout.addWidget(self.leveling_widget, 0, 0)
        container_layout.addWidget(self.filtering_widget, 1, 0)
        container_layout.addWidget(self.graph_widget, 0, 1, 2, 1)
        container_widget.setLayout(container_layout)
        
        scroll_area = QScrollArea()
        scroll_area.setWidget(container_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def build_leveling_widget(self):
        leveling_layout = QVBoxLayout()
        leveling_layout.setSpacing(5)  # Compact spacing

        # Auto Dropdown
        auto_dropdown_layout = QHBoxLayout()
        self.auto_label = QLabel("Auto:")
        self.auto_dropdown = QComboBox()
        self.auto_dropdown.addItems(AUTO_LIST)
        auto_dropdown_layout.addWidget(self.auto_label)
        auto_dropdown_layout.addWidget(self.auto_dropdown)
        leveling_layout.addLayout(auto_dropdown_layout)

        # Plane and Line Layouts
        plane_line_layout = QGridLayout()
        plane_line_layout.setHorizontalSpacing(5)  # Tighten up the spacing

        # Plane Layout
        self.plane_label = QLabel("Plane")
        plane_line_layout.addWidget(self.plane_label, 0, 0)
        self.add_spinboxes(plane_line_layout, "X", 1, 0)
        self.add_spinboxes(plane_line_layout, "Y", 2, 0)
        self.add_checkbox(plane_line_layout, "-Mean", 3, 0)

        # Line Layout
        self.line_label = QLabel("Line")
        plane_line_layout.addWidget(self.line_label, 0, 1)
        self.add_spinboxes(plane_line_layout, "X", 1, 1)
        self.add_spinboxes(plane_line_layout, "Y", 2, 1)
        self.add_checkbox(plane_line_layout, "-Median", 3, 1)

        leveling_layout.addLayout(plane_line_layout)

        leveling_widget = QWidget()
        leveling_widget.setLayout(leveling_layout)
        return leveling_widget

    def add_spinboxes(self, layout, label, row, column):
        layout_item = QHBoxLayout()
        spinbox_label = QLabel(label)
        spinbox = QSpinBox()
        spinbox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout_item.addWidget(spinbox_label)
        layout_item.addWidget(spinbox)
        layout.addLayout(layout_item, row, column)

    def add_checkbox(self, layout, label, row, column):
        checkbox_layout = QHBoxLayout()
        checkbox_layout.setSpacing(2)  # Compact spacing for checkboxes
        checkbox_label = QLabel(label)
        checkbox = QCheckBox()
        checkbox_layout.addWidget(checkbox_label)
        checkbox_layout.addWidget(checkbox)
        layout.addLayout(checkbox_layout, row, column)

    def build_filtering_widget(self):
        filtering_layout = QVBoxLayout()
        filtering_layout.setSpacing(5)  # Compact spacing

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
        filter_spinbox_label = QLabel("Spinbox:")
        filter_spinbox = QSpinBox()
        filter_spinbox.setFixedWidth(40)  # Smaller spinbox width
        filter_spinbox_layout.addWidget(filter_spinbox_label)
        filter_spinbox_layout.addWidget(filter_spinbox)
        filtering_layout.addLayout(filter_spinbox_layout)

        # Subtract Mode Checkbox
        self.subtract_mode_checkbox = QCheckBox("Subtract mode")
        filtering_layout.addWidget(self.subtract_mode_checkbox)

        # Zero All and Restore Buttons
        button_layout = QHBoxLayout()
        zero_all_button = QPushButton("Zero all")
        restore_button = QPushButton("Restore")
        zero_all_button.setFixedWidth(80)  # Smaller button width
        restore_button.setFixedWidth(80)  # Smaller button width
        button_layout.addWidget(zero_all_button)
        button_layout.addWidget(restore_button)
        filtering_layout.addLayout(button_layout)

        filtering_widget = QWidget()
        filtering_widget.setLayout(filtering_layout)
        return filtering_widget

    def build_graph_widget(self):
        graph_layout = QVBoxLayout()
        graph_layout.setSpacing(5)  # Compact spacing

        # Mask and Z-scale Radio Buttons
        mask_radio = QRadioButton("Mask")
        zscale_radio = QRadioButton("Z-scale")
        radio_button_group = QButtonGroup()
        radio_button_group.addButton(mask_radio)
        radio_button_group.addButton(zscale_radio)
        mask_toggle_layout = QHBoxLayout()
        mask_toggle_layout.addWidget(mask_radio)
        mask_toggle_layout.addWidget(zscale_radio)
        graph_layout.addLayout(mask_toggle_layout)

        # Method Dropdown with Clear Button
        method_clear_layout = QHBoxLayout()
        self.method_label = QLabel("Method:")
        self.method_dropdown = QComboBox()
        self.method_dropdown.addItems(MASK_METHOD_LIST)
        clear_button = QPushButton("Clear")
        method_clear_layout.addWidget(self.method_label)
        method_clear_layout.addWidget(self.method_dropdown)
        method_clear_layout.addWidget(clear_button)
        graph_layout.addLayout(method_clear_layout)

        # Mask Controls - First Row (3 buttons per row)
        mask_controls_layout1 = QHBoxLayout()
        buttons_row1 = ["Log y", "Zoom", "Fit"]
        for button_text in buttons_row1:
            button = QPushButton(button_text)
            button.setFixedWidth(65)  # Wider button width for longer text
            mask_controls_layout1.addWidget(button)
        graph_layout.addLayout(mask_controls_layout1)

        # Mask Controls - Second Row
        mask_controls_layout2 = QHBoxLayout()
        buttons_row2 = ["Draw Mask", "Invert", "View Mask"]
        for button_text in buttons_row2:
            button = QPushButton(button_text)
            button.setFixedWidth(80)  # Wider button width for longer text
            mask_controls_layout2.addWidget(button)
        graph_layout.addLayout(mask_controls_layout2)

        # Add an empty graph using Matplotlib
        self.figure, self.ax = plt.subplots(figsize=(3, 1.5))
        self.canvas = FigureCanvas(self.figure)
        self.ax.plot([], [])
        graph_layout.addWidget(self.canvas)

        # Sliders for Limits
        lower_limit_slider = QSlider(Qt.Orientation.Horizontal)
        upper_limit_slider = QSlider(Qt.Orientation.Horizontal)
        graph_layout.addWidget(QLabel("lower limit"))
        graph_layout.addWidget(lower_limit_slider)
        graph_layout.addWidget(QLabel("upper limit"))
        graph_layout.addWidget(upper_limit_slider)

        # Mask with Z-scale Checkbox
        mask_with_zscale_checkbox = QCheckBox("Mask with z-scale")
        graph_layout.addWidget(mask_with_zscale_checkbox)

        # Analyze Mask Button
        analyze_mask_button = QPushButton("Analyze Mask")
        analyze_mask_button.setFixedWidth(100)  # Wider button width for longer text
        graph_layout.addWidget(analyze_mask_button)

        graph_widget = QWidget()
        graph_widget.setLayout(graph_layout)
        return graph_widget

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
