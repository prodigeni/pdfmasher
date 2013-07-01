/* 
Copyright 2013 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/gplv3_license
*/

#import "PMAppDelegate.h"
#import "Utils.h"
#import "HSPyUtil.h"
#import "Dialogs.h"
#import "ProgressController.h"

@implementation PMAppDelegate

@synthesize model;
@synthesize updater;
@synthesize mainWindow;

- (id)init
{
    self = [super init];
    
    [self setModel:[[[PyPdfMasher alloc] init] autorelease]];
    [[self model] bindCallback:createCallback(@"PdfMasherView", self)];
    progressWindow = [[HSProgressWindow alloc] initWithPyRef:[[self model] progressWindow] view:nil];
    [self setUpdater:[[[SUUpdater alloc] init] autorelease]];
    [self setMainWindow:[[[PMMainWindow alloc] initWithAppDelegate:self] autorelease]];
    aboutBox = nil; // Lazily loaded
    
    return self;
}

- (void)dealloc
{
    [aboutBox release];
    [progressWindow release];
    [super dealloc];
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

/* Python --> Cocoa */
- (void)showMessage:(NSString *)msg
{
    [Dialogs showMessage:msg];
}

- (NSString *)queryLoadPathWithPrompt:(NSString *)prompt
{
    NSOpenPanel *op = [NSOpenPanel openPanel];
    [op setCanChooseFiles:YES];
    [op setCanChooseDirectories:NO];
    [op setCanCreateDirectories:NO];
    [op setAllowsMultipleSelection:NO];
    [op setTitle:prompt];
    if ([op runModal] == NSOKButton) {
        return [[op filenames] objectAtIndex:0];
    }
    else {
        return nil;
    }
}

- (NSString *)querySavePathWithPrompt:(NSString *)prompt allowedExts:(NSArray *)allowedExts
{
    NSSavePanel *sp = [NSSavePanel savePanel];
    [sp setTitle:prompt];
    [sp setAllowedFileTypes:allowedExts];
    [sp setAllowsOtherFileTypes:YES];
    if ([sp runModal] == NSOKButton) {
        return [[sp URL] path];
    }
    else {
        return nil;
    }
}
@end
