#!/usr/bin/env python
# encoding: utf-8

import hashlib
import sys
import struct
import unittest
import base64
import fingerprint

class SSHHostKey(object):
    VALID_KEYTYPES = ('ssh-rsa', 'ssh-dss')

    @staticmethod
    def gen_fields(raw):
        index = 0
        while index < len(raw):
            length = struct.unpack('!L', raw[index:index + 4])[0]
            field = raw[index + 4 : index + 4 + length]
            index = index + 4 + length
            yield field

    def __init__(self, key):
        self.raw = base64.b64decode(key)
        fields = list(SSHHostKey.gen_fields(self.raw))
        self.type = fields[0]
        assert self.type in SSHHostKey.VALID_KEYTYPES
        if self.type == 'ssh-rsa':
            self.exponent = fields[1].encode('hex')
            self.modulus = fields[2].encode('hex')
            
    def get_fingerprint(self):
        return fingerprint.make_pretty_fingerprint(hashlib.md5(self.raw).hexdigest())


class SSHHostKeyTests(unittest.TestCase):
    RSA_HOSTKEY = "AAAAB3NzaC1yc2EAAAABIwAAAQEAq2A7hRGmdnm9tUDbO9IDSwBK6T" + \
                  "bQa+PXYPCPy6rbTrTtw7PHkccKrpp0yVhp5HdEIcKr6pLlVDBfOLX9" + \
                  "QUsyCOV0wzfjIJNlGEYsdlLJizHhbn2mUjvSAHQqZETYP81eFzLQNn" + \
                  "PHt4EVVUh7VfDESU84KezmD5QlWpXLmvU31/yMf+Se8xhHTvKSCZIF" + \
                  "ImWwoG6mbUoWf9nzpIoaSjB+weqqUUmpaaasXVal72J+UX2B+2RPW3" + \
                  "RcT0eOzQgqlJL3RKrTJvdsjE3JEAvGq3lGHSZXy28G3skua2SmVi/w" + \
                  "4yCE6gbODqnTWlg7+wC604ydGXA8VJiS5ap43JXiUFFAaQ=="
    
    RSA_FINGERPRINT = "16:27:ac:a5:76:28:2d:36:63:1b:56:4d:eb:df:a6:48"
                
    DSS_HOSTKEY = "AAAAB3NzaC1kc3MAAACBAPbrZJjgneUMUxNZBNbXqnYJhHFuHRQa1r" + \
                  "Y77R4CzMZAHY4ASgeJscidNEQRkAU+dDwM6GihU7EDsZV2Oe3oP7Nx" + \
                  "gp5Uel1uln0lC+9YvgyEI1LqrUDw8Y+iOJpVA1h/cMgxogMJ+1U8y6" + \
                  "gewowj62Y6amnGdYQj0UYLza539tyPAAAAFQDljY3MwLmIPWozasMX" + \
                  "BMJrT14i4QAAAIBX6IwVeOWVe2CAvnklxRu71RbD6+WZ/On7wJY51X" + \
                  "ZrczIqWHVyLDvMmM6dnBguPAEzrSaRXicJEBchRTw6pNJ0oHdqCfzo" + \
                  "MxFF3gUrPGcgMW0HNXdeY9cHKNGiyHovtg8nz/b1ZJDA3o38DLrZb1" + \
                  "Qg+hYw0II+5Eo5xeqejoynZgAAAIAYExkaMNl7Ek4UAQyfrVkWoUGu" + \
                  "b0bZc45cAzUQKqU7aJf+p0QwwZmxz7NzvbA4piUrAfUmEvdri6T0RE" + \
                  "fjGZ5OMX8fOg6/7oE4czRKWl0mZlQ7B9sbpmwfeCOE+l0npkqcVbvR" + \
                  "tUgrTvZbZtzm3n2yGcl7Yyz+WImHSDGtAEhxuA=="
                  
    DSS_FINGERPRINT = "16:b6:81:18:08:f0:b0:a7:a1:08:b7:fb:22:18:1f:e3"

    def testRSA(self):
        k = SSHHostKey(self.RSA_HOSTKEY)
        self.assertEquals(k.type, "ssh-rsa")
        self.assertEquals(k.get_fingerprint(), self.RSA_FINGERPRINT)
        
    def testDSS(self):
        k = SSHHostKey(self.DSS_HOSTKEY)
        self.assertEquals(k.type, "ssh-dss")
        self.assertEquals(k.get_fingerprint(), self.DSS_FINGERPRINT)
        
    def testInvalid(self):
        pass
        #k = SSHHostKey("asd")

if __name__ == '__main__':
    unittest.main()