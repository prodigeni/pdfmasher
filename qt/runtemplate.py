#!/usr/bin/env python3.1
# Created By: Virgil Dupras
# Created On: 2011-06-12
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import sys

from PyQt4.QtGui import QApplication

from qt.mainwindow import MainWindow

def main(argv):
    app = QApplication(argv)
    app.setOrganizationName("Hardcoded Software")
    app.setApplicationName("PdfMasher")
    mw = MainWindow()
    mw.show()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
