# Copyright 2008, Kovid Goyal kovid@kovidgoyal.net
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license



from core import __appname__, __version__

import sys, locale, codecs, os, importlib, collections

_plat = sys.platform.lower()
iswindows = 'win32' in _plat or 'win64' in _plat
isosx     = 'darwin' in _plat
isnewosx  = isosx and getattr(sys, 'new_app_bundle', False)
isfreebsd = 'freebsd' in _plat
isnetbsd = 'netbsd' in _plat
isbsd = isfreebsd or isnetbsd
islinux   = not(iswindows or isosx or isbsd)
isunix = isosx or islinux

try:
    preferred_encoding = locale.getpreferredencoding()
    codecs.lookup(preferred_encoding)
except:
    preferred_encoding = 'utf-8'

win32event = importlib.import_module('win32event') if iswindows else None
winerror   = importlib.import_module('winerror') if iswindows else None
win32api   = importlib.import_module('win32api') if iswindows else None
fcntl      = None if iswindows else importlib.import_module('fcntl')

filesystem_encoding = sys.getfilesystemencoding()
if filesystem_encoding is None: filesystem_encoding = 'utf-8'

