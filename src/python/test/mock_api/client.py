#!/usr/bin/env python2.7

from __future__ import print_function, unicode_literals

import dxpy
import json
import random
import time
import os
import hashlib
import multiprocessing
import subprocess
import sys
import struct
import io

oneMB = 1048576
rndbufsz = oneMB*10
rndbuf = os.urandom(rndbufsz/2).encode('hex')

def get_pseudo_random_MB(seed):
  r = random.Random()
  b = bytearray()
  r.seed(seed)
  byte4min=-(2**31)
  byte4max= (2**31) - 1
  # 2^18 4-byte random numbers for a total of 1MB
  # getting 4 random bytes at a time instead of 1 byte to make things faster
  for i in xrange(2**18):
    b.extend(struct.pack(b'>i',r.randint(byte4min, byte4max)))
  return b

for i in range(8196):
    t=time.time()
    ics = hashlib.md5(get_pseudo_random_MB(str(i))).hexdigest()
    mb = os.urandom(oneMB)
    dxpy.DXHTTPRequest("/system/setPayload", {})
    file_desc = dxpy.describe("file-0123456789ABCDEF01234567")
    fh = dxpy.open_dxfile("file-0123456789ABCDEF01234567")
    data = io.BytesIO()
    while True:
        chunk = fh.read(oneMB)
        if len(chunk) == 0:
            break
        data.write(chunk)
    data = data.getvalue()
    cs = hashlib.md5(data).hexdigest()
    if cs != file_desc["md5"]:
        print("Checksum mismatch: {real} != {expected} ({i})".format(real=cs, expected=file_desc["md5"], i=i))
        with open("dl_corruption.{}".format(i), "wb") as fh:
            fh.write(data)
        dxpy.download_dxfile("file-0123456789ABCDEF01234567", "dl_corruption.{}.retry".format(i))
    else:
        print(i, cs)
    sys.stdout.flush()
