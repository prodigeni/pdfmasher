/* 
Copyright 2013 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/gplv3_license
*/

#import <Cocoa/Cocoa.h>

#import "HSGUIController.h"
#import "PyPdfMasher.h"
#import "PyEditPane.h"

@interface PMEditPane : HSGUIController
{
    NSButton *hideIgnoredButton;
    NSTextView *editTextView;
    NSButton *saveButton;
    NSButton *cancelButton;
    
    PyPdfMasher *app;
}

@property (readwrite, retain) NSButton *hideIgnoredButton;
@property (readwrite, retain) NSTextView *editTextView;
@property (readwrite, retain) NSButton *saveButton;
@property (readwrite, retain) NSButton *cancelButton;

- (id)initWithPyParent:(id)aPyParent;
- (PyEditPane *)model;

- (void)selectNormal;
- (void)selectTitle;
- (void)selectFootnote;
- (void)selectToFix;
- (void)selectIgnored;
- (void)toggleHideIgnored;
- (void)saveEdits;
- (void)cancelEdits;
@end