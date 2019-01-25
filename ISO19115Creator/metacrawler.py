# -*- coding: utf-8 -*-

import logging
import os
import uuid
import datetime

from ISO19115Creator import stringinformation
from ISO19115Creator import gdalreader
from ISO19115Creator import metadatawriter
from ISO19115Creator import pdalreader
from ISO19115Creator import functions

#Set up logging
log = logging.getLogger(__name__)

class Crawler:
    """ 
    Class to crawl a specific directory and all the subdirectories and files,
    to search for files with of a specific file extension.
    Catchwords and date informations are, if possible extracted by the directory
    and filenames. 
      
    Attributes: 
        rootDir (string): The path of the directory to be crawled.
        number (integer): The number of created .xml files
        Catchwords (list): A list of extracted Catchwords.
        fileextensions (tuple): A list of the file extensions that are to be searched.  
    """
    
    def __init__(self, rootDir, defaultValues, cswURL, username, password, upload=False):
        """ 
        The constructor for the Crawler class. 
          
        Arguments: 
            rootDir (string): The path of the directory to be crawled. 
            defaultValues (list): A list of certain default values for the xml. 
            CSW_URL (string): The URL of the Geonetwork CSW publication server.
            username (string): The username to authenticate with.
            password (string): The password of the user.
            upload (Boolean): Specify wheather to upload the file to Geonetwork or not.
        """
        
        self.rootDir = rootDir
        self.number = 0
        self.cswURL = cswURL
        self.username = username
        self.password = password
        self.upload = upload
        #Extract possible Date, Catchwords of the root directory 
        self.rootDate = stringinformation.searchDate(os.path.basename(os.path.normpath(self.rootDir)))
        self.Catchwords = stringinformation.searchCatchwords(os.path.basename(os.path.normpath(self.rootDir)))
        self.rasterExtensions = ('.img','tif','.IMG','.TIF')
        self.vectorExtensions = ('.shp','.SHP')
        self.pointcloudExtensions = ('.las', '.LAS')
        self.defaultLocale = defaultValues[0]
        self.resourceScope = defaultValues[1]
        self.roleCode = defaultValues[2]
        self.Organisation = defaultValues[3]
        self.Abstract = defaultValues[4]
        self.Keywords = defaultValues[5]
        self.ProgressCode = defaultValues[6]
        self.ClassificationCode = defaultValues[7]
        
        log.info('Crawler successfully initialized. root dir: %s', rootDir)
        
    def createMetadata(self):
        """ 
        Function to start the crawler and create .xml metadata files. 
          
        Arguments: 
            rootDir (string): The path of the directory to be crawled.   
        """
        
        for dirName, subdirList, fileList in os.walk(self.rootDir):
            #Add Catchwords extracted from directory name to Catchwords list
            Catchwords = self.Catchwords
            Catchwords.extend(stringinformation.searchCatchwords(os.path.basename(os.path.normpath(dirName))))
            #Extract possible Date information from directory
            dirdate = stringinformation.searchDate(os.path.basename(os.path.normpath(dirName)))
            #If no Date could be found use rootDate
            if dirdate == 'undefined':
                dirdate = self.rootDate
            for fname in fileList:                                
                #Create metadata only for files with certain extension
                if fname.endswith(self.rasterExtensions + self.vectorExtensions):
                    log.info('Opening %s.', dirName+'\\'+fname)
                    log.debug('File is of type raster or vector. Using gdalreader.')
                    #Extract Catchwords from file name 
                    fileCatchwords = stringinformation.searchCatchwords(os.path.basename(os.path.normpath(os.path.splitext(fname)[0])))
                    #Extract possible Date from file name
                    filedate = stringinformation.searchDate(os.path.basename(os.path.normpath(fname)))
                    #If no Date could be found use rootDate
                    if filedate == 'undefined':
                        filedate = dirdate
                    #Add Catchwords together and check for duplicates
                    finalCatchwords = Catchwords + fileCatchwords
                    log.debug('Extracted Catchwords: %s', finalCatchwords)
                    log.debug('Extracted Date: %s', filedate)
                    
                    file_path = os.path.realpath(os.path.join(dirName, fname))
                    filename = os.path.splitext(file_path)[0]
                    try:
                        reader = gdalreader.GdalData(file_path)
                    except:
                        log.error('Failed to open file with gdalreader')
                        raise
                    log.debug('File sucessfully opened with gdalreader')
                    try:
                        writer = metadatawriter.Metadata()
                    except:
                        log.error('Failed to initialize metadatawriter')
                        raise
                    
                    #Write metadata
                    writer.metadataIdentifier(str(uuid.uuid1()))   
                    writer.defaultLocale(self.defaultLocale)        
                    writer.metadataScope(self.resourceScope)           
                    writer.contact(self.roleCode, self.Organisation)           
                    writer.dateInfo(datetime.datetime.today().strftime('%Y-%m-%d'), 'creation')           
                    writer.referenceSystemInfo(reader.EPSG,'geodeticGeographic2D')
                    BBOX = reader.BBOX
                    if len(finalCatchwords) >= 3:
                        title = finalCatchwords[-3]+'_'+finalCatchwords[-2]+'_'+finalCatchwords[-1]
                    elif len(finalCatchwords) == 2:
                        title = finalCatchwords[-2]+'_'+finalCatchwords[-1]
                    elif len(finalCatchwords) == 1:
                        title = finalCatchwords[-1]
                    elif len(finalCatchwords) == 0:
                        title = 'undefined'
                    timePeriod = [filedate, filedate]
                    #AssociatedResource = ['title', 'UUID']
                    self.Abstract += 'Catchwords: ' + ', '.join(finalCatchwords)
                    writer.identificationInfo(title,self.Abstract, self.ProgressCode, reader.resolution, BBOX, timePeriod, reader.driver, self.Keywords, self.ClassificationCode, 'unclassified')
                    writer.distributionInfo('Offline File. Acessible at the given location', file_path) 
                    writer.write_to_file(filename, writer)
                    self.number += 1
                    log.info('Successfully created .xml for %s', dirName+'\\'+fname )
                    #Upload to Geonetwork
                    filename_open = os.path.splitext(fname)[0]
                    xmlPath = os.path.realpath(os.path.join(dirName,filename_open))+".xml"
                    if self.upload == True:
                        functions.CSWInsert(self.cswURL, self.username, self.password, xmlPath)
                    
                    
                if fname.endswith(self.pointcloudExtensions):
                    log.info('Opening %s.', dirName+'\\'+fname)
                    log.debug('File is of type raster or vector. Using pdalreader.')
                    #Extract Catchwords from file name 
                    fileCatchwords = stringinformation.searchCatchwords(os.path.basename(os.path.normpath(os.path.splitext(fname)[0])))
                    #Extract possible Date from file name
                    filedate = stringinformation.searchDate(os.path.basename(os.path.normpath(fname)))
                    #If no Date could be found use rootDate
                    if filedate == 'undefined':
                        filedate = dirdate
                    #Add Catchwords together and check for duplicates
                    finalCatchwords = list(set(Catchwords + fileCatchwords))
                    log.info('Extracted Catchwords: %s', finalCatchwords)
                    log.info('Extracted Date: %s', filedate)
                    
                    file_path = os.path.realpath(os.path.join(dirName, fname))
                    filename = os.path.splitext(file_path)[0]
                    log.debug('Opening %s.', dirName+'\\'+fname)
                    try:
                        reader = pdalreader.PdalData(file_path)
                    except:
                        log.error('Failed to open file with pdalreader')
                        raise
                    log.debug('File sucessfully opened with pdalreader')
                        
                    try:
                        writer = metadatawriter.Metadata()
                    except:
                        log.error('Failed to initialize metadatawriter')
                        raise
                        
                    #Write metadata
                    writer.metadataIdentifier(str(uuid.uuid1()))   
                    writer.defaultLocale('en')        
                    writer.metadataScope('dataset')           
                    writer.contact('user', 'University of Trier: Departement of Environmental Remote Sensing and Geoinformatics')           
                    writer.dateInfo(datetime.datetime.today().strftime('%Y-%m-%d'), 'creation')           
                    writer.referenceSystemInfo(reader.EPSG,'geodeticGeographic2D')
                    BBOX = reader.BBOX
                    if len(finalCatchwords) >= 3:
                        title = finalCatchwords[-3]+'_'+finalCatchwords[-2]+'_'+finalCatchwords[-1]
                    elif len(finalCatchwords) == 2:
                        title = finalCatchwords[-2]+'_'+finalCatchwords[-1]
                    elif len(finalCatchwords) == 1:
                        title = finalCatchwords[-1]
                    elif len(finalCatchwords) == 0:
                        title = 'undefined'
                    timePeriod = [filedate, filedate]
                    #AssociatedResource = ['title', 'UUID']
                    writer.identificationInfo(title,self.Abstract, self.ProgressCode, None, BBOX, timePeriod, 'LAS File Format', self.Keywords, self.ClassificationCode, 'unclassified')
                    writer.distributionInfo('Offline File. Acessible at the given location', file_path)
                    
                    writer.write_to_file(filename, writer)
                    self.number += 1
                    log.info('Successfully created .xml for %s', dirName+'\\'+fname )
                    test = dirName+'\\'+fname
                    print(os.path.normpath(test))
                    #Upload to Geonetwork
                    filename_open = os.path.splitext(fname)[0]
                    xmlPath = os.path.realpath(os.path.join(dirName,filename_open))+".xml"
                    if self.upload == True:
                        functions.CSWInsert(self.cswURL, self.username, self.password, xmlPath)
