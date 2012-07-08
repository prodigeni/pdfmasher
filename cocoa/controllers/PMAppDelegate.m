/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/gplv3_license
*/

#import "PMAppDelegate.h"
#import "Utils.h"
#import "HSPyUtil.h"
#import "Dialogs.h"
#import "HSFairwareReminder.h"
#import "ProgressController.h"
#import "PMMainMenu_UI.h"

@implementation PMAppDelegate

@synthesize updater;
@synthesize mainWindow;

- (void)awakeFromNib
{
    [NSApp setMainMenu:createPMMainMenu_UI(self)];
    // py has to be initialized "lazily" because awakeFromNib's order is undefined, so PMAppDelegate
    // might be awoken after PMMainWindow, and PMMainWindow needs PyPdfMasher on its own awakeFromNib.
    // However, we cannot initialize it to nil here because we might overwrite an already initialized
    // PyPdfMasher.
    aboutBox = nil; // Lazily loaded
}

- (void)dealloc
{
    [aboutBox release];
    [model release];
    [super dealloc];
}

- (PyPdfMasher *)model {
    if (model == nil) {
        model = [[PyPdfMasher alloc] init];
        [model bindCallback:createCallback(@"FairwareView", self)];
        [[ProgressController mainProgressController] setWorker:model];
    }
    return model;
}

- (void)openWebsite
{
    [[NSWorkspace sharedWorkspace] openURL:[NSURL URLWithString:@"http://www.hardcoded.net/pdfmasher/"]];
}

- (void)openHelp
{
    NSBundle *b = [NSBundle mainBundle];
    NSString *p = [b pathForResource:@"index" ofType:@"html" inDirectory:@"help"];
    NSURL *u = [NSURL fileURLWithPath:p];
    [[NSWorkspace sharedWorkspace] openURL:u];
}

- (void)showAboutBox
{
    if (aboutBox == nil) {
        aboutBox = [[HSAboutBox alloc] initWithApp:model];
    }
    [[aboutBox window] makeKeyAndOrderFront:nil];
}

/* Delegate */
- (void)applicationDidFinishLaunching:(NSNotification *)aNotification
{
    [[self model] initialRegistrationSetup];
}

/* Python --> Cocoa */
- (void)setupAsRegistered
{
    // Nothing to do.
}

- (void)showMessage:(NSString *)msg
{
    [Dialogs showMessage:msg];
}

- (void)showFairwareNagWithPrompt:(NSString *)prompt
{
    [HSFairwareReminder showFairwareNagWithApp:[self model] prompt:prompt];
}

- (void)showDemoNagWithPrompt:(NSString *)prompt
{
    [HSFairwareReminder showDemoNagWithApp:[self model] prompt:prompt];
}
@end