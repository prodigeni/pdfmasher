/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "BSD" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/bsd_license
*/

#import <Cocoa/Cocoa.h>
#import "PMEditPane.h"
#import "PMBuildPane.h"
#import "PMOpenedFileLabel.h"
#import "PMElementTable.h"
#import "PMPageRepr.h"
#import "PMAppDelegate.h"

@interface PMMainWindow : NSWindowController
{
    IBOutlet NSTextField *openedFileLabelView;
    IBOutlet NSTableView *elementsTableView;
    IBOutlet NSView *pageReprPlaceholder;
    IBOutlet NSTabView *tabView;
    IBOutlet PMAppDelegate *appDelegate;
    
    PyPdfMasher *app;
    PMOpenedFileLabel *openedFileLabel;
    PMElementTable *elementTable;
    PMPageRepr *pageRepr;
    PMEditPane *editPane;
    PMBuildPane *buildPane;
}

- (IBAction)loadPDF:(id)sender;
- (IBAction)prevPage:(id)sender;
- (IBAction)nextPage:(id)sender;
@end