text = '<a href="/cgi-bin/as-report?as=AS0&view=(null)">AS0    </a> -Reserved AS-'
import re
r = re.compile("^<a href.*>(.*)</a>(.*)$")
print r.match(text).group(2)



