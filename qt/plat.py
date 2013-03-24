# Created By: Virgil Dupras
# Created On: 2011-06-21
# Copyright 2013 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

from hscommon.plat import ISWINDOWS, ISLINUX, ISOSX

if ISWINDOWS:
    from .plat_win import *
elif ISLINUX:
    from .plat_lnx import *
elif ISOSX:
    from .plat_osx import *
else:
    print("Unsupported platform")
