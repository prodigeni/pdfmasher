/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/gplv3_license
*/

#import "PMOpenedFileLabel.h"

@implementation PMOpenedFileLabel
- (id)initWithPyRef:(PyObject *)aPyRef textView:(NSTextField *)aView
{
    self = [super initWithPyRef:aPyRef wrapperClass:[PyOpenedFileLabel class]
        callbackClassName:@"GUIObjectView" view:aView];
    return self;
}
        
- (PyOpenedFileLabel *)model
{
    return (PyOpenedFileLabel *)model;
}

- (NSTextField *)view
{
    return (NSTextField *)[super view];
}

/* model --> view */

- (void)refresh
{
    [[self view] setStringValue:[[self model] text]];
}

@end