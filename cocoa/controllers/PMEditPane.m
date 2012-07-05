/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/gplv3_license
*/

#import "PMEditPane.h"
#import "PMEditPane_UI.h"
#import "HSPyUtil.h"

@implementation PMEditPane

@synthesize hideIgnoredButton;
@synthesize editTextView;
@synthesize saveButton;
@synthesize cancelButton;

/* Until we push down all the logic that has anything to do with "app", we're stuck with the old
   initWithPyParent.
*/ 
- (id)initWithPyParent:(id)aPyParent
{
    PyEditPane *m = [[PyEditPane alloc] initWithModel:[(PyPdfMasher *)aPyParent editPane]];
    self = [self initWithModel:m];
    app = (PyPdfMasher *)aPyParent;
    [self setView:createPMEditPane_UI(self)];
    [m bindCallback:createCallback(@"EditPaneView", self)];
    [m release];
    return self;
}
        
- (PyEditPane *)model
{
    return (PyEditPane *)model;
}

- (void)selectNormal
{
    [app changeStateOfSelected:@"normal"];
}

- (void)selectTitle
{
    [app changeStateOfSelected:@"title"];
}

- (void)selectFootnote
{
    [app changeStateOfSelected:@"footnote"];
}

- (void)selectToFix
{
    [app changeStateOfSelected:@"tofix"];
}

- (void)selectIgnored
{
    [app changeStateOfSelected:@"ignored"];
}

- (void)toggleHideIgnored
{
    BOOL isChecked = [hideIgnoredButton state] == NSOnState;
    [app setHideIgnored:isChecked];
}

- (void)saveEdits
{
    [[self model] setEditText:[editTextView string]];
    [[self model] saveEdits];
}

- (void)cancelEdits
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