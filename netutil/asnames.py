import re
import urllib2

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
                asn = m.groups()[0].rstrip().lstrip().replace('AS','')
                # handle weird . notation for > 16-bit ASNs
                if '.' in asn:
                    b, s = asn.split('.')
                    asn = (int(b) << 16) + int(s)
                else:
                    asn = int(asn)
                name = m.groups()[1].rstrip().lstrip()
                yield (asn, name)
