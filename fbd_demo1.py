from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsItem, QLabel
from PyQt6.QtGui import QPainter, QBrush, QPen
from PyQt6.QtCore import Qt, QRectF

class FunctionBlock(QGraphicsItem):
    def __init__(self, name, inputs, outputs):
        super().__init__()
        self.name = name
        self.inputs = inputs
        self.outputs = outputs

    def boundingRect(self):
        return QRectF(0, 0, 120, 100)

    def paint(self, painter, option, widget):
        # Draw the block
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        painter.setBrush(QBrush(Qt.GlobalColor.lightGray))
        painter.drawRect(self.boundingRect())

        # Block name
        painter.drawText(self.boundingRect(), Qt.AlignmentFlag.AlignCenter, self.name)

        # Draw inputs and outputs as circles and label them
        for i, inp in enumerate(self.inputs, start=1):
            painter.drawEllipse(10, i * 20 - 10, 10, 10)
            painter.drawText(0, i * 20, inp)

        for i, out in enumerate(self.outputs, start=1):
            painter.drawEllipse(100, i * 20 - 10, 10, 10)
            painter.drawText(110, i * 20, out)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        # Example function block
        block = FunctionBlock("Sum", ["A", "B"], ["Out"])
        self.scene.addItem(block)
        block.setPos(50, 50)

        self.setWindowTitle("Function Block Diagram Example")
        self.setGeometry(100, 100, 800, 600)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
