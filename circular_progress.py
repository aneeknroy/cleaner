import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QSizePolicy
from PyQt5.QtCore import Qt, QTimer, QRectF
from PyQt5.QtGui import QPainter, QColor, QPen

class CircularProgress(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(100, 100)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.progress = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateProgress)
        self.startAnimation()  # Start animation automatically

    def setProgress(self, value):
        self.progress = value
        self.update()

    def startAnimation(self):
        self.timer.start(100)

    def updateProgress(self):
        self.progress += 1
        if self.progress >= 100:
            self.timer.stop()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = min(self.width(), self.height())
        side = min(self.width(), self.height())

        # Background circle
        painter.setPen(QPen(Qt.lightGray, 10, Qt.SolidLine))
        painter.drawEllipse(QRectF(5, 5, side - 10, side - 10))

        # Progress arc
        painter.setPen(QPen(Qt.blue, 10, Qt.SolidLine))
        painter.drawArc(QRectF(5, 5, side - 10, side - 10), 90 * 16, -self.progress * 360 * 16 / 100)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    progress = CircularProgress()
    progress.show()
    sys.exit(app.exec_())
