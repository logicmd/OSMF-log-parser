import time, re
def parse(s):

    t = time.strptime(s, '%a %b %d %Y %I:%M:%S %p.%f')
    reg = re.compile('\.\\d{3}')
    if (reg.search(s)):
        ms = float(reg.search(s).group(0))
    else:
        raise('invalid time format')

    #print ms
    #print time.mktime(t)
    #print "%.3f" % (ms + time.mktime(t))
    return ms + time.mktime(t)


if __name__ == "__main__":
    print parse('Thu Sep 27 2012 10:41:09 AM.066')
    print parse('Fri Oct 5 2012 07:57:59 PM.404')