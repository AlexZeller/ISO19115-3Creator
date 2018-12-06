# -*- coding: utf-8 -*-

import dateutil.parser as dparser
from datetime import datetime
import re
import logging

#Set up logging
log = logging.getLogger(__name__)

def searchDate(string):
    """ 
    Search for date information in a given string. 
      
    Arguments: 
        string (string): The string to be searched.
    """
    
    #Only consider strings that are longer then 4 characters
    if len(string)>4:
        #Search for format YYYY_MM_DD
        try:
            pattern = re.search(r'\d{4}_\d{2}_\d{2}',string)
            date = datetime.strptime(pattern.group(),'%Y_%m_%d').date()
            return date.strftime("%Y-%m-%d")
        except:
            pass
        #Search for format DD_MM_YYYY
        try:
            pattern = re.search(r'\d{2}_\d{2}_\d{4}',string)
            date = datetime.strptime(pattern.group(),'%d_%m_%Y').date()
            return date.strftime("%Y-%m-%d")
        except:
            pass
        #Search for formats with fuzzy logic using dateutil
        try:
            date = dparser.parse(string,fuzzy=True)
            return date.strftime("%Y-%m-%d")
        except:
            pass
        #Search for formats DDMMYYY
        try:
            pattern = re.search(r'\d{8}',string)
            date = datetime.strptime(pattern.group(),'%d%m%Y').date()
            return date.strftime("%Y-%m-%d")
        except:
            return 'undefined'
    else:
        log.debug('No date information available')
        return 'undefined'
        
    

def searchKeywords(string):
    """ 
    Splits String (at '_', '-' and '.' and searches for non-digit strings that
    are longer than 2 characters.
    
      
    Arguments: 
        string (string): The string to be searched.
    """

    #Exceptions that should not be considered Keywords    
    exceptions = ['tif', 'aux', 'ref', 'etrs']
    
    #Create empty list
    Keywords = []
    
    #Split list at underscores
    split_list_underscore = string.split('_') 
    for item in split_list_underscore:
        #Split items in list at points
        split_list_point = item.split('.')
        for item in split_list_point:
            #Split items in list at hyphen
            split_list = item.split('-')
            for item in split_list:
                #Make all items lowercase to enable removing duplicates with list(set())
                item = item.lower()
                if not item in exceptions:   
                    #Do not consider items with digits as keywords
                    if not item.isdigit():
                        if not len(item)<3:
                            Keywords.append(item)

    return Keywords 
    
    

