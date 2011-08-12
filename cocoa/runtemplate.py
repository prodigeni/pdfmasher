#!/usr/bin/env python3
# Created By: Virgil Dupras
# Created On: 2011-06-19
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

import sys
import os

def main():
    return os.system('open {{app_path}}')

if __name__ == '__main__':
    sys.exit(main())