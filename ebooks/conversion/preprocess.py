#!/usr/bin/env python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

__license__   = 'GPL v3'
__copyright__ = '2009, Kovid Goyal <kovid@kovidgoyal.net>'
__docformat__ = 'restructuredtext en'

import functools, re

from ..utils import entity_to_unicode, as_unicode

XMLDECL_RE    = re.compile(r'^\s*<[?]xml.*?[?]>')
SVG_NS       = 'http://www.w3.org/2000/svg'
XLINK_NS     = 'http://www.w3.org/1999/xlink'

convert_entities = functools.partial(entity_to_unicode,
        result_exceptions = {
            u'<' : '&lt;',
            u'>' : '&gt;',
            u"'" : '&apos;',
            u'"' : '&quot;',
            u'&' : '&amp;',
        })
_span_pat = re.compile('<span.*?</span>', re.DOTALL|re.IGNORECASE)

LIGATURES = {
#        u'\u00c6': u'AE',
#        u'\u00e6': u'ae',
#        u'\u0152': u'OE',
#        u'\u0153': u'oe',
#        u'\u0132': u'IJ',
#        u'\u0133': u'ij',
#        u'\u1D6B': u'ue',
        u'\uFB00': u'ff',
        u'\uFB01': u'fi',
        u'\uFB02': u'fl',
        u'\uFB03': u'ffi',
        u'\uFB04': u'ffl',
        u'\uFB05': u'ft',
        u'\uFB06': u'st',
        }

_ligpat = re.compile(u'|'.join(LIGATURES))

def sanitize_head(match):
    x = match.group(1)
    x = _span_pat.sub('', x)
    return '<head>\n%s\n</head>' % x

def chap_head(match):
    chap = match.group('chap')
    title = match.group('title')
    if not title:
        return '<h1>'+chap+'</h1><br/>\n'
    else:
        return '<h1>'+chap+'</h1>\n<h3>'+title+'</h3>\n'

def wrap_lines(match):
    ital = match.group('ital')
    if not ital:
        return ' '
    else:
        return ital+' '

class DocAnalysis(object):
    '''
    Provides various text analysis functions to determine how the document is structured.
    format is the type of document analysis will be done against.
    raw is the raw text to determine the line length to use for wrapping.
    Blank lines are excluded from analysis
    '''

    def __init__(self, format='html', raw=''):
        raw = raw.replace('&nbsp;', ' ')
        if format == 'html':
            linere = re.compile('(?<=<p)(?![^>]*>\s*</p>).*?(?=</p>)', re.DOTALL)
        elif format == 'pdf':
            linere = re.compile('(?<=<br>)(?!\s*<br>).*?(?=<br>)', re.DOTALL)
        elif format == 'spanned_html':
            linere = re.compile('(?<=<span).*?(?=</span>)', re.DOTALL)
        elif format == 'txt':
            linere = re.compile('.*?\n')
        self.lines = linere.findall(raw)

    def line_length(self, percent):
        '''
        Analyses the document to find the median line length.
        percentage is a decimal number, 0 - 1 which is used to determine
        how far in the list of line lengths to use. The list of line lengths is
        ordered smallest to larged and does not include duplicates. 0.5 is the
        median value.
        '''
        lengths = []
        for line in self.lines:
            if len(line) > 0:
                lengths.append(len(line))

        if not lengths:
            return 0

        lengths = list(set(lengths))
        total = sum(lengths)
        avg = total / len(lengths)
        max_line = avg * 2

        lengths = sorted(lengths)
        for i in range(len(lengths) - 1, -1, -1):
            if lengths[i] > max_line:
                del lengths[i]

        if percent > 1:
            percent = 1
        if percent < 0:
            percent = 0

        index = int(len(lengths) * percent) - 1

        return lengths[index]

    def line_histogram(self, percent):
        '''
        Creates a broad histogram of the document to determine whether it incorporates hard
        line breaks.  Lines are sorted into 20 'buckets' based on length.
        percent is the percentage of lines that should be in a single bucket to return true
        The majority of the lines will exist in 1-2 buckets in typical docs with hard line breaks
        '''
        minLineLength=20 # Ignore lines under 20 chars (typical of spaces)
        maxLineLength=1900 # Discard larger than this to stay in range
        buckets=20 # Each line is divided into a bucket based on length

        #print "there are "+str(len(lines))+" lines"
        #max = 0
        #for line in self.lines:
        #    l = len(line)
        #    if l > max:
        #        max = l
        #print "max line found is "+str(max)
        # Build the line length histogram
        hRaw = [ 0 for i in range(0,buckets) ]
        for line in self.lines:
            l = len(line)
            if l > minLineLength and l < maxLineLength:
                    l = int(l/100)
                    #print "adding "+str(l)
                    hRaw[l]+=1

        # Normalize the histogram into percents
        totalLines = len(self.lines)
        if totalLines > 0:
            h = [ float(count)/totalLines for count in hRaw ]
        else:
            h = []
        #print "\nhRaw histogram lengths are: "+str(hRaw)
        #print "              percents are: "+str(h)+"\n"

        # Find the biggest bucket
        maxValue = 0
        for i in range(0,len(h)):
            if h[i] > maxValue:
                maxValue = h[i]

        if maxValue < percent:
            #print "Line lengths are too variable. Not unwrapping."
            return False
        else:
            #print str(maxValue)+" of the lines were in one bucket"
            return True

