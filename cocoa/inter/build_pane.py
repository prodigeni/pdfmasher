# Created By: Virgil Dupras
# Created On: 2011-07-09
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from hscommon.cocoa.inter import signature, PyGUIObject

from core.gui.build_pane import BuildPane

class PyBuildPane(PyGUIObject):
    py_class = BuildPane
    
    def lastGenDesc(self):
        return self.py.lastgen_desc
    
    @signature('c@:')
    def postProcessingEnabled(self):
        return self.py.post_processing_enabled
    
    def generateMarkdown(self):
        self.py.generate_markdown()
    
    def editMarkdown(self):
        self.py.edit_markdown()
    
    def revealMarkdown(self):
        self.py.reveal_markdown()
    
    def viewHTML(self):
        self.py.view_html()
    
