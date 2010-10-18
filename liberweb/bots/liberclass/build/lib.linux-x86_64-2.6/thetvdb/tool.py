#!/usr/bin/env python
# -*- coding: utf-8 -*-

from thetvdb.mirror import Mirror
import random
from thetvdb.config import USER_AGENT, API_KEY
import urllib
from xml.dom import minidom
from zipfile import ZipFile
import re

class Tool(object):

    def __init__(self):
        """
        Crea tres variables de mirrors por tipo
        """
        mirror = Mirror()
        self.xmlmirror = random.choice(mirror.get_xml_mirrors())
        self.bannermirror = random.choice(mirror.get_banner_mirrors())
        self.zipmirror = random.choice(mirror.get_zip_mirrors())

    def get_server_time(self):
        """
        Obtiene la hora del servidor del webservice
        """
        server_time_url = 'http://www.thetvdb.com/api/Updates.php?type=none'
        urllib.URLopener.version = USER_AGENT
        f = urllib.urlopen(server_time_url)
        xml_doc = f.read()
        f.close()

        doc = minidom.parseString(xml_doc)
        for node in doc.getElementsByTagName('Time'):
            self.servertime = node.firstChild.nodeValue

        return self.servertime

    def get_series(self, name):
        """
        Devuelve un diccionario con el id de la serie como clave y el nombre
        de la serie como valor
        """
        series_url = 'http://www.thetvdb.com/api/GetSeries.php?seriesname='
        serie_name = urllib.quote(name)
        series_url += serie_name

        urllib.URLopener.version = USER_AGENT
        f = urllib.urlopen(series_url)
        xml_doc = f.read()
        f.close()

        doc = minidom.parseString(xml_doc)
        seriesid = []
        seriesname = []
        for node in doc.getElementsByTagName('seriesid'):
            seriesid.append(node.firstChild.nodeValue)
        for node in doc.getElementsByTagName('SeriesName'):
            seriesname.append(node.firstChild.nodeValue)

        return dict(zip(seriesid, seriesname))

    def get_bulk_serie_information(self, serie_id, language):
        """
        Devuelve un diccionario con información de la serie.
        data['LANG'] es información general de la serie.
        data['banners'] es información de donde están los banners.
        data['actors'] es información de los actores de la serie.
        """
        zip_url = self.zipmirror + "/api/%s/series/%s/all/%s.zip" % (API_KEY, serie_id, language)

        urllib.URLopener.version = USER_AGENT
        fh = urllib.urlretrieve(zip_url, '/tmp/serie_information.zip')
        zipfile = ZipFile('/tmp/serie_information.zip', 'r')

        data = {}
        for archive in zipfile.namelist():
            archive = re.sub('\.xml', '', archive)
            fh = open("/tmp/%s" % archive, 'w')
            fh.write(zipfile.read(archive + '.xml'))
            fh.close()
            fh = open("/tmp/%s" % archive, 'r')
            data[archive] = fh.read()
            fh.close()

        return data

    def get_serie_information(self, serie_id, language):
        """
        Devuelve un diccionario con la información de las serie
        """
        bulk_data = self.get_bulk_serie_information(serie_id, language)
        
        # Diccionario donde está la info de la serie
        xml_doc = minidom.parseString(bulk_data['es'])

        # Diccionario que devolveremos
        data = {}

        # Extraer el nombre de la serie
        for node in xml_doc.getElementsByTagName('SeriesName'):
            data['name'] = node.firstChild.nodeValue

        # Extraer el nombre de la red de televisión
        for node in xml_doc.getElementsByTagName('Network'):
            data['network'] = node.firstChild.nodeValue

        # Extraer los géneros
        for node in xml_doc.getElementsByTagName('Genre'):
            data['genres'] = tuple(item for item in node.firstChild.nodeValue.split('|') if item.strip())

        # Extraer el runtime de la serie
        for node in xml_doc.getElementsByTagName('Runtime'):
            data['runtime'] = node.firstChild.nodeValue

        # Extraer los actores de la serie
        for node in xml_doc.getElementsByTagName('Actors'):
            data['actors'] = tuple(item for item in node.firstChild.nodeValue.split('|') if item.strip())

        # Extraer la descripción de la serie
        data['description'] = xml_doc.getElementsByTagName('Overview')[0].firstChild.nodeValue

        return data

