/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/gplv3_license
*/

#import <Cocoa/Cocoa.h>
#import "HSAboutBox.h"
#import "PyPdfMasher.h"

@interface PMAppDelegate : NSObject
{
    PyPdfMasher *py;
    HSAboutBox *aboutBox;
}

- (PyPdfMasher *)py;

- (IBAction)openWebsite:(id)sender;
- (IBAction)openHelp:(id)sender;
- (IBAction)showAboutBox:(id)sender;
@end