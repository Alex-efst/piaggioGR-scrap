import pandas as pd
import re
import os
import time
import shutil


def groupSearch(count,line,temp_categ,temp_desc,temp_codes2,codes):
    """
    Aquire info from txt in current folder, seperate info based on regex patterns and assign them to vars
    
   :param param1: Counter to filter
   :param param2: Current line read from file
   :param param3: var to assign category
   :param param4: var to assign subcategory
   :param param5: temporary var to hold codes
   :param param6: var to assign codes
   :returns: return None, it changes var values
    """

    sys_pattern = re.compile(r"""^Σύστημα\s(.*)|(ΑΝΑΡΤΗΣΗΣ|ΠΛΑΣΤΙΚΑ|ΗΛΕΚΤΡΙΚΑ|Κινητήρας)""") #Σύστημα ψύξης εχεί ως σύστημα "Κινητήρας"
    temp_desc_pattern =  re.compile(r"""Περιγραφή\s(.*)|Εσωτερικοί επιλογείς ταχυτήτων""")
    temp_codes_pattern =  re.compile(r"""^(\d\d\||\d\|).*""")
    if (len(line)) == 1 and count != 0:
        codes.append(list(temp_codes2))
        temp_codes2 *= 0
    else:
        try:
            temp_categ.append(sys_pattern.match(line).group()) #Match keyword,space(group1)
        except AttributeError:
            sys_pattern.match(line)    
        try:
            temp_desc.append(temp_desc_pattern.match(line).group()) #Match keyword,space(group1)
        except AttributeError:
            temp_desc_pattern.match(line)      
        try:
            temp_codes2.append(temp_codes_pattern.match(line).group()) #Match keyword,space(group1)
        except AttributeError:
            temp_codes_pattern.match(line)

def cleanGroups(temp_categ,categ,temp_desc,desc):
    counter = 0
    for i in temp_categ:
        counter += 1
        countIndex.append(counter)
        if 'Σύστημα' in i:
            categ.append(re.sub(r"""^Σύστημα\s""", "", i))
        else:
            categ.append(i)        
    for i in temp_desc:
        if 'Περιγραφή' in i:
            desc.append(re.sub(r"""^Περιγραφή\s""", "", i))
        else:
            desc.append(i)    
    return countIndex

def num_Categ(categ):
    """
    Match categ, turn them into numerical values instead of strings for it to match mass entry software

    :param param1: Category
    :returns: strings matched turn into numeric
    """
    anart_patern = re.compile(r"""ΑΝΑΡΤΗΣΕΙΣ|ΑΝΑΡΤΗΣΗΣ|Αναρτήσεις - Τροχοί""")
    metad_patern = re.compile(r"""Σύστημα πέδησης - Μετάδοσης|Σύστημα πέδησης""")
    hlektrika_patern = re.compile(r"""ΗΛΕΚΤΡΙΚΑ|Ηλεκτρικές διατάξεις|Ηλεκτρική εγκατάσταση""")
    kinhthras_patern = re.compile(r"""Κινητήρας|Maintenance""")
    plasio_patern = re.compile(r"""ΠΛΑΣΤΙΚΑ$|Πλαίσιο - Πλαστικά μέρη - Αμαξώματα|ΡΕΖΕΡΒΟΥαριστ.""")
    timoni_patern = re.compile(r"""Τιμόνι\/Σύστημα διεύθυνσης|Τιμόνι - Χειριστήρια""")
    
    for i in range(len(categ)):
        if anart_patern.match(categ[i]):
            categ[i] = '1'
        elif metad_patern.match(categ[i]):
            categ[i] = '2'
        elif hlektrika_patern.match(categ[i]):
            categ[i] = '3'
        elif kinhthras_patern.match(categ[i]):
            categ[i] = '4'
        elif plasio_patern.match(categ[i]):
            categ[i] = '5'
        elif timoni_patern.match(categ[i]):
            categ[i] = '6'
        else:
            print ('EXCEPTION IN CATEGORY!!!!!!!!!!!!!!!!!!!!!')

