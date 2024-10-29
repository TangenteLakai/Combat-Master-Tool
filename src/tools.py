import sys
import os
import requests
from PyQt5 import QtWidgets, QtCore

class Tools(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Recommended Modding Tools")
        self.setGeometry(400, 200, 500, 150)

        # Layouts
        main_layout = QtWidgets.QVBoxLayout()
        button_layout = QtWidgets.QHBoxLayout()

        # Download Buttons
        self.uabea_button = QtWidgets.QPushButton("Download UABEA")
        self.uabea_button.clicked.connect(lambda: self.download_tool(
            "https://github.com/nesrak1/UABEA/releases/latest/download/UABEA.zip", "UABEA.zip"
        ))
        button_layout.addWidget(self.uabea_button)

        self.asset_studio_button = QtWidgets.QPushButton("Download AssetStudio")
        self.asset_studio_button.clicked.connect(lambda: self.download_tool(
            "https://github.com/Perfare/AssetStudio/releases/latest/download/AssetStudio.zip", "AssetStudio.zip"
        ))
        button_layout.addWidget(self.asset_studio_button)

        # Progress Bar
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setValue(0)

        # Add widgets to layout
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.progress_bar)
        self.setLayout(main_layout)

    def download_tool(self, url, filename):
        """Downloads a file from a URL with a progress bar."""
        self.progress_bar.setValue(0)
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get("content-length", 0))

        with open(filename, "wb") as file:
            downloaded_size = 0
            for data in response.iter_content(1024):
                file.write(data)
                downloaded_size += len(data)
                progress = int((downloaded_size / total_size) * 100)
                self.progress_bar.setValue(progress)
                QtCore.QCoreApplication.processEvents()  # Update UI during download

        QtWidgets.QMessageBox.information(self, "Download Complete", f"{filename} has been downloaded.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    tools_window = Tools()
    tools_window.show()
    sys.exit(app.exec_())
