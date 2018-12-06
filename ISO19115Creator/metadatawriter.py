# -*- coding: utf-8 -*-

import logging
import xml.etree.ElementTree as ET 
from xml.dom import minidom 

#Set up logging
log = logging.getLogger(__name__)

# Namespaces
xsi ='http://www.w3.org/2001/XMLSchema-instance'
xlink = 'http://www.w3.org/1999/xlink'
gml = 'http://www.opengis.net/gml/3.2'
cat = 'http://standards.iso.org/iso/19115/-3/cat/1.0'
gco = 'http://standards.iso.org/iso/19115/-3/gco/1.0'
gcx = 'http://standards.iso.org/iso/19115/-3/gcx/1.0'
gex = 'http://standards.iso.org/iso/19115/-3/gex/1.0'
lan = 'http://standards.iso.org/iso/19115/-3/lan/1.0'
mas = 'http://standards.iso.org/iso/19115/-3/mas/1.0'
mcc = 'http://standards.iso.org/iso/19115/-3/mcc/1.0'
mco = 'http://standards.iso.org/iso/19115/-3/mco/1.0'
mda = 'http://standards.iso.org/iso/19115/-3/mda/1.0'
mdq = 'http://standards.iso.org/iso/19157/-2/mdq/1.0'
mex = 'http://standards.iso.org/iso/19115/-3/mex/1.0'
mmi = 'http://standards.iso.org/iso/19115/-3/mmi/1.0'
mpc = 'http://standards.iso.org/iso/19115/-3/mpc/1.0'
mrd = 'http://standards.iso.org/iso/19115/-3/mrd/1.0'
mri = 'http://standards.iso.org/iso/19115/-3/mri/1.0'
mrs = 'http://standards.iso.org/iso/19115/-3/mrs/1.0'
cit = 'http://standards.iso.org/iso/19115/-3/cit/2.0'
mac = 'http://standards.iso.org/iso/19115/-3/mac/2.0'
mdb = 'http://standards.iso.org/iso/19115/-3/mdb/2.0'
mds = 'http://standards.iso.org/iso/19115/-3/mds/2.0'
mdt = 'http://standards.iso.org/iso/19115/-3/mdt/2.0'
mrl = 'http://standards.iso.org/iso/19115/-3/mrl/2.0'
mrc = 'http://standards.iso.org/iso/19115/-3/mrc/2.0'
msr = 'http://standards.iso.org/iso/19115/-3/msr/2.0'
srv = 'http://standards.iso.org/iso/19115/-3/srv/2.0'
schemaLocation = 'http://standards.iso.org/iso/19115/-3/mdb/2.0 http://standards.iso.org/iso/19115/-3/mdt/2.0/mdt.xsd'

ET.register_namespace('xsi',xsi)
ET.register_namespace('xlink',xlink)
ET.register_namespace('gml',gml)
ET.register_namespace('cat',cat)
ET.register_namespace('gco',gco)
ET.register_namespace('gcx',gcx)
ET.register_namespace('gex',gex)
ET.register_namespace('lan',lan)
ET.register_namespace('mas',mas)
ET.register_namespace('mcc',mcc)
ET.register_namespace('mco',mco)
ET.register_namespace('mda',mda)
ET.register_namespace('mdq',mdq)
ET.register_namespace('mex',mex)
ET.register_namespace('mmi',mmi)
ET.register_namespace('mpc',mpc)
ET.register_namespace('mrd',mrd)
ET.register_namespace('mri',mri)
ET.register_namespace('mrs',mrs)
ET.register_namespace('cit',cit)
ET.register_namespace('mac',mac)
ET.register_namespace('mdb',mdb)
ET.register_namespace('mds',mds)
ET.register_namespace('mdt',mdt)
ET.register_namespace('mrl',mrl)
ET.register_namespace('mrc',mrc)
ET.register_namespace('msr',msr)
ET.register_namespace('srv',srv)

#CodeLists
codelist_LanguageCode = 'http://www.loc.gov/standards/iso639-2/'
codelist_MD_CharacterSetCode = 'codeListLocation#MD_CharacterSetCode'
codelist_MD_ScopeCode = 'http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_ScopeCode'
codelist_CI_RoleCode = 'http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#CI_RoleCode'
codelist_CI_DateTypeCode = 'http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#CI_DateTypeCode'
codelist_MD_ReferenceSystemTypeCode = 'http://standards.iso.org/iso/19115/resources/Codelists/cat/codelists.xml#MD_ReferenceSystemTypeCode'
codelist_MD_ProgressCode = 'http://standards.iso.org/iso/19115/resources/Codelist/cat/codelists.xml#MD_ProgressCode'
codelist_MD_ClassificationCode = 'http://standards.iso.org/iso/19115/resources/Codelist/cat/codelists.xml#MD_ClassificationCode'
codelist_DS_AssociationTypeCode = 'http://standards.iso.org/iso/19115/resources/Codelist/cat/codelists.xml#DS_AssociationTypeCode'

