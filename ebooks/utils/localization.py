#!/usr/bin/env python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import absolute_import

__license__   = 'GPL v3'
__copyright__ = '2009, Kovid Goyal <kovid@kovidgoyal.net>'
__docformat__ = 'restructuredtext en'

import os, locale, re, cStringIO, cPickle
from gettext import GNUTranslations, NullTranslations
from zipfile import ZipFile

_available_translations = None

def available_translations():
    global _available_translations
    if _available_translations is None:
        stats = P('localization/stats.pickle', allow_user_override=False)
        if os.path.exists(stats):
            stats = cPickle.load(open(stats, 'rb'))
        else:
            stats = {}
        _available_translations = [x for x in stats if stats[x] > 0.1]
    return _available_translations

def get_lang():
    'Try to figure out what language to display the interface in'
    from .config_base import prefs
    lang = prefs['language']
    lang = os.environ.get('CALIBRE_OVERRIDE_LANG', lang)
    if lang is not None:
        return lang
    try:
        lang = locale.getdefaultlocale(['LANGUAGE', 'LC_ALL', 'LC_CTYPE',
                                    'LC_MESSAGES', 'LANG'])[0]
    except:
        pass # This happens on Ubuntu apparently
    if lang is None and os.environ.has_key('LANG'): # Needed for OS X
        try:
            lang = os.environ['LANG']
        except:
            pass
    if lang:
        match = re.match('[a-z]{2,3}(_[A-Z]{2}){0,1}', lang)
        if match:
            lang = match.group()
    if lang == 'zh':
        lang = 'zh_CN'
    if lang is None:
        lang = 'en'
    return lang

def get_lc_messages_path(lang):
    hlang = None
    if zf_exists():
        if lang in available_translations():
            hlang = lang
        else:
            xlang = lang.split('_')[0]
            if xlang in available_translations():
                hlang = xlang
    return hlang

def zf_exists():
    return os.path.exists(P('localization/locales.zip',
                allow_user_override=False))

def set_translators():
    # To test different translations invoke as
    # CALIBRE_OVERRIDE_LANG=de_DE.utf8 program
    lang = get_lang()
    if lang:
        buf = iso639 = None
        mpath = get_lc_messages_path(lang)
        if mpath and os.access(mpath+'.po', os.R_OK):
            from calibre.translations.msgfmt import make
            buf = cStringIO.StringIO()
            make(mpath+'.po', buf)
            buf = cStringIO.StringIO(buf.getvalue())

        if mpath is not None:
            with ZipFile(P('localization/locales.zip',
                allow_user_override=False), 'r') as zf:
                if buf is None:
                    buf = cStringIO.StringIO(zf.read(mpath + '/messages.mo'))
                if mpath == 'nds':
                    mpath = 'de'
                isof = mpath + '/iso639.mo'
                try:
                    iso639 = cStringIO.StringIO(zf.read(isof))
                except:
                    pass # No iso639 translations for this lang

        t = None
        if buf is not None:
            t = GNUTranslations(buf)
            if iso639 is not None:
                iso639 = GNUTranslations(iso639)
                t.add_fallback(iso639)

        if t is None:
            t = NullTranslations()

        t.install(unicode=True, names=('ngettext',))

_iso639 = None
_extra_lang_codes = {
        'pt_BR' : 'Brazilian Portuguese',
        'en_GB' : 'English (UK)',
        'zh_CN' : 'Simplified Chinese',
        'zh_HK' : 'Chinese (HK)',
        'zh_TW' : 'Traditional Chinese',
        'en'    : 'English',
        'en_AU' : 'English (Australia)',
        'en_NZ' : 'English (New Zealand)',
        'en_CA' : 'English (Canada)',
        'en_GR' : 'English (Greece)',
        'en_IN' : 'English (India)',
        'en_TH' : 'English (Thailand)',
        'en_TR' : 'English (Turkey)',
        'en_CY' : 'English (Cyprus)',
        'en_CZ' : 'English (Czechoslovakia)',
        'en_PK' : 'English (Pakistan)',
        'en_HR' : 'English (Croatia)',
        'en_ID' : 'English (Indonesia)',
        'en_IL' : 'English (Israel)',
        'en_SG' : 'English (Singapore)',
        'en_YE' : 'English (Yemen)',
        'en_IE' : 'English (Ireland)',
        'en_CN' : 'English (China)',
        'en_ZA' : 'English (South Africa)',
        'es_PY' : 'Spanish (Paraguay)',
        'es_UY' : 'Spanish (Uruguay)',
        'es_AR' : 'Spanish (Argentina)',
        'es_MX' : 'Spanish (Mexico)',
        'es_CU' : 'Spanish (Cuba)',
        'es_CL' : 'Spanish (Chile)',
        'es_EC' : 'Spanish (Ecuador)',
        'es_HN' : 'Spanish (Honduras)',
        'es_VE' : 'Spanish (Venezuela)',
        'es_BO' : 'Spanish (Bolivia)',
        'es_NI' : 'Spanish (Nicaragua)',
        'es_CO' : 'Spanish (Colombia)',
        'de_AT' : 'German (AT)',
        'fr_BE' : 'French (BE)',
        'nl'    : 'Dutch (NL)',
        'nl_BE' : 'Dutch (BE)',
        'und'   : 'Unknown',
        }

_lcase_map = {}
for k in _extra_lang_codes:
    _lcase_map[k.lower()] = k

def get_language(lang):
    global _iso639
    translate = _
    lang = _lcase_map.get(lang, lang)
    if lang in _extra_lang_codes:
        # The translator was not active when _extra_lang_codes was defined, so
        # re-translate
        return translate(_extra_lang_codes[lang])
    ip = P('localization/iso639.pickle')
    if not os.path.exists(ip):
        return lang
    if _iso639 is None:
        _iso639 = cPickle.load(open(ip, 'rb'))
    ans = lang
    lang = lang.split('_')[0].lower()
    if len(lang) == 2:
        ans = _iso639['by_2'].get(lang, ans)
    elif len(lang) == 3:
        if lang in _iso639['by_3b']:
            ans = _iso639['by_3b'][lang]
        else:
            ans = _iso639['by_3t'].get(lang, ans)
    return translate(ans)


_udc = None

def get_udc():
    global _udc
    if _udc is None:
        from ..unihandecode import Unihandecoder
        _udc = Unihandecoder(lang=get_lang())
    return _udc


