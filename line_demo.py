import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import Qt, QPoint

class LineDrawerWidget(QWidget):
    def __init__(self, parent=None):
        super(LineDrawerWidget, self).__init__(parent)
        self.start_point = None
        self.end_point = None
        self.setMouseTracking(True)  # Enable mouse tracking

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if not self.start_point:
                self.start_point = event.position().toPoint()
            else:
                self.end_point = event.position().toPoint()
                self.update()  # Trigger the paint event

    def mouseMoveEvent(self, event):
        if self.start_point is not None:
            self.end_point = event.position().toPoint()
            self.update()  # Trigger the paint event

    def paintEvent(self, event):
        if self.start_point and self.end_point:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.GlobalColor.black, 2))
            painter.drawLine(self.start_point, self.end_point)

    def clear(self):
        self.start_point = None
        self.end_point = None
        self.update()

class MainWindow(QMainWindow):
    def __init__(self, widget):
        super().__init__()
        self.setWindowTitle('Line Drawer with PyQt6')
        self.setGeometry(100, 100, 800, 600)
        self.setCentralWidget(widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    line_drawer_widget = LineDrawerWidget()
    main_window = MainWindow(line_drawer_widget)
    main_window.show()
    sys.exit(app.exec())
