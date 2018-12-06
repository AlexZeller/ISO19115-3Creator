from lxml import etree                                                         

def checkXML(xml):  
    """ 
    Function to chec a xml file for syntax errors and validate it against the ISO19115-3 schemas.
    
    Arguments: 
        xml: The path of the xml file to be validated.
    """
                                                                          
    xsd = r'.\ISO19115Creator\standards.iso.org\iso\19115\-3\mdt\2.0\mdt.xsd'
    #xml = r'F:\20170328_Bernkastel\RGB_thermal.xml'                                                          
                                                                                    
    #Open xsd file                                                                                                                                         
    with open(xsd) as f:                                                
        doc = etree.parse(f)                                                    
        schema = etree.XMLSchema(doc)  
                                                                                                        
    #Open xml file                                                                                                                                                                                                                 
    with open(xml) as f:   
        try:                                             
            doc = etree.parse(f) 
            print ('XML well formed')
        except etree.XMLSyntaxError as err:
            print (err)
                                                                                                                                                                               
    try:                                                                        
        schema.assertValid(doc) 
        print ('XML valid')                                                 
    except etree.DocumentInvalid as err:                                     
        print (err)                                                                 
                                                                

    

