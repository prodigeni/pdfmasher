#!/usr/bin/env python3
# Created By: Virgil Dupras
# Created On: 2011-06-12
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

import sys
import gc
import sip
sip.setapi('QVariant', 1)

from PyQt4.QtGui import QApplication, QIcon, QPixmap

from qtlib.error_report_dialog import install_excepthook
from hscommon.trans import install_qt_trans
from hscommon.plat import ISWINDOWS
from core import __appname__, __version__
import qt.pm_rc

if ISWINDOWS:
    import qt.cxfreeze_fix

def main(argv):
    app = QApplication(argv)
    app.setWindowIcon(QIcon(QPixmap(":/logo_small")))
    app.setOrganizationName("Hardcoded Software")
    app.setApplicationName(__appname__)
    app.setApplicationVersion(__version__)
    install_qt_trans('en')
    from qt.app import PdfMasher
    pmapp = PdfMasher()
    install_excepthook()
    result = app.exec()
    # Avoid "QObject::startTimer: QTimer can only be used with threads started with QThread" on shutdown
    del pmapp
    gc.collect()
    return result

if __name__ == "__main__":
    sys.exit(main(sys.argv))
