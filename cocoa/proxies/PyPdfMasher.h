#import <Cocoa/Cocoa.h>
#import "PyFairware.h"
#import "ProgressController.h"
#import "PyElementTable.h"
#import "PyOpenedFileLabel.h"
#import "PyPageController.h"
#import "PyBuildPane.h"
#import "PyEditPane.h"

@interface PyPdfMasher : PyFairware <Worker> {}
- (void)bindCocoa:(id)cocoa;
- (PyElementTable *)elementTable;
- (PyOpenedFileLabel *)openedFileLabel;
- (PyPageController *)pageController;
- (PyBuildPane *)buildPane;
- (PyEditPane *)editPane;
- (void)changeStateOfSelected:(NSString *)newstate;
- (void)loadPDF:(NSString *)path;
- (BOOL)hideIgnored;
- (void)setHideIgnored:(BOOL)value;
@end