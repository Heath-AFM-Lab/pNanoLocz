import sys
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QFileDialog
from PyQt6.QtCore import pyqtSignal

class FolderOpener(QDialog):
    # Custom signal that transmits the folder path to the QFileTree
    folderReceived = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select a folder or a session file")

        layout = QVBoxLayout(self)
        label = QLabel("Select a folder or a session file", self)
        layout.addWidget(label)

        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

        self.folderPath = ""

    def exec(self):
        if super().exec() == QDialog.DialogCode.Accepted:
            return self.folderPath
        else:
            return ""

    def accept(self):
        self.folderPath = QFileDialog.getExistingDirectory(self, "Select Folder")
        if self.folderPath:
            self.folderReceived.emit(self.folderPath)  # Emit the folder path via signal
        super().accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    folderOpener = FolderOpener()
    folderOpenerResult = folderOpener.exec()
    if folderOpenerResult:
        print(f"Selected folder: {folderOpenerResult}")
        # Perform further actions with folderOpenerResult as needed
    sys.exit(app.exec())
