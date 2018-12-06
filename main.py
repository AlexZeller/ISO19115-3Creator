import logging
import time
from halo import Halo
#from ISO19115Creator import xmlschematest

#Get execution time
start_time = time.time()

#Set up logging
logging.basicConfig(filename='logfile.log',filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

#Import after the logging set up to allow for proper logging between modules
from ISO19115Creator import metacrawler

#Directory to be crawled
rootDir = r'F:\20170328_Bernkastel'

#Default Information
defaultLocale = 'en'
resourceScope = 'dataset'
roleCode = 'user'
Organisation = 'University of Trier: Departement of Environmental Remote Sensing and Geoinformatics'
ProgressCode = 'onGoing'
ClassificationCode = 'unclassified'

defaultValues = [defaultLocale, resourceScope, roleCode, Organisation, ProgressCode, ClassificationCode]

#Start spinner to indicate progress
spinner = Halo(text='Crawling Directory '+rootDir, spinner='dots')
spinner.start()
   
#Initiate crawler and create metadata
crawler = metacrawler.Crawler(rootDir, defaultValues)
crawler.createMetadata()

#Stop spinner
spinner.succeed(text='Successful')
print("\nExecution Time: %s seconds. \n%d xml files created" % ((time.time() - start_time), crawler.number))

#xmlschematest.checkXML(r'F:\20170328_Bernkastel\RGB_thermal.xml')
    

 