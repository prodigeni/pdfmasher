

import os
from zipfile import ZipInfo

def zip_add_dir(zipfile, path, prefix=''):
    '''
    Add a directory recursively to the zip file with an optional prefix.
    '''
    if prefix:
        zi = ZipInfo(prefix+'/')
        zi.external_attr = 16
        zipfile.writestr(zi, '')
    cwd = os.path.abspath(os.getcwd())
    try:
        os.chdir(path)
        fp = (prefix + ('/' if prefix else '')).replace('//', '/')
        for f in os.listdir('.'):
            arcname = fp + f
            if os.path.isdir(f):
                zipfile.add_dir(f, prefix=arcname)
            else:
                zipfile.write(f, arcname)
    finally:
        os.chdir(cwd)