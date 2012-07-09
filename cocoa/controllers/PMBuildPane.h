/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/gplv3_license
*/

#import <Cocoa/Cocoa.h>

#import "HSGUIController.h"
#import "PyPdfMasher.h"
#import "PyBuildPane.h"

@interface PMBuildPane : HSGUIController
{
    NSTextField *lastGenDescLabel;
    NSButton *editMarkdownButton;
    NSButton *revealMarkdownButton;
    NSButton *viewHTMLButton;
    NSButton *createEbookButton;
    NSTextField *ebookTitleTextField;
    NSTextField *ebookAuthorTextField;
    NSMatrix *ebookTypeRadioButtons;
}

@property (readwrite, retain) NSTextField *lastGenDescLabel;
@property (readwrite, retain) NSButton *editMarkdownButton;
@property (readwrite, retain) NSButton *revealMarkdownButton;
@property (readwrite, retain) NSButton *viewHTMLButton;
@property (readwrite, retain) NSButton *createEbookButton;
@property (readwrite, retain) NSTextField *ebookTitleTextField;
@property (readwrite, retain) NSTextField *ebookAuthorTextField;
@property (readwrite, retain) NSMatrix *ebookTypeRadioButtons;

- (id)initWithPyRef:(PyObject *)aPyRef;
- (PyBuildPane *)model;

- (void)generateMarkdown;
- (void)editMarkdown;
- (void)revealInFinder;
- (void)viewHTML;
- (void)createEbook;
- (void)selectEbookType;
@end