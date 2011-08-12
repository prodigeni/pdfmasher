# Copyright 2008, Kovid Goyal <kovid at kovidgoyal.net>
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

from struct import pack

def compress_doc(data):
    out = bytearray()
    i = 0
    ldata = len(data)
    while i < ldata:
        if i > 10 and (ldata - i) > 10:
            chunk = ''
            match = -1
            for j in range(10, 2, -1):
                chunk = data[i:i+j]
                try:
                    match = data.rindex(chunk, 0, i)
                except ValueError:
                    continue
                if (i - match) <= 2047:
                    break
                match = -1
            if match >= 0:
                n = len(chunk)
                m = i - match
                code = 0x8000 + ((m << 3) & 0x3ff8) + (n - 3)
                out += pack(b'>H', code)
                i += n
                continue
        ch = data[i]
        och = ord(ch)
        i += 1
        if ch == b' ' and (i + 1) < ldata:
            onch = ord(data[i])
            if onch >= 0x40 and onch < 0x80:
                out += pack(b'>B', onch ^ 0x80)
                i += 1
                continue
        if och == 0 or (och > 8 and och < 0x80):
            out += ch
        else:
            j = i
            binseq = [ch]
            while j < ldata and len(binseq) < 8:
                ch = data[j]
                och = ord(ch)
                if och == 0 or (och > 8 and och < 0x80):
                    break
                binseq.append(ch)
                j += 1
            out += pack(b'>B', len(binseq))
            out += b''.join(binseq)
            i += len(binseq) - 1
    return bytes(out)

