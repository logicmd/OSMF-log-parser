import re

re_begin = re.compile('download begin \\d+')
re_end = re.compile('Loading complete\\. .+ sec \\d+ bytes')
re_buffer = re.compile('buffer = .+, bufferTime = .+')
re_play_quality = re.compile('swicth to index \\d')
re_quality = re.compile('quality=\\d+')
re_bw = re.compile('Bandwidth .+ kbps')
re_newone = re.compile("(\\{\\{\\{\\{\\{\\}\\}\\}\\}\\})|(QoSInfo)|(Ideal bitrate)|(=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=)")

def parse(s, add_bw_metric=False):

    if re_begin.search(s):
        return begin_parse(re_begin.search(s).group(0))
    elif re_end.search(s):
        return end_parse(re_end.search(s).group(0))
    elif re_buffer.search(s):
        return buffer_parse(re_buffer.search(s).group(0))
    elif re_play_quality.search(s):
        return switch_parse(re_play_quality.search(s).group(0))
    elif re_quality.search(s):
        return f4fhandler_parse(re_quality.search(s).group(0))
    elif add_bw_metric and re_bw.search(s):
        return bw_parse(re_bw.search(s).group(0))
    elif re_newone.search(s):
        pass
    else:
        print s
        raise('invalid message format')


def begin_parse(s):
    bitrate = int(s.replace('download begin ', ''))
    result = {
        0: 0,
        1: 1,
        2: 2,
        3: 3,
        4: 4
    }[bitrate]
    return [1, 0, result, 0]

def end_parse(s):
    re_ = re.compile('Loading complete\\. .+ sec')
    if re_.search(s):
        # when replacing, strip the \\
        time = float(re_.search(s).group(0).replace('Loading complete. ', '')\
            .replace(' sec', ''))
    else:
        raise ('invalid downloading completed')

    re__ = re.compile('sec \\d+ bytes')
    if re__.search(s):
        size = float(re__.search(s).group(0).replace('sec ', '')\
            .replace(' bytes', ''))
    else:
        raise ('invalid downloading size')
    if time == 0:
        time_ = time + 0.0005
        flag = 1
    else:
        time_ = time
        flag = 0

    throughput = size/time_/1024
    return [1, 1, time, size]

def buffer_parse(s):
    s = s.split(',')
    buffer_ = float(s[0].replace('buffer = ', ''))
    buffer_time = float(s[1].replace('bufferTime = ', ''))
    return [2, buffer_, buffer_time]

def switch_parse(s):
    index = int(s.replace('swicth to index ', ''))
    return [3, index]

def f4fhandler_parse(s):
    index = int(s.replace('quality=', ''))
    return [4, index]

def bw_parse(s):
    bw = float(s.replace('Bandwidth ', '').replace(' kbps', ''))
    return [5, bw]

if __name__ == "__main__":
    print parse('download begin 0')
    print parse('download begin 2')
    print parse('Loading complete. 0.001 sec 458792 bytes.')
    print parse('Loading complete. 0.013 sec 418063 bytes.')
    print parse('buffer = 5.114, bufferTime = 4')
    print parse('swicth to index 2')
    print parse('Bandwidth 2421 kbps', True)
    print parse('Bandwidth 3882.211 kbps', True)
    print parse('[[[[[]]]]] size =  252554')
