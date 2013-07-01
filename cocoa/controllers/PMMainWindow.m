/* 
Copyright 2013 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/gplv3_license
*/

#import "PMMainWindow.h"
#import "PMMainWindow_UI.h"
#import "ProgressController.h"
#import "Dialogs.h"
#import "PMConst.h"

@implementation PMMainWindow

@synthesize openedFileLabelView;
@synthesize elementsTableView;
@synthesize topTabView;
@synthesize bottomTabView;

- (id)initWithAppDelegate:(PMAppDelegate *)aAppDelegate
{
    self = [super initWithWindow:nil];
    [self setWindow:createPMMainWindow_UI(self)];
    app = (PyPdfMasher *)[aAppDelegate model];
    openedFileLabel = [[HSTextField alloc] initWithPyRef:[app openedFileLabel] view:openedFileLabelView];
    elementTable = [[PMElementTable alloc] initWithPyRef:[app elementTable] tableView:elementsTableView];
    pageController = [[PMPageController alloc] initWithPyRef:[app pageController]];
    editPane = [[PMEditPane alloc] initWithPyParent:app];
    buildPane = [[PMBuildPane alloc] initWithPyRef:[app buildPane]];
    
    NSTabViewItem *item = [[NSTabViewItem alloc] initWithIdentifier:@"edit_pane"];
    [item setLabel:@"Edit"];
    [item setView:[editPane view]];
    [bottomTabView addTabViewItem:item];
    [item release];
    item = [[NSTabViewItem alloc] initWithIdentifier:@"build_pane"];
    [item setLabel:@"Build"];
    [item setView:[buildPane view]];
    [bottomTabView addTabViewItem:item];
    [item release];
    item = [[NSTabViewItem alloc] initWithIdentifier:@"page_pane"];
    [item setLabel:@"Page"];
    [item setView:[pageController view]];
    [topTabView addTabViewItem:item];
    [item release];
    
    return self;
}

- (void)dealloc
{
    [openedFileLabel release];
    [elementTable release];
    [pageController release];
    [editPane release];
    [buildPane release];
    [super dealloc];
}

- (void)loadPDF
{
    [app loadPDF];
}
@end