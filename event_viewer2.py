import sys
import zmq
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QCheckBox, QLabel, QScrollArea
from PyQt6.QtCore import QTimer, QDateTime, Qt
from PyQt6.QtWidgets import QHeaderView
from threading import Thread

class ZMQListener(Thread):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.active = True
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        try:
            self.socket.connect("tcp://localhost:5555")  # Adjust as needed
        except zmq.ZMQError as e:
            print(f"Failed to connect: {e}")
            self.active = False
        self.topics = {str(i): False for i in range(1, 33)}

    def run(self):
        while self.active:
            try:
                message = self.socket.recv_string(zmq.NOBLOCK)
                topic, msg = message.split()
                if topic in self.topics and self.topics[topic]:
                    timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss.zzz")
                    self.callback(timestamp, topic, msg)
            except zmq.Again:
                continue

    def subscribe(self, topic):
        if self.active:
            self.socket.setsockopt_string(zmq.SUBSCRIBE, topic)
            self.topics[topic] = True

    def unsubscribe(self, topic):
        if self.active:
            self.socket.setsockopt_string(zmq.UNSUBSCRIBE, topic)
            self.topics[topic] = False

    def hide_topic(self, topic, hide):
        if topic in self.topics:
            self.topics[topic] = not hide

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.listener = ZMQListener(self.add_message)
        if self.listener.active:
            self.listener.start()

    def initUI(self):
        self.setWindowTitle('ZeroMQ Topic Monitor')
        self.setGeometry(100, 100, 1000, 800)

        mainLayout = QVBoxLayout()
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Timestamp", "Topic ID", "Message"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        self.topicControls = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scrollWidget = QWidget()
        scroll.setWidget(scrollWidget)
        scrollWidget.setLayout(self.topicControls)

        for i in range(1, 33):
            checkBox = QCheckBox(f"Enable/Hide Topic {i}")
            checkBox.stateChanged.connect(lambda checked, topic=str(i): self.toggle_topic(topic, checked))
            self.topicControls.addWidget(checkBox)

        mainLayout.addWidget(self.tableWidget)
        mainLayout.addWidget(scroll)

        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

    def toggle_topic(self, topic, checked):
        if checked == Qt.CheckState.Checked:
            self.listener.subscribe(topic)
        else:
            self.listener.hide_topic(topic, True)
        self.listener.unsubscribe(topic)

    def add_message(self, timestamp, topic, message):
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(timestamp))
        self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(topic))
        self.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(message))

app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()
sys.exit(app.exec())
