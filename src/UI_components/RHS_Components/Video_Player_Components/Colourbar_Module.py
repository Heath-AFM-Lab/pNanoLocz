import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from core.Colormaps_Module.Colormaps import CMAPS, DEFAULT_CMAP_NAME
import matplotlib.ticker as ticker

class MatplotlibColourBarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        
        self.fig = Figure(figsize=(1.5, 4))
        self.fig.patch.set_alpha(0)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setStyleSheet("background-color: transparent;")
        
        self._create_colour_bar()
        
        layout.addWidget(self.canvas)
        
    def _create_colour_bar(self):
        self.norm = plt.Normalize(vmin=0, vmax=1)
        
        self.cax = self.fig.add_axes([0.2, 0.05, 0.3, 0.9])
        
        self.cbar = self.fig.colorbar(plt.cm.ScalarMappable(norm=self.norm, cmap=CMAPS[DEFAULT_CMAP_NAME]), 
                                      cax=self.cax, orientation='vertical')
        
        self.cbar.ax.yaxis.set_ticks_position('right')
        self.cbar.ax.yaxis.set_label_position('right')

        self.cbar.ax.yaxis.label.set_color('white')
        self.cbar.ax.tick_params(axis='y', colors='white', pad=5)

        self.cbar.ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=5))

    def set_cmap(self, cmap_name: str):
        cmap = CMAPS[cmap_name]
        self.cax.clear()
        sm = plt.cm.ScalarMappable(norm=self.norm, cmap=cmap)
        self.cbar = self.fig.colorbar(sm, cax=self.cax, orientation='vertical')
        
        self.cbar.ax.yaxis.set_ticks_position('right')
        self.cbar.ax.yaxis.set_label_position('right')
        self.cbar.ax.yaxis.label.set_color('white')
        self.cbar.ax.tick_params(axis='y', colors='white', pad=5)
        self.cbar.ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=5))

        self.canvas.draw()

    def set_min_max_limits(self, *args):
        if len(args) == 1 and isinstance(args[0], tuple) and len(args[0]) == 2:
            min_val, max_val = args[0]
        elif len(args) == 2:
            min_val, max_val = args
        else:
            raise ValueError("You must provide either a tuple (min, max) or two individual arguments min and max.")
        
        self.norm.vmax = max_val
        self.norm.vmin = min_val

        self.cbar.ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MatplotlibColourBarWidget()
    window.setWindowTitle("Vertical Colour Bar Example")
    window.resize(150, 400)
    window.show()
    sys.exit(app.exec())