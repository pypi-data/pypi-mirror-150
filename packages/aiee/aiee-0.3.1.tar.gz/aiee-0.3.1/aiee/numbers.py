# standard imports
import re
import logging

logg = logging.getLogger(__name__)


re_number_postfix = r'^(\d+(\.\d+)?)(([kmgtpezyE])(-?\d+)?)?$'
def postfix_to_int(s):
    s = s.replace(' ', '')
    m = re.match(re_number_postfix, s)
    if not m:
        raise ValueError('invalid postfix expansion value: {}'.format(s))
    v = 0
    d = 0
    p = 0
    if m[2] == None:
        v = int(m[1])
    else:
        (n, f) = m[1].split('.')
        if int(f) == 0:
            v = int(n)
        else:
            p -= len(f)
            v = int(n + f)

    if m[4] == 'k':
        p += 3
    elif m[4] == 'm':
        p += 6
    elif m[4] == 'g':
        p += 9
    elif m[4] == 't':
        p += 12
    elif m[4] == 'p':
        p += 15
    elif m[4] == 'e':
        p += 18
    elif m[4] == 'z':
        p += 21
    elif m[4] == 'y':
        p += 24
    elif m[4] == 'E':
        p += int(m[5])

    r = int(v * (10 ** p))
    logg.debug('number {} translated to {}'.format(s, r))

    return r
