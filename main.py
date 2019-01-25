# -*- coding: utf-8 -*-

import logging
import time
from halo import Halo
#import module to test the xml for syntax and the correct schema. Takes very long and only works when the schema location is
#set in the xml file
#from ISO19115Creator import xmlschematest

#Get execution time
start_time = time.time()

#Set up logging
logging.basicConfig(filename='logfile.log',filemode='w', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

#Import after the logging set up to allow for proper logging between modules
from ISO19115Creator import metacrawler

#Directory to be crawled

######################
rootDir = r'D:test'
######################

#Default Information
defaultLocale = 'en'
resourceScope = 'dataset'
roleCode = 'user'
Organisation = 'University of Trier: Departement of Environmental Remote Sensing and Geoinformatics'
Abstract = 'This file was automatically generated and has no Abstract. '
Keywords = ['Remote Sensing', 'Automatic Generation']
ProgressCode = 'onGoing'
ClassificationCode = 'unclassified'

defaultValues = [defaultLocale, resourceScope, roleCode, Organisation, Abstract, Keywords, ProgressCode, ClassificationCode]

#CSW information for the insert of the xml
csw_url = 'http://136.199.176.14:8080/geonetwork/srv/en/csw-publication'
user = 'admin'
passwd = 'admin'

#Start spinner to indicate progress
spinner = Halo()
spinner.start()
   
###Initiate crawler and create metadata
crawler = metacrawler.Crawler(rootDir, defaultValues, csw_url, user, passwd, upload=False)
crawler.createMetadata()

#Stop spinner
spinner.succeed()
print("\nExecution Time: %s seconds. \n%d xml files created" % ((time.time() - start_time), crawler.number))

#Schema test
#xmlschematest.checkXML(r'G:\Test_Data\shp\Kehlen_Nagem_2011.xml')

    

 