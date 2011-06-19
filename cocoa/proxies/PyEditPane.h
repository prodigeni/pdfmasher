#import <Cocoa/Cocoa.h>
#import "PyGUI.h"

@interface PyEditPane : PyGUI {}
- (NSString *)editText;
- (void)setEditText:(NSString *)value;
- (BOOL)editEnabled;
- (void)saveEdits;
- (void)cancelEdits;
@end