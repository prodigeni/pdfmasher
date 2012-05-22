/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/gplv3_license
*/

#import "PMPageController.h"
#import "Utils.h"

@implementation PMPageController
- (id)initWithPyRef:(PyObject *)aPyRef
{
    PyPageController *m = [[PyPageController alloc] initWithModel:aPyRef];
    self = [self initWithModel:m];
    [NSBundle loadNibNamed:@"PagePane" owner:self];
    [self setView:wholeView];
    [m bindCallback:createCallback(@"PageControllerView", self)];
    [m release];
    pageRepr = [[PMPageRepr alloc] initWithPyRef:[[self model] pageRepr]];
    replacePlaceholderInView(pageReprPlaceholder, pageRepr);
    return self;
}
        
- (PyPageController *)model
{
    return (PyPageController *)model;
}

- (IBAction)prevPage:(id)sender
{
    [[self model] prevPage];
}

- (IBAction)nextPage:(id)sender
{
    [[self model] nextPage];
}

- (IBAction)toggleShowOrder:(id)sender
{
    BOOL isChecked = [reorderModeButton state] == NSOnState;
    [[self model] setReorderMode:isChecked];
}

/* model --> view */
- (void)refreshPageLabel
{
    [pageLabelTextField setStringValue:[[self model] pageLabel]];
}
@end