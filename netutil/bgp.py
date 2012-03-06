import re
import csv
import urllib2
import os.path
import ip4

class BGPRecord(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
        if self.prefix_length is None:
            self.prefix_length = ip4.guess_prefix_length(self.prefix)

    def __str__(self):
        return '<BGPRecord (%s/%s)>' % (self.prefix, self.prefix_length)

    def __get_begin_address(self):
        return ip4.str_to_int(self.prefix)
    begin_address = property(__get_begin_address)

    def __get_begin_address_str(self):
        return self.prefix
    begin_address_str = property(__get_begin_address_str)

    def __get_end_address(self):
        print ip4.get_bounds_from_cidr(self.prefix, self.prefix_length)
        return ip4.get_bounds_from_cidr(self.prefix, self.prefix_length)[1]
    end_address = property(__get_end_address)

    def __get_end_address_str(self):
        return ip4.int_to_str(self.end_address)
    end_address_str = property(__get_end_address_str)


class BGPDump(object):
    re_bgp_record = re.compile("^\*>i((?:\d{1,3}\.){3}\d{1,3})(?:/(\d{1,2}))?\s+((?:\d{1,3}\.){3}\d{1,3})\s+(\d+)\s+(\d{3})?\s{2,6}(\d{1,5}) ((?:\d{1,6} )*)((?:i|\?)*)")
    re_bgp_split = re.compile("^\*>i((?:\d{1,3}\.){3}\d{1,3})(/\d{1,2})?\s*$")

    def __init__(self, path):
        assert os.path.exists(path)
        self.__path = path

    def __parse_path(self, path):
        return map(lambda i: int(i), path.split(' ')[:-1])

    def __gen_bgpobj(self, rem):
        assert rem
        n, m, hop, met, lcprf, w, p, f = rem.groups()
        path = p.rstrip().split(' ') if p else []
        options = f.split(' ') if f else []
        return BGPRecord(
            prefix = n,
            prefix_length = m,
            next_hop_str = n,
            next_hop = ip4.str_to_int(n),
            metric = met,
            loc_prf = lcprf,
            weight = w,
            path = path,
            origin_asn = path[-1] if path else None
        )

    def __iter__(self):
        with open(self.__path) as fd:
            prev = None
            for r in fd:
                print r.rstrip()
                if r.startswith('*>') or prev:
                    if self.re_bgp_split.match(r):
                        prev = r
                        continue
                    elif prev:
                        r = prev.rstrip() + ' ' + r
                        prev = None
                    yield self.__gen_bgpobj(self.re_bgp_record.match(r))


class CIDRReportASNameDump(object):
    """ASNNameDump represents the full list of
    registered AS Numbers on CIDR report. Acts as an iterator that
    will provide tuples: (AS Number, AS Name)"""

    CIDR_REPORT_URL = "http://www.cidr-report.org/as2.0/autnums.html"
    ENTRY_REGEX = re.compile("^<a href.*>(.*)</a>(.*)$")

    def __init__(self):
        self.__f = None

    def fetch(self):
        if not self.__f:
            self.__f = urllib2.urlopen(self.CIDR_REPORT_URL)

    def __iter__(self):
        self.fetch()
        for line in self.__f.readlines():
            m = self.ENTRY_REGEX.match(line)
            if m:
                yield (m.groups[1], m.groups[2])

