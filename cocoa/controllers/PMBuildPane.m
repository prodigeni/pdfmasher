/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/gplv3_license
*/

#import "PMBuildPane.h"

@implementation PMBuildPane
- (id)initWithPyParent:(id)aPyParent
{
    self = [super initWithPyClassName:@"PyBuildPane" pyParent:aPyParent];
    [NSBundle loadNibNamed:@"BuildPane" owner:self];
    [[self py] connect];
    return self;
}

- (PyBuildPane *)py
{
    return (PyBuildPane *)py;
}

- (NSView *)view
{
    return wholeView;
}

- (IBAction)generateMarkdown:(id)sender
{
    [[self py] generateMarkdown];
}

- (IBAction)editMarkdown:(id)sender
{
    [[self py] editMarkdown];
}

- (IBAction)revealInFinder:(id)sender
{
    [[self py] revealMarkdown];
}

- (IBAction)viewHTML:(id)sender
{
    [[self py] viewHTML];
}

/* model --> view */
- (void)refresh
{
    [lastGenDescLabel setStringValue:[[self py] lastGenDesc]];
    BOOL enabled = [[self py] postProcessingEnabled];
    [editMarkdownButton setEnabled:enabled];
    [revealMarkdownButton setEnabled:enabled];
    [viewHTMLButton setEnabled:enabled];
}
@end