import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QFileDialog
from PyQt5.QtCore import Qt
import subprocess

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSV Processing App")
        self.setGeometry(100, 100, 600, 200)

        self.initUI()

    def initUI(self):
        # File Selection Row
        self.file_textbox = QLineEdit(self)
        self.file_textbox.setGeometry(10, 10, 400, 30)

        self.browse_button = QPushButton("Browse", self)
        self.browse_button.setGeometry(420, 10, 80, 30)
        self.browse_button.clicked.connect(self.browse_file)

        # Action Row
        self.completion_label = QLabel("Not Completed", self)
        self.completion_label.setGeometry(10, 60, 150, 30)

        self.run_button = QPushButton("Run Script", self)
        self.run_button.setGeometry(170, 60, 100, 30)
        self.run_button.clicked.connect(self.run_script)

    def browse_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)", options=options)
        if file_name:
            self.file_textbox.setText(file_name)

    def run_script(self):
        csv_file = self.file_textbox.text()
        if csv_file:
            try:
                # Run the script using subprocess
                # Example command: python script.py input.csv
                subprocess.run(["python", "bandpassFun.py", csv_file], check=True)
                self.completion_label.setText("Completed")
            except subprocess.CalledProcessError:
                self.completion_label.setText("Error occurred")
        else:
            self.completion_label.setText("No file selected")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
