/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/gplv3_license
*/

#import "PMPageController.h"
#import "PMPageController_UI.h"
#import "Utils.h"
#import "HSPyUtil.h"

@implementation PMPageController

@synthesize pageReprPlaceholder;
@synthesize pageLabelTextField;
@synthesize reorderModeButton;

- (id)initWithPyRef:(PyObject *)aPyRef
{
    PyPageController *m = [[PyPageController alloc] initWithModel:aPyRef];
    self = [self initWithModel:m];
    [self setView:createPMPageController_UI(self)];
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

- (void)prevPage
{
    [[self model] prevPage];
}

- (void)nextPage
{
    [[self model] nextPage];
}

- (void)toggleShowOrder
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