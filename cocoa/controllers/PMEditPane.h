/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "BSD" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/bsd_license
*/

#import <Cocoa/Cocoa.h>

#import "HSGUIController.h"
#import "PyApp.h"
#import "PyEditPane.h"

@interface PMEditPane : HSGUIController
{
    IBOutlet NSView *wholeView;
    IBOutlet NSButton *hideIgnoredButton;
    IBOutlet NSTextField *editTextField;
    IBOutlet NSButton *saveButton;
    IBOutlet NSButton *cancelButton;
    
    PyApp *app;
}
- (id)initWithPyParent:(id)aPyParent;
- (PyEditPane *)py;
- (NSView *)view;

- (IBAction)selectNormal:(id)sender;
- (IBAction)selectTitle:(id)sender;
- (IBAction)selectFootnote:(id)sender;
- (IBAction)selectIgnored:(id)sender;
- (IBAction)toggleHideIgnored:(id)sender;
- (IBAction)saveEdits:(id)sender;
- (IBAction)cancelEdits:(id)sender;
@end