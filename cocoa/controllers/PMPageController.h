/* 
Copyright 2013 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/gplv3_license
*/

#import <Cocoa/Cocoa.h>

#import "HSGUIController.h"
#import "PMPageRepr.h"
#import "PyPageController.h"

@interface PMPageController : HSGUIController
{
    NSView *pageReprPlaceholder;
    NSTextField *pageLabelTextField;
    NSButton *reorderModeButton;
    
    PMPageRepr *pageRepr;
}

@property (readwrite, retain) NSView *pageReprPlaceholder;
@property (readwrite, retain) NSTextField *pageLabelTextField;
@property (readwrite, retain) NSButton *reorderModeButton;

- (id)initWithPyRef:(PyObject *)aPyRef;
- (PyPageController *)model;

- (void)prevPage;
- (void)nextPage;
- (void)toggleShowOrder;
@end