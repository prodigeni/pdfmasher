/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/gplv3_license
*/

#import "PMBuildPane.h"
#import "Utils.h"

#define PMEbookTypeMOBI 1
#define PMEbookTypeEPUB 2

@implementation PMBuildPane
- (id)initWithPyRef:(PyObject *)aPyRef
{
    PyBuildPane *m = [[PyBuildPane alloc] initWithModel:aPyRef];
    self = [self initWithModel:m];
    [NSBundle loadNibNamed:@"BuildPane" owner:self];
    [self setView:wholeView];
    [m bindCallback:createCallback(@"GUIObjectView", self)];
    [m release];
    return self;
}

- (PyBuildPane *)model
{
    return (PyBuildPane *)model;
}

- (IBAction)generateMarkdown:(id)sender
{
    [[self model] generateMarkdown];
}

- (IBAction)editMarkdown:(id)sender
{
    [[self model] editMarkdown];
}

- (IBAction)revealInFinder:(id)sender
{
    [[self model] revealMarkdown];
}

- (IBAction)viewHTML:(id)sender
{
    [[self model] viewHTML];
}

- (IBAction)createEbook:(id)sender
{
    [[self model] setEbookTitle:[ebookTitleTextField stringValue]];
    [[self model] setEbookAuthor:[ebookAuthorTextField stringValue]];
    NSSavePanel *sp = [NSSavePanel savePanel];
    [sp setTitle:@"Select a destination for the e-book"];
    NSString *ext;
    if ([[self model] selectedEbookType] == PMEbookTypeEPUB) {
        ext = @"epub";
    }
    else {
        ext = @"mobi";
    }
    [sp setAllowedFileTypes:[NSArray arrayWithObject:ext]];
    [sp setAllowsOtherFileTypes:YES];
    if ([sp runModal] == NSOKButton) {
        NSString *filename = [[sp URL] path];
        [[self model] createEbookAtPath:filename];
    }
}

- (IBAction)selectEbookType:(id)sender
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