class Metadata:
    '''Class to create ISO19115-3 Metadata Entries.'''
    
    def __init__(self):
        self.root = ET.Element('{'+ mdb +'}MD_Metadata', attrib={"{" + xsi + "}schemaLocation" : schemaLocation})
          
    def prettify(self):
        '''Return a pretty-printed XML string for the Element.'''
        rough_string = ET.tostring(self.root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
    
    def write_to_file(self, filename, metadata):
        xml_metadata = metadata.prettify()
        output_file = open(filename +".xml" , 'w' )
        output_file.write(xml_metadata)
        output_file.close()
    
    def metadataIdentifier(self, UUID):
        a = ET.SubElement(self.root, '{'+ mdb +'}metadataIdentifier')
        b = ET.SubElement(a, '{'+ mcc +'}MD_Identifier')
        c = ET.SubElement(b, '{'+ mcc +'}code')
        d = ET.SubElement(c, '{'+ gco +'}CharacterString')
        d.text = UUID
        
    def defaultLocale(self, LanguageCode):
        a = ET.SubElement(self.root, '{'+ mdb +'}defaultLocale')
        b = ET.SubElement(a, '{'+ lan +'}PT_Locale')
        c = ET.SubElement(b, '{'+ lan +'}language')
        ET.SubElement(c, '{'+ lan +'}LanguageCode', codeList=codelist_LanguageCode, codeListValue=LanguageCode)
        
        d = ET.SubElement(b, '{'+ lan +'}characterEncoding')
        ET.SubElement(d, '{'+ lan +'}MD_CharacterSetCode', codeList=codelist_MD_CharacterSetCode, codeListValue="utf8")
                      
    def metadataScope(self, ScopeCode):
        a = ET.SubElement(self.root, '{'+ mdb +'}metadataScope')
        b = ET.SubElement(a, '{'+ mdb +'}MD_MetadataScope')
        c = ET.SubElement(b, '{'+ mdb +'}resourceScope')
        ET.SubElement(c, '{'+ mcc +'}MD_ScopeCode', codeList=codelist_MD_ScopeCode, codeListValue=ScopeCode)
        
    def contact(self, RoleCode, OrganisationName):
        a = ET.SubElement(self.root, '{'+ mdb +'}contact')
        b = ET.SubElement(a, '{'+ cit +'}CI_Responsibility')
        c = ET.SubElement(b, '{'+ cit +'}role')
        ET.SubElement(c, '{'+ cit +'}CI_RoleCode', codeList=codelist_CI_RoleCode, codeListValue=RoleCode)    

        g = ET.SubElement(b, '{'+ cit +'}party')
        d = ET.SubElement(g, '{'+ cit +'}CI_Organisation')
        e = ET.SubElement(d, '{'+ cit +'}name')
        f = ET.SubElement(e, '{'+ gco +'}CharacterString')
        f.text = OrganisationName
        
    def dateInfo(self, DateTime, DateTypeCode):
        a = ET.SubElement(self.root, '{'+ mdb +'}dateInfo')
        b = ET.SubElement(a, '{'+ cit +'}CI_Date')
        c = ET.SubElement(b, '{'+ cit +'}date')
        d = ET.SubElement(c, '{'+ gco +'}Date')
        d.text = DateTime       
        e = ET.SubElement(b, '{'+ cit +'}dateType')
        ET.SubElement(e, '{'+ cit +'}CI_DateTypeCode', codeList=codelist_CI_DateTypeCode, codeListValue=DateTypeCode)
        
    def referenceSystemInfo(self, EPSG_Code, ReferenceSystemTypeCode):
        a = ET.SubElement(self.root, '{'+ mdb +'}referenceSystemInfo')
        b = ET.SubElement(a, '{'+ mrs +'}MD_ReferenceSystem')
        c = ET.SubElement(b, '{'+ mrs +'}referenceSystemIdentifier')
        d = ET.SubElement(c, '{'+ mcc +'}MD_Identifier')
        e = ET.SubElement(d, '{'+ mcc +'}code')
        f = ET.SubElement(e, '{'+ gco +'}CharacterString')
        f.text = EPSG_Code
        
        g = ET.SubElement(d, '{'+ mcc +'}codeSpace')
        h = ET.SubElement(g, '{'+ gco +'}CharacterString')
        h.text = 'EPSG'      
        i = ET.SubElement(b, '{'+ mrs +'}referenceSystemType')
        ET.SubElement(i, '{'+ mrs +'}MD_ReferenceSystemTypeCode', codeList=codelist_MD_ReferenceSystemTypeCode, codeListValue=ReferenceSystemTypeCode)

    def identificationInfo(self, DatasetTitle, Abstract, ProgressCode, spatialResolution, BBOX, timePeriod, Formattitle, Keywords, ClassificationCode, useLimitation):
        a = ET.SubElement(self.root, '{'+ mdb +'}identificationInfo')
        b = ET.SubElement(a, '{'+ mri +'}MD_DataIdentification')
        
        c = ET.SubElement(b, '{'+ mri +'}citation')
        d = ET.SubElement(c, '{'+ cit +'}CI_Citation')
        e = ET.SubElement(d, '{'+ cit +'}title')
        f = ET.SubElement(e, '{'+ gco +'}CharacterString')
        f.text = DatasetTitle
        
        k = ET.SubElement(b, '{'+ mri +'}abstract')
        l = ET.SubElement(k, '{'+ gco +'}CharacterString')
        l.text = Abstract
        
        m = ET.SubElement(b, '{'+ mri +'}status')
        ET.SubElement(m, '{'+ mcc +'}MD_ProgressCode', codeList=codelist_MD_ProgressCode, codeListValue=ProgressCode)

        if spatialResolution:
            ar = ET.SubElement(b, '{'+ mri +'}spatialResolution')
            at = ET.SubElement(ar, '{'+ mri +'}MD_Resolution')
            au = ET.SubElement(at, '{'+ mri +'}distance')
            av = ET.SubElement(au, '{'+ gco +'}Distance', uom="meter")
            av.text = str(spatialResolution)

        n = ET.SubElement(b, '{'+ mri +'}extent')
        o = ET.SubElement(n, '{'+ gex +'}EX_Extent')
        
        p = ET.SubElement(o, '{'+ gex +'}geographicElement')
        q = ET.SubElement(p, '{'+ gex +'}EX_GeographicBoundingBox')
        r = ET.SubElement(q, '{'+ gex +'}westBoundLongitude')
        s = ET.SubElement(r, '{'+ gco +'}Decimal')
        s.text = BBOX[0]
        t = ET.SubElement(q, '{'+ gex +'}eastBoundLongitude')
        u = ET.SubElement(t, '{'+ gco +'}Decimal')
        u.text = BBOX[2]
        v = ET.SubElement(q, '{'+ gex +'}southBoundLatitude')
        w = ET.SubElement(v, '{'+ gco +'}Decimal')
        w.text = BBOX[1]
        x = ET.SubElement(q, '{'+ gex +'}northBoundLatitude')
        y = ET.SubElement(x, '{'+ gco +'}Decimal')
        y.text = BBOX[3]
        
        al = ET.SubElement(o, '{'+ gex +'}temporalElement')
        am = ET.SubElement(al, '{'+ gex +'}EX_TemporalExtent')
        an = ET.SubElement(am, '{'+ gex +'}extent')
        ao = ET.SubElement(an, '{'+ gml +'}TimePeriod')
        ao.set('gml:id','TimePeriod')
        ap = ET.SubElement(ao, '{'+ gml +'}beginPosition')
        aq = ET.SubElement(ao, '{'+ gml +'}endPosition')
        ap.text = timePeriod[0]
        aq.text = timePeriod[1]
        
        z = ET.SubElement(b, '{'+ mri +'}resourceFormat')
        aa = ET.SubElement(z, '{'+ mrd +'}MD_Format')
        ab = ET.SubElement(aa, '{'+ mrd +'}formatSpecificationCitation')
        ac = ET.SubElement(ab, '{'+ cit +'}CI_Citation')
        ad = ET.SubElement(ac, '{'+ cit +'}title')
        af = ET.SubElement(ad, '{'+ gco +'}CharacterString')
        af.text = Formattitle
        
        ag = ET.SubElement(b, '{'+ mri +'}descriptiveKeywords')
        ah = ET.SubElement(ag, '{'+ mri +'}MD_Keywords')
        
        for Keyword in Keywords:          
            aj = ET.SubElement(ah, '{'+ mri +'}keyword')
            ak = ET.SubElement(aj, '{'+ gco +'}CharacterString')
            ak.text = Keyword  
            
        ba = ET.SubElement(b, '{'+ mri +'}resourceConstraints')
        bb = ET.SubElement(ba, '{'+ mco +'}MD_SecurityConstraints')
        
        bc = ET.SubElement(bb, '{'+ mco +'}classification')
        ET.SubElement(bc, '{'+ mco +'}MD_ClassificationCode', codeList=codelist_MD_ClassificationCode, codeListValue=ClassificationCode)
        
        be = ET.SubElement(bb, '{'+ mco +'}userNote')
        bf = ET.SubElement(be, '{'+ gco +'}CharacterString')
        bf.text = useLimitation        

#        bg = ET.SubElement(b, '{'+ mri +'}associatedResource')
#        bh = ET.SubElement(bg, '{'+ mri +'}MD_AssociatedResource')
#        bi = ET.SubElement(bh, '{'+ mri +'}associationType') 
#        ET.SubElement(bi, '{'+ mri +'}DS_AssociationTypeCode', codeList=codelist_DS_AssociationTypeCode, codeListValue='largerWorkCitation')    
#        bk = ET.SubElement(bh, '{'+ mri +'}metadataReference')
#        bl = ET.SubElement(bk, '{'+ cit +'}CI_Citation')
#        bm = ET.SubElement(bl, '{'+ cit +'}title')
#        bn = ET.SubElement(bm, '{'+ gco +'}CharacterString')
#        bn.text = AssociatedResource[0]
#        bo = ET.SubElement(bl, '{'+ cit +'}identifier')
#        bp = ET.SubElement(bo, '{'+ mcc +'}MD_Identifier')
#        bq = ET.SubElement(bp, '{'+ mcc +'}code')
#        br = ET.SubElement(bq, '{'+ gco +'}CharacterString')
#        br.text = AssociatedResource[1] 

    def distributionInfo(self, Description, MediumName):
        a = ET.SubElement(self.root, '{'+ mdb +'}distributionInfo')
        b = ET.SubElement(a, '{'+ mrd +'}MD_Distribution')
        
        c = ET.SubElement(b, '{'+ mrd +'}description')
        d = ET.SubElement(c, '{'+ gco +'}CharacterString')
        d.text = Description
        
        c = ET.SubElement(b, '{'+ mrd +'}transferOptions')
        d = ET.SubElement(c, '{'+ mrd +'}MD_DigitalTransferOptions')
        e = ET.SubElement(d, '{'+ mrd +'}offLine')
        f = ET.SubElement(e, '{'+ mrd +'}MD_Medium')
        g = ET.SubElement(f, '{'+ mrd +'}name')
        h = ET.SubElement(g, '{'+ cit +'}CI_Citation')
        i = ET.SubElement(h, '{'+ cit +'}title')
        j = ET.SubElement(i, '{'+ gco +'}CharacterString')
        j.text = MediumName
        
    def acquisitionInformation(self, ScopeCode, PlatformCode, PlatformDescription, InstrumentCode, InstrumentDescription):
        a = ET.SubElement(self.root, '{'+ mdb +'}acquisitionInformation')
        b = ET.SubElement(a, '{'+ mac +'}MI_AcquisitionInformation') 
        
        c = ET.SubElement(b, '{'+ mac +'}scope')
        t = ET.SubElement(c, '{'+ mcc +'}MD_Scope')
        u = ET.SubElement(t, '{'+ mcc +'}level')
        ET.SubElement(u, '{'+ mcc +'}MD_ScopeCode', codeList=codelist_MD_ScopeCode, codeListValue=ScopeCode)

        d = ET.SubElement(b, '{'+ mac +'}platform')
        e = ET.SubElement(d, '{'+ mac +'}MI_Platform')
        
        f = ET.SubElement(e, '{'+ mac +'}identifier')
        
        g = ET.SubElement(f, '{'+ mcc +'}MD_Identifier')
        h = ET.SubElement(g, '{'+ mcc +'}code')
        i = ET.SubElement(h, '{'+ gco +'}CharacterString')
        i.text = PlatformCode
        
        j = ET.SubElement(e, '{'+ mac +'}description')
        k = ET.SubElement(j, '{'+ gco +'}CharacterString')
        k.text = PlatformDescription
        
        l = ET.SubElement(e, '{'+ mac +'}instrument')
        m = ET.SubElement(l, '{'+ mac +'}MI_Instrument')
        n = ET.SubElement(m, '{'+ mac +'}identifier')
        o = ET.SubElement(n, '{'+ mcc +'}MD_Identifier')
        p = ET.SubElement(o, '{'+ mcc +'}code')
        q = ET.SubElement(p, '{'+ gco +'}CharacterString')
        q.text = InstrumentCode
        r = ET.SubElement(m, '{'+ mac +'}type')
        s = ET.SubElement(r, '{'+ gco +'}CharacterString')
        s.text = InstrumentDescription
        
        
        


        
        
        
        
        
        
    
