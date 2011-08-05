#import <Cocoa/Cocoa.h>
#import "Utils.h"

int main(int argc, char *argv[])
{
    NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];
    [Utils setPluginName:@"pyplugin"];
    [pool release];
    return NSApplicationMain(argc,  (const char **) argv);
}
