import sys
import os
import json
import requests
import zipfile
import subprocess
from PyQt5 import QtWidgets, QtCore

SETTINGS_FILE = "settings.json"

class Tools(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.load_settings()
        self.init_ui()

    def load_settings(self):
        """Load download status from the settings file."""
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as file:
                self.settings = json.load(file)
        else:
            self.settings = {"UABEA_downloaded": False, "AssetStudio_downloaded": False}

    def save_settings(self):
        """Save the current download status to the settings file."""
        with open(SETTINGS_FILE, "w") as file:
            json.dump(self.settings, file)

    def init_ui(self):
        self.setWindowTitle("Recommended Modding Tools")
        self.setGeometry(400, 200, 500, 200)

        # Layouts
        main_layout = QtWidgets.QVBoxLayout()
        button_layout = QtWidgets.QHBoxLayout()

        # UABEA Button
        if self.settings.get("UABEA_downloaded"):
            self.uabea_button = QtWidgets.QPushButton("Open UABEA")
            self.uabea_button.clicked.connect(lambda: self.open_program("additional_programs/UABEA/UABEAvalonia.exe"))
        else:
            self.uabea_button = QtWidgets.QPushButton("Download UABEA")
            self.uabea_button.clicked.connect(lambda: self.start_download(
                "https://github.com/nesrak1/UABEA/releases/download/v7/uabea-windows.zip", 
                "UABEA.zip", "UABEA"
            ))
        button_layout.addWidget(self.uabea_button)

        # AssetStudio Button
        if self.settings.get("AssetStudio_downloaded"):
            self.asset_studio_button = QtWidgets.QPushButton("Open AssetStudio")
            self.asset_studio_button.clicked.connect(lambda: self.open_program("additional_programs/AssetStudio/AssetStudioGUI.exe"))
        else:
            self.asset_studio_button = QtWidgets.QPushButton("Download AssetStudio")
            self.asset_studio_button.clicked.connect(lambda: self.start_download(
                "https://github.com/Perfare/AssetStudio/releases/download/v0.16.47/AssetStudio.net6.v0.16.47.zip", 
                "AssetStudio.zip", "AssetStudio"
            ))
        button_layout.addWidget(self.asset_studio_button)

        # Progress Bar
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setValue(0)

        # Add widgets to layout
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.progress_bar)
        self.setLayout(main_layout)

    def start_download(self, url, filename, folder_name):
        """Starts the download in a new thread."""
        self.progress_bar.setValue(0)
        self.thread = DownloadThread(url, filename, folder_name)
        self.thread.progress.connect(self.progress_bar.setValue)
        self.thread.finished.connect(lambda: self.on_download_complete(folder_name, filename))
        self.thread.start()

    def on_download_complete(self, folder_name, filename):
        """Handles actions after download completes and file is unzipped."""
        QtWidgets.QMessageBox.information(self, "Download Complete", f"{filename} has been downloaded and unzipped.")
        
        # Update the UI to show the Open button and save the download status
        if folder_name == "UABEA":
            self.uabea_button.setText("Open UABEA")
            self.uabea_button.clicked.disconnect()
            self.uabea_button.clicked.connect(lambda: self.open_program("additional_programs/UABEA/UABEAvalonia.exe"))
            self.settings["UABEA_downloaded"] = True
        elif folder_name == "AssetStudio":
            self.asset_studio_button.setText("Open AssetStudio")
            self.asset_studio_button.clicked.disconnect()
            self.asset_studio_button.clicked.connect(lambda: self.open_program("additional_programs/AssetStudio/AssetStudioGUI.exe"))
            self.settings["AssetStudio_downloaded"] = True

        self.save_settings()

    def open_program(self, path):
        """Opens the specified program using subprocess."""
        try:
            subprocess.Popen(path)
        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(self, "File Not Found", f"Could not find the file {path}")

class DownloadThread(QtCore.QThread):
    progress = QtCore.pyqtSignal(int)

    def __init__(self, url, filename, folder_name):
        super().__init__()
        self.url = url
        self.filename = filename
        self.folder_name = folder_name

    def run(self):
        response = requests.get(self.url, stream=True)
        total_size = int(response.headers.get("content-length", 0))

        # Ensure the additional_programs directory exists
        os.makedirs("additional_programs", exist_ok=True)

        # Download the file
        with open(self.filename, "wb") as file:
            downloaded_size = 0
            for data in response.iter_content(1024):
                file.write(data)
                downloaded_size += len(data)
                progress = int((downloaded_size / total_size) * 100)
                self.progress.emit(progress)

        # Unzip the file to the specified folder within additional_programs
        unzip_path = os.path.join("additional_programs", self.folder_name)
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.filename, "r") as zip_ref:
            zip_ref.extractall(unzip_path)

        # Delete the zip file after extraction
        os.remove(self.filename)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Tools()
    window.show()
    sys.exit(app.exec())
