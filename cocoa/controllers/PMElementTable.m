/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/gplv3_license
*/

#import "PMElementTable.h"

@implementation PMElementTable
- (id)initWithPy:(id)aPy tableView:(PMElementTableView *)aTableView
{
    self = [super initWithPy:aPy view:aTableView];
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
        {@"page", 50, 20, 0, YES, nil},
        {@"order", 50, 20, 0, YES, nil},
        {@"x", 50, 20, 0, YES, nil},
        {@"y", 50, 20, 0, YES, nil},
        {@"fontsize", 70, 20, 0, YES, nil},
        {@"text_length", 70, 20, 0, YES, nil},
        {@"state", 75, 20, 0, YES, nil},
        {@"text", 150, 20, 0, YES, nil},
        nil
    };
    [[self columns] initializeColumns:defs];
    // [[self columns] restoreColumns];
}

/* Delegate */

- (void)flagShortcutPressed:(NSString *)shortcut
{
    [[self py] pressKey:shortcut];
}

@end