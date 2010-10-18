#!/usr/bin/env python
# -*- coding: utf-8 -*-

def FileExtract(file):
    ''' 
    Recibe un fichero con el listado del episodio, lo convierte en una lista y 
    le quita los \n del final de la linea, lo vuelve a convertir en lista y
    lo devuelve 
    '''
    text_file = open(file, "r")
    urls = text_file.readlines()
    text_file.close()
    newurls = []
    for url in urls:
        newurls.append(url.replace('\n',''))
    return newurls

