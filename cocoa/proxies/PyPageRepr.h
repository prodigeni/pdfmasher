#import <Cocoa/Cocoa.h>
#import "PyGUI.h"

@interface PyPageRepr : PyGUI {}
- (void)drawWithViewWidth:(CGFloat)view_height height:(CGFloat)view_height;
- (void)mouseDownAtX:(CGFloat)x y:(CGFloat)y;
- (void)mouseMoveAtX:(CGFloat)x y:(CGFloat)y;
- (void)mouseUp;
- (void)prevPage;
- (void)nextPage;
@end