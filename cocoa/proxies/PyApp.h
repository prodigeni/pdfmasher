#import <Cocoa/Cocoa.h>

@interface PyApp : NSObject {}
- (NSString *)buildHtml;
- (void)changeStateOfSelected:(NSString *)newstate;
- (void)openFile:(NSString *)path;
- (BOOL)hideIgnored;
- (void)setHideIgnored:(BOOL)value;
@end