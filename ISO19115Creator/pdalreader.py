import json
import pdal
import logging
 
from ISO19115Creator import functions

#Set up logging
log = logging.getLogger(__name__)

class PdalData:
    
    def __init__(self, inputdata):
        """ 
        The constructor for the GDALData class. 
          
        Arguments: 
            inputdata (string): The path of the file to be opened as a raw string!   
        """
        
        self.path = '"' + inputdata.replace("\\", "/")+ '"'
        self.jsonstring = """
                            {
                              "pipeline": [
                               """ + self.path + """
                              ]
                            }"""
        pipeline = pdal.Pipeline(self.jsonstring)
        try:
            pipeline.validate()
        except:
            log.error('Failed to validate pdal pipeline')
            raise
        try:
            pipeline.execute()
        except:
            log.error('Failed to execute pdal pipeline')
            raise
        self.metadata = json.loads(pipeline.metadata)
        log.debug('pdal metadata succesfully loaded')
        try:
            self.wkt = self.metadata['metadata']['readers.las'][0]['spatialreference']
            self.EPSG = functions.EPSGfromWKT(self.wkt)
            if self.EPSG == 'None':
                wkt_without_compdcs = self.wkt.split(',', 1)[-1]
                self.EPSG = functions.EPSGfromWKT(wkt_without_compdcs)
        except:
            log.error('Error getting EPSG from pdal metadata')
            raise
        try:
            self.BBOX = [0,0,0,0]
            self.BBOX[0] = self.metadata['metadata']['readers.las'][0]['minx']
            self.BBOX[1] = self.metadata['metadata']['readers.las'][0]['miny']
            self.BBOX[2] = self.metadata['metadata']['readers.las'][0]['maxx']
            self.BBOX[3] = self.metadata['metadata']['readers.las'][0]['maxy']
            if self.EPSG == 'None':
                self.BBOX[0] = '0'
                self.BBOX[1] = '0'
                self.BBOX[2] = '0'
                self.BBOX[3] = '0'
            elif self.EPSG != '4326':
                self.BBOX = functions.BBOXtoWGS84(self.BBOX, self.EPSG)
            #Convert to string
            self.BBOX[0] = str(self.BBOX[0])
            self.BBOX[1] = str(self.BBOX[1])
            self.BBOX[2] = str(self.BBOX[2])
            self.BBOX[3] = str(self.BBOX[3])
        except:
            log.error('Error getting Bounding Box from pdal metadata')
            raise
        

 



