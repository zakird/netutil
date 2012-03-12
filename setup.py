import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "netutil",
    version = "0.2.0",
    author = "Zakir Durumeric",
    author_email = "zakird@gmail.com",
    maintainer = "Zakir Durumeric",
    maintainer_email = "zakird@gmail.com",
    download_url = "https://github.com/zakird/netutil/zipball/master",
    url = "https://github.com/zakird/netutil",
    description = "Set of high-level networking helpers used in various projects",
    license = "GNUv3",
    keywords = "python network cidr bgp asn certificate ssl",
    packages=[
        'netutil'
    ],
    long_description = read('README.rst'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: System Administrators",
        "Natural Language :: English",
    ],
    install_requires=[
        'setuptools',
        'm2crypto',
        'paramiko'
    ]
)
