#!/usr/bin/env python3
# Created By: Virgil Dupras
# Created On: 2011-06-18
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

import sys
import os
import os.path as op
import shutil
import json
from argparse import ArgumentParser

from hscommon import sphinxgen
from hscommon.build import (print_and_do, copy_packages, get_module_version, filereplace,
    build_all_qt_locs)

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--clean', action='store_true', dest='clean',
        help="Clean build folder before building")
    parser.add_argument('--doc', action='store_true', dest='doc',
        help="Build only the help file")
    parser.add_argument('--loc', action='store_true', dest='loc',
        help="Build only localization")
    args = parser.parse_args()
    return args

def build_cocoa(dev):
    from pluginbuilder import build_plugin
    # if not dev:
    #     print("Building help index")
    #     help_path = op.abspath('help/moneyguru_help')
    #     os.system('open -a /Developer/Applications/Utilities/Help\\ Indexer.app {0}'.format(help_path))
    # 
    # build_all_cocoa_locs('cocoalib')
    # build_all_cocoa_locs('cocoa')
        
    print("Building py.plugin")
    if dev:
        copy_packages(['cocoa/inter'], 'build')
    else:
        copy_packages(['core', 'hscommon', 'cocoa/inter'], 'build')
    shutil.copy('cocoa/pyplugin.py', 'build')
    os.chdir('build')
    # We have to exclude PyQt4 specifically because it's conditionally imported in hscommon.trans
    build_plugin('pyplugin.py', excludes=['PyQt4'], alias=dev)
    os.chdir('..')
    pluginpath = 'cocoa/pyplugin.plugin'
    if op.exists(pluginpath):
        shutil.rmtree(pluginpath)
    shutil.move('build/dist/pyplugin.plugin', pluginpath)
    if dev:
        # In alias mode, the tweakings we do to the pythonpath aren't counted in. We have to
        # manually put a .pth in the plugin
        pthpath = op.join(pluginpath, 'Contents/Resources/dev.pth')
        open(pthpath, 'w').write(op.abspath('.'))
    os.chdir('cocoa')
    print('Generating Info.plist')
    app_version = get_module_version('core')
    filereplace('InfoTemplate.plist', 'Info.plist', version=app_version)
    print("Building the XCode project")
    args = []
    if dev:
        args.append('-configuration dev')
    else:
        args.append('-configuration release')
    args = ' '.join(args)
    os.system('xcodebuild {0}'.format(args))
    os.chdir('..')
    print("Creating the run.py file")
    subfolder = 'dev' if dev else 'release'
    app_path = 'cocoa/build/{0}/PdfMasher.app'.format(subfolder)
    tmpl = open('cocoa/runtemplate.py', 'rt').read()
    run_contents = tmpl.replace('{{app_path}}', app_path)
    open('run.py', 'wt').write(run_contents)

def build_qt():
    print("Building resource file")
    qrc_path = op.join('qt', 'pm.qrc')
    pyrc_path = op.join('qt', 'pm_rc.py')
    print_and_do("pyrcc4 -py3 {0} > {1}".format(qrc_path, pyrc_path))
    print("Creating the run.py file")
    runtemplate_path = op.join('qt', 'runtemplate.py')
    shutil.copy(runtemplate_path, 'run.py')

def build_help():
    print("Generating Help")
    platform = 'osx' if sys.platform == 'darwin' else 'win'
    current_path = op.abspath('.')
    confpath = op.join(current_path, 'help', 'conf.tmpl')
    help_basepath = op.join(current_path, 'help', 'en')
    help_destpath = op.join(current_path, 'build', 'help')
    changelog_path = op.join(current_path, 'help', 'changelog')
    tixurl = "http://bitbucket.org/hsoft/pdfmasher/issue/{0}"
    confrepl = {'platform': platform}
    sphinxgen.gen(help_basepath, help_destpath, changelog_path, tixurl, confrepl, confpath)

def build_localizations(ui):
    print("Building localizations")
    if ui == 'qt':
        print("Building .ts files")
        build_all_qt_locs(op.join('qt', 'lang'), extradirs=[op.join('qtlib', 'lang')])

def build_normal(ui, dev):
    build_help()
    build_localizations(ui)
    if ui == 'cocoa':
        build_cocoa(dev)
    elif ui == 'qt':
        build_qt()

def main():
    args = parse_args()
    conf = json.load(open('conf.json'))
    ui = conf['ui']
    dev = conf['dev']
    print("Building PdfMasher with UI {0}".format(ui))
    if dev:
        print("Building in Dev mode")
    if args.clean:
        if op.exists('build'):
            shutil.rmtree('build')
    if not op.exists('build'):
        os.mkdir('build')
    if args.doc:
        build_help()
    elif args.loc:
        build_localizations(ui)
    else:
        build_normal(ui, dev)

if __name__ == '__main__':
    main()
