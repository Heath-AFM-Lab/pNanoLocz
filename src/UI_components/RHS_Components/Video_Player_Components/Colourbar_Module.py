import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np

class MatplotlibColourBarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create a vertical layout
        layout = QVBoxLayout(self)
        
        # Create a figure with a transparent background
        self.fig = Figure(figsize=(1, 4))
        self.fig.patch.set_alpha(0)  # Set the figure background to transparent
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setStyleSheet("background-color: transparent;")  # Set the canvas background to transparent
        
        # Create the colour bar
        self._create_colour_bar()
        
        # Add the canvas to the layout
        layout.addWidget(self.canvas)
        
    def _create_colour_bar(self):
        # Create a colormap
        cmap = plt.get_cmap('viridis')
        
        # Create a normalizer
        norm = plt.Normalize(vmin=0, vmax=1)
        
        # Create an axes for the colour bar with fixed aspect ratio
        cax = self.fig.add_axes([0.2, 0.05, 0.6, 0.9], aspect=20)  # aspect set to 20 to maintain aspect ratio
        
        # Create a colour bar with the specified orientation
        cbar = self.fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cax, orientation='vertical')
        
        # Move the colour bar to the right-hand side
        cbar.ax.yaxis.set_ticks_position('right')
        cbar.ax.yaxis.set_label_position('right')

        # Set axis label and tick colors to white
        cbar.ax.yaxis.label.set_color('white')
        cbar.ax.tick_params(axis='y', colors='white')
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create and show the ColourBarWidget
    window = MatplotlibColourBarWidget()
    window.setWindowTitle("Vertical Colour Bar Example")
    window.resize(100, 400)  # Set the window size to 100x400 pixels
    window.show()
    
    sys.exit(app.exec())
