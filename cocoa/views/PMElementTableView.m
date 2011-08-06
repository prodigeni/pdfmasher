/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "BSD" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/bsd_license
*/

#import "PMElementTableView.h"
#import "NSEventAdditions.h"

@implementation PMElementTableView
- (void)keyDown:(NSEvent *)event 
{
    BOOL handled = NO;
    id delegate = [self delegate];
    BOOL responds = [delegate respondsToSelector:@selector(flagShortcutPressed:)];
    if ((responds) && ([event modifierKeysFlags] == 0)) { // No modif flag
        NSString *s = [event characters];
        NSSet *acceptableFlagKeys = [NSSet setWithObjects:@"n", @"t", @"f", @"x", @"i", nil];
        if ([acceptableFlagKeys containsObject:s]) {
            [delegate flagShortcutPressed:s];
            handled = YES;
        }
    }
    if (!handled) {
        [super keyDown:event];
    }
}
@end