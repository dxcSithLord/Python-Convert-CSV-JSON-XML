import sys # To take arguments from user
import csv # To do operations with csv file
import json # To do operations with json file
import xml.etree.ElementTree as ET # To do operations with xml file
from lxml import etree # To xml file validate with xsd file
from xml.dom import minidom # I just used it to print regularly into the xml file 

# I use encode utf-8 to read and write the files.
# Because the csv file given to us has Turkish characters.

# In the main function, arguments are taken from users. And whatever action is to be taken to that fuction.
def main():
    print("python file  ☞ ",sys.argv[0]) # 2017510049.py
    print("input file  ☞ ",sys.argv[1]) # input file
    print("output file  ☞ ",sys.argv[2]) # output file
    print("Conversion type  ☞ ",sys.argv[3]) # convert type

    if sys.argv[3]=="1": # Convert from csv to xml file
        convertCsv2Xml(sys.argv[1], sys.argv[2])
        print(" ☞ convert csv file to xml file !!!")

    elif sys.argv[3]=="2": # Convert from xml to csv file
        convertXml2Csv(sys.argv[1], sys.argv[2])
        print(" ☞ convert xml file to csv file !!!")

    elif sys.argv[3]=="3": # Convert from xml to json file
        convertXml2Json(sys.argv[1],sys.argv[2])
        print(" ☞ convert xml file to json file !!!")

    elif sys.argv[3]=="4": # Convert from json to xml file
        convertJson2Xml(sys.argv[1], sys.argv[2])
        print(" ☞ convert json file to xml file !!!")

    elif sys.argv[3]=="5": # Convert from csv to json file
        convertCsv2Json(sys.argv[1], sys.argv[2])
        print(" ☞ convert csv file to json file !!!")

    elif sys.argv[3]=="6": # Convert from json to csv file
        convertJson2Csv(sys.argv[1], sys.argv[2])
        print(" ☞ convert json file to csv file !!!")

    elif sys.argv[3]=="7": # xml file validation with xsd file
        validateXmlWithXsd(sys.argv[1], sys.argv[2])
        print(" ☞ xml file validate with xsd file !!!")

# This function converts from csv file to xml file.
def convertCsv2Xml(csvFlile, xmlFile): #1

    # Reading the csv file wit utf-8
    with open(csvFlile,'r+',encoding='utf-8') as f:
        csv_file=csv.reader(f,delimiter=';')
        data = ET.Element('depertments')
        uniName="name"
        f=0

        # Lines separated by semicolons are written to xml file as desired
        for row in csv_file:

            # This condition is headers in the first line of the csv file and to avoid writing them to the xml file
            if f>0:

                # This condition is to re-create 'univetsity' in xml file in every new university in csv file
                # New 'university' sub-elemet is created
                # university name and type attributes are added
                if uniName!=row[1]:
                    university = ET.SubElement(data, 'university')
                    university.set('name',row[1])
                    university.set('uType',row[0])
                    uniName=row[1]

                # The sub-element of 'university' creates a new 'item'
                # id and faculty attributes are added
                item = ET.SubElement(university, 'item')
                item.set('id',row[3])
                item.set('faculty',row[2])

                # Sub-element of 'item' creates 'name' 
                name=ET.SubElement(item, 'name')

                # If the language id 'İngilizce', 'language' is 'en', otherwise 'empty'
                if row[5]=="İngilizce":
                    language="en"
                else:
                    language=''

                # If the second id 'İkinci Öğretim', 'second' is 'Yes', otherwise 'No'
                if row[6]=="İkinci Öğretim":
                    second="Yes"
                else:
                    second="No"
                
                # language and second attributes are added
                name.set('language',language)
                name.set('second',second)
                name.text = row[4]

                # Sub-element of 'item' creates 'period' 
                period = ET.SubElement(item, 'period')
                period.text = row[8]

                # Sub-element of 'item' creates 'quota' 
                quota=ET.SubElement(item, 'quota')
                quota.set('spec',row[11])
                quota.text = row[10]

                # Sub-element of 'item' creates 'field' 
                field = ET.SubElement(item, 'field')
                field.text = row[9]

                # Sub-element of 'item' creates 'last_min_score' 
                last_min_score=ET.SubElement(item, 'last_min_score')
                last_min_score.set('last_min_order',row[12])
                if row[13]=="-":
                    last_min_score.text = ''
                else:
                    last_min_score.text = row[13]

                # Sub-element of 'item' creates 'grant'  
                grant=ET.SubElement(item, 'grant')
                grant.text = row[7]

                #Create a new xml file
                # It is written to the xml file
                # 'minidom' was only used to properly write the xml file with utf-8
                mydata=minidom.parseString(ET.tostring(data,encoding="utf-8")).toprettyxml(indent='\t')
                myfile = open(xmlFile, "w",encoding="utf-8")
                myfile.write(mydata)       
            f=f+1

