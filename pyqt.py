import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QFileDialog, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyleFactory

import subprocess
from circular_progress import CircularProgress  # Importing the CircularProgress widget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PPG Data Processing")
        self.setGeometry(100, 100, 600, 200)

        # Apply 'Cleanlooks' style
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))  # Use QApplication directly

        self.initUI()

    def initUI(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # File Selection Row
        file_row_layout = QHBoxLayout()
        layout.addLayout(file_row_layout)

        file_label = QLabel("Selected CSV File:")
        file_row_layout.addWidget(file_label)

        self.file_textbox = QLineEdit()
        self.file_textbox.setReadOnly(True)
        file_row_layout.addWidget(self.file_textbox)

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_file)
        self.browse_button.setStyleSheet("font-weight: bold;")  # Make the button text bold
        file_row_layout.addWidget(self.browse_button)

        # Action Row
        action_row_layout = QHBoxLayout()
        layout.addLayout(action_row_layout)

        completion_label = QLabel("Completion Indicator:")
        action_row_layout.addWidget(completion_label)

        self.completion_indicator = QLabel("Not Completed")
        action_row_layout.addWidget(self.completion_indicator)

        self.run_button = QPushButton("Run Script")
        self.run_button.clicked.connect(self.run_script)
        action_row_layout.addWidget(self.run_button)

        # Circular Progress Bar
        #self.circular_progress = CircularProgress()
        #layout.addWidget(self.circular_progress)
        #self.circular_progress.hide()  # Initially hide the circular progress bar

    def browse_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)", options=options)
        if file_name:
            self.file_textbox.setText(file_name)

    def run_script(self):
        csv_file = self.file_textbox.text()
        #self.circular_progress.show()
        if csv_file:
            try:
                # Show circular progress bar
                # Run the script using subprocess
                # Example command: python script.py input.csv
                subprocess.run(["python", "bandpassFun.py", csv_file], check=True)
                self.completion_indicator.setText("Completed")
            except subprocess.CalledProcessError:
                self.completion_indicator.setText("Error occurred")
            finally:
                # Hide circular progress bar after completion
                self.circular_progress.hide()
        else:
            self.completion_indicator.setText("No file selected")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
