# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 12:31:46 2018

@author: s6alzell
"""

from owslib.csw import CatalogueServiceWeb
from owslib.fes import PropertyIsEqualTo, PropertyIsLike, BBox

csw = CatalogueServiceWeb('http://136.199.176.14:8080/geonetwork/srv/en/csw')
csw.identification.type

 
query = PropertyIsEqualTo('csw:AnyText', 'sirius')
csw.getrecords2(constraints=[query])
csw.results

for rec in csw.records:
    print(csw.records[rec].title)
    

