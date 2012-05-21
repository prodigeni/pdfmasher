#!/usr/bin/env python3
# Created By: Virgil Dupras
# Created On: 2011-06-18
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

import os
import os.path as op
import shutil
import json
from argparse import ArgumentParser

from setuptools import setup, Extension

from hscommon import sphinxgen
from hscommon.build import (print_and_do, copy_packages, get_module_version, filereplace, move)
from hscommon.plat import ISOSX

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--clean', action='store_true', dest='clean',
        help="Clean build folder before building")
    parser.add_argument('--cocoamod', action='store_true', dest='cocoamod',
        help="Build only Cocoa modules")
    parser.add_argument('--doc', action='store_true', dest='doc',
        help="Build only the help file")
    args = parser.parse_args()
    return args

def build_cocoa(dev):
    from pluginbuilder import build_plugin
    build_cocoa_proxy_module()
    print("Building py.plugin")
    if dev:
        copy_packages(['cocoa/inter', 'cocoalib/cocoa'], 'build')
    else:
        copy_packages(['core', 'hscommon', 'cocoa/inter', 'cocoalib/cocoa'], 'build')
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

def build_cocoa_ext(extname, dest, source_files, extra_frameworks=(), extra_includes=()):
    extra_link_args = ["-framework", "CoreFoundation", "-framework", "Foundation"]
    for extra in extra_frameworks:
        extra_link_args += ['-framework', extra]
    ext = Extension(extname, source_files, extra_link_args=extra_link_args, include_dirs=extra_includes)
    setup(script_args=['build_ext', '--inplace'], ext_modules=[ext])
    fn = extname + '.so'
    assert op.exists(fn)
    move(fn, op.join(dest, fn))

def build_cocoa_proxy_module():
    print("Building Cocoa Proxy")
    import objp.p2o
    objp.p2o.generate_python_proxy_code('cocoalib/cocoa/CocoaProxy.h', 'build/CocoaProxy.m')
    build_cocoa_ext("CocoaProxy", 'cocoalib/cocoa',
        ['cocoalib/cocoa/CocoaProxy.m', 'build/CocoaProxy.m', 'build/ObjP.m', 'cocoalib/HSErrorReportWindow.m'],
        ['AppKit', 'CoreServices'],
        ['cocoalib'])

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
    platform = 'osx' if ISOSX else 'win'
    current_path = op.abspath('.')
    confpath = op.join(current_path, 'help', 'conf.tmpl')
    help_basepath = op.join(current_path, 'help', 'en')
    help_destpath = op.join(current_path, 'build', 'help')
    changelog_path = op.join(current_path, 'help', 'changelog')
    tixurl = "http://bitbucket.org/hsoft/pdfmasher/issue/{0}"
    confrepl = {'platform': platform}
    sphinxgen.gen(help_basepath, help_destpath, changelog_path, tixurl, confrepl, confpath)

def build_normal(ui, dev):
    build_help()
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
    elif args.cocoamod:
        build_cocoa_proxy_module()
    else:
        build_normal(ui, dev)

if __name__ == '__main__':
    main()