class Dehyphenator(object):
    '''
    Analyzes words to determine whether hyphens should be retained/removed.  Uses the document
    itself is as a dictionary. This method handles all languages along with uncommon, made-up, and
    scientific words. The primary disadvantage is that words appearing only once in the document
    retain hyphens.
    '''

    def __init__(self, verbose=0, log=None):
        self.log = log
        self.verbose = verbose
        # Add common suffixes to the regex below to increase the likelihood of a match -
        # don't add suffixes which are also complete words, such as 'able' or 'sex'
        # only remove if it's not already the point of hyphenation
        self.suffix_string = "((ed)?ly|'?e?s||a?(t|s)?ion(s|al(ly)?)?|ings?|er|(i)?ous|(i|a)ty|(it)?ies|ive|gence|istic(ally)?|(e|a)nce|m?ents?|ism|ated|(e|u)ct(ed)?|ed|(i|ed)?ness|(e|a)ncy|ble|ier|al|ex|ian)$"
        self.suffixes = re.compile(r"^%s" % self.suffix_string, re.IGNORECASE)
        self.removesuffixes = re.compile(r"%s" % self.suffix_string, re.IGNORECASE)
        # remove prefixes if the prefix was not already the point of hyphenation
        self.prefix_string = '^(dis|re|un|in|ex)'
        self.prefixes = re.compile(r'%s$' % self.prefix_string, re.IGNORECASE)
        self.removeprefix = re.compile(r'%s' % self.prefix_string, re.IGNORECASE)

    def dehyphenate(self, match):
        firsthalf = match.group('firstpart')
        secondhalf = match.group('secondpart')
        try:
            wraptags = match.group('wraptags')
        except:
            wraptags = ''
        hyphenated = unicode(firsthalf) + "-" + unicode(secondhalf)
        dehyphenated = unicode(firsthalf) + unicode(secondhalf)
        if self.suffixes.match(secondhalf) is None:
            lookupword = self.removesuffixes.sub('', dehyphenated)
        else:
            lookupword = dehyphenated
        if len(firsthalf) > 4 and self.prefixes.match(firsthalf) is None:
            lookupword = self.removeprefix.sub('', lookupword)
        if self.verbose > 2:
            self.log("lookup word is: "+str(lookupword)+", orig is: " + str(hyphenated))
        try:
            searchresult = self.html.find(lookupword.lower())
        except:
            return hyphenated
        if self.format == 'html_cleanup' or self.format == 'txt_cleanup':
            if self.html.find(lookupword) != -1 or searchresult != -1:
                if self.verbose > 2:
                    self.log("    Cleanup:returned dehyphenated word: " + str(dehyphenated))
                return dehyphenated
            elif self.html.find(hyphenated) != -1:
                if self.verbose > 2:
                    self.log("        Cleanup:returned hyphenated word: " + str(hyphenated))
                return hyphenated
            else:
                if self.verbose > 2:
                    self.log("            Cleanup:returning original text "+str(firsthalf)+" + linefeed "+str(secondhalf))
                return firsthalf+u'\u2014'+wraptags+secondhalf

        else:
            if self.format == 'individual_words' and len(firsthalf) + len(secondhalf) <= 6:
                if self.verbose > 2:
                    self.log("too short, returned hyphenated word: " + str(hyphenated))
                return hyphenated
            if len(firsthalf) <= 2 and len(secondhalf) <= 2:
                if self.verbose > 2:
                    self.log("too short, returned hyphenated word: " + str(hyphenated))
                return hyphenated
            if self.html.find(lookupword) != -1 or searchresult != -1:
                if self.verbose > 2:
                    self.log("     returned dehyphenated word: " + str(dehyphenated))
                return dehyphenated
            else:
                if self.verbose > 2:
                    self.log("          returned hyphenated word: " + str(hyphenated))
                return hyphenated

    def __call__(self, html, format, length=1):
        self.html = html
        self.format = format
        if format == 'html':
            intextmatch = re.compile(u'(?<=.{%i})(?P<firstpart>[^\W\-]+)(-|‐)\s*(?=<)(?P<wraptags>(</span>)?\s*(</[iubp]>\s*){1,2}(?P<up2threeblanks><(p|div)[^>]*>\s*(<p[^>]*>\s*</p>\s*)?</(p|div)>\s+){0,3}\s*(<[iubp][^>]*>\s*){1,2}(<span[^>]*>)?)\s*(?P<secondpart>[\w\d]+)' % length)
        elif format == 'pdf':
            intextmatch = re.compile(u'(?<=.{%i})(?P<firstpart>[^\W\-]+)(-|‐)\s*(?P<wraptags><p>|</[iub]>\s*<p>\s*<[iub]>)\s*(?P<secondpart>[\w\d]+)'% length)
        elif format == 'txt':
            intextmatch = re.compile(u'(?<=.{%i})(?P<firstpart>[^\W\-]+)(-|‐)(\u0020|\u0009)*(?P<wraptags>(\n(\u0020|\u0009)*)+)(?P<secondpart>[\w\d]+)'% length)
        elif format == 'individual_words':
            intextmatch = re.compile(u'(?!<)(?P<firstpart>[^\W\-]+)(-|‐)\s*(?P<secondpart>\w+)(?![^<]*?>)')
        elif format == 'html_cleanup':
            intextmatch = re.compile(u'(?P<firstpart>[^\W\-]+)(-|‐)\s*(?=<)(?P<wraptags></span>\s*(</[iubp]>\s*<[iubp][^>]*>\s*)?<span[^>]*>|</[iubp]>\s*<[iubp][^>]*>)?\s*(?P<secondpart>[\w\d]+)')
        elif format == 'txt_cleanup':
            intextmatch = re.compile(u'(?P<firstpart>[^\W\-]+)(-|‐)(?P<wraptags>\s+)(?P<secondpart>[\w\d]+)')


        html = intextmatch.sub(self.dehyphenate, html)
        return html