# This function converts from xml file to csv file.
def convertXml2Csv(xmlFile, csvFlile): #2

    # Create a new csv file
    with open(csvFlile, 'w') as csvfile:

        # The headers of the new csv file are also kept in the list
        fieldnames = ['ÜNİVERSİTE_TÜRÜ', 'ÜNİVERSİTE','FAKÜLTE','PROGRAM_KODU','PROGRAM','DİL','ÖĞRENİM_TÜRÜ','BURS',
        'ÖĞRENİM_SÜRESİ','PUAN_TÜRÜ','KONTENJAN','OKUL_BİRİNCİSİ_KONTENJANI','GEÇEN_YIL_MİN_SIRALAMA','GEÇEN_YIL_MİN_PUAN']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=';')
        writer.writeheader()

        tree = ET.parse(xmlFile)
        root = tree.getroot()

        for element in root:
            for elem in element:
                for x in elem:

                    if x.tag=='name':
                        bolum=x.text

                        # 'language' is checked and if 'en' is in 'İngilizce' otherwise it is empty
                        if x.get('language')=='en':
                            language='İngilizce'
                        else:
                            language=x.get('language')
                        
                         # 'second' is checked and if 'Yes' is in 'İkinci Öğretim' otherwise it is empty
                        if x.get('second')=='Yes':
                            second='İkinci Öğretim'
                        else:
                            second=''

                    # 'period', 'grant', 'quota', 'spec', 'last_min_score','last_min_order'
                    #  and 'grant' information is written into csv file from xml file
                    elif x.tag=='period':
                        period=x.text

                    elif x.tag=='grant':
                        grant=x.text

                    elif x.tag=='quota':
                        quota=x.text

                        spec=x.get('spec')
                    elif x.tag=='field':
                        field=x.text

                    elif x.tag=='last_min_score':
                        order=x.get('last_min_order')
                        minScore=x.text

                    else:
                        grant=x.text
                    
                # Write in csv file
                writer.writerow({fieldnames[0]: element.get('uType'), fieldnames[1]: element.get('name'),
                fieldnames[2]: elem.get('faculty'), fieldnames[3]: elem.get('id'),fieldnames[4]: bolum, fieldnames[5]: language,
                fieldnames[6]: second,fieldnames[7]: grant, fieldnames[8]: period, fieldnames[9]: field, fieldnames[10]: quota,
                fieldnames[11]: spec, fieldnames[12]: order, fieldnames[13]: minScore})

