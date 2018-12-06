# -*- coding: utf-8 -*-

import os
import ogr
import gdal
import osr
import logging

from ISO19115Creator import functions

#Set up logging
log = logging.getLogger(__name__)

class GdalData:
    """ 
    Class to read gdal supported raster files and extract specific metadata
    attributes. 
      
    Attributes: 
        inputdata (string): The path of the file to be opened. 
        dataset (osgeo.gdal.Dataset): GDAL Dataset
        driver (string): The long name of the driver e.g. GeoTIFF.
        projection (osgeo.osr.SpatialReference): Spatial Reference of the dataset.
        EPSG (string): The EPSG code of the Projection.
        geotransform (tuple): affine transform coefficients (https://www.gdal.org/gdal_datamodel.html)
        BBOX (list): List of the Bounding Box Coordinates (min Longitude ,min Latitude ,max Longitude ,max Latitude) 
        resolution (float): spatial Resolution of the dataset. Only available on raster datasets.         
    """
    
    def __init__(self, inputdata):
        """ 
        The constructor for the GDALData class. 
          
        Arguments: 
            inputdata (string): The path of the file to be opened.   
        """
        
        supportedRasterData = ['.tif', '.TIF']
        supportedVectorData = ['.shp', '.SHP']
        
        self.fileextension = os.path.splitext(inputdata)[1]
        
        if self.fileextension in supportedRasterData: 
            log.debug('Opening raster file')
            try:
                self.data = gdal.Open(inputdata)
            except:
                log.error('Failed to open raster file')
                raise
            self.driver = self.data.GetDriver().LongName
            self.geotransform = self.data.GetGeoTransform()
            self.resolution = self.geotransform[1]
            #In case no srs is defined fill all values with 'undefined'
            try:
                self.spatialRef = osr.SpatialReference(wkt=self.data.GetProjection())
                self.EPSG = functions.EPSGfromWKT(self.spatialRef)
                self.BBOX = self.getBoundingBox()
            except:
                log.debug('No EPSG or BBOX could be extracted')
                self.spatialRef = 'undefined'
                self.EPSG = 'undefined'
                self.BBOX = ['0','0','0','0']

        if self.fileextension in supportedVectorData:
            log.debug('Opening vector file')
            try:
                self.data = ogr.Open(inputdata)
            except:
                log.error('Failed to open vector file')
                raise
            self.driver = 'ESRI Shapefile'
            self.layer = self.data.GetLayer()
            self.resolution = None
            #In case no srs is defined fill all values with 'undefined'
            try:
                self.spatialRef = self.layer.GetSpatialRef()
                self.EPSG = functions.EPSGfromWKT(self.spatialRef)
                #Get bounding box from vector
                self.BBOX = [0,0,0,0]
                self.BBOX[0], self.BBOX[1], self.BBOX[2], self.BBOX[3] = self.layer.GetExtent() 
                if self.EPSG != '4326':
                    self.BBOX = functions.BBOXtoWGS84(self.BBOX, self.EPSG)
                #Convert to string
                self.BBOX[0] = str(self.BBOX[0])
                self.BBOX[1] = str(self.BBOX[1])
                self.BBOX[2] = str(self.BBOX[2])
                self.BBOX[3] = str(self.BBOX[3])
            except:
                log.debug('No EPSG or BBOX could be extracted')
                self.EPSG = 'undefined'
                self.BBOX = ['0','0','0','0']
                

        
    def getBoundingBox(self): 
        """ 
        Function to get the Bounding Box from the affine transform coefficients 
        (https://www.gdal.org/gdal_datamodel.html). Since the ISO19115-3 xml represents
        the coordinates of the BBOX as lat, lon the BBOX gets transformed to EPSG 4326
        if the coordinates are not already in this crs. 
        """
        
        #bbox = left,bottom,right,top
        #bbox = min Longitude , min Latitude , max Longitude , max Latitude
        BBOX = []
        BBOX.append(self.geotransform[0])
        BBOX.append(self.geotransform[3]+self.data.RasterYSize*self.geotransform[5])
        BBOX.append(self.geotransform[0]+self.data.RasterXSize*self.geotransform[1])
        BBOX.append(self.geotransform[3])
        
        if self.EPSG != '4326':
            self.BBOX = functions.BBOXtoWGS84(BBOX, self.EPSG)
            
        #Convert to string
        BBOX[0] = str(BBOX[0])
        BBOX[1] = str(BBOX[1])
        BBOX[2] = str(BBOX[2])
        BBOX[3] = str(BBOX[3])

        return BBOX
    
