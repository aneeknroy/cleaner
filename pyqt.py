import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QFileDialog, QVBoxLayout, QWidget, QHBoxLayout, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
from script import main as script_main  # import the main function from script.py



import subprocess
from circular_progress import CircularProgress  # Importing the CircularProgress widget

import pandas as pd

# The rest of your imports and other code ...

class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return self._data.index[col]
        return None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PPG Data Processing")
        self.setGeometry(100, 100, 600, 200)

        # Apply 'Cleanlooks' style
        #QApplication.setStyle(QStyleFactory.create('Cleanlooks'))  # Use QApplication directly

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
        self.browse_button.setStyleSheet("font-weight: bold;")
        file_row_layout.addWidget(self.browse_button)

        # Subject Name Row
        subject_row_layout = QHBoxLayout()
        layout.addLayout(subject_row_layout)

        subject_label = QLabel("Subject Name:")
        subject_row_layout.addWidget(subject_label)

        self.subject_textbox = QLineEdit()
        subject_row_layout.addWidget(self.subject_textbox)

        # Folder Selection Row
        folder_row_layout = QHBoxLayout()
        layout.addLayout(folder_row_layout)

        folder_label = QLabel("Save to Folder:")
        folder_row_layout.addWidget(folder_label)

        self.folder_textbox = QLineEdit()
        self.folder_textbox.setReadOnly(True)
        folder_row_layout.addWidget(self.folder_textbox)

        self.folder_browse_button = QPushButton("Select Folder")
        self.folder_browse_button.clicked.connect(self.select_folder)
        folder_row_layout.addWidget(self.folder_browse_button)

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

        # Add a QTableView to the layout
        self.tableView = QTableView(self)
        layout.addWidget(self.tableView)  # Add the table view to the main layout

        # Window settings
        self.setWindowTitle("CSV Script Runner")
        self.setGeometry(300, 300, 600, 200)
        self.show()

        # Circular Progress Bar
        #self.circular_progress = CircularProgress()
        #layout.addWidget(self.circular_progress)
        #self.circular_progress.hide()  # Initially hide the circular progress bar

    def browse_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)", options=options)
        if file_name:
            self.file_textbox.setText(file_name)
    
    def select_folder(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)
        if folder_path:
            self.folder_textbox.setText(folder_path)

    def run_script(self):
        self.run_button.setEnabled(False)  # Disable the run button to prevent re-execution
        csv_file = self.file_textbox.text()
        output_folder = self.folder_textbox.text()
        subject_name = self.subject_textbox.text()

        if csv_file:
            try:
                subprocess.run(["python", "script.py", csv_file, output_folder, subject_name], check=True)
                results_df = script_main()  # add the necessary arguments if needed
                self.completion_indicator.setText("Completed")
            except subprocess.CalledProcessError:
                self.completion_indicator.setText("Error occurred")
            except Exception as e:
                self.completion_indicator.setText(f"Unexpected error: {e}")
            finally:
                self.run_button.setEnabled(True)  # Re-enable the run button
        else:
            self.completion_indicator.setText("No file selected")
            self.run_button.setEnabled(True)  # Re-enable the run button if no file is selected
        
        self.model = PandasModel(results_df)
        self.tableView.setModel(self.model)
        self.tableView.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
