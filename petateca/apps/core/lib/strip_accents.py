import unicodedata


def strip_accents(string):
    return unicodedata.normalize('NFKD', string).encode('ascii','ignore')
