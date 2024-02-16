import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QMessageBox, QToolBar, QStyle)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.statusBar().showMessage('Ready')

        # Create actions
        exitAct = QAction('Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(QApplication.instance().quit)

        aboutAct = QAction('About', self)
        aboutAct.triggered.connect(self.about)

        # Menu Bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(aboutAct)

        # Toolbar
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        # Create actions with standard icons
        action_names = ["New", "Open", "Save", "About"]
        tooltips = ["Create something new", "Open a file", "Save the file", "Show the application's About box"]
        standard_icons = [QStyle.StandardPixmap.SP_FileIcon, QStyle.StandardPixmap.SP_DirOpenIcon,
                          QStyle.StandardPixmap.SP_DialogSaveButton, QStyle.StandardPixmap.SP_DialogHelpButton]

        for name, tooltip, icon in zip(action_names, tooltips, standard_icons):
            action = QAction(self.style().standardIcon(icon), name, self)
            action.setToolTip(tooltip)
            if name == "About":
                action.triggered.connect(self.about)
            toolbar.addAction(action)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')

    def about(self):
        QMessageBox.about(self, "About Application",
                          "Version 1.0\nThis is a simple PyQt6 application example with a toolbar using standard icons.")

def main():
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
