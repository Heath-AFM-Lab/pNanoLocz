from PyQt6.QtWidgets import QWidget, QHBoxLayout, QComboBox
from PyQt6.QtCore import pyqtSignal
from core.Image_Storage_Module.Media_Data_Manager_Class import MediaDataManager
from utils.file_reader.File_Reader import loadFileData

class DropdownWidget(QWidget):
    channelChanged = pyqtSignal(str)  # Signal to emit when channel changes

    def __init__(self):
        super().__init__()
        self.build_dropdown_widgets()
    
    def build_dropdown_widgets(self):
        self.media_data_manager = MediaDataManager()

        dropdown_layout = QHBoxLayout()

        self.dropdown1 = QComboBox()
        self.dropdown1.addItems(["All files", "Processed"])
        self.dropdown1.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        dropdown_layout.addWidget(self.dropdown1)

        self.channels_dropdown = QComboBox()
        self.channels_dropdown.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        dropdown_layout.addWidget(self.channels_dropdown)

        self.dropdown3 = QComboBox()
        self.dropdown3.addItems(["Stack off", "Stack on", "Intercalate"])
        self.dropdown3.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        dropdown_layout.addWidget(self.dropdown3)

        dropdown_layout.addStretch(1)
        self.setLayout(dropdown_layout)

        self.dropdown1.currentIndexChanged.connect(self.on_dropdown1_index_changed)
        self.channels_dropdown.currentIndexChanged.connect(self.on_channels_dropdown_index_changed)
        self.dropdown3.currentIndexChanged.connect(self.on_dropdown3_index_changed)
        self.media_data_manager.new_file_loaded.connect(self.load_channels)

    def on_dropdown1_index_changed(self):
        pass

    def on_channels_dropdown_index_changed(self):
        loadFileData(self.media_data_manager.get_file_path(), self.channels_dropdown.currentText())
        
    def on_dropdown3_index_changed(self):
        pass

    def load_channels(self):
        self.channels_dropdown.blockSignals(True)
        self.channels_dropdown.clear()
        self.channels_dropdown.addItems(self.media_data_manager.get_channels_list())
        self.channels_dropdown.setCurrentText(self.media_data_manager.get_cw_channel())
        self.channels_dropdown.adjustSize()  # Adjust size after adding items
        self.channels_dropdown.blockSignals(False)

if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    dropdown = DropdownWidget()
    dropdown.show()
    sys.exit(app.exec())