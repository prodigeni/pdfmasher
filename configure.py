#!/usr/bin/env python3
# Created By: Virgil Dupras
# Created On: 2011-06-18
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

import sys
from argparse import ArgumentParser
import json

def main(ui, dev):
    if ui not in {'cocoa', 'qt'}:
        ui = 'cocoa' if sys.platform == 'darwin' else 'qt'
    build_type = 'Dev' if dev else 'Release'
    print("Configuring PdfMasher for UI {0} ({1})".format(ui, build_type))
    conf = {
        'ui': ui,
        'dev': dev,
    }
    json.dump(conf, open('conf.json', 'w'))

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--ui', dest='ui',
        help="Type of UI to build. 'qt' or 'cocoa'. Default is determined by your system.")
    parser.add_argument('--dev', action='store_true', dest='dev', default=False,
        help="If this flag is set, will configure for dev builds.")
    args = parser.parse_args()
    main(args.ui, args.dev)