class CSSPreProcessor(object):

    PAGE_PAT   = re.compile(r'@page[^{]*?{[^}]*?}')
    # Remove some of the broken CSS Microsoft products
    # create
    MS_PAT     = re.compile(r'''
        (?P<start>^|;|\{)\s*    # The end of the previous rule or block start
        (%s).+?                 # The invalid selectors
        (?P<end>$|;|\})         # The end of the declaration
        '''%'mso-|panose-|text-underline|tab-interval',
        re.MULTILINE|re.IGNORECASE|re.VERBOSE)

    def ms_sub(self, match):
        end = match.group('end')
        try:
            start = match.group('start')
        except:
            start = ''
        if end == ';':
            end = ''
        return start + end

    def __call__(self, data, add_namespace=False):
        from ..oeb.base import XHTML_CSS_NAMESPACE
        data = self.PAGE_PAT.sub('', data)
        data = self.MS_PAT.sub(self.ms_sub, data)
        if not add_namespace:
            return data
        ans, namespaced = [], False
        for line in data.splitlines():
            ll = line.lstrip()
            if not (namespaced or ll.startswith('@import') or
                        ll.startswith('@charset')):
                ans.append(XHTML_CSS_NAMESPACE.strip())
                namespaced = True
            ans.append(line)

        return u'\n'.join(ans)

