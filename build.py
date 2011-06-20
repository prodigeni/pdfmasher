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

from hscommon.build import print_and_do, copy_packages, get_module_version, filereplace

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
    if not dev:
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

def main():
    conf = json.load(open('conf.json'))
    ui = conf['ui']
    dev = conf['dev']
    print("Building PdfMasher with UI {0}".format(ui))
    if dev:
        print("Building in Dev mode")
    if op.exists('build'):
        shutil.rmtree('build')
    os.mkdir('build')
    # build_help()
    # if dev:
    #     print("Generating devdocs")
    #     print_and_do('sphinx-build devdoc devdoc_html')
    if ui == 'cocoa':
        build_cocoa(dev)
    elif ui == 'qt':
        build_qt()

if __name__ == '__main__':
    main()
