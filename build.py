#!/usr/bin/env python3
# Created By: Virgil Dupras
# Created On: 2011-06-18
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

import sys
import os
import os.path as op
import shutil
import json
from argparse import ArgumentParser

from setuptools import setup, Extension

from hscommon import sphinxgen
from hscommon.build import (print_and_do, copy_packages, get_module_version, filereplace, move,
    add_to_pythonpath, copy, copy_sysconfig_files_for_embed, create_osx_app_structure)
from hscommon.plat import ISOSX

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--clean', action='store_true', dest='clean',
        help="Clean build folder before building")
    parser.add_argument('--cocoa-compile', action='store_true', dest='cocoa_compile',
        help="Build only Cocoa modules and executables")
    parser.add_argument('--xibless', action='store_true', dest='xibless',
        help="Build only xibless UIs")
    parser.add_argument('--doc', action='store_true', dest='doc',
        help="Build only the help file")
    args = parser.parse_args()
    return args

def build_xibless():
    import xibless
    if not op.exists('cocoa/autogen'):
        os.mkdir('cocoa/autogen')
    xibless.generate('cocoalib/ui/progress.py', 'cocoa/autogen/ProgressController_UI')
    xibless.generate('cocoalib/ui/about.py', 'cocoa/autogen/HSAboutBox_UI')
    xibless.generate('cocoalib/ui/fairware_reminder.py', 'cocoa/autogen/HSFairwareReminder_UI')
    xibless.generate('cocoalib/ui/demo_reminder.py', 'cocoa/autogen/HSDemoReminder_UI')
    xibless.generate('cocoalib/ui/enter_code.py', 'cocoa/autogen/HSEnterCode_UI')
    xibless.generate('cocoalib/ui/error_report.py', 'cocoa/autogen/HSErrorReportWindow_UI')
    xibless.generate('cocoa/ui/edit_pane.py', 'cocoa/autogen/PMEditPane_UI')
    xibless.generate('cocoa/ui/build_pane.py', 'cocoa/autogen/PMBuildPane_UI')
    xibless.generate('cocoa/ui/page_pane.py', 'cocoa/autogen/PMPageController_UI')
    xibless.generate('cocoa/ui/main_window.py', 'cocoa/autogen/PMMainWindow_UI')
    xibless.generate('cocoa/ui/main_menu.py', 'cocoa/autogen/PMMainMenu_UI')

def build_cocoa(dev):
    print("Building the cocoa layer")
    build_xibless()
    if not op.exists('build/py'):
        os.mkdir('build/py')
    build_cocoa_proxy_module()
    build_cocoa_bridging_interfaces()
    from pluginbuilder import copy_embeddable_python_dylib, collect_dependencies
    copy_embeddable_python_dylib('build')
    tocopy = ['core', 'hscommon', 'cocoa/inter', 'cocoalib/cocoa']
    copy_packages(tocopy, 'build')
    copy('cocoa/pyplugin.py', 'build/pyplugin.py')
    os.chdir('build')
    collect_dependencies('pyplugin.py', 'py', excludes=['PyQt4'])
    os.chdir('..')
    if dev:
        copy_packages(tocopy, 'build/py', create_links=True)
    copy_sysconfig_files_for_embed('build/py')
    os.chdir('cocoa')
    print('Generating Info.plist')
    app_version = get_module_version('core')
    filereplace('InfoTemplate.plist', 'Info.plist', version=app_version)
    print("Compiling with WAF")
    os.system('{0} waf configure && {0} waf'.format(sys.executable))
    os.chdir('..')
    print("Creating the .app folder")
    resources = ['images/main_icon.icns', 'cocoa/dsa_pub.pem', 'build/pyplugin.py',
        'build/py', 'build/help']
    frameworks = ['build/Python', 'cocoa/Sparkle.framework']
    create_osx_app_structure('build/PdfMasher.app', 'cocoa/build/PdfMasher', 'cocoa/Info.plist',
        resources, frameworks, symlink_resources=dev)
    print("Creating the run.py file")
    copy('cocoa/runtemplate.py', 'run.py')

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
        ['cocoalib/cocoa/CocoaProxy.m', 'build/CocoaProxy.m', 'build/ObjP.m',
            'cocoalib/HSErrorReportWindow.m', 'cocoa/autogen/HSErrorReportWindow_UI.m'],
        ['AppKit', 'CoreServices'],
        ['cocoalib', 'cocoa/autogen'])

def build_cocoa_bridging_interfaces():
    print("Building Cocoa Bridging Interfaces")
    import objp.o2p
    import objp.p2o
    add_to_pythonpath('cocoa')
    add_to_pythonpath('cocoalib')
    from cocoa.inter import (PyGUIObject, GUIObjectView, PyTable, TableView, PyColumns,
        ColumnsView, PyFairware, FairwareView, PyTextField)
    from inter.app import PyPdfMasher, PdfMasherView
    from inter.build_pane import PyBuildPane
    from inter.edit_pane import PyEditPane, EditPaneView
    from inter.element_table import PyElementTable
    from inter.page_controller import PyPageController, PageControllerView
    from inter.page_repr import PyPageRepr, PageReprView
    allclasses = [PyGUIObject, PyTable, PyColumns, PyFairware, PyTextField, PyPdfMasher,
        PyBuildPane, PyEditPane, PyElementTable, PyPageController, PyPageRepr]
    for class_ in allclasses:
        objp.o2p.generate_objc_code(class_, 'cocoa/autogen', inherit=True)
    allclasses = [GUIObjectView, TableView, ColumnsView, FairwareView, EditPaneView,
        PageControllerView, PageReprView, PdfMasherView]
    clsspecs = [objp.o2p.spec_from_python_class(class_) for class_ in allclasses]
    objp.p2o.generate_python_proxy_code_from_clsspec(clsspecs, 'build/CocoaViews.m')
    build_cocoa_ext('CocoaViews', 'build/py', ['build/CocoaViews.m', 'build/ObjP.m'])

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
    elif args.cocoa_compile:
        build_cocoa_proxy_module()
        build_cocoa_bridging_interfaces()
        os.chdir('cocoa')
        os.system('{0} waf configure && {0} waf'.format(sys.executable))
        os.chdir('..')
        copy('cocoa/build/PdfMasher', 'build/PdfMasher.app/Contents/MacOS/PdfMasher')
    elif args.xibless:
        build_xibless()
    else:
        build_normal(ui, dev)

if __name__ == '__main__':
    main()
