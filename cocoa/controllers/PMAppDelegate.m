/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/gplv3_license
*/

#import "PMAppDelegate.h"
#import "Utils.h"
#import "HSFairwareReminder.h"
#import "ProgressController.h"

@implementation PMAppDelegate
- (void)awakeFromNib
{
    // py has to be initialized "lazily" because awakeFromNib's order is undefined, so PMAppDelegate
    // might be awoken after PMMainWindow, and PMMainWindow needs PyPdfMasher on its own awakeFromNib.
    // However, we cannot initialize it to nil here because we might overwrite an already initialized
    // PyPdfMasher.
    aboutBox = nil; // Lazily loaded
}

- (void)dealloc
{
    [aboutBox release];
    [py release];
    [super dealloc];
}

- (PyPdfMasher *)py {
    if (py == nil) {
        Class PyPdfMasher = [Utils classNamed:@"PyPdfMasher"];
        py = [[PyPdfMasher alloc] init];
        [[ProgressController mainProgressController] setWorker:py];
    }
    return py;
}

- (IBAction)openWebsite:(id)sender
{
    [[NSWorkspace sharedWorkspace] openURL:[NSURL URLWithString:@"http://www.hardcoded.net/pdfmasher/"]];
}

- (IBAction)openHelp:(id)sender
{
    NSBundle *b = [NSBundle mainBundle];
    NSString *p = [b pathForResource:@"index" ofType:@"html" inDirectory:@"help"];
    NSURL *u = [NSURL fileURLWithPath:p];
    [[NSWorkspace sharedWorkspace] openURL:u];
}

- (IBAction)showAboutBox:(id)sender
{
    if (aboutBox == nil) {
        aboutBox = [[HSAboutBox alloc] initWithApp:py];
    }
    [[aboutBox window] makeKeyAndOrderFront:sender];
}

/* Delegate */
- (void)applicationDidFinishLaunching:(NSNotification *)aNotification
{
    [HSFairwareReminder showNagWithApp:[self py]];
}
@end