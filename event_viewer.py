import sys
import zmq
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QCheckBox
from PyQt6.QtCore import QTimer, QDateTime
from threading import Thread

class ZMQListener(Thread):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.active = True
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect("tcp://localhost:5555")  # Adjust as needed
        self.topics = {}

    def run(self):
        while self.active:
            message = self.socket.recv_string()
            topic, msg = message.split()
            if topic in self.topics and self.topics[topic]:
                timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss.zzz")
                self.callback(timestamp, topic, msg)

    def subscribe(self, topic):
        self.socket.setsockopt_string(zmq.SUBSCRIBE, topic)
        self.topics[topic] = True

    def unsubscribe(self, topic):
        self.socket.setsockopt_string(zmq.UNSUBSCRIBE, topic)
        del self.topics[topic]

    def hide_topic(self, topic, hide):
        self.topics[topic] = not hide

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.listener = ZMQListener(self.add_message)
        self.listener.start()

    def initUI(self):
        self.setWindowTitle('ZeroMQ Topic Monitor')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Timestamp", "Topic ID", "Message"])
        
        self.controlsLayout = QHBoxLayout()
        self.topicInput = QCheckBox("Enable Topic 1")
        self.topicInput.toggled.connect(self.toggle_topic)
        self.controlsLayout.addWidget(self.topicInput)

        self.hideButton = QPushButton("Hide Topic")
        self.hideButton.clicked.connect(self.hide_topic)
        self.controlsLayout.addWidget(self.hideButton)

        layout.addWidget(self.tableWidget)
        layout.addLayout(self.controlsLayout)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def toggle_topic(self, checked):
        topic = "1"  # Example topic ID
        if checked:
            self.listener.subscribe(topic)
        else:
            self.listener.unsubscribe(topic)

    def hide_topic(self):
        topic = "1"  # Example topic ID
        self.listener.hide_topic(topic, True)

    def add_message(self, timestamp, topic, message):
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(timestamp))
        self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(topic))
        self.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(message))

app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()
sys.exit(app.exec_())
