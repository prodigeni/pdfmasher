/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "BSD" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/bsd_license
*/

#import "PMElementTable.h"

@implementation PMElementTable
- (id)initWithPyParent:(id)aPyParent tableView:(NSTableView *)aTableView
{
    self = [super initWithPyClassName:@"PyElementTable" pyParent:aPyParent view:aTableView];
    columns = [[HSColumns alloc] initWithPyParent:[self py] tableView:aTableView];
    [self initializeColumns];
    [self connect];
    return self;
}

- (void)dealloc
{
    [columns release];
    [super dealloc];
}

- (PyElementTable *)py
{
    return (PyElementTable *)py;
}

- (HSColumns *)columns
{
    return columns;
}

- (void)initializeColumns
{
    HSColumnDef defs[] = {
        {@"id", @"ID", 50, 20, 0, YES, nil},
        {@"page", @"Page", 50, 20, 0, YES, nil},
        {@"x", @"X", 50, 20, 0, YES, nil},
        {@"y", @"Y", 50, 20, 0, YES, nil},
        {@"fontsize", @"Font Size", 75, 20, 0, YES, nil},
        {@"state", @"State", 75, 20, 0, YES, nil},
        {@"text", @"Text", 250, 20, 0, YES, nil},
        nil
    };
    [[self columns] initializeColumns:defs];
    // [[self columns] restoreColumns];
}

@end