import re

# regular expression for a base 64-encoded certificate. e.g.
"""
-----BEGIN CERTIFICATE-----
MIIFzzCCBTigAwIBAgIKUJaUxQADAABKaDANBgkqhkiG9w0BAQUFADBGMQswCQYD
VQQGEwJVUzETMBEGA1UEChMKR29vZ2xlIEluYzEiMCAGA1UEAxMZR29vZ2xlIElu
dGVybmV0IEF1dGhvcml0eTAeFw0xMjAyMjgxMjQ5MzRaFw0xMzAyMjgxMjU5MzRa
MGYxCzAJBgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRYwFAYDVQQHEw1N
b3VudGFpbiBWaWV3MRMwEQYDVQQKEwpHb29nbGUgSW5jMRUwEwYDVQQDFAwqLmdv
b2dsZS5jb20wgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBANfXb/1NezWuQDF7
Kd1zlBT+5SsP1LAm4NwNngwPPgTgusWn28Acmz+1JvWV/TFz0Lv2LdhR/iQ1gify
l00rF6MbGWUbJVNWyDqOmldjbjb8Zk4N6g1Ix4TTbxaXLEqnZ6Me5BOGWGJd0PW4
/zMGZh/N/y6LY5Nmz6Mh2gqJSS/LAgMBAAGjggOiMIIDnjAdBgNVHSUEFjAUBggr
BgEFBQcDAQYIKwYBBQUHAwIwHQYDVR0OBBYEFAYVZrugvmq59Ok/kemr41Qw4Ul5
MB8GA1UdIwQYMBaAFL/AMOv1QxE+Z7qekfv8atrjaxIkMFsGA1UdHwRUMFIwUKBO
oEyGSmh0dHA6Ly93d3cuZ3N0YXRpYy5jb20vR29vZ2xlSW50ZXJuZXRBdXRob3Jp
dHkvR29vZ2xlSW50ZXJuZXRBdXRob3JpdHkuY3JsMGYGCCsGAQUFBwEBBFowWDBW
BggrBgEFBQcwAoZKaHR0cDovL3d3dy5nc3RhdGljLmNvbS9Hb29nbGVJbnRlcm5l
dEF1dGhvcml0eS9Hb29nbGVJbnRlcm5ldEF1dGhvcml0eS5jcnQwggJ2BgNVHREE
ggJtMIICaYIMKi5nb29nbGUuY29tggpnb29nbGUuY29tggsqLmF0Z2dsLmNvbYIN
Ki55b3V0dWJlLmNvbYILeW91dHViZS5jb22CFioueW91dHViZS1ub2Nvb2tpZS5j
b22CCHlvdXR1LmJlggsqLnl0aW1nLmNvbYIPKi5nb29nbGUuY29tLmJygg4qLmdv
b2dsZS5jby5pboILKi5nb29nbGUuZXOCDiouZ29vZ2xlLmNvLnVrggsqLmdvb2ds
ZS5jYYILKi5nb29nbGUuZnKCCyouZ29vZ2xlLnB0ggsqLmdvb2dsZS5pdIILKi5n
b29nbGUuZGWCCyouZ29vZ2xlLmNsggsqLmdvb2dsZS5wbIILKi5nb29nbGUubmyC
DyouZ29vZ2xlLmNvbS5hdYIOKi5nb29nbGUuY28uanCCCyouZ29vZ2xlLmh1gg8q
Lmdvb2dsZS5jb20ubXiCDyouZ29vZ2xlLmNvbS5hcoIPKi5nb29nbGUuY29tLmNv
gg8qLmdvb2dsZS5jb20udm6CDyouZ29vZ2xlLmNvbS50coINKi5hbmRyb2lkLmNv
bYILYW5kcm9pZC5jb22CFCouZ29vZ2xlY29tbWVyY2UuY29tghAqLnVybC5nb29n
bGUuY29tghYqLmdvb2dsZXRhZ21hbmFnZXIuY29tghRnb29nbGV0YWdtYW5hZ2Vy
LmNvbYIMKi51cmNoaW4uY29tggp1cmNoaW4uY29tghYqLmdvb2dsZS1hbmFseXRp
Y3MuY29tghRnb29nbGUtYW5hbHl0aWNzLmNvbYISKi5jbG91ZC5nb29nbGUuY29t
MA0GCSqGSIb3DQEBBQUAA4GBAHCi0tdgY/fTSLxvTbUzXkWWWTS/mBflcTbOmViw
vwz6SeU0f2rb4EAWcyMAFPbzX+P7GkiAoE/pUrk7ZRRgQ9N7SWdn6PNAxZzeFAPp
wjDQUlsjpX4kFHJwJ4VgPJ33dncxaCAOq4MGfl0ozBPHdgRSBO72Jz66gHwNDCz+
exi9
-----END CERTIFICATE-----

"""


REGEX_BASE64_CERTIFICATE = re.compile("^(-----BEGIN CERTIFICATE-----)"
                           "([\w\d\+\/]*[\n\r]+)*([\w\d\+\/]*\=*[\n\r]+)"
                           "(-----END CERTIFICATE-----)$")

REGEX_BASE64 = re.compile("([\w\d\+\/]*[\n\r]+)*([\w\d\+\/]*\=*[\n\r]+)")