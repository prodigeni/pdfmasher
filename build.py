import sys
import os.path as op
import shutil

def main():
    runtemplate_path = op.join('qt', 'runtemplate.py')
    shutil.copy(runtemplate_path, 'run.py')

if __name__ == '__main__':
    main()
