/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "BSD" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/bsd_license
*/

#import "PMMainWindow.h"
#import "ProgressController.h"
#import "Dialogs.h"
#import "Utils.h"
#import "PMConst.h"

@implementation PMMainWindow
- (void)awakeFromNib
{
    [self window];
    app = [appDelegate py];
    openedFileLabel = [[PMOpenedFileLabel alloc] initWithPyParent:app textView:openedFileLabelView];
    elementTable = [[PMElementTable alloc] initWithPyParent:app tableView:elementsTableView];
    pageRepr = [[PMPageRepr alloc] initWithPyParent:app];
    editPane = [[PMEditPane alloc] initWithPyParent:app];
    buildPane = [[PMBuildPane alloc] initWithPyParent:app];
    
    replacePlaceholderInView(pageReprPlaceholder, pageRepr);
    
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
    
    [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(jobStarted:) name:JobStarted object:nil];
    [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(jobInProgress:) name:JobInProgress object:nil];
}

- (void)dealloc
{
    [openedFileLabel release];
    [elementTable release];
    [editPane release];
    [buildPane release];
    [super dealloc];
}

- (IBAction)loadPDF:(id)sender
{
    NSOpenPanel *op = [NSOpenPanel openPanel];
    [op setCanChooseFiles:YES];
    [op setCanChooseDirectories:NO];
    [op setCanCreateDirectories:NO];
    [op setAllowsMultipleSelection:NO];
    [op setTitle:@"Select a PDF to work with"];
    if ([op runModal] == NSOKButton) {
        NSString *filename = [[op filenames] objectAtIndex:0];
        [app loadPDF:filename];
    }
}

- (IBAction)prevPage:(id)sender
{
    [pageRepr prevPage];
}

- (IBAction)nextPage:(id)sender
{
    [pageRepr nextPage];
}

/* Notifications */
- (void)jobInProgress:(NSNotification *)aNotification
{
    [Dialogs showMessage:@"A previous action is still hanging in there. You can't start a new one yet. Wait a few seconds, then try again."];
}

- (void)jobStarted:(NSNotification *)aNotification
{
    [[self window] makeKeyAndOrderFront:nil];
    NSDictionary *ui = [aNotification userInfo];
    NSString *desc = [ui valueForKey:@"desc"];
    [[ProgressController mainProgressController] setJobDesc:desc];
    NSString *jobid = [ui valueForKey:@"jobid"];
    [[ProgressController mainProgressController] setJobId:jobid];
    [[ProgressController mainProgressController] showSheetForParent:[self window]];
}
@end