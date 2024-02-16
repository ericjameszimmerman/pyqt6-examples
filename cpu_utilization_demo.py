import sys
import numpy as np
import psutil
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class SystemMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("System Performance Monitor")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Labels for instantaneous and average values
        self.cpu_label = QLabel("CPU: 0%")
        self.mem_label = QLabel("Memory: 0%")
        self.avg_cpu_label = QLabel("Average CPU: 0%")
        self.avg_mem_label = QLabel("Average Memory: 0%")

        # Set large font for labels
        font = QFont("Arial", 16)
        self.cpu_label.setFont(font)
        self.mem_label.setFont(font)
        self.avg_cpu_label.setFont(font)
        self.avg_mem_label.setFont(font)

        # Add labels to layout
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.mem_label)
        layout.addWidget(self.avg_cpu_label)
        layout.addWidget(self.avg_mem_label)

        # Matplotlib Figure for plotting
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.ax = self.figure.add_subplot(111)

        # Data storage
        self.time_window = 20  # seconds
        self.update_interval = 1000  # milliseconds
        self.time_data = np.linspace(-self.time_window, 0, num=int(self.time_window * 1000 / self.update_interval))
        self.cpu_data = np.zeros_like(self.time_data)
        self.mem_data = np.zeros_like(self.time_data)

        # Set up plot
        self.cpu_line, = self.ax.plot(self.time_data, self.cpu_data, label="CPU (%)")
        self.mem_line, = self.ax.plot(self.time_data, self.mem_data, label="Memory (%)")
        self.ax.legend(loc="upper left")
        self.ax.set_ylim(0, 100)
        self.ax.set_title("CPU and Memory Utilization")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Utilization (%)")

        # Timer to update data
        self.timer = QTimer()
        self.timer.setInterval(self.update_interval)
        self.timer.timeout.connect(self.update_data)
        self.timer.start()

    def update_data(self):
        # Fetch new data
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent

        # Update data arrays
        self.cpu_data = np.roll(self.cpu_data, -1)
        self.mem_data = np.roll(self.mem_data, -1)
        self.cpu_data[-1] = cpu
        self.mem_data[-1] = mem

        # Update plot lines
        self.cpu_line.set_ydata(self.cpu_data)
        self.mem_line.set_ydata(self.mem_data)

        # Update labels
        self.cpu_label.setText(f"CPU: {cpu}%")
        self.mem_label.setText(f"Memory: {mem}%")
        self.avg_cpu_label.setText(f"Average CPU: {np.mean(self.cpu_data):.2f}%")
        self.avg_mem_label.setText(f"Average Memory: {np.mean(self.mem_data):.2f}%")

        # Redraw the canvas
        self.canvas.draw()


def main():
    app = QApplication(sys.argv)
    ex = SystemMonitor()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
