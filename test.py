from ISO19115Creator import gdalreader
from ISO19115Creator import functions
import gdal
import osr
import sridentify
rootDir = r'D:\test\dem.tif'

test = gdalreader.GdalData(rootDir)

print(test.getBoundingBox())


test = gdal.Open(rootDir)
print(test.GetProjection())
print(test)
print(test.getBoundingBox())
spatialRef = osr.SpatialReference(wkt=test.GetProjection())
print (spatialRef)

test2 = functions.EPSGfromWKT(spatialRef)

test = sridentify.Sridentify(prj='PROJCS["unnamed",GEOGCS["ETRS89",DATUM["unknown",SPHEROID["GRS 1980",6378137,298.2572221010042,AUTHORITY["EPSG","7019"]],AUTHORITY["EPSG","6258"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4258"]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",9],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AUTHORITY["EPSG","25832"]]', epsg_code=25832)
test.save_to_db()
help(sridentify)

from owslib.etree import etree
import io

XML=r"D:\test\dem.xml"

record=open(XML, 'rb').read()
record
etree.fromstring(record)
