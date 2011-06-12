import sys

from PyQt4.QtGui import QApplication

from qt.mainwindow import MainWindow

def main(argv):
    app = QApplication(argv)
    mw = MainWindow()
    mw.show()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
