/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "BSD" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/bsd_license
*/

#import "PMEditPane.h"

@implementation PMEditPane
- (id)initWithPyParent:(id)aPyParent
{
    self = [super initWithPyClassName:@"PyEditPane" pyParent:aPyParent];
    [NSBundle loadNibNamed:@"EditPane" owner:self];
    app = (PyApp *)aPyParent;
    [[self py] connect];
    return self;
}
        
- (PyEditPane *)py
{
    return (PyEditPane *)py;
}

- (NSView *)view
{
    return wholeView;
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
    [[self py] setEditText:[editTextField stringValue]];
    [[self py] saveEdits];
}

- (IBAction)cancelEdits:(id)sender
{
    [[self py] cancelEdits];
    [editTextField setStringValue:[[self py] editText]];
}

/* model --> view */

- (void)refreshEditText
{
    [editTextField setStringValue:[[self py] editText]];
    BOOL enabled = [[self py] editEnabled];
    [editTextField setEnabled:enabled];
    [saveButton setEnabled:enabled];
    [cancelButton setEnabled:enabled];
}

@end