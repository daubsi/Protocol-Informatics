import sys, math

# width defines bar width
# percent defines current percentage
def progress(width, percent):
    marks = math.floor(width * (percent / 100.0))
    spaces = math.floor(width - marks)
 
    loader = '[' + ('=' * int(marks)) + (' ' * int(spaces)) + ']'
 
    sys.stdout.write("%s %d%%\r" % (loader, percent))
    if percent >= 100:
        sys.stdout.write("\n")
    sys.stdout.flush() 


# vim: set sts=4 sw=4 cindent nowrap expandtab:
