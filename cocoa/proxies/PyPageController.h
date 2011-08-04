#import <Cocoa/Cocoa.h>
#import "PyGUI.h"

@interface PyPageController : PyGUI {}
- (void)setChildren:(NSArray *)children;
- (void)prevPage;
- (void)nextPage;
- (NSString *)pageLabel;
- (void)setShowOrder:(BOOL)flag;
@end