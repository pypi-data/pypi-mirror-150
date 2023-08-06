# standard import
import re


re_name = r'^[a-zA-Z_\.]+$'
re_arg = r'^[a-zA-Z][a-zA-z\-]+$'
re_dest = r'^[a-zA-Z_]+$'

def to_key(v):
    if not re.match(re_name, v):
        raise ValueError('invalid key {}'.format(v))
    return v.upper()


class ArgFlag:

    def __init__(self):
        self.__pure = []
        self.__alias = []
        self.__reverse = {}
        self.__c = 1
        self.__all = 0


    @property
    def all(self):
        return self.__all


    def val(self, v):
        if isinstance(v, int):
            if self.__reverse.get(v) == None:
                raise ValueError('not a valid flag value: {}'.format(v))
            return v
        k = to_key(v)
        return getattr(self, k)


    def add(self, k):
        k = to_key(k)
        if getattr(self, k, False):
            raise ValueError('key exists: {}'.format(k))
        setattr(self, k, self.__c)
        self.__pure.append(k)
        self.__reverse[self.__c] = k
        self.__c <<= 1
        self.__all = self.__c - 1


    def have_all(self, v):
        if v & self.__all != v:
            raise ValueError('missing flag {} in {}'.format(v, self.__all))
        return v


    def match(self, k, v):
        k = to_key(k)
        return getattr(self, k) & v > 0


    def alias(self, k, *args):
        k = to_key(k)
        if getattr(self, k, False):
            raise ValueError('key exists: {}'.format(k))
        r = 0
        for v in args:
            r |= self.val(v)
        r = self.have_all(r)
        setattr(self, k, r)
        self.__alias.append(k)
        self.__reverse[r] = k


    def less(self, k, v):
        try:
            k = to_key(k)
            flags = getattr(self, k)
        except TypeError:
            flags = k
        try:
            vv = to_key(v)
            v = getattr(self, vv)
        except TypeError:
            pass
        mask = ~(self.__all & v)
        r = flags & mask
        return r


    def more(self, k, v):
        try:
            k = to_key(k)
            flags = getattr(self, k)
        except TypeError:
            flags = k
        try:
            vv = to_key(v)
            v = getattr(self, vv)
        except TypeError:
            pass

        return flags | v


    def names(self, flags):
        flags_debug = []
        c = 1
        i = 0
        while c < self.__c:
            if flags & c > 0:
                k = self.__pure[i]
                flags_debug.append(k)
            c <<= 1
            i += 1
        return flags_debug


    def get(self, k):
        k = to_key(k)
        v = getattr(self, k)
        return self.val(v)


class Arg:

    def __init__(self, flags):
        self.__flags = flags
        self.__v = {}
        self.__long = {}
        self.__k = []
        self.__l = []
        self.__dest = {}
        self.__x = {}
        self.__crsr = 0
        self.__typ = {}
        self.__z = 0


    def add(self, k, v, check=True, typ=str, dest=None, **kwargs):
        if len(k) != 1 and check:
            raise ValueError('short flag must have length 1, got "{}"'.format(k))
        v = self.__flags.val(v)
        if self.__v.get(v) == None:
            self.__v[v] = []
        self.__v[v].append(k)
        self.__z |= v
        self.__k.append(k)
        if dest != None:
            if not re.match(re_dest, dest):
                raise ValueError('invalid destination name: {}'.format(dest))
        else:
            dest = k
        self.__dest[k] = dest

        self.__x[k] = kwargs
        self.__typ[k] = typ


    def add_long(self, k, v, typ=str, dest=None, **kwargs):
        v = self.__flags.val(v)
        if self.__v.get(v) == None:
            self.__v[v] = []
        self.__v[v].append(k)
        self.__z |= v
        self.__l.append(k)
        if dest != None:
            if not re.match(re_dest, dest):
                raise ValueError('invalid destination name: {}'.format(dest))
        self.__dest[k] = dest

        self.__x[k] = kwargs
        self.__typ[k] = typ


    def set_long(self, short, long, dest=None):
        if not re.match(re_arg, long):
            raise ValueError('invalid flag name: {}'.format(long))
        if short not in self.__k:
            raise ValueError('unknown short flag: {}'.format(long))
        self.__long[short] = long

        if dest != None:
            if not re.match(re_dest, dest):
                raise ValueError('invalid destination name: {}'.format(dest))
            self.__dest[short] = dest


    def get(self, k):
        k = self.__flags.val(k)
        r = []
        for v in self.__v[k]:
            long = None
            short = None
            if v in self.__l:
                long = '--' + v
            else:
                long = self.__long.get(v)
                if long != None:
                    long = '--' + long
                short = '-' + v
            dest = self.__dest[v]
            typ = self.__typ[v]
            r.append((short, long, dest, typ,))
        return r


    def val(self, k):
        return self.__flags.get(k)


    def match(self, k, v_cmp, negate=False):
        k = to_key(k)
        v = self.__flags.val(k)
        if v == 0:
            return False
        r = 0
        if not negate:
            r = (v & self.__z & v_cmp)
        return r == v


    def __iter__(self):
        self.__crsr = 1
        return self


    def __next__(self):
        while True:
            v = None
            try:
                v = self.__flags.val(self.__crsr)
            except ValueError:
                self.__crsr = 0
            if self.__crsr == 0:
                raise StopIteration()

            v = self.__crsr
            self.__crsr <<= 1
            if self.__v.get(v) != None:
                return v


    def kwargs(self, k):
        return self.__x.get(k, {})


def process_args(argparser, args, flags):
    for flag in args:

        if flag & flags == 0:
            continue

        for (short, long, dest, typ,) in args.get(flag):

            kw = {}
            try:
                kw = args.kwargs(short[1:])
            except TypeError:
                kw = args.kwargs(long[2:])

            if typ == bool:
                kw['action'] = 'store_true'
            else:
                kw['type'] = typ
            kw['dest'] = dest

            if long == None:
                argparser.add_argument(short, **kw)
            elif short == None:
                argparser.add_argument(long, **kw)
            else:
                argparser.add_argument(short, long, **kw)

    return argparser
