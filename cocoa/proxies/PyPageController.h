#import <Cocoa/Cocoa.h>
#import "PyGUI.h"
#import "PyPageRepr.h"

@interface PyPageController : PyGUI {}
- (PyPageRepr *)pageRepr;
- (void)prevPage;
- (void)nextPage;
- (NSString *)pageLabel;
- (void)setReorderMode:(BOOL)flag;
@end