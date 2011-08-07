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
#define PageColorElemTitle 101
#define PageColorElemFootnote 102
#define PageColorElemIgnored 103
#define PageColorElemToFix 104
#define PageColorElemSelected 105
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
    else if (c == PageColorElemTitle) {
        return [NSColor orangeColor];
    }
    else if (c == PageColorElemFootnote) {
        return [NSColor blackColor];
    }
    else if (c == PageColorElemIgnored) {
        return [NSColor grayColor];
    }
    else if (c == PageColorElemToFix) {
        return [NSColor redColor];
    }
    else if (c == PageColorElemSelected) {
        return [NSColor blueColor];
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
    [[self window] makeFirstResponder:self];
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
    // Just monitoring flagsChanged is not enough because the shift key might have been pressed
    // before our view was first responder.
    BOOL isShiftHeld = ([event modifierFlags] & NSShiftKeyMask) > 0;
    [py setShiftKeyHeld:isShiftHeld];
    [py mouseUp];
}

- (void)flagsChanged:(NSEvent *)event
{
    BOOL isShiftHeld = ([event modifierFlags] & NSShiftKeyMask) > 0;
    [py setShiftKeyHeld:isShiftHeld];
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
    // Define points
    NSPoint pt1 = NSMakePoint(x1, y1);
    NSPoint pt2 = NSMakePoint(x2, y2);
    CGFloat lineAngle = angleFromPoints(pt1, pt2);
    CGFloat arrowsize = MIN(20, distance(pt1, pt2) / 2);
    NSPoint arrowPt1 = pointInCircle(pt2, arrowsize, lineAngle + M_PI + (M_PI / 8));
    NSPoint arrowPt2 = pointInCircle(pt2, arrowsize, lineAngle + M_PI - (M_PI / 8));
    // The drawn line has to actually be a bit shorter than asked because when the width is larger
    // than one, the tip of the arrow is larger than expected. So we shorten the line by half the
    // arrowsize
    NSPoint adjustedPt2 = pointInCircle(pt2, arrowsize/2, lineAngle + M_PI);
    
    // Draw line
    [NSGraphicsContext saveGraphicsState];
    NSColor *color = getColorFromConst(iColor);
    [color setStroke];
    NSBezierPath *p = [NSBezierPath bezierPath];
    [p setLineWidth:width];
    [p moveToPoint:pt1];
    [p lineToPoint:adjustedPt2];
    [p stroke];
    
    // arrowhead
    [color setFill];
    p = [NSBezierPath bezierPath];
    [p moveToPoint:pt2];
    [p lineToPoint:arrowPt1];
    [p lineToPoint:arrowPt2];
    [p fill];
    [NSGraphicsContext restoreGraphicsState];
}

@end