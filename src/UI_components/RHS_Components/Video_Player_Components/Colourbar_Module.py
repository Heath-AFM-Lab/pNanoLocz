import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from core.Colormaps import CMAPS, DEFAULT_CMAP_NAME



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
        # Create a normalizer
        self.norm = plt.Normalize(vmin=0, vmax=1)
        
        # Create an axes for the colour bar with fixed aspect ratio
        self.cax = self.fig.add_axes([0.2, 0.05, 0.6, 0.9], aspect=25)  # aspect set to 25 to maintain aspect ratio
        
        # Create a colour bar with the specified orientation
        self.cbar = self.fig.colorbar(plt.cm.ScalarMappable(norm=self.norm, cmap=CMAPS[DEFAULT_CMAP_NAME]), cax=self.cax, orientation='vertical')
        
        # Move the colour bar to the right-hand side
        self.cbar.ax.yaxis.set_ticks_position('right')
        self.cbar.ax.yaxis.set_label_position('right')

        # Set axis label and tick colors to white
        self.cbar.ax.yaxis.label.set_color('white')
        self.cbar.ax.tick_params(axis='y', colors='white')


    def set_cmap(self, cmap_name: str):
        # Retrieve the new colormap
        cmap = CMAPS[cmap_name]
        
        # Remove the existing colorbar
        self.cax.clear()
        
        # Create a new ScalarMappable with the updated colormap
        sm = plt.cm.ScalarMappable(norm=self.norm, cmap=cmap)
        
        # Create a new colorbar with the updated ScalarMappable
        self.cbar = self.fig.colorbar(sm, cax=self.cax, orientation='vertical')
        
        # Move the colorbar to the right-hand side (if necessary)
        self.cbar.ax.yaxis.set_ticks_position('right')
        self.cbar.ax.yaxis.set_label_position('right')

        # Set axis label and tick colours to white
        self.cbar.ax.yaxis.label.set_color('white')
        self.cbar.ax.tick_params(axis='y', colors='white')

        # Redraw the canvas to update the colour bar
        self.canvas.draw()
        

    def set_min_max_limits(self, *args):
        """Set the minimum and maximum limits.

        Args:
            *args: A tuple (min, max) or two individual arguments min and max, both of type float.

        Raises:
            ValueError: If the inputs are not valid.
        """
        if len(args) == 1 and isinstance(args[0], tuple) and len(args[0]) == 2:
            min, max = args[0]
        elif len(args) == 2:
            min, max = args
        else:
            raise ValueError("You must provide either a tuple (min, max) or two individual arguments min and max.")

        if not (isinstance(min, float) and isinstance(max, float)):
            raise ValueError("Both min and max must be of type float.")
        
        self.norm.vmax = max
        self.norm.vmin = min



        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create and show the ColourBarWidget
    window = MatplotlibColourBarWidget()
    window.setWindowTitle("Vertical Colour Bar Example")
    window.resize(100, 400)  # Set the window size to 100x400 pixels
    window.show()
    
    sys.exit(app.exec())
