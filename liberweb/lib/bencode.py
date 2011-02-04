"""
===================
HunnyB (de|en)coder
===================

Something like "Bencode remixed"
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

HunnyB implements the `bencode`_ encoding/decoding originally
created by `Petru Paler`_ for use in the guts of `BitTorrent`_,
brainchild of `Bram Cohen`_.  
        
        >>> from lib import bencode as hunnyb

Import of the hunnyb module will register the encode/decode functions 
with the standard library `codecs`_ module, meaning strings may be 
encoded in one of the following ways:

        >>> "foobaz hambones".encode('hunnyb')
        '15:foobaz hambones'
        
        >>> "foobaz hambones".encode('hb')
        '15:foobaz hambones'
        
        >>> "foobaz hambones".encode('bencode')
        '15:foobaz hambones'
        
        >>> "foobaz hambones".encode('b')
        '15:foobaz hambones'


Likewise, bencoded strings may be decoded, although the result will always
be a string (a requirement of `codecs`_), meaning one will have to 
``eval()`` said result if not of string type.

        >>> enc_str = "ForkingHam BIZZYBONE RazzMATAZZ".encode('hb')

        >>> print enc_str
        31:ForkingHam BIZZYBONE RazzMATAZZ

        >>> enc_str.decode('hb')
        'ForkingHam BIZZYBONE RazzMATAZZ'

        >>> enc_dict = hunnyb.encode({'foo': 99000, 0: [99, 8, 'bobob']})

        >>> print enc_dict
        d1:0li99ei8e5:bobobe3:fooi99000ee
        
        >>> enc_dict.decode('bencode')
        "{'0': [99, 8, 'bobob'], 'foo': 99000}"


Alternatively, the ``encode`` and ``decode`` functions available in 
``hunnyb`` may be used directly, with decoding always returning a 
given object's Python equivalent.

        >>> hunnyb.decode(enc_dict)
        {'0': [99, 8, 'bobob'], 'foo': 99000}


.. _bencode: http://en.wikipedia.org/wiki/Bencode
.. _Petru Paler: http://petru.paler.net/
.. _BitTorrent: http://www.bittorrent.com/what-is-bittorrent
.. _Bram Cohen: http://en.wikipedia.org/wiki/Bram_Cohen
.. _codecs: http://docs.python.org/lib/module-codecs.html
.. vim:filetype=rst
"""
# 2008 Dan Buch daniel.buch@gmail.com - Licensed MIT
        
import codecs as _codecs
from encodings import aliases as _aliases


HUNNYB_ENC_NAME = "hunnyb"
HB = 'hb'
HB_ALIASES = (HB, 'bencode', 'benc', 'b')
INT_BEGIN = 'i'
LIST_BEGIN = 'l'
DICT_BEGIN = 'd'
STR_BEGIN0 = '0'
STR_BEGIN1 = '1'
STR_BEGIN2 = '2'
STR_BEGIN3 = '3'
STR_BEGIN4 = '4'
STR_BEGIN5 = '5'
STR_BEGIN6 = '6'
STR_BEGIN7 = '7'
STR_BEGIN8 = '8'
STR_BEGIN9 = '9'
ENC_END = 'e'
ENC_JOIN = ':'
_DECODE_FUNCS_CACHE = {}
_ENCODE_FUNCS_CACHE = {}
INT = 0
LNG = 1
STR = 2
LST = 3
TUP = 4
DCT = 5
BOO = 6


class HunnyBError(Exception):
    pass


class HunnyBDecodingError(HunnyBError):
    pass


def _hunnyb_search_func(name):
    """search function required by ``codecs.register``"""
    if name in (HUNNYB_ENC_NAME,) + HB_ALIASES:
        return (_encode, _decode, None, None)


def _label_duck(obj):
    if isinstance(obj, basestring):
        return STR
    elif str(obj).isdigit():
        return INT
    elif hasattr(obj, 'append') and hasattr(obj, 'index'):
        return LST
    elif hasattr(obj, '__iter__') and not hasattr(obj, 'append') \
            and not hasattr(obj, 'items'):
        return TUP
    elif hasattr(obj, 'items') and hasattr(obj, 'keys') \
            and hasattr(obj, 'values'):
        return DCT
    elif str(obj) in ('True', 'False'):
        return BOO
    else:
        raise HunnyBError("not an encodeable object: " + str(obj))


def _decode_int(obj, count):
    count += 1
    new_count = obj.index(ENC_END, count)
    num = int(obj[count:new_count])
    if obj[count] == '-':
        if obj[count + 1] == STR_BEGIN0:
            raise HunnyBDecodingError 
    elif obj[count] == STR_BEGIN0 and new_count != count + 1:
        raise HunnyBDecodingError
    return (num, new_count + 1)


