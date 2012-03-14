#!/usr/bin/env python
# encoding: utf-8
"""
sshhostkeycheck.py

"""

import sys
import os
import unittest
import socket

try:
    import paramiko
except ImportError, e:
    print "ERROR: unable to import paramiko. you need to run `sudo easy_install paramiko`."

class OverrideMissingHostKeyException(Exception):
    def __init__(self, client, hostname, key):
        self.client = client
        self.hostname = hostname
        self.key = key


class OverrideMissingHostKeyPolicy(paramiko.MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):
        raise OverrideMissingHostKeyException(client, hostname, key)


class SSHHostKeyGrabber(object):
    TIMEOUT = 3 # seconds

    def __init__(self, timeout=None):
        self.__paramiko_client = paramiko.SSHClient()
        # set empty missing host key policy so that a catchable
        # exception is raised instead of something generic as
        # would be raised by the default policy
        self.__paramiko_client.set_missing_host_key_policy(OverrideMissingHostKeyPolicy())
        # explicitly ignore all the system keys automatically
        # imported by the library
        self.__paramiko_client._system_host_keys = {}
        self._timeout = timeout if timeout else self.TIMEOUT

    def get_hostkey(self, address, port=22):
        try:
            self.__paramiko_client.connect(
                hostname = address,
                port = port,
                timeout = self._timeout,
                look_for_keys = False
            )
        except OverrideMissingHostKeyException, e:
            return e.key.get_base64()
        raise Exception("connection should always raise MissingHostKey Exception")

    def close(self):
        return self.__paramiko_client.close()


class SSHHostKeyGrabberTests(unittest.TestCase):
    KNOWN_HOST = "github.com"
    ASSOC_HOST_KEY = "AAAAB3NzaC1yc2EAAAABIwAAAQEAq2A7hRGmdnm9tUDbO9IDSwBK6T" + \
                  "bQa+PXYPCPy6rbTrTtw7PHkccKrpp0yVhp5HdEIcKr6pLlVDBfOLX9" + \
                  "QUsyCOV0wzfjIJNlGEYsdlLJizHhbn2mUjvSAHQqZETYP81eFzLQNn" + \
                  "PHt4EVVUh7VfDESU84KezmD5QlWpXLmvU31/yMf+Se8xhHTvKSCZIF" + \
                  "ImWwoG6mbUoWf9nzpIoaSjB+weqqUUmpaaasXVal72J+UX2B+2RPW3" + \
                  "RcT0eOzQgqlJL3RKrTJvdsjE3JEAvGq3lGHSZXy28G3skua2SmVi/w" + \
                  "4yCE6gbODqnTWlg7+wC604ydGXA8VJiS5ap43JXiUFFAaQ=="

    def setUp(self):
        self.key_check = SSHHostKeyGrabber()

    def testKnownHost(self):
        self.assertEqual(self.key_check.get_hostkey(self.KNOWN_HOST, 22), self.ASSOC_HOST_KEY)

    def testBadHost(self):
        DNE_HOST = "thismachinedne.eecs.umich.edu"
        self.assertRaises(socket.gaierror, self.key_check.get_hostkey, DNE_HOST, 22)

    def testConnectionRefused(self):
        DNE_HOST = "github.com"
        self.assertRaises(socket.error, self.key_check.get_hostkey, DNE_HOST, 24)

    def testTimeout(self):
        DNE_HOST = "0.0.0.0"
        self.assertRaises(socket.error, self.key_check.get_hostkey, DNE_HOST, 22)

    def testNotSSH(self):
        DNE_HOST = "github.com"
        self.assertRaises(paramiko.ssh_exception.SSHException, self.key_check.get_hostkey, DNE_HOST, 443)

    def tearDown(self):
        if self.key_check:
            self.key_check.close()
        self.key_check = None


if __name__ == '__main__':
    unittest.main()
