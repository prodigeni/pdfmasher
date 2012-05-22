/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/gplv3_license
*/

#import <Cocoa/Cocoa.h>
#import "PMEditPane.h"
#import "PMBuildPane.h"
#import "HSTextField.h"
#import "PMElementTable.h"
#import "PMPageController.h"
#import "PMAppDelegate.h"
#import "PMElementTableView.h"

@interface PMMainWindow : NSWindowController
{
    IBOutlet NSTextField *openedFileLabelView;
    IBOutlet PMElementTableView *elementsTableView;
    IBOutlet NSTabView *topTabView;
    IBOutlet NSTabView *bottomTabView;
    IBOutlet PMAppDelegate *appDelegate;
    
    PyPdfMasher *app;
    HSTextField *openedFileLabel;
    PMElementTable *elementTable;
    PMPageController *pageController;
    PMEditPane *editPane;
    PMBuildPane *buildPane;
}

- (IBAction)loadPDF:(id)sender;
@end