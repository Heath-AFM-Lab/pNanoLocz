from PyQt6 import QtWidgets, QtGui, QtCore
from vispy.scene import SceneCanvas, visuals
import numpy as np
import sys

class VispyCanvasWrapper(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.canvas = SceneCanvas(app='pyqt6', bgcolor=(86 / 255, 86/255, 86/255, 0.1))  # Set the background color to almost transparent
        self.grid = self.canvas.central_widget.add_grid()
        self.view_vispy = self.grid.add_view(0, 0, bgcolor=(0, 0, 0, 0.1))  # Set the view's background color to almost transparent

        self.view_vispy.camera = "panzoom"
        self.view_vispy.camera.aspect = 1.0

        # Set the parent widget of the canvas.native widget to this widget
        self.canvas.native.setParent(self)
        self.geometry = QtCore.QRect(0, 0, 500, 500)
        self.canvas.native.setGeometry(self.geometry)

        self.setObjectName('background_layer')

        # create a transparent background
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAutoFillBackground(False)

        self.this_style_sheet = """
                                background-color: transparent;
                                selection-background-color:transparent;
                            """
        self.setStyleSheet(self.this_style_sheet)
        self.canvas.native.setStyleSheet(self.this_style_sheet)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # apply transparent style sheet
        self.this_style_sheet = """
                    background-color: transparent;
                    selection-background-color:transparent;
                """

        self.transparent_viewport_style_sheet = """
                    background-color: transparent;
                """

        # Geometry of the window
        self.geometry = QtCore.QRect(0, 0, 800, 800)
        self.scene_rect_value = QtCore.QRectF(0, 0, 200, 200)
        self.setGeometry(self.geometry)

        # Create central widget and layout
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Graphics view widget (bottom layer)
        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView = QtWidgets.QGraphicsView()
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setSceneRect(self.scene_rect_value)
        layout.addWidget(self.graphicsView, 0, 0)

        # vispy widget (top layer)
        self.vispy_canvas = VispyCanvasWrapper(self)
        layout.addWidget(self.vispy_canvas, 0, 0)

        # Dummy line
        self.dummy_lines()

    def dummy_lines(self):
        # add some lines to the line gv
        line_list = [[[0, 0], [250, 100]], [[250, 100], [200, -150]]]
        pen = QtGui.QPen(QtGui.QColor(255, 0, 0))
        for line in line_list:
            x1 = line[0][0]
            y1 = -line[0][1]
            x2 = line[1][0]
            y2 = -line[1][1]
            line_item = QtWidgets.QGraphicsLineItem(x1, y1, x2, y2)
            line_item.setPen(pen)
            self.scene.addItem(line_item)

        # add line to vispy
        line_data = np.array([[[0, 0], [250, 100]], [[250, 100], [200, -150]]])
        self.line = visuals.Line(line_data, parent=self.vispy_canvas.view_vispy.scene, color='black')
        # Set the zoom extent
        self.vispy_canvas.view_vispy.camera.set_range(x=(0, 200), y=(0, 200))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
