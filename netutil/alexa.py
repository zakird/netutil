import os
import os.path
import datetime
import csv
import zipfile
import urllib

class AlexTopOneMillion(object):
    """Alex Top 1 million websites fetcher/parser/iterator.
	e.g. usage:
		a = AlexTopOneMillion()
		for rating, website in a:
			print rating, website"""

    TEMP_LOCATION = "/tmp"
    FILE_LOCATION = "http://s3.amazonaws.com/alexa-static/top-1m.csv.zip"

    def __init__(self):
        self._parsed = []

    def __make_download_path(self):
        d = datetime.datetime.now().strftime("%m%d%Y")
        return os.path.join(self.TEMP_LOCATION, '.'.join(("alexa", d, "zip")))

    def __make_expanded_path(self):
        d = datetime.datetime.now().strftime("%m%d%Y")
        return os.path.join(self.TEMP_LOCATION, '.'.join(("alexa", d)))

    def fetch(self):
        if not self._parsed:
            d_path = self.__make_download_path()
            e_path = self.__make_expanded_path()
	    f_path = os.path.join(e_path, "top-1m.csv")
            urllib.urlretrieve(self.FILE_LOCATION, d_path)
            assert os.path.exists(d_path)
	    z = zipfile.ZipFile(d_path)
            z.extract("top-1m.csv", e_path)
            z.close()
            os.remove(d_path)
            assert os.path.exists(e_path)
            with open(f_path, 'r') as fd:
                for r in csv.reader(fd):
                    self._parsed.append((int(r[0].rstrip()), r[1].rstrip()))
            os.remove(f_path)
	    os.rmdir(e_path)
            # sort by alexa rating
            self._parsed.sort(key=lambda x: x[0])

    def __iter__(self):
        """iterate over sorted tuples (rating, website) in the alexa top 1million list"""
        self.fetch()
        for r in self._parsed:
            yield r


def main():
    a = AlexTopOneMillion()
    for r in a:
        print r

if __name__ == "__main__":
    main()
