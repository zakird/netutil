import re
import csv
import urllib2
import os.path
import ip4

class BGPRecord(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

class BGPDump(object):
    def __init__(self, path):
        assert os.path.exists(path)
        self.__path = path

    def __parse_path(self, path):
        return map(lambda i: int(i), path.split(' ')[:-1])

    def __fileiter(self):
        r = re.compile("\s+")
        with open(self.__path) as fd:
            for l in fd:
                if l.startswith('*>i'):
                    yield re.split(r, l.rstrip())

    def __iter__(self):
        for r in self.__fileiter():
            network = r[0].lstrip('*>i')
            if '/' not in network:
                continue
            print r
            path = self.__parse_path(r[5]),
            yield BGPRecord(
                network = network,
                begin_addr = ip4.get_bounds_from_cidr(network)[0],
                end_addr = ip4.get_bounds_from_cidr(network)[1],
                next_hop = r[1],
                metric = r[2],
                loc_prf = int(r[3]),
                weight = int(r[4]),
                path = path,
                origin_asn = path[-1],
            )


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

if __name__ == '__main__':
    x = BGPDump('/Users/zakir/Dropbox/hubble/bgp-table')
    for r in x:
        print r
