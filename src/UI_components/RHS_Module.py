import sys
import os
import re
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtGui import QValidator
from UI_components.RHS_Components import VideoDropdownWidget, VideoEditingIconsWidget, VideoPlayerWidget



class RHSWidgets(QWidget):
    def __init__(self):
        super().__init__()
        self.buildRHS()

    # Function builds the right hand side of the NanoLocz program
    def buildRHS(self):
        # Build the widgets and layouts
        self.layout = QVBoxLayout(self)

        self.videoEditingIconsWidget = VideoEditingIconsWidget()
        self.videoDropdownWidgets = VideoDropdownWidget()
        self.videoPlayerWidgets = VideoPlayerWidget()
        # videoAndParticleControlWidgets = self.buildVideoAndParticleControlWidgets()

        self.layout.addWidget(self.videoEditingIconsWidget)
        self.layout.addWidget(self.videoDropdownWidgets)
        self.layout.addWidget(self.videoPlayerWidgets)
        # self.layout.addWidget(videoAndParticleControlWidgets)
        
        self.setLayout(self.layout)


    def buildVideoAndParticleControlWidgets(self) -> QWidget:
        pass


# TODO: remove once finished
if __name__ == '__main__':
    app = QApplication(sys.argv)
    rhs_widgets = RHSWidgets()
    rhs_widgets.show()
    sys.exit(app.exec())