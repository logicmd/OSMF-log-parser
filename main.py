import time_parser, msg_parser, re
FILE = 'sample.log'


def parse(l, add_bw_metric=False):
    if l[0] == '[':
        return

    re_time = re.compile(\
        '\\w{3} \\w{3} (\\d{2}|\\d{1}) \\d{4} ' +
        '(([01]\\d)|(2[0-3])):[0-5]\\d(:[0-5]\\d) ' +
        '\\w{2}\.\\d{3}')

    m = re_time.search(l)
    if m:
        str_time = m.group(0)
        t = time_parser.parse(str_time)
        #print '%.4f' % t
    else:
        print l
        print 'date and time pattern not match'

    re_ex_msg = re.compile(' \\[\\w+\\] \\[.+\\] ')
    m = re_ex_msg.search(l)
    if m:
        str_package = m.group(0)
        str_msg = l.replace(str_time, '').replace(str_package, '')
        if msg_parser.parse(str_msg, add_bw_metric) != None:
            return [t] + msg_parser.parse(str_msg, add_bw_metric)
    else:
        print 'level and package not match'

def read(file_name, bw_metric=True):
    f = open(file_name, 'r')
    result = []
    for line in f:
        if parse(line, bw_metric):
            result.append(parse(line, bw_metric))  # result += [parse(line)]

    return result

    #line=f.readline()

def write(li):
    category = [[], [], [], [], []]
    for ele in li:
        category[ele[1] - 1].append(ele)

    file_name = {
        1: 'downloader',
        2: 'buffer',
        3: 'quality',
        4: 'f4f_quality',
        5: 'bandwidth'
    }

    cat_num = 0
    for cat in category:
        fn = 'output\out_' + file_name[cat_num + 1] + '.txt'
        f = open(fn, 'w')
        for ca in cat:
            for c in ca:
                f.write(str(c) + ' ')
            f.write('\n')
        f.close()
        cat_num += 1


if __name__ == "__main__":
    #time_parser.parse('10:35:15 AM.888')
    result_ = read(FILE)
    write(result_)
