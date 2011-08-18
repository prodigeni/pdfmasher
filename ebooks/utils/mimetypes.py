import mimetypes

EXTRA_TYPES = {
    'text/fb2+xml': ['fb2'],
    'text/x-sony-bbeb+xml': ['lrs'],
    'application/x-sony-bbeb': ['lrf', 'lrx'],
    'application/adobe-page-template+xml': ['xpgt'],
    'application/x-font-opentype': ['otf'],
    'application/x-font-truetype': ['ttf'],
    'application/x-mobipocket-ebook': ['mobi', 'prc', 'azw'],
    'application/x-cbz': ['cbz'],
    'application/x-cbr': ['cbr'],
    'application/x-cb7': ['cb7'],
    'application/x-koboreader-ebook': ['kobo'],
    'image/wmf': ['wmf'],
    'application/ereader': ['pdb'],
    'application/epub+zip': ['epub'],
    'application/xhtml+xml': ['xhtml'],
    'application/x-dtbncx+xml': ['ncx'],
    'application/oebps-package+xml': ['opf'],
}

mimetypes.init()

for t, exts in EXTRA_TYPES.items():
    for ext in exts:
        mimetypes.add_type(t, '.'+ext)

guess_type = mimetypes.guess_type
guess_all_extensions = mimetypes.guess_all_extensions
def get_types_map():
    return mimetypes.types_map