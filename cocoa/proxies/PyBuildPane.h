#import <Cocoa/Cocoa.h>
#import "PyGUI.h"

@interface PyBuildPane : PyGUI {}
- (NSString *)lastGenDesc;
- (BOOL)postProcessingEnabled;

- (NSInteger)selectedEbookType;
- (void)setSelectedEbookType:(NSInteger)type;

- (void)generateMarkdown;
- (void)editMarkdown;
- (void)revealMarkdown;
- (void)viewHTML;
- (void)createEbookAtPath:(NSString *)path;
@end