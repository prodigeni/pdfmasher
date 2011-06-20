/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "BSD" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/bsd_license
*/

#import "PMBuildPane.h"

@implementation PMBuildPane
- (id)initWithPyParent:(id)aPyParent
{
    self = [super init];
    [NSBundle loadNibNamed:@"BuildPane" owner:self];
    app = (PyApp *)aPyParent;
    return self;
}

- (NSView *)view
{
    return wholeView;
}
        
- (IBAction)viewHTML:(id)sender
{
    NSString *path = [app buildHtml];
    [[NSWorkspace sharedWorkspace] openFile:path];
}

@end