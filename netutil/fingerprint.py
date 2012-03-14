import textwrap 

def make_pretty_fingerprint(fp):
    return ':'.join(textwrap.wrap(fp, 2))