# This function converts from xml file to json file.
def convertXml2Json(xmlFile,jsonFile): #3

    #Read xml file
    tree = ET.parse(xmlFile)
    root = tree.getroot()

    # I kept all the information in the dict structure so that it is easy to put it in the json file
    item={}
    items = {}
    department={"faculty":"faculty"}
    universities={}
    items = {"university Name":'name',"uType":'typeU'}
    universities['universities']=[]

    for elem2 in root:
        item={}
        items = {}

        # I wrote a condition here. There are both 'Mühendislik ve Mimarlık Fakültesi' and 'Mühendislik Fakültesi' as
        # faculty from the csv file. So I tried to solve it like this. I could not solve it otherwise.
        if elem2.get('name')=="İZMİR KATİP ÇELEBİ ÜNİVERSİTESİ" or elem2.get('name')=="İZMİR BAKIRÇAY ÜNİVERSİTESİ":
            department={"faculty":"Mühendislik ve Mimarlık Fakültesi"}
        else:
            department={"faculty":"Mühendislik Fakültesi"}

        items = {"university Name":elem2.get('name'),"uType":elem2.get('uType')}
    
        items['items'] = []
        department['department'] = []
        item['item'] = []

        for elem in elem2:
            id=elem.get('id')
            items['items'] = []
            for x in elem:

                if x.tag=='name':
                    bolum=x.text

                    # The 'language' is 'en' or '' in the xml file. The condition has been written to be like this in the json file.
                    if x.get('language')=='en':
                        language='en'
                    else:
                        language=None
                    
                    # The 'second' is 'Yes' or 'No' in the xml file. The condition has been written to be like this in the json file
                    if x.get('second')=='Yes':
                        second='Yes'
                    else:
                        second='No'

                elif x.tag=='period':
                    # The 'period' is numerical number in the xml file
                    # I put a condition that a black trial is made for the period. In fact, it is not necessary for the csv file given to us.
                    if x.text!=None:
                        period=int(x.text)
                    else:
                        period=None

                elif x.tag=='quota':

                    #I wrote this condition because the 'quota' of some universities are empty
                    if x.text!=None:
                        quota=int(x.text)
                    else:
                        quota=None

                    #I wrote this condition because the 'spec' of some universities are empty
                    if x.get('spec')!='':
                        spec=int(x.get('spec'))
                    else:
                        spec=None

                elif x.tag=='field':
                    field=x.text
                    
                elif x.tag=='last_min_score':
                    #I wrote this condition because the 'last_min_order' of some universities are empty
                    if x.get('last_min_order')=='' or x.get('last_min_order')==None:
                        order=None
                    else:
                        order=int(x.get('last_min_order'))

                    #',' and '.' it was necessary to replace for file
                    if x.text!=None:
                        minScore=float(x.text.replace(',','.'))
                    else:
                        minScore=None

                #Some universities may not have grant, others may
                else:
                    if x.text=="25" or x.text=="50" or x.text=="100":
                        grant=int(x.text)
                    else:
                        grant=None
                    
            item= {"id": id, "name":bolum,"lang": language, "second": second,"period":period,"spec":spec,"quota": quota,
            "field":field,"last_min_score": minScore, "last_min_order": order,"grant":grant} 
                
            department['department'].append(item)
            items['items'].append(department)
        universities['universities'].append(items)

    # write json file with utf-8    
    with open(jsonFile, 'w',encoding='utf-8') as outfile:
        json.dump(universities, outfile,indent=4,ensure_ascii=False)

