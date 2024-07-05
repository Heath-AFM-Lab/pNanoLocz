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

# Range validator for the "delete frames" input (attached to the video controls widget)
class RangeValidator(QValidator):
    def validate(self, input_str, pos):
        # Empty input is considered intermediate state (not invalid)
        if not input_str:
            return (QValidator.State.Intermediate, input_str, pos)

        # Regular expression to match a single number or a range like "10-20"
        range_pattern = re.compile(r'^\d+(-\d+)?$')
        
        if range_pattern.match(input_str):
            return (QValidator.State.Acceptable, input_str, pos)
        else:
            return (QValidator.State.Invalid, input_str, pos)

    def fixup(self, input_str):
        # Optionally, implement any automatic fixes for invalid input
        return input_str



# TODO: remove once finished
if __name__ == '__main__':
    app = QApplication(sys.argv)
    rhs_widgets = RHSWidgets()
    rhs_widgets.show()
    sys.exit(app.exec())