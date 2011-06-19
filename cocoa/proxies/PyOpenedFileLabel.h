#import <Cocoa/Cocoa.h>
#import "PyGUI.h"

@interface PyOpenedFileLabel : PyGUI {}
- (NSString *)text;
- (void)setText:(NSString *)value;
@end