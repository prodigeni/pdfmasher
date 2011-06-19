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
#import "PyApp.h"

@interface PMMainWindow : NSWindowController
{
    IBOutlet NSTextField *openedFileLabelView;
    IBOutlet NSTableView *elementsTableView;
    IBOutlet NSTabView *tabView;
    
    PyApp *app;
    PMOpenedFileLabel *openedFileLabel;
    PMElementTable *elementTable;
    PMEditPane *editPane;
    PMBuildPane *buildPane;
}

- (IBAction)openFile:(id)sender;
@end