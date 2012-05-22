# Created By: Virgil Dupras
# Created On: 2011-07-09
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

from cocoa.inter import PyGUIObject

class PyBuildPane(PyGUIObject):
    def lastGenDesc(self) -> str:
        return self.model.lastgen_desc
    
    def postProcessingEnabled(self) -> bool:
        return self.model.post_processing_enabled
    
    def selectedEbookType(self) -> int:
        return self.model.selected_ebook_type
    
    def setSelectedEbookType_(self, value: int):
        self.model.selected_ebook_type = value
    
    def setEbookTitle_(self, value: str):
        self.model.ebook_title = value
    
    def setEbookAuthor_(self, value: str):
        self.model.ebook_author = value
    
    def generateMarkdown(self):
        self.model.generate_markdown()
    
    def editMarkdown(self):
        self.model.edit_markdown()
    
    def revealMarkdown(self):
        self.model.reveal_markdown()
    
    def viewHTML(self):
        self.model.view_html()
    
    def createEbookAtPath_(self, path: str):
        self.model.create_ebook(path)
    
