import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from UI_components.RHS_Components import VideoDropdownWidget, VideoEditingIconsWidget, VideoPlayerWidget, ParticleViewerAndControlWidget

class RHSWidgets(QWidget):
    def __init__(self):
        super().__init__()
        self.buildRHS()

    # Function builds the right hand side of the NanoLocz program
    def buildRHS(self):
        # Build the widgets and layouts
        self.layout = QVBoxLayout(self)
        self.mediaLayout = QHBoxLayout()

        self.videoEditingIconsWidget = VideoEditingIconsWidget()
        self.videoDropdownWidgets = VideoDropdownWidget()
        self.videoPlayerWidgets = VideoPlayerWidget()
        self.particleViewerWidgets = ParticleViewerAndControlWidget()

        # Set size policy for video and particle widgets in a 1:1 ratio
        mediaPlayersSizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        mediaPlayersSizePolicy.setHorizontalStretch(1)
        self.videoPlayerWidgets.setSizePolicy(mediaPlayersSizePolicy)
        self.particleViewerWidgets.setSizePolicy(mediaPlayersSizePolicy)

        # Stick video and particle viewer widgets together
        self.mediaLayout.addWidget(self.videoPlayerWidgets)
        self.mediaLayout.addWidget(self.particleViewerWidgets)

        # Assemble final layout
        self.layout.addWidget(self.videoEditingIconsWidget)
        self.layout.addWidget(self.videoDropdownWidgets)
        self.layout.addLayout(self.mediaLayout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    rhs_widgets = RHSWidgets()
    rhs_widgets.show()
    sys.exit(app.exec())
