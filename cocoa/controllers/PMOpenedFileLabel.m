/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "BSD" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/bsd_license
*/

#import "PMOpenedFileLabel.h"

@implementation PMOpenedFileLabel
- (id)initWithPyParent:(id)aPyParent view:(NSTextField *)aView
{
    self = [super initWithPyClassName:@"PyOpenedFileLabel" pyParent:aPyParent];
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