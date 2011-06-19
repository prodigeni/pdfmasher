/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "BSD" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/bsd_license
*/

#import "PMMainWindow.h"
#import "Utils.h"

@implementation PMMainWindow
- (void)awakeFromNib
{
    [self window];
    Class PyApp = [Utils classNamed:@"PyApp"];
    app = [[PyApp alloc] init];
    openedFileLabel = [[PMOpenedFileLabel alloc] initWithPyParent:app view:openedFileLabelView];
    elementTable = [[PMElementTable alloc] initWithPyParent:app view:elementsTableView];
    editPane = [[PMEditPane alloc] initWithPyParent:app];
    buildPane = [[PMBuildPane alloc] initWithPyParent:app];
    
    NSTabViewItem *item = [[NSTabViewItem alloc] initWithIdentifier:@"edit_pane"];
    [item setLabel:@"Edit"];
    [item setView:[editPane view]];
    [tabView addTabViewItem:item];
    [item release];
    item = [[NSTabViewItem alloc] initWithIdentifier:@"build_pane"];
    [item setLabel:@"Build"];
    [item setView:[buildPane view]];
    [tabView addTabViewItem:item];
    [item release];
}

- (void)dealloc
{
    [openedFileLabel release];
    [elementTable release];
    [editPane release];
    [buildPane release];
    [app release];
    [super dealloc];
}

- (IBAction)openFile:(id)sender
{
    NSOpenPanel *op = [NSOpenPanel openPanel];
    [op setCanChooseFiles:YES];
    [op setCanChooseDirectories:NO];
    [op setCanCreateDirectories:NO];
    [op setAllowsMultipleSelection:NO];
    [op setTitle:@"Select a PDF to work with"];
    if ([op runModal] == NSOKButton) {
        NSString *filename = [[op filenames] objectAtIndex:0];
        [app openFile:filename];
    }
}
@end