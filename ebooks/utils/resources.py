# Copyright 2009, Kovid Goyal <kovid@kovidgoyal.net>
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

import builtins
import os.path as op

RESPATH = op.join(op.dirname(__file__), '..', 'resources')

def get_path(path):
    return op.join(RESPATH, path)

builtins.__dict__['P'] = get_path
