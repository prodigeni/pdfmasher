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
    IBOutlet NSView *wholeView;
    IBOutlet NSTextField *lastGenDescLabel;
    IBOutlet NSButton *editMarkdownButton;
    IBOutlet NSButton *revealMarkdownButton;
    IBOutlet NSButton *viewHTMLButton;
    IBOutlet NSButton *createEbookButton;
    IBOutlet NSTextField *ebookTitleTextField;
    IBOutlet NSTextField *ebookAuthorTextField;
    IBOutlet NSMatrix *ebookTypeRadioButtons;
}
- (id)initWithPy:(id)aPy;
- (PyBuildPane *)py;
- (NSView *)view;

- (IBAction)generateMarkdown:(id)sender;
- (IBAction)editMarkdown:(id)sender;
- (IBAction)revealInFinder:(id)sender;
- (IBAction)viewHTML:(id)sender;
- (IBAction)createEbook:(id)sender;
- (IBAction)selectEbookType:(id)sender;
@end