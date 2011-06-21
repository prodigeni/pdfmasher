#import <Cocoa/Cocoa.h>
#import "PyFairware.h"

@interface PyApp : PyFairware {}
- (NSString *)buildHtml;
- (void)changeStateOfSelected:(NSString *)newstate;
- (void)openFile:(NSString *)path;
- (BOOL)hideIgnored;
- (void)setHideIgnored:(BOOL)value;
@end