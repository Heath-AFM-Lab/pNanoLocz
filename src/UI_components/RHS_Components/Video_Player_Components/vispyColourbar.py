from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from vispy import scene
from vispy.color import Colormap
from vispy.visuals import ColorBarVisual, AxisVisual
from vispy.scene.visuals import create_visual_node

# Create custom nodes for ColorBarVisual and AxisVisual
ColorBarNode = create_visual_node(ColorBarVisual)
AxisNode = create_visual_node(AxisVisual)

class ColorBarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set up the layout
        layout = QHBoxLayout(self)
        layout.addSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create a Vispy canvas with a transparent background
        self.canvas = scene.SceneCanvas(keys='interactive', show=False)
        self.canvas.unfreeze()
        
        # Create a viewbox for the color bar and axis
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = 'panzoom'
        self.view.camera.rect = (0, 0, 1, 1)
        self.view.bgcolor = 'transparent'  # Set the view background color
        
        # Create a ColorBarNode with adjusted size
        cmap = Colormap(['#000000', '#FF0000', '#FFFF00', '#FFFFFF'])
        self.colorbar = ColorBarNode(cmap=cmap, orientation='right', size=(200, 30), label='Intensity')
        self.colorbar.transform = scene.STTransform(translate=(0, 0))  # No offset
        
        # Create an AxisNode
        axis_pos = [[0, 0], [0, 1]]
        self.axis = AxisNode(pos=axis_pos, axis_label='Intensity', tick_direction=(0, -1),
                             axis_color='black', tick_color='black', text_color='black')
        self.axis.transform = scene.STTransform(translate=(40, 0))  # Adjusted position
        
        # Add the colorbar and axis to the view
        self.view.add(self.colorbar)
        self.view.add(self.axis)
        
        # Add the canvas to the layout
        layout.addWidget(self.canvas.native)
        
        # Update the layout
        self.setLayout(layout)

        self.canvas.freeze()

if __name__ == '__main__':
    import sys
    
    app = QApplication(sys.argv)
    
    # Create the main window
    main_window = QWidget()
    main_layout = QVBoxLayout(main_window)
    
    # Add the ColorBarWidget to the main window
    colorbar_widget = ColorBarWidget()
    main_layout.addWidget(colorbar_widget)
    colorbar_widget.setFixedWidth(200)  # Adjust width as needed
    
    main_window.setLayout(main_layout)
    main_window.setWindowTitle('PyQt6 Vispy ColorBar')
    main_window.show()
    
    sys.exit(app.exec())
