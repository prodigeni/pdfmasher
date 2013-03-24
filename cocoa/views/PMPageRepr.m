/* 
Copyright 2013 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/gplv3_license
*/

#import "PMPageRepr.h"
#import "HSPyUtil.h"
#import "HSGeometry.h"
#import "NSEventAdditions.h"

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
- (id)initWithPyRef:(PyObject *)aPyRef
{
    self = [super init];
    model = [[PyPageRepr alloc] initWithModel:aPyRef];
    [model bindCallback:createCallback(@"PageReprView", self)];
    return self;
}

- (PyPageRepr *)model
{
    return model;
}

- (BOOL)isFlipped
{
    return YES;
}

- (void)drawRect:(NSRect)rect
{
    [model drawWithViewWidth:NSWidth(rect) height:NSHeight(rect)];
}

- (void)mouseDown:(NSEvent *)event
{
    [[self window] makeFirstResponder:self];
    NSPoint windowPos = [event locationInWindow];
    NSPoint pos = [self convertPoint:windowPos fromView:nil];
    [model mouseDownAtX:pos.x y:pos.y];
}

- (void)mouseDragged:(NSEvent *)event
{
    NSPoint windowPos = [event locationInWindow];
    NSPoint pos = [self convertPoint:windowPos fromView:nil];
    [model mouseMoveAtX:pos.x y:pos.y];
}

- (void)mouseUp:(NSEvent *)event
{
    // Just monitoring flagsChanged is not enough because the shift key might have been pressed
    // before our view was first responder.
    BOOL isShiftHeld = ([event modifierFlags] & NSShiftKeyMask) > 0;
    [model setShiftKeyHeld:isShiftHeld];
    [model mouseUp];
}

- (void)flagsChanged:(NSEvent *)event
{
    BOOL isShiftHeld = ([event modifierFlags] & NSShiftKeyMask) > 0;
    [model setShiftKeyHeld:isShiftHeld];
}

- (void)keyDown:(NSEvent *)event 
{
    if ([event modifierKeysFlags] == 0) { // No modif flag
        NSString *s = [event characters];
        NSSet *acceptableFlagKeys = [NSSet setWithObjects:@"n", @"t", @"f", @"x", @"i", nil];
        if ([acceptableFlagKeys containsObject:s]) {
            [model pressKey:s];
        }
    }
}

/* model --> view */
- (void)refresh
{
    [self setNeedsDisplay:YES];
}

- (void)drawRect:(NSRect)rect bgColor:(NSInteger)bgColor penColor:(NSInteger)penColor
{
    [NSGraphicsContext saveGraphicsState];
    NSColor *bg = getColorFromConst(bgColor);
    NSColor *pen = getColorFromConst(penColor);
    NSBezierPath *p = [NSBezierPath bezierPathWithRect:rect];
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

- (void)drawArrowFrom:(NSPoint)src to:(NSPoint)dst width:(CGFloat)width color:(NSInteger)iColor
{
    // Define points
    CGFloat lineAngle = angleFromPoints(src, dst);
    CGFloat arrowsize = MIN(20, distance(src, dst) / 2);
    NSPoint arrowPt1 = pointInCircle(dst, arrowsize, lineAngle + M_PI + (M_PI / 8));
    NSPoint arrowPt2 = pointInCircle(dst, arrowsize, lineAngle + M_PI - (M_PI / 8));
    // The drawn line has to actually be a bit shorter than asked because when the width is larger
    // than one, the tip of the arrow is larger than expected. So we shorten the line by half the
    // arrowsize
    NSPoint adjustedPt2 = pointInCircle(dst, arrowsize/2, lineAngle + M_PI);
    
    // Draw line
    [NSGraphicsContext saveGraphicsState];
    NSColor *color = getColorFromConst(iColor);
    [color setStroke];
    NSBezierPath *p = [NSBezierPath bezierPath];
    [p setLineWidth:width];
    [p moveToPoint:src];
    [p lineToPoint:adjustedPt2];
    [p stroke];
    
    // arrowhead
    [color setFill];
    p = [NSBezierPath bezierPath];
    [p moveToPoint:dst];
    [p lineToPoint:arrowPt1];
    [p lineToPoint:arrowPt2];
    [p fill];
    [NSGraphicsContext restoreGraphicsState];
}

- (void)drawText:(NSString *)text inRect:(NSRect)rect
{
    [NSGraphicsContext saveGraphicsState];
    NSFont *font = [NSFont labelFontOfSize:11];
    NSMutableParagraphStyle *pstyle = [[[NSMutableParagraphStyle alloc] init] autorelease];
	[pstyle setAlignment:NSCenterTextAlignment ];
    NSDictionary *attr = [NSDictionary dictionaryWithObjectsAndKeys:
        font, NSFontAttributeName,
        [NSColor blackColor], NSForegroundColorAttributeName,
        pstyle, NSParagraphStyleAttributeName,
        nil];
    [text drawInRect:rect withAttributes:attr];
    [NSGraphicsContext restoreGraphicsState];
}

@end