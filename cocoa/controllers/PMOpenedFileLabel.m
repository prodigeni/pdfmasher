/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/gplv3_license
*/

#import "PMOpenedFileLabel.h"

@implementation PMOpenedFileLabel
- (id)initWithPy:(id)aPy textView:(NSTextField *)aView
{
    self = [super initWithPy:aPy view:aView];
    label = aView;
    [self connect];
    return self;
}
        
- (PyOpenedFileLabel *)py
{
    return (PyOpenedFileLabel *)py;
}

/* model --> view */

- (void)refresh
{
    [label setStringValue:[[self py] text]];
}

@end