# This function converts from json file to xml file.
def convertJson2Xml(jsonFile, xmlFile): #4

    #read json file
    with open(jsonFile,'r+') as json_file:
        data2=json.load(json_file)
        mydata=""
        data = ET.Element('depertments')    
        uniName="name"
        uniType="uType"
        
        for p in data2['universities']:
            
            # Every time the 'university name' changes, the 'university' sub-element is created
            if uniName!=p.get('university Name'):
                uniName=p.get('university Name')
                uniType=p.get('uType')
                university = ET.SubElement(data, 'university')
                university.set('name',uniName)
                university.set('uType',uniType)
            
            for s in p['items']:
                for a in s['department']:

                    # Created the 'item', which is the sub-element of the 'university'
                    item = ET.SubElement(university, 'item')

                    if a.get('id')!=None:
                        id=a.get('id')
                    else:
                        id=''

                    # Created the sub-elements of the 'item'
                    item.set('id',id)
                    
                    item.set('faculty',s.get('faculty'))
                    
                    name=ET.SubElement(item, 'name')
                    name.text=a.get('name')
                    
                    # 'language' is checked, it is empty or 'en'
                    if a.get('lang')=='en':
                        name.set('language','en')
                    else:
                        name.set('language','')

                    name.set('second',a.get('second'))
                    
                    # 'period' is checked
                    period2=ET.SubElement(item,'period')
                    if a.get('period')!=None:
                        period=str(a.get('period'))
                    else:
                        period=None
                    period2.text=period
                    
                    quota=ET.SubElement(item,'quota')

                     # 'spec' is checked, it is empty or integer
                    if a.get('spec')==None:
                        quota.set('spec','')
                    else:
                        quota.set('spec',str(a.get('spec')))

                    # 'quota' is checked, it is empty or integer
                    if a.get('quota')==None:
                        quota.text=''
                    else:
                        quota.text=str(a.get('quota'))
                    
                    # 'field' is checked, it is empty or integer
                    field=ET.SubElement(item,'field')
                    if a.get('field')==None:
                        field.text=''
                    else:
                        field.text=a.get('field')
                    
                    last_min_score=ET.SubElement(item,'last_min_score')

                    # 'last_min_order' is checked, it is empty or integer
                    if a.get('last_min_order')==None:
                        last_min_score.set('last_min_order','')
                    else:
                        last_min_score.set('last_min_order',str(a.get('last_min_order')))
                    
                    # 'last_min_score' is checked, it is empty or integer
                    if a.get('last_min_score')==None:
                        last_min_score.text=''
                    else:
                        last_min_score.text=str(a.get('last_min_score'))
                    
                    grant=ET.SubElement(item,'grant')

                    # 'grant' is checked, it is empty or integer
                    if a.get('grant')==None:
                        grant.text=''
                    else:
                        grant.text=str(a.get('grant'))

        # Create xml file and written in                                     
        mydata=minidom.parseString(ET.tostring(data,encoding="utf-8")).toprettyxml(indent='\t')
        myfile = open(xmlFile, "w",encoding="utf-8")
        myfile.write(mydata) 
        
# This function converts from csv file to json file.
def convertCsv2Json(csvFile, jsonFile): #5

    # I kept all the information in the dict structure so that it is easy to put it in the json file
    item={}
    deneme = {}
    department={}
    universities={}
    deneme = {"university Name":'name',"uType":'typeU'}
    universities['universities']=[]

    #Read csv file
    with open(csvFile,'r+',encoding='utf-8') as f:
        csv_file=csv.reader(f,delimiter=';')
        
        uniName="name"
        f=0

         # Lines separated by semicolons are written to json file as desired
        for row in csv_file:

            # This condition is headers in the first line of the csv file and to avoid writing them to the xml file
            if f>0:
                # This condition is to re-create 'univetsity' in json file in every new university in csv file
                if uniName!=row[1]:
                    item={}
                    deneme = {}
                    department={"faculty":row[2]}
                    deneme = {"university Name":row[1],"uType":row[0]}
                    deneme['items'] = []
                    department['department'] = []
                    item['item'] = []                   
                deneme['items'] = []

                if row[3]!='':
                    id=row[3]
                else:
                    id=None

                if row[4]!='':
                    bName=row[4]
                else:
                    bName=None

                # 'language' is checked, it is empty or 'İngilizce'
                if row[5]=="İngilizce":
                    language="en"
                else:
                    language=None

                # 'second' is checked, it is empty or 'İkinci Öğretim'
                if row[6]=="İkinci Öğretim":
                    second="Yes"
                else:
                    second="No"

                # Convert to int if not empty
                if row[8]!='':
                    period=int(row[8])
                else:
                    period=None

                if row[11]!='':
                    spec=int(row[11])
                else:
                    spec=None

                if row[10]!='':
                    quota=int(row[10])
                else:
                    quota=None

                if row[9]=='':
                    field=None
                else:
                    field=row[9]

                if row[13]!='' and row[13]!='-':
                    minScore=float(row[13].replace(',','.'))
                else:
                    minScore=None
                
                if row[12]!='':
                    minOrder=int(row[12])
                else:
                    minOrder=None

                if row[7]!='':
                    grant=int(row[7])
                else:
                    grant=None

                item= {"id": id, "name": bName,"lang": language, "second": second,"period": period,"spec":spec,
                "quota": quota,"field":field,"last_min_score": minScore, "last_min_order": minOrder,"grant":grant} 
                
                department['department'].append(item)
                deneme['items'].append(department)
            f=f+1
            if f!=1 and uniName!=row[1]:
                universities['universities'].append(deneme)
                uniName=row[1]
        
    # Create json file
    with open(jsonFile, 'w', encoding='utf-8') as outfile:
        json.dump(universities, outfile,indent=4,ensure_ascii=False)

