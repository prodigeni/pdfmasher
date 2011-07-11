# cxfreeze has some problems detecting all dependencies.
# This modules explicitly import those problematic modules.

import os
import markdown.etree_loader

# Normally, cmap files are directly in pdfminer/cmap, but
# with cx_freeze, pdfminer is in a zip file and it confuses
# everything. Fortunately, we can override cmap's location
# through environment variables, which we do here.
os.environ['CMAP_PATH'] = 'cmap'