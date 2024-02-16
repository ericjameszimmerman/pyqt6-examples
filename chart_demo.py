import sys
import matplotlib

matplotlib.use('QT5Agg')  # Use QT5Agg backend for compatibility with PyQt6
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):
    def __init__(self, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Application with Buttons, Labels, and Matplotlib Chart")

        # Create a central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create a vertical layout
        self.layout = QVBoxLayout(self.central_widget)

        # Add a button
        self.button = QPushButton("Click Me")
        self.layout.addWidget(self.button)

        # Add a label
        self.label = QLabel("Hello, PyQt6!")
        self.layout.addWidget(self.label)

        # Add a Matplotlib chart
        self.canvas = MplCanvas(width=5, height=4, dpi=100)
        self.canvas.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        self.layout.addWidget(self.canvas)

        # Connect button click to the method
        self.button.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        self.label.setText("Button clicked!")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
