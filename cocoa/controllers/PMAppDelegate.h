/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/gplv3_license
*/

#import <Cocoa/Cocoa.h>
#import <Sparkle/SUUpdater.h>
#import "HSAboutBox.h"
#import "PyPdfMasher.h"

@interface PMAppDelegate : NSObject
{
    IBOutlet SUUpdater *updater;
    IBOutlet id mainWindow;
    PyPdfMasher *model;
    HSAboutBox *aboutBox;
}

@property (readwrite, retain) SUUpdater *updater;
@property (readwrite, retain) id mainWindow;

- (PyPdfMasher *)model;

- (void)openWebsite;
- (void)openHelp;
- (void)showAboutBox;
@end