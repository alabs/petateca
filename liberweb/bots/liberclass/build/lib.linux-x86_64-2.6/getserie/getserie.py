#!/usr/bin/python

from xml.dom import minidom
from thetvdb.tool import Tool 

class GetSerie(object):
    '''
    Receives letter and name and returns import_file and export_file
    '''
    def __init__ (self, serie):
        self.serie = serie

    def swap_dictionary(self, original_dict):
        ''' Swap values/keys '''
        return dict([(v, k) for (k, v) in original_dict.iteritems()])
    
    def xml_get_text(self, nodelist):
        ''' Get Text from NodeList (minidom) ''' 
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)
    
    def get_serie(self):
        ''' Receives a serie an return a dict with all the data '''
        t = Tool()
        # little hack to ask for name instead of ID
        query = self.swap_dictionary(t.get_series(self.serie))
        serie_id = query.get(self.serie)
        try:
            s = t.get_serie_information(serie_id,'en')
            doc = minidom.parseString(s['en'])
            
            keys = { 'actors': 'Actors', 
                     'genre': 'Genre', 
                     'imdbid': 'IMDB_ID', 
                     'lang': 'Language', 
                     'network': 'Network', 
                     'description': 'Overview', 
                     'runtime': 'Runtime', 
                     'name': 'SeriesName', 
                     'status': 'Status' }
            
            special_keys = ('actors', 'genre') # list separate in '|'
            
            for k in keys: 
               tag = keys.get(k)
               keys[k] = self.xml_get_text(doc.getElementsByTagName(tag)[0].childNodes)
            
            for k in special_keys:
                keys[k] = keys[k].strip('|').split('|')
       
            return keys
        except:
            print "FUCKER"

if '__name__' == '__main__':
    pass
