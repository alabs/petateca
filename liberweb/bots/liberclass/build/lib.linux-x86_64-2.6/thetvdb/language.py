#!/usr/bin/env python
# -*- coding: utf-8 -*-

from thetvdb.mirror import Mirror
import random
from thetvdb.config import API_KEY, USER_AGENT
import urllib
from xml.dom import minidom

class Language(object):

    def __init__(self):
        """
        Abre el fichero XML con la lista de lenguajes
        """
        mirror = Mirror()
        xml_mirrors = mirror.get_xml_mirrors()
        xml_mirror = random.choice(xml_mirrors)
        languages_url = xml_mirror + "/api/%s/languages.xml" % (API_KEY)
        urllib.URLopener.version = USER_AGENT 
        f = urllib.urlopen(languages_url)
        self.xml_doc = f.read()
        f.close()

    def get_languages(self):
        """
        Devuelve un diccionario con el id como clave y el lenguaje
        como valor
        """
        ids = []
        langs = []
        doc = minidom.parseString(self.xml_doc)
        for node in doc.getElementsByTagName('id'):
            ids.append(node.firstChild.nodeValue)
        for node in doc.getElementsByTagName('name'):
            langs.append(node.firstChild.nodeValue)

        return dict(zip(ids, langs))

    def get_abbreviations(self):
        """
        Devuelve un diccionario con el id como calve y la abreviación del
        lenguaje como valor
        """
        ids = []
        abbr = []
        doc = minidom.parseString(self.xml_doc)
        for node in doc.getElementsByTagName('id'):
            ids.append(node.firstChild.nodeValue)
        for node in doc.getElementsByTagName('abbreviation'):
            abbr.append(node.firstChild.nodeValue)

        return dict(zip(ids, abbr))

