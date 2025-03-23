from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QComboBox, QLineEdit, QFileDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from rfdetr import RFDETRBase
from ui.workers import Worker1, Worker2

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simple RF-DETR Application")
        self.resize(800, 600)

        self.VBL = QVBoxLayout()

        self.FeedLabel = QLabel()
        self.VBL.addWidget(self.FeedLabel, alignment = Qt.AlignmentFlag.AlignCenter)

        self.CancelButton = QPushButton("Cancel")
        self.CancelButton.clicked.connect(self.CancelFeed)
        self.VBL.addWidget(self.CancelButton)

        self.StartButton = QPushButton("Start")
        self.StartButton.clicked.connect(self.StartFeed)
        self.VBL.addWidget(self.StartButton)

        # Combobox to pick either from file or live camera
        self.combobox = QComboBox()
        self.combobox.addItems(['From camera', 'From file'])
        self.VBL.addWidget(self.combobox)
        
        # Text field to show the file path
        self.filePathEdit = QLineEdit(self)
        self.filePathEdit.setEnabled(False)
        self.VBL.addWidget(self.filePathEdit)

        # Button to open the file dialog
        self.browseButton = QPushButton("Browse...", self)
        self.browseButton.setEnabled(False)
        self.browseButton.clicked.connect(self.open_file_dialog)
        self.VBL.addWidget(self.browseButton)

        # Connect combobox changes to a callback function
        self.combobox.currentTextChanged.connect(self.mode_changed)

        self.setLayout(self.VBL)
    
    def open_file_dialog(self):
            # Open the file dialog and get the file path
            file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")
            if file_path:
                self.filePathEdit.setText(file_path)
    
    def mode_changed(self, text):
        if text == "From file":
            self.filePathEdit.setEnabled(True)
            self.browseButton.setEnabled(True)
        else:
            self.filePathEdit.setEnabled(False)
            self.browseButton.setEnabled(False)

    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))
    
    def CancelFeed(self):
        selected_option = self.combobox.currentText()
        if selected_option == "From camera":
            self.LiveFeedWorker.stop()
        elif selected_option == "From file":
            self.FileWorker.stop()
        else:
            raise
        self.FeedLabel.clear()
    
    def StartFeed(self):
        selected_option = self.combobox.currentText()

        if selected_option == "From camera":
            self.LiveFeedWorker = Worker1()
            self.LiveFeedWorker.start()
            self.LiveFeedWorker.ImageUpdate.connect(self.ImageUpdateSlot)
        elif selected_option == "From file":
            self.FileWorker = Worker2(filepath=self.filePathEdit.text())
            self.FileWorker.start()
            self.FileWorker.ImageUpdate.connect(self.ImageUpdateSlot)
        else:
            raise 