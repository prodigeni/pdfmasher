# Created By: Virgil Dupras
# Created On: 2011-08-07
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

class ElementState:
    Normal = 'normal'
    Title = 'title'
    Footnote = 'footnote'
    ToFix = 'tofix'
    Ignored = 'ignored'

SHORTCUTKEY2FLAG = {
    'N': ElementState.Normal,
    'T': ElementState.Title,
    'F': ElementState.Footnote,
    'X': ElementState.ToFix,
    'I': ElementState.Ignored,
}