import os
import shutil
import json
from datetime import datetime
from PyQt5 import QtWidgets, QtGui, QtCore

CONFIG_FILE = "config.json"
MODIFIED_FILES_JSON = "modified_files.json"

class FileCopier(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.file_paths = []
        self.backup_location = ""
        self.destination_dir = ""
        self.load_configuration()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Combat Master File Copier")
        self.setGeometry(300, 300, 800, 400)
        main_layout = QtWidgets.QVBoxLayout()
        button_layout = QtWidgets.QHBoxLayout()
        self.files_list_widget = QtWidgets.QListWidget()
        main_layout.addWidget(self.files_list_widget)
        select_files_button = QtWidgets.QPushButton("Select Files")
        select_files_button.clicked.connect(self.select_files)
        button_layout.addWidget(select_files_button)
        remove_files_button = QtWidgets.QPushButton("Remove Selected File")
        remove_files_button.clicked.connect(self.remove_selected_file)
        button_layout.addWidget(remove_files_button)
        self.backup_checkbox = QtWidgets.QCheckBox("Backup destination folder before copying")
        button_layout.addWidget(self.backup_checkbox)
        select_backup_location_button = QtWidgets.QPushButton("Select Backup Location")
        select_backup_location_button.clicked.connect(self.select_backup_location)
        button_layout.addWidget(select_backup_location_button)
        main_layout.addLayout(button_layout)
        copy_files_button = QtWidgets.QPushButton("Start Copying")
        copy_files_button.clicked.connect(self.copy_files)
        main_layout.addWidget(copy_files_button)
        self.setLayout(main_layout)
        self.load_modified_files()

    def select_files(self):
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Select Files")
        if files:
            self.file_paths.extend(files)
            for file in files:
                file_name = os.path.basename(file)
                self.files_list_widget.addItem(file_name)
            self.update_modified_files()

    def remove_selected_file(self):
        selected_items = self.files_list_widget.selectedItems()
        for item in selected_items:
            index = self.files_list_widget.row(item)
            self.files_list_widget.takeItem(index)
            del self.file_paths[index]
        self.update_modified_files()

    def select_backup_location(self):
        backup_location = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Backup Location")
        if backup_location:
            self.backup_location = backup_location

    def backup_destination(self, destination_dir):
        if not self.backup_location:
            QtWidgets.QMessageBox.critical(self, "Error", "No backup location selected.")
            return False

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = os.path.join(self.backup_location, f"backup_{timestamp}")
        try:
            shutil.copytree(destination_dir, backup_dir)
            QtWidgets.QMessageBox.information(self, "Backup", f"Backup created at: {backup_dir}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to create backup: {str(e)}")
            return False

        return True

    def copy_files(self):
        if not os.path.exists(self.destination_dir):
            QtWidgets.QMessageBox.critical(self, "Error", "Destination folder not found. Please ensure Combat Master is installed.")
            self.prompt_user_for_path()
            return

        if self.backup_checkbox.isChecked():
            if not self.backup_destination(self.destination_dir):
                return

        if not self.file_paths:
            QtWidgets.QMessageBox.warning(self, "Warning", "No files selected.")
            return

        for i, file_path in enumerate(self.file_paths):
            # Determine destination directory based on file extension
            file_extension = os.path.splitext(file_path)[1].lower()
            target_dir = self.destination_dir  # Default target

            if file_extension == ".resource":
                if "SteamLibrary" in self.destination_dir:
                    target_dir = os.path.join("SteamLibrary", "steamapps", "common", "Combat Master", "Data")
                else:
                    target_dir = os.path.join("Steam", "steamapps", "common", "Combat Master", "Data")

            # Copy the file to the target directory
            try:
                shutil.copy(file_path, target_dir)
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to copy {os.path.basename(file_path)}: {str(e)}")
                return

        QtWidgets.QMessageBox.information(self, "Success", "All files successfully copied to your game files.")

    def update_modified_files(self):
        with open(MODIFIED_FILES_JSON, "w") as file:
            json.dump(self.file_paths, file, indent=4)

    def load_modified_files(self):
        if os.path.exists(MODIFIED_FILES_JSON):
            with open(MODIFIED_FILES_JSON, "r") as file:
                self.file_paths = json.load(file)
                for file_path in self.file_paths:
                    file_name = os.path.basename(file_path)
                    self.files_list_widget.addItem(file_name)

    def load_configuration(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                config = json.load(file)
                self.destination_dir = config.get("destination_dir", "")
                if self.destination_dir and os.path.exists(self.destination_dir):
                    return  # Config is valid

        self.destination_dir = self.find_game_folder()
        if not self.destination_dir:
            self.prompt_user_for_path()
        else:
            self.save_configuration()

    def save_configuration(self):
        config = {"destination_dir": self.destination_dir}
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file, indent=4)

    def find_game_folder(self):
        possible_drives = [f"{chr(drive)}:\\" for drive in range(65, 91) if os.path.exists(f"{chr(drive)}:\\")]
        possible_paths = [
            "Steam\\steamapps\\common\\Combat Master\\Data\\StreamingAssets\\Bundles",
            "SteamLibrary\\steamapps\\common\\Combat Master\\Data\\StreamingAssets\\Bundles"
        ]

        linux_path = os.path.expanduser("~/.local/share/Steam/steamapps/common/Combat Master/Data/StreamingAssets/Bundles/")
        if os.path.exists(linux_path):
            return linux_path

        for drive in possible_drives:
            for path in possible_paths:
                potential_path = os.path.join(drive, path)
                if os.path.exists(potential_path):
                    return potential_path

        return ""

    def prompt_user_for_path(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Combat Master Bundles Folder")
        if path:
            self.destination_dir = path
            self.save_configuration()