class HTMLPreProcessor(object):

    PREPROCESS = [
                  # Convert all entities, since lxml doesn't handle them well
                  (re.compile(r'&(\S+?);'), convert_entities),
                  ]
    
    def __init__(self, log=None, extra_opts=None):
        self.log = log
        self.extra_opts = extra_opts

    def __call__(self, html, remove_special_chars=None,
            get_preprocess_html=False):
        if remove_special_chars is not None:
            html = remove_special_chars.sub('', html)
        html = html.replace('\0', '')
        rules = []

        start_rules = []
        if not getattr(self.extra_opts, 'keep_ligatures', False):
            html = _ligpat.sub(lambda m:LIGATURES[m.group()], html)

        for search, replace in [['sr3_search', 'sr3_replace'], ['sr2_search', 'sr2_replace'], ['sr1_search', 'sr1_replace']]:
            search_pattern = getattr(self.extra_opts, search, '')
            if search_pattern:
                try:
                    search_re = re.compile(search_pattern)
                    replace_txt = getattr(self.extra_opts, replace, '')
                    if not replace_txt:
                        replace_txt = ''
                    rules.insert(0, (search_re, replace_txt))
                except Exception as e:
                    self.log.error('Failed to parse %r regexp because %s' %
                            (search, as_unicode(e)))

        end_rules = []

        length = -1
        if getattr(self.extra_opts, 'unwrap_factor', 0.0) > 0.01:
            docanalysis = DocAnalysis('pdf', html)
            length = docanalysis.line_length(getattr(self.extra_opts, 'unwrap_factor'))
            if length:
                #print "The pdf line length returned is " + str(length)
                # unwrap em/en dashes
                end_rules.append((re.compile(u'(?<=.{%i}[–—])\s*<p>\s*(?=[[a-z\d])' % length), lambda match: ''))
                end_rules.append(
                    # Un wrap using punctuation
                    (re.compile(u'(?<=.{%i}([a-zäëïöüàèìòùáćéíóńśúâêîôûçąężıãõñæøþðßě,:)\IA\u00DF]|(?<!\&\w{4});))\s*(?P<ital></(i|b|u)>)?\s*(</p>\s*<p>\s*)+\s*(?=(<(i|b|u)>)?\s*[\w\d$(])' % length, re.UNICODE), wrap_lines),
                )

        for rule in self.PREPROCESS + start_rules:
            html = rule[0].sub(rule[1], html)

        if get_preprocess_html:
            return html

        def dump(raw, where):
            import os
            dp = getattr(self.extra_opts, 'debug_pipeline', None)
            if dp and os.path.exists(dp):
                odir = os.path.join(dp, 'input')
                if os.path.exists(odir):
                    odir = os.path.join(odir, where)
                    if not os.path.exists(odir):
                        os.makedirs(odir)
                    name, i = None, 0
                    while not name or os.path.exists(os.path.join(odir, name)):
                        i += 1
                        name = '%04d.html'%i
                    with open(os.path.join(odir, name), 'wb') as f:
                        f.write(raw.encode('utf-8'))

        for rule in rules + end_rules:
            html = rule[0].sub(rule[1], html)

        html = XMLDECL_RE.sub('', html)

        if getattr(self.extra_opts, 'asciiize', False):
            from calibre.utils.localization import get_udc
            unihandecoder = get_udc()
            html = unihandecoder.decode(html)

        if getattr(self.extra_opts, 'enable_heuristics', False):
            from calibre.ebooks.conversion.utils import HeuristicProcessor
            preprocessor = HeuristicProcessor(self.extra_opts, self.log)
            html = preprocessor(html)

        unsupported_unicode_chars = self.extra_opts.output_profile.unsupported_unicode_chars
        if unsupported_unicode_chars:
            from calibre.utils.localization import get_udc
            unihandecoder = get_udc()
            for char in unsupported_unicode_chars:
                asciichar = unihandecoder.decode(char)
                html = html.replace(char, asciichar)

        return html
    