def _decode_string(obj, count):
    colon = obj.index(ENC_JOIN, count)
    num = int(obj[count:colon])
    if obj[count] == STR_BEGIN0 and colon != count + 1:
        raise HunnyBDecodingError 
    colon += 1
    return (obj[colon:colon + num], colon + num)


def _decode_list(obj, count, dec_funcs=_DECODE_FUNCS_CACHE):
    buf = []
    count += 1
    while obj[count] != ENC_END:
        item, count = dec_funcs[obj[count]](obj, count)
        buf.append(item)
    return (buf, count + 1)


def _decode_dict(obj, count, dec_str=_decode_string, 
        dec_funcs=_DECODE_FUNCS_CACHE):
    ret = {}
    count += 1
    while obj[count] != ENC_END:
        key, count = dec_str(obj, count)
        ret[key], count = dec_funcs[obj[count]](obj, count)
    return (ret, count + 1)


def _decode(obj, decode_funcs=_DECODE_FUNCS_CACHE, stringify=True):
    try:
        ret, length = decode_funcs[obj[0]](obj, 0)
    except HunnyBDecodingError:
        raise HunnyBError("not a hunnyb-encoded string")
    if length != len(obj):
        raise HunnyBError("not a valid encoded value")
    if stringify:
        return (str(ret), len(ret))
    else:
        return (ret, len(ret))


def decode(obj, decode_funcs=_DECODE_FUNCS_CACHE, dec=_decode):
    """decode bencoded string, returning python object"""
    return dec(obj, decode_funcs, False)[0]


def _encode_int(obj, buf):
    buf.extend(['i', str(obj), 'e'])


def _encode_bool(obj, buf, enc_int=_encode_int):
    if obj:
        enc_int(1, buf)
    else:
        enc_int(0, buf)

        
def _encode_string(obj, buf):
    buf.extend([str(len(obj)), ':', obj])


def _encode_list(obj, buf, enc_funcs=_ENCODE_FUNCS_CACHE):
    buf.append('l')
    for item in obj:
        enc_funcs[_label_duck(item)](item, buf)
    buf.append('e')


def _encode_dict(obj, buf, enc_funcs=_ENCODE_FUNCS_CACHE):
    buf.append('d')
    for key, val in sorted(obj.items()):
        buf.extend([str(len(str(key))), ':', key])
        enc_funcs[_label_duck(val)](val, buf)
    buf.append('e')


def _encode(obj, enc_funcs=_ENCODE_FUNCS_CACHE):
    lstbuf = []
    enc_funcs[_label_duck(obj)](obj, lstbuf)
    ret = ''.join([str(i) for i in lstbuf])
    return (ret, len(ret))


def encode(obj, enc_funcs=_ENCODE_FUNCS_CACHE, enc=_encode):
    """encode given object, returning bencoded string"""
    return enc(obj, enc_funcs)[0]


# register with codecs, aliases set in encodings.aliases
_codecs.register(_hunnyb_search_func)
_aliases.aliases.update(
    dict([(__a, HUNNYB_ENC_NAME) for __a in HB_ALIASES]))

# function mappings
_DECODE_FUNCS_CACHE[INT_BEGIN] = _decode_int
_DECODE_FUNCS_CACHE[LIST_BEGIN] = _decode_list
_DECODE_FUNCS_CACHE[DICT_BEGIN] = _decode_dict
_DECODE_FUNCS_CACHE[STR_BEGIN0] = _decode_string
_DECODE_FUNCS_CACHE[STR_BEGIN1] = _decode_string
_DECODE_FUNCS_CACHE[STR_BEGIN2] = _decode_string
_DECODE_FUNCS_CACHE[STR_BEGIN3] = _decode_string
_DECODE_FUNCS_CACHE[STR_BEGIN4] = _decode_string
_DECODE_FUNCS_CACHE[STR_BEGIN5] = _decode_string
_DECODE_FUNCS_CACHE[STR_BEGIN6] = _decode_string
_DECODE_FUNCS_CACHE[STR_BEGIN7] = _decode_string
_DECODE_FUNCS_CACHE[STR_BEGIN8] = _decode_string
_DECODE_FUNCS_CACHE[STR_BEGIN9] = _decode_string
_ENCODE_FUNCS_CACHE[INT] = _encode_int
_ENCODE_FUNCS_CACHE[BOO] = _encode_bool
_ENCODE_FUNCS_CACHE[LNG] = _encode_int
_ENCODE_FUNCS_CACHE[STR] = _encode_string
_ENCODE_FUNCS_CACHE[LST] = _encode_list
_ENCODE_FUNCS_CACHE[TUP] = _encode_list
_ENCODE_FUNCS_CACHE[DCT] = _encode_dict

# vim:fileencoding=utf-8
