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

for i in range(8196):
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
