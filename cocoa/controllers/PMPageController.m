/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "BSD" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/bsd_license
*/

#import "PMPageController.h"
#import "Utils.h"

@implementation PMPageController
- (id)initWithPyParent:(id)aPyParent
{
    self = [super initWithPyClassName:@"PyPageController" pyParent:aPyParent];
    [NSBundle loadNibNamed:@"PagePane" owner:self];
    pageRepr = [[PMPageRepr alloc] initWithPyParent:aPyParent];
    
    NSArray *children = [NSArray arrayWithObjects:[pageRepr py], nil];
    [[self py] setChildren:children];
    
    replacePlaceholderInView(pageReprPlaceholder, pageRepr);
    [[self py] connect];
    return self;
}
        
- (PyPageController *)py
{
    return (PyPageController *)py;
}

- (NSView *)view
{
    return wholeView;
}

- (IBAction)prevPage:(id)sender
{
    [[self py] prevPage];
}

- (IBAction)nextPage:(id)sender
{
    [[self py] nextPage];
}

- (IBAction)toggleShowOrder:(id)sender
{
    BOOL isChecked = [reorderModeButton state] == NSOnState;
    [[self py] setReorderMode:isChecked];
}

/* model --> view */
- (void)refreshPageLabel
{
    [pageLabelTextField setStringValue:[[self py] pageLabel]];
}
@end