def df_format(categ,desc,codes,countIndex):
    """
    Collect all info/vars into one file (currently xlsx/excel)
    
    :param param1: var with category
    :param param2: var with subcategory
    :param param3: var with codes
    :param param4: var with a count index
    :returns: return None, it saves all vars into file
    """
    data = {
        'Index': countIndex,
        'kathgoria': categ,
        'titlos': desc,
        'code': codes
    }
    print (data)

    #Troubleshoot Lenght
    if len(codes) == len(categ) == len(desc) == len(countIndex):
        print('Same length')
    else:
        print ('NOT SAME LENGTH!')
    print(len(codes),len(categ),len(desc),len(countIndex))
    print ('---------------')   

    df = pd.DataFrame(data)
    df = df.astype(str).apply(lambda col: col.str.strip('[]').str.replace("'","")) #Cleans leftover characters
    excelFile = str(insideDoubleDir[:-4])+".xlsx"
    df.to_excel(excelFile, index=False)
 
    
count = 0
countIndex = []
temp_categ=[]
categ=[]
temp_desc = []
desc=[]
codes=[]
temp_codes2 = []
partlist = []
baseDir = os.path.dirname(__file__)
og_path = os.listdir()
print ('Program Start')
for i in range(len(og_path)):
    print ('----'+ og_path[i] +'----') 
    if os.path.isdir(og_path[i]): #Level outside of motos, Check for moto folder 
        insideDir = os.path.join(baseDir,og_path[i]) #Path for a motor
        path_Files = os.listdir(insideDir) #var all files in moto

        for i in range(len(path_Files)):#Check all files in moto
            insideDoubleDir = os.path.join(insideDir,path_Files[i]) #Path for file/folder
            if insideDoubleDir.endswith('.txt'):#Detect .txt
                    with open (insideDoubleDir,'a')as f: #modify txt (needed)
                        f.write('\n')
                    with open (insideDoubleDir,'r')as f: #Open individual .txt
                        count = 0
                        countIndex *= 0
                        temp_categ *= 0 #Fastest clear apparently
                        categ *= 0
                        temp_desc *= 0
                        desc *= 0
                        codes *= 0
                        for line in f:
                            groupSearch(count,line,temp_categ,temp_desc,temp_codes2,codes)
                            count += 1
                        cleanGroups(temp_categ,categ,temp_desc,desc)
                        num_Categ(categ)
                        
                        #print (categ)
                        #print (desc)
                        #print (codes)
                        df_format(categ,desc,codes,countIndex)

        for i in range(len(path_Files)):#Repeat checking all files, needs txt first
            insideDoubleDir = os.path.join(insideDir,path_Files[i]) #Path for file/folder
            if os.path.isdir(insideDoubleDir):
                insideCateg = os.path.join(insideDir,insideDoubleDir) #Path inside a categ folder
                categList = os.listdir(insideCateg)
                for file in categList:
                    categPathFile = os.path.join(insideCateg,file)
                    partlist.append(categPathFile) #List of all images in categ
        #Naming
        nameExcel = re.search(r"(?<=\d )(.+)$", insideDir).group() #match path of moto folders (without the digit)
        copyExcel = nameExcel +" path.xlsx"
        nameExcel += ".xlsx"

        #Path define
        copyPathExcel =os.path.join(insideDir,copyExcel)
        pathExcel = os.path.join(insideDir,nameExcel)
        shutil.copy(pathExcel, copyPathExcel)
        df = pd.read_excel(pathExcel)
        df['path'] = ''
        for i in range(len(partlist)):
            matchWebp = re.search(r"(?<=\d\s)[^\\]+(?=\.webp)", partlist[i]).group().replace('_','/') #grab .webp from var and filter | [^\d\\]+(?=\s*\.webp$) needs trim front
            #print(matchWebp)
            df.loc[df['titlos'] == matchWebp, 'path'] = partlist[i]
            df.to_excel(copyPathExcel, index=False)
        os.remove(pathExcel)
    partlist *= 0
    

print ('Finished')

time.sleep(10000)
