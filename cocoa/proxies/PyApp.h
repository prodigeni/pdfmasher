#import <Cocoa/Cocoa.h>
#import "PyFairware.h"
#import "ProgressController.h"

@interface PyApp : PyFairware <Worker> {}
- (NSString *)buildHtml;
- (void)changeStateOfSelected:(NSString *)newstate;
- (void)openFile:(NSString *)path;
- (BOOL)hideIgnored;
- (void)setHideIgnored:(BOOL)value;
@end