# This function converts from json file to csv file.
def convertJson2Csv(jsonFile, csvFile): #6

    # Create csv file
    with open(csvFile, 'w') as csvfile:

        # The headers of the new csv file are also kept in the list
        fieldnames = ['ÜNİVERSİTE_TÜRÜ', 'ÜNİVERSİTE','FAKÜLTE','PROGRAM_KODU','PROGRAM','DİL','ÖĞRENİM_TÜRÜ',
        'BURS','ÖĞRENİM_SÜRESİ','PUAN_TÜRÜ','KONTENJAN','OKUL_BİRİNCİSİ_KONTENJANI','GEÇEN_YIL_MİN_SIRALAMA','GEÇEN_YIL_MİN_PUAN']
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=';')
        writer.writeheader()
        uniType="type"
        uniName="name"

        # Read json file
        with open(jsonFile,'r') as json_file:
            data=json.load(json_file)

            for p in data['universities']:
                
                if uniName!=p.get('university Name'):
                    uniName=p.get('university Name')
                    uniType=p.get('uType')

                for s in p['items']:
                    for a in s['department']:

                        # 'lang' is 'null' in some places in json file but needs to '' in csv file
                        if(a.get('lang'))=='en':
                            language='İngilizce'
                        else:
                            language=''
                        
                        # 'second' is 'No' in some places in json file but needs to '' in csv file
                        if a.get('second')=='Yes':
                            second='İkinci Öğretim'
                        else:
                            second=''

                        # Wtire csv file
                        writer.writerow({fieldnames[0]: uniType, fieldnames[1]: uniName,
                        fieldnames[2]: s.get('faculty'), fieldnames[3]: a.get('id'),fieldnames[4]: a.get('name'), 
                        fieldnames[5]: language, fieldnames[6]: second, fieldnames[7]: a.get('grant'), 
                        fieldnames[8]: a.get('period'), fieldnames[9]: a.get('field'), fieldnames[10]: a.get('quota'), 
                        fieldnames[11]: a.get('spec'), fieldnames[12]: a.get('last_min_order'), 
                        fieldnames[13]: a.get('last_min_score')})

# This function validation xml file with xsd file
def validateXmlWithXsd(xmlFile, xsdFile): #7

    # Checks if the xml file complies with the rules in the xsd file

    # Open xsd file
    with open(xsdFile) as f:                                               
        xsd_doc = etree.parse(f)                                                   
        schema = etree.XMLSchema(xsd_doc) 

    # Open xsd file
    with open(xmlFile) as f:                                               
        xml_doc = etree.parse(f)                                                        
        validation_result = schema.validate(xml_doc)   
    schema.assert_(xml_doc)  

    print ("** ",validation_result," **" )

main()