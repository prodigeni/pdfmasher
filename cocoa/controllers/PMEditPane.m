/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/gplv3_license
*/

#import "PMEditPane.h"
#import "HSPyUtil.h"

@implementation PMEditPane
/* Until we push down all the logic that has anything to do with "app", we're stuck with the old
   initWithPyParent.
*/ 
- (id)initWithPyParent:(id)aPyParent
{
    PyEditPane *m = [[PyEditPane alloc] initWithModel:[(PyPdfMasher *)aPyParent editPane]];
    self = [self initWithModel:m];
    [NSBundle loadNibNamed:@"EditPane" owner:self];
    app = (PyPdfMasher *)aPyParent;
    [self setView:wholeView];
    [m bindCallback:createCallback(@"EditPaneView", self)];
    [m release];
    return self;
}
        
- (PyEditPane *)model
{
    return (PyEditPane *)model;
}

- (IBAction)selectNormal:(id)sender
{
    [app changeStateOfSelected:@"normal"];
}

- (IBAction)selectTitle:(id)sender
{
    [app changeStateOfSelected:@"title"];
}

- (IBAction)selectFootnote:(id)sender
{
    [app changeStateOfSelected:@"footnote"];
}

- (IBAction)selectToFix:(id)sender
{
    [app changeStateOfSelected:@"tofix"];
}

- (IBAction)selectIgnored:(id)sender
{
    [app changeStateOfSelected:@"ignored"];
}

- (IBAction)toggleHideIgnored:(id)sender
{
    BOOL isChecked = [hideIgnoredButton state] == NSOnState;
    [app setHideIgnored:isChecked];
}

- (IBAction)saveEdits:(id)sender
{
    [[self model] setEditText:[editTextView string]];
    [[self model] saveEdits];
}

- (IBAction)cancelEdits:(id)sender
{
    [[self model] cancelEdits];
    [editTextView setString:[[self model] editText]];
}

/* model --> view */

- (void)refreshEditText
{
    [editTextView setString:[[self model] editText]];
    BOOL enabled = [[self model] editEnabled];
    [editTextView setEditable:enabled];
    [saveButton setEnabled:enabled];
    [cancelButton setEnabled:enabled];
}

@end