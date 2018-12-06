# -*- coding: utf-8 -*-

import logging
from sridentify import Sridentify
from pyproj import Proj, transform

#Set up logging
log = logging.getLogger(__name__)
  
def EPSGfromWKT(wkt):
    """ 
    Function to get the EPSG code from the WKT (Well-Known-Text).
    
    Arguments: 
        wkt: The WKT.
    """
    try:
        ident = Sridentify(prj=str(wkt))
        EPSG = ident.get_epsg()
    except:
        log.error('Failed to get EPSG from WKT')
        raise
    
    return str(EPSG)


def BBOXtoWGS84(BBOX, inputProjectionEPSG):
    """ 
    Function to transform Bounding Box coordinates to WGS84 for lat, long 
    representation in ISO19115-3 xml.
    
    Arguments: 
        BBOX (array): The BBOX to tranform.
        inputProjectionEPSG (string): The EPSG Code of the input BBOX.
    """
    try:
        inProj = Proj(init='epsg:' + inputProjectionEPSG)
        outProj = Proj(init='epsg:4326')
        #Careful with the order of the BBOX
        x = [BBOX[0], BBOX[2]]
        y = [BBOX[1], BBOX[3]] 
        x, y = transform(inProj,outProj,x, y)
        BBOX[0],BBOX[1], BBOX[2], BBOX[3] = x[0], y[0], x[1], y[1]
    except:
        log.error('Failed to convert Bounding Box to WGS84')
        raise

    return BBOX