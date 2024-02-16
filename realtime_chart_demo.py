import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QDial
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class SineWavePlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sine Wave Plotter")
        self.setGeometry(100, 100, 800, 600)  # x, y, width, height

        # Central Widget and Layout
        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        # Matplotlib Figure
        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.ax = self.canvas.figure.subplots()
        self.layout.addWidget(self.canvas)

        # Frequency Dial
        self.freqDial = QDial()
        self.freqDial.setMinimum(1)
        self.freqDial.setMaximum(20)
        self.freqDial.setValue(5)
        self.freqDial.valueChanged.connect(self.update_plot)
        self.layout.addWidget(self.freqDial)

        # Amplitude Dial
        self.ampDial = QDial()
        self.ampDial.setMinimum(1)
        self.ampDial.setMaximum(10)
        self.ampDial.setValue(1)
        self.ampDial.valueChanged.connect(self.update_plot)
        self.layout.addWidget(self.ampDial)

        # Frequency Label
        self.freqLabel = QLabel("Frequency: 5 Hz")
        self.freqLabel.setFont(QFont("Arial", 16))
        self.freqLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.freqLabel)

        # Amplitude Label
        self.ampLabel = QLabel("Amplitude: 1")
        self.ampLabel.setFont(QFont("Arial", 16))
        self.ampLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.ampLabel)

        # Initial Plot
        self.update_plot()

    def update_plot(self):
        freq = self.freqDial.value()
        amp = self.ampDial.value()
        self.freqLabel.setText(f"Frequency: {freq} Hz")
        self.ampLabel.setText(f"Amplitude: {amp}")

        t = np.linspace(0, 1, 1000)
        y = amp * np.sin(2 * np.pi * freq * t)
        self.ax.clear()
        self.ax.plot(t, y)
        self.ax.set(xlabel='Time (s)', ylabel='Amplitude',
                    title='Real-time Sine Wave Plot')
        self.canvas.draw()

def main():
    app = QApplication(sys.argv)
    window = SineWavePlotter()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
