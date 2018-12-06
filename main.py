# -*- coding: utf-8 -*-

import logging
import time
from halo import Halo
from ISO19115Creator import xmlschematest

#Get execution time
start_time = time.time()

#Set up logging
logging.basicConfig(filename='logfile.log',filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

#Import after the logging set up to allow for proper logging between modules
from ISO19115Creator import metacrawler

#Directory to be crawled
rootDir = r'G:\Test_Data\shp'

#Default Information
defaultLocale = 'en'
resourceScope = 'dataset'
roleCode = 'user'
Organisation = 'University of Trier: Departement of Environmental Remote Sensing and Geoinformatics'
Abstract = 'This file was automatically generated and has no Abstract'
ProgressCode = 'onGoing'
ClassificationCode = 'unclassified'

defaultValues = [defaultLocale, resourceScope, roleCode, Organisation, Abstract, ProgressCode, ClassificationCode]

#Start spinner to indicate progress
spinner = Halo(text='Crawling Directory '+rootDir, spinner='dots')
spinner.start()
   
#Initiate crawler and create metadata
crawler = metacrawler.Crawler(rootDir, defaultValues)
crawler.createMetadata()

#Stop spinner
spinner.succeed()
print("\nExecution Time: %s seconds. \n%d xml files created" % ((time.time() - start_time), crawler.number))

xmlschematest.checkXML(r'G:\Test_Data\shp\Kehlen_Nagem_2011.xml')
    

 