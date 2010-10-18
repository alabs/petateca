#!/usr/bin/env python
# -*- coding: utf-8 -*-

class AskLetter(object):
    '''
    Receives letter and name and returns import_file and export_file
    '''
    def __init__ (self, letter, name):
        self.letter = letter
        self.name = name
    def __new__( self, letter, name):
        import_file = 'sites/' + name + '/showlist/' + letter + '.txt'
        export_file = 'sites/' + name + '/dump/' + letter + '.json'
        return import_file, export_file

class AskLetterEspoilerTV(object):
    '''
    Receives letter based on EspoilerTV and returns import_url and export_file
    http://espoilertv.com/filtro/?b=A
    '''
    def __init__ (self, letter, name):
        self.letter = letter
        self.name = name
    def __new__( self, letter, name):
        import_url = 'http://espoilertv.com/filtro/?b=' + letter
        export_file = 'sites/' + name + '/dump/' + letter + '.json'
        return import_url, export_file

class AskRSSLetter(object):
    '''
    Receives letter and name and returns export_rss_file
    '''
    def __init__ (self, name):
        self.name = name
    def __new__( self, name):
        from time import gmtime, strftime
	date = strftime("%Y%m%d-%H%M", gmtime())
        export_rss_file = 'sites/' + name + '/rss/' + date + '.json'
        return export_rss_file
