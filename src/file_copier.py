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
        
        # Select Files Button
        select_files_button = QtWidgets.QPushButton("Select Files")
        select_files_button.clicked.connect(self.select_files)
        button_layout.addWidget(select_files_button)
        
        # Remove Files Button
        remove_files_button = QtWidgets.QPushButton("Remove Selected File")
        remove_files_button.clicked.connect(self.remove_selected_file)
        button_layout.addWidget(remove_files_button)
        
        # Backup Checkbox and Backup Location Button
        self.backup_checkbox = QtWidgets.QCheckBox("Backup destination folder before copying")
        button_layout.addWidget(self.backup_checkbox)
        select_backup_location_button = QtWidgets.QPushButton("Select Backup Location")
        select_backup_location_button.clicked.connect(self.select_backup_location)
        button_layout.addWidget(select_backup_location_button)
        
        # Copy Files Button
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
            QtWidgets.QMessageBox.warning(self,
