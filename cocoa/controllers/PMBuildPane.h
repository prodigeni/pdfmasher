/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "BSD" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/bsd_license
*/

#import <Cocoa/Cocoa.h>

#import "HSGUIController.h"
#import "PyApp.h"
#import "PyBuildPane.h"

@interface PMBuildPane : HSGUIController
{
    IBOutlet NSView *wholeView;
    IBOutlet NSTextField *lastGenDescLabel;
    IBOutlet NSButton *editMarkdownButton;
    IBOutlet NSButton *revealMarkdownButton;
    IBOutlet NSButton *viewHTMLButton;
}
- (id)initWithPyParent:(id)aPyParent;
- (PyBuildPane *)py;
- (NSView *)view;

- (IBAction)generateMarkdown:(id)sender;
- (IBAction)editMarkdown:(id)sender;
- (IBAction)revealInFinder:(id)sender;
- (IBAction)viewHTML:(id)sender;
@end