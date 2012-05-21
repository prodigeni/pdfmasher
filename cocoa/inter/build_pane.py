# Created By: Virgil Dupras
# Created On: 2011-07-09
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

from hscommon.cocoa.inter import signature, PyGUIObject

class PyBuildPane(PyGUIObject):
    def lastGenDesc(self):
        return self.py.lastgen_desc
    
    @signature('c@:')
    def postProcessingEnabled(self):
        return self.py.post_processing_enabled
    
    @signature('i@:')
    def selectedEbookType(self):
        return self.py.selected_ebook_type
    
    @signature('v@:i')
    def setSelectedEbookType_(self, value):
        self.py.selected_ebook_type = value
    
    def setEbookTitle_(self, value):
        self.py.ebook_title = value
    
    def setEbookAuthor_(self, value):
        self.py.ebook_author = value
    
    def generateMarkdown(self):
        self.py.generate_markdown()
    
    def editMarkdown(self):
        self.py.edit_markdown()
    
    def revealMarkdown(self):
        self.py.reveal_markdown()
    
    def viewHTML(self):
        self.py.view_html()
    
    def createEbookAtPath_(self, path):
        self.py.create_ebook(path)
    
