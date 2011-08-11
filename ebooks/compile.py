import os
import os.path as op

from setuptools import setup, Extension

def move(src, dst):
    if not op.exists(src):
        return
    if op.exists(dst):
        os.remove(dst)
    print 'Moving %s --> %s' % (src, dst)
    os.rename(src, dst)

def build_ext():
    exts = [
        Extension('cPalmdoc', ['compression/palmdoc.c']),
        # Extension('icu', ['utils/icu.c']),
    ]
    setup(
        script_args = ['build_ext', '--inplace'],
        ext_modules = exts,
    )
    move('cPalmdoc.so', op.join('compression', 'cPalmdoc.so'))
    move('icu.so', op.join('utils', '_icu.so'))

if __name__ == '__main__':
    build_ext()