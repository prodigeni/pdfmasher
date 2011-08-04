/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "BSD" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/bsd_license
*/

#import "PMPageRepr.h"
#import "Utils.h"
#import "HSGeometry.h"

// in sync with core.gui.page_repr.PageColor
#define PageColorPageBg 1
#define PageColorPageBorder 2
#define PageColorElemNormal 100
#define PageColorElemSelected 101
#define PageColorElemIgnored 102
#define PageColorElemOrderArrow 200
#define PageColorMouseSelection 300

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
    else if (c == PageColorElemOrderArrow) {
        return [NSColor redColor];
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

- (PyPageRepr *)py
{
    return py;
}

- (BOOL)isFlipped
{
    return YES;
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

/* model --> view */
- (void)refresh
{
    [self setNeedsDisplay:YES];
}

- (void)drawRectAtX:(CGFloat)x y:(CGFloat)y width:(CGFloat)width height:(CGFloat)height bgColor:(NSInteger)bgColor penColor:(NSInteger)penColor
{
    [NSGraphicsContext saveGraphicsState];
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
    [NSGraphicsContext restoreGraphicsState];
}

- (void)drawArrowFromX:(CGFloat)x1 y:(CGFloat)y1 toX:(CGFloat)x2 y:(CGFloat)y2 width:(CGFloat)width color:(NSInteger)iColor
{
    [NSGraphicsContext saveGraphicsState];
    NSColor *color = getColorFromConst(iColor);
    [color setStroke];
    NSBezierPath *p = [NSBezierPath bezierPath];
    [p setLineWidth:width];
    NSPoint pt1 = NSMakePoint(x1, y1);
    NSPoint pt2 = NSMakePoint(x2, y2);
    [p moveToPoint:pt1];
    [p lineToPoint:pt2];
    [p stroke];
    
    // arrowhead
    [color setFill];
    CGFloat lineAngle = angleFromPoints(pt1, pt2);
    CGFloat arrowsize = MIN(20, distance(pt1, pt2) / 2);
    NSPoint arrowPt1 = pointInCircle(pt2, arrowsize, lineAngle + M_PI + (M_PI / 8));
    NSPoint arrowPt2 = pointInCircle(pt2, arrowsize, lineAngle + M_PI - (M_PI / 8));
    p = [NSBezierPath bezierPath];
    [p moveToPoint:pt2];
    [p lineToPoint:arrowPt1];
    [p lineToPoint:arrowPt2];
    [p fill];
    
    [NSGraphicsContext restoreGraphicsState];
}

@end