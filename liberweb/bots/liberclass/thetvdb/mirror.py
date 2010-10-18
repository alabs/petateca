#!/usr/bin/env python
# -*- coding: utf-8 -*-

from thetvdb.config import API_KEY, USER_AGENT
import urllib
from xml.dom import minidom

class Mirror(object):
    
    def __init__(self):
        """
        Abre el fichero XML con la lista de mirrors
        """
        mirrors_url = "http://www.thetvdb.com/api/%s/mirrors.xml" % (API_KEY)
        urllib.URLopener.version = USER_AGENT 
        f = urllib.urlopen(mirrors_url)
        self.xml_doc = f.read()
        f.close()

    def get_mirrors(self):
        """
        Devuelve un diccionario con el typemask como clave y
        la URL del mirror como valor
        """
        typemasks = []
        mirrors_url = []
        doc = minidom.parseString(self.xml_doc)
        for node in doc.getElementsByTagName('typemask'):
            typemasks.append(node.firstChild.nodeValue)
        for node in doc.getElementsByTagName('mirrorpath'):
            mirrors_url.append(node.firstChild.nodeValue)
        
        return dict(zip(typemasks, mirrors_url))

    def get_rol_of_mirror(self, rol):
        """
        Devuelve el mirror para un rol dado
        """
        mirrors = self.get_mirrors()
        for k, v in mirrors.iteritems():
            if rol == k:
                return v

    def get_xml_mirrors(self):
        """
        Devuelve una lista de mirrors que sirven XML
        """
        data = []
        data.append(self.get_rol_of_mirror('1'))
        data.append(self.get_rol_of_mirror('3'))
        data.append(self.get_rol_of_mirror('5'))
        data.append(self.get_rol_of_mirror('7'))

        return [k for k in data if k != None]

    def get_banner_mirrors(self):
        """
        Devuelve una lista de mirrors que sirven banners
        """
        data = []
        data.append(self.get_rol_of_mirror('2'))
        data.append(self.get_rol_of_mirror('3'))
        data.append(self.get_rol_of_mirror('6'))
        data.append(self.get_rol_of_mirror('7'))
        
        return [k for k in data if k != None]

    def get_zip_mirrors(self):
        """
        Devuelve una lista de mirrors que sirven ficheros ZIP
        """
        data = []
        data.append(self.get_rol_of_mirror('4'))
        data.append(self.get_rol_of_mirror('5'))
        data.append(self.get_rol_of_mirror('6'))
        data.append(self.get_rol_of_mirror('7'))

        return [k for k in data if k != None]

