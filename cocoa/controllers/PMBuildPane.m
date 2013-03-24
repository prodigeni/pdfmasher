/* 
Copyright 2013 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/gplv3_license
*/

#import "PMBuildPane.h"
#import "PMBuildPane_UI.h"
#import "HSPyUtil.h"

#define PMEbookTypeMOBI 1
#define PMEbookTypeEPUB 2

@implementation PMBuildPane

@synthesize lastGenDescLabel;
@synthesize editMarkdownButton;
@synthesize revealMarkdownButton;
@synthesize viewHTMLButton;
@synthesize createEbookButton;
@synthesize ebookTitleTextField;
@synthesize ebookAuthorTextField;
@synthesize ebookTypeRadioButtons;

- (id)initWithPyRef:(PyObject *)aPyRef
{
    PyBuildPane *m = [[PyBuildPane alloc] initWithModel:aPyRef];
    self = [self initWithModel:m];
    [self setView:createPMBuildPane_UI(self)];
    [m bindCallback:createCallback(@"GUIObjectView", self)];
    [m release];
    return self;
}

- (PyBuildPane *)model
{
    return (PyBuildPane *)model;
}

- (void)generateMarkdown
{
    [[self model] generateMarkdown];
}

- (void)editMarkdown
{
    [[self model] editMarkdown];
}

- (void)revealInFinder
{
    [[self model] revealMarkdown];
}

- (void)viewHTML
{
    [[self model] viewHTML];
}

- (void)createEbook
{
    [[self model] setEbookTitle:[ebookTitleTextField stringValue]];
    [[self model] setEbookAuthor:[ebookAuthorTextField stringValue]];
    [[self model] createEbook];
}

- (void)selectEbookType
{
    NSInteger newtype;
    NSInteger col = [ebookTypeRadioButtons selectedColumn];
    if (col == 1) {
        newtype = PMEbookTypeEPUB;
    }
    else {
        newtype = PMEbookTypeMOBI;
    }
    [[self model] setSelectedEbookType:newtype];
}

/* model --> view */
- (void)refresh
{
    [lastGenDescLabel setStringValue:[[self model] lastGenDesc]];
    BOOL enabled = [[self model] postProcessingEnabled];
    [editMarkdownButton setEnabled:enabled];
    [revealMarkdownButton setEnabled:enabled];
    [viewHTMLButton setEnabled:enabled];
    [createEbookButton setEnabled:enabled];
}
@end