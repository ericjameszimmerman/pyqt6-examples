import sys
import zmq
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTableWidget, QTableWidgetItem, QLabel, QScrollArea, QPushButton)
from PyQt6.QtCore import QTimer, QDateTime, Qt
from PyQt6.QtGui import QIcon, QPixmap
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
        self.topics = {str(i): {'subscribe': False, 'visible': True} for i in range(1, 33)}

    def run(self):
        while self.active:
            try:
                message = self.socket.recv_string(zmq.NOBLOCK)
                topic, msg = message.split()
                if topic in self.topics and self.topics[topic]['subscribe'] and self.topics[topic]['visible']:
                    timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss.zzz")
                    self.callback(timestamp, topic, msg)
            except zmq.Again:
                continue

    def subscribe(self, topic):
        if self.active:
            self.socket.setsockopt_string(zmq.SUBSCRIBE, topic)
            self.topics[topic]['subscribe'] = True

    def unsubscribe(self, topic):
        if self.active:
            self.socket.setsockopt_string(zmq.UNSUBSCRIBE, topic)
            self.topics[topic]['subscribe'] = False

    def toggle_visibility(self, topic):
        self.topics[topic]['visible'] = not self.topics[topic]['visible']

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.listener = ZMQListener(self.add_message)
        if self.listener.active:
            self.listener.start()

    def initUI(self):
        self.setWindowTitle('ZeroMQ Topic Monitor')
        self.setGeometry(100, 100, 1200, 800)

        mainLayout = QHBoxLayout()
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Timestamp", "Topic ID", "Message"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        sidebar = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scrollWidget = QWidget()
        scroll.setWidget(scrollWidget)
        scrollWidget.setLayout(sidebar)

        # Load icons for visibility toggle
        eye_open_icon = QIcon(QPixmap("images/eye-regular.png"))  # Adjust path
        eye_closed_icon = QIcon(QPixmap("images/eye-slash-regular.png"))  # Adjust path

        for i in range(1, 33):
            topicLayout = QHBoxLayout()
            toggleButton = QPushButton("Enable")
            toggleButton.setCheckable(True)
            toggleButton.toggled.connect(lambda checked, topic=str(i): self.toggle_topic(topic, checked))
            topicLayout.addWidget(toggleButton)

            eyeButton = QPushButton()
            eyeButton.setIcon(eye_open_icon)
            eyeButton.clicked.connect(lambda _, topic=str(i): self.toggle_visibility(topic, eyeButton, eye_open_icon, eye_closed_icon))
            topicLayout.addWidget(eyeButton)

            sidebar.addLayout(topicLayout)

        mainLayout.addWidget(self.tableWidget)
        mainLayout.addLayout(sidebar)

        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

    def toggle_topic(self, topic, checked):
        if checked:
            self.listener.subscribe(topic)
        else:
            self.listener.unsubscribe(topic)

    def toggle_visibility(self, topic, button, open_icon, closed_icon):
        self.listener.toggle_visibility(topic)
        current_icon = open_icon if self.listener.topics[topic]['visible'] else closed_icon
        button.setIcon(current_icon)

    def add_message(self, timestamp, topic, message):
        if self.listener.topics[topic]['visible']:
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(timestamp))
            self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(topic))
            self.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(message))

app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()
sys.exit(app.exec())
