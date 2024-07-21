import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
import matplotlib.pyplot as plt
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Colourbar Widget Example')

        # Create a central widget and set layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # Create a Matplotlib figure and axis
        self.figure, self.ax = plt.subplots(figsize=(5, 2))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Create a colorbar
        self.create_colorbar()

        # Add a navigation toolbar
        toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(toolbar)

    def create_colorbar(self):
        # Create some data for the colorbar
        data = np.random.rand(10, 10)

        # Create an image plot
        cax = self.ax.imshow(data, cmap='viridis')
        self.figure.colorbar(cax, ax=self.ax, orientation='horizontal')

        # Draw the canvas
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
