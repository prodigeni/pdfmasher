/* 
Copyright 2013 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/gplv3_license
*/

#import <Cocoa/Cocoa.h>
#import "PyPdfMasher.h"
#import "PMEditPane.h"
#import "PMBuildPane.h"
#import "HSTextField.h"
#import "PMElementTable.h"
#import "PMPageController.h"
#import "PMElementTableView.h"

@class PMAppDelegate;

@interface PMMainWindow : NSWindowController
{
    NSTextField *openedFileLabelView;
    PMElementTableView *elementsTableView;
    NSTabView *topTabView;
    NSTabView *bottomTabView;
    
    PyPdfMasher *app;
    HSTextField *openedFileLabel;
    PMElementTable *elementTable;
    PMPageController *pageController;
    PMEditPane *editPane;
    PMBuildPane *buildPane;
}

@property (readwrite, retain) NSTextField *openedFileLabelView;
@property (readwrite, retain) PMElementTableView *elementsTableView;
@property (readwrite, retain) NSTabView *topTabView;
@property (readwrite, retain) NSTabView *bottomTabView;

- (id)initWithAppDelegate:(PMAppDelegate *)aAppDelegate;
- (void)loadPDF;
@end