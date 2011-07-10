#import <Cocoa/Cocoa.h>
#import "PyGUI.h"

@interface PyBuildPane : PyGUI {}
- (NSString *)lastGenDesc;
- (BOOL)postProcessingEnabled;

- (void)generateMarkdown;
- (void)editMarkdown;
- (void)revealMarkdown;
- (void)viewHTML;
@end