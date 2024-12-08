from mainwindow import Window
from PySide6.QtWidgets import QApplication

def runGUI() -> None:
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()

if __name__ == '__main__':
    runGUI()
        