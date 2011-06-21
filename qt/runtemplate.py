#!/usr/bin/env python3
# Created By: Virgil Dupras
# Created On: 2011-06-12
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import sys
import sip
sip.setapi('QVariant', 1)

from PyQt4.QtGui import QApplication, QIcon, QPixmap

from hscommon.trans import install_qt_trans
from core import __appname__, __version__
import qt.pm_rc

def main(argv):
    app = QApplication(argv)
    app.setWindowIcon(QIcon(QPixmap(":/logo_small")))
    app.setOrganizationName("Hardcoded Software")
    app.setApplicationName(__appname__)
    app.setApplicationVersion(__version__)
    install_qt_trans('en')
    from qt.app import PdfMasher
    pmapp = PdfMasher()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
