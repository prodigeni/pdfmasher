/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "BSD" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/bsd_license
*/

#import "PMPageRepr.h"
#import "Utils.h"

#define PageColorPageBg 1
#define PageColorPageBorder 2
#define PageColorElemNormal 100
#define PageColorElemSelected 101
#define PageColorElemIgnored 102
#define PageColorMouseSelection 200

static NSColor* getColorFromConst(NSInteger c)
{
    if (c == PageColorPageBg) {
        return [NSColor whiteColor];
    }
    else if (c == PageColorPageBorder) {
        return [NSColor blackColor];
    }
    else if (c == PageColorElemNormal) {
        return [NSColor blackColor];
    }
    else if (c == PageColorElemSelected) {
        return [NSColor blueColor];
    }
    else if (c == PageColorElemIgnored) {
        return [NSColor grayColor];
    }
    else if (c == PageColorMouseSelection) {
        return [NSColor blueColor];
    }
    return nil;
}

@implementation PMPageRepr
- (id)initWithPyParent:(id)aPyParent
{
    self = [super init];
    Class pyClass = [Utils classNamed:@"PyPageRepr"];
    py = [[pyClass alloc] initWithCocoa:self pyParent:aPyParent];
    [py connect];
    return self;
}

- (void)drawRect:(NSRect)rect
{
    [py drawWithViewWidth:NSWidth(rect) height:NSHeight(rect)];
}

- (void)mouseDown:(NSEvent *)event
{
    NSPoint windowPos = [event locationInWindow];
    NSPoint pos = [self convertPoint:windowPos fromView:nil];
    [py mouseDownAtX:pos.x y:pos.y];
}

- (void)mouseDragged:(NSEvent *)event
{
    NSPoint windowPos = [event locationInWindow];
    NSPoint pos = [self convertPoint:windowPos fromView:nil];
    [py mouseMoveAtX:pos.x y:pos.y];
}

- (void)mouseUp:(NSEvent *)event
{
    [py mouseUp];
}

/* Public */
- (void)prevPage
{
    [py prevPage];
}

- (void)nextPage
{
    [py nextPage];
}

/* model --> view */
- (void)refresh
{
    [self setNeedsDisplay:YES];
}

- (void)drawRectAtX:(CGFloat)x y:(CGFloat)y width:(CGFloat)width height:(CGFloat)height bgColor:(NSInteger)bgColor penColor:(NSInteger)penColor
{
    NSColor *bg = getColorFromConst(bgColor);
    NSColor *pen = getColorFromConst(penColor);
    NSRect r = NSMakeRect(x, y, width, height);
    NSBezierPath *p = [NSBezierPath bezierPathWithRect:r];
    if (bg != nil) {
        [bg setFill];
        [p fill];
    }
    if (pen != nil) {
        [pen setStroke];
        [p setLineWidth:0.0];
        [p stroke];
    }
}
@end