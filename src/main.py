import sys
from PyQt5 import QtWidgets
from file_copier import FileCopier
from tools import Tools

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Modding Tool Launcher")
        self.setGeometry(400, 200, 300, 150)

        # Layout
        layout = QtWidgets.QVBoxLayout()

        # Buttons to launch the other windows
        self.launch_copier_button = QtWidgets.QPushButton("Launch File Copier")
        self.launch_copier_button.clicked.connect(self.launch_file_copier)
        layout.addWidget(self.launch_copier_button)

        self.launch_tools_button = QtWidgets.QPushButton("Launch Recommended Modding Tools")
        self.launch_tools_button.clicked.connect(self.launch_tools)
        layout.addWidget(self.launch_tools_button)

        self.setLayout(layout)

    def launch_file_copier(self):
        """Launch the File Copier window."""
        self.file_copier = FileCopier()
        self.file_copier.show()

    def launch_tools(self):
        """Launch the Tools window."""
        self.tools_window = Tools()
        self.tools_window.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
