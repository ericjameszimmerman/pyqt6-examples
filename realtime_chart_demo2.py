import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class RealTimePlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set the window title and size
        self.setWindowTitle("Real-Time Signal Plotter")
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget and set layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create a matplotlib figure for plotting the signals
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.ax = self.figure.add_subplot(111)

        # Initialize data storage for voltage, current, and power
        self.time_window = 30  # seconds
        self.update_interval = 500  # milliseconds
        self.time_data = np.linspace(-self.time_window, 0, num=int(self.time_window*1000/self.update_interval))
        self.voltage_data = np.zeros_like(self.time_data)
        self.current_data = np.zeros_like(self.time_data)
        self.power_data = np.zeros_like(self.time_data)

        # Set up the plot
        self.ax.set_xlim(-self.time_window, 0)
        self.ax.set_ylim(-10, 10)
        self.voltage_line, = self.ax.plot(self.time_data, self.voltage_data, label="Voltage (V)")
        self.current_line, = self.ax.plot(self.time_data, self.current_data, label="Current (A)")
        self.power_line, = self.ax.plot(self.time_data, self.power_data, label="Power (W)")
        self.ax.legend(loc="upper left")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Signal")

        # Set up a timer to update the plot
        self.timer = QTimer()
        self.timer.setInterval(self.update_interval)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        # Generate pseudo-random data for voltage, current, and power
        self.voltage_data = np.roll(self.voltage_data, -1)
        self.current_data = np.roll(self.current_data, -1)
        self.power_data = np.roll(self.power_data, -1)

        self.voltage_data[-1] = np.sin(np.pi * np.random.rand()) * 8
        self.current_data[-1] = np.cos(np.pi * np.random.rand()) * 5
        self.power_data[-1] = self.voltage_data[-1] * self.current_data[-1] * 0.1  # Simplified calculation

        # Update the plot lines
        self.voltage_line.set_ydata(self.voltage_data)
        self.current_line.set_ydata(self.current_data)
        self.power_line.set_ydata(self.power_data)

        # Redraw the canvas
        self.canvas.draw()

def main():
    app = QApplication(sys.argv)
    main_window = RealTimePlotter()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
