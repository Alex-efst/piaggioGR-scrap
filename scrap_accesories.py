from selenium import webdriver
#from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import urllib.request
import os
import re
import pandas as pd
import random

#=== Page Loop Related // START // ===

def staticVars(titlosPath,abstractPath,timhPath):
    titlos = driver.find_element(By.XPATH, titlosPath).text
    abstract = driver.find_element(By.XPATH, abstractPath).text
    timh = driver.find_element(By.XPATH, timhPath).text
    timh = timh[2:]
    print (titlos)
    print (abstract)
    print (timh)
    return titlos,abstract,timh
    
def category():
    siteUrl = driver.current_url
    siteUrl = urllib.parse.unquote(siteUrl)
    categorySearch = re.findall('^[^/]*/[^/]*/[^/]*/[^/]*/[^/]*/([^/]*)', siteUrl)
    subcategorySearch = re.findall('^[^/]*/[^/]*/[^/]*/[^/]*/[^/]*/[^/]*/([^/]*)', siteUrl)
    category = str(categorySearch[0])
    subCategory = str(subcategorySearch[0])
    print(category)
    return siteUrl, category, subCategory

def dirNFiles(varCategory,titlos):
    #File/Directorie paths
    baseDir = os.path.dirname(__file__)
    catDir = os.path.join(baseDir,varCategory)
    itemDir = os.path.join(catDir,titlos)
    itemFileDir = os.path.join(itemDir,titlos + ".xlsx")

    #Check/Create
    if not os.path.isdir(catDir):
        os.makedirs(catDir)
    if not os.path.isdir(itemDir):
        os.makedirs(itemDir)
    try:
        with open(itemFileDir,'x'):
            pass
    except FileExistsError as e:
        print ("File already exists:\n",e)
    
    return itemDir,itemFileDir

def clickNextButton(numOfPhotoPath,nextButtonPath):
    #Find an elem that has the amount of imgs + reformat for counter
    try:
        numOfPhotoElem = driver.find_element(By.XPATH, numOfPhotoPath)
        numOfPhotoElem = numOfPhotoElem.get_attribute("innerText")
        numOfPhoto = numOfPhotoElem[-1]
        numOfPhoto = int(numOfPhoto)
    except:
        numOfPhoto = 1
    #-1 for use in counter, value doesn't change download image order
    if numOfPhoto>1: 
        numOfPhoto -= 1
        print ('First colour ' + str(numOfPhoto+1) + ' Images')
    else:
        print ('First colour ' + str(numOfPhoto) + ' Images')
    
    
    #Note: Problem was not all images loaded on first colour, it seems that it loads all image expect the one before the last one (e.g. 4 imgs, didn't load 3rd)
    #All images loaded for other colours

    #For first colour, click X amount of time to the next image
    try:
        for button in range(numOfPhoto):
            nextButtonElem = driver.find_element(By.XPATH, nextButtonPath).click()
            time.sleep(1.33)
    except:
        print('Next button not displayed')

def codeImgRepeat(buttonColourPath,currentColourTitlePath,prodCodePath,photoPath,titlos,itemDir):
    #Download/Naming Image(s)
    listSrc = []
    listAlt = []
    listImgPaths = []
    listCheckColour = []
    checkDuplicate = []
    def downImg(photoPath,titlos,itemDir):
        photoElem = driver.find_elements(By.XPATH, photoPath)
        if len(photoElem) != 0 : #If photo is empty (won't hit it on except)
            for link in photoElem: #Extraction of sources
                listSrc.append(link.get_attribute("src"))
                listAlt.append(link.get_attribute("alt"))
            for i in range(len(listAlt)): #Naming img
                if listSrc[i] not in checkDuplicate: #Check for Duplicated Images
                    listImgPaths.append(listSrc[i])
                    #----- Download Method---
                    listAlt[i] = listAlt[i].replace(titlos,"")
                    listAlt[i] = listAlt[i].strip(" ")
                    checkColour = listAlt[i] #Hold Colour here
                    listCheckColour.append(checkColour)
                    checkDuplicate.append(checkColour)
                    #imgName = str(i) + " " + listAlt[i] + ".webp"
                    #imgDir = os.path.join(itemDir,imgName)
                    #urllib.request.urlretrieve(listSrc[i], imgDir) #Download Command
                    checkDuplicate.append(listSrc[i])
                    #listImgPaths.append(imgDir)
                    time.sleep(randomFloat)
                else:
                    listCheckColour.append('remove')
                    listImgPaths.append('remove')
                    listAlt[i] = 'remove'
            
            for word in list(listCheckColour):
                if word == 'remove':
                    listCheckColour.remove(word)
                    
            for word in list(listImgPaths):
                if word == 'remove':
                    listImgPaths.remove(word)
                    
            for word in list(listAlt):
                if word == 'remove':
                    listAlt.remove(word)
        else:
            listImgPaths.append('Empty')
            #Static elem searche
            try:
                checkColour = driver.find_element(By.XPATH, currentColourTitlePath)
            except:
                checkColour = driver.find_element(By.XPATH, (currentColourTitlePath+"""/span"""))
            listCheckColour.append(checkColour.get_attribute("innerText"))
                
            print ('in except')
        
        print (str(listCheckColour)+'\n'+str(listImgPaths))
        print (len(listCheckColour))
        print (len(listImgPaths))
    
    # def rgbValue(rgbValuePath):
        # rgbValueElem = driver.find_element(By.XPATH, rgbValuePath)
        # rgbValueElem = rgbValueElem.get_attribute("style")
        # tempRgb = re.findall(r"\((.+?(?=\)))", rgbValueElem)
        # tempRgb = str(tempRgb[0])
        # varRgb = re.sub(r",",";",tempRgb)
        # varRgb = re.sub(r"\s","",varRgb)
        # varRgb = "=myRGB(" + varRgb + ")"
        # print (varRgb)
        # return varRgb
    
    #Get Code of product + trim spaces
    def mainCode(prodCodePath): 
        prodCode = driver.find_element(By.XPATH, prodCodePath).text 
        prodCode = prodCode.strip(" ")
        print (prodCode)

    #Grab code/img for all colours
    buttonColour = driver.find_elements(By.XPATH, buttonColourPath)
    for button in buttonColour:
        button.click()
        mainCode(prodCodePath)
        #varRgb = rgbValue(rgbValuePath)
        downImg(photoPath,titlos,itemDir)
        time.sleep(smallRandomFloat)
    
    return listCheckColour,listImgPaths
        
def writeFile1(itemFileDir,titlos,abstract,timh,familyFill,varCategory,subCategory,listCheckColour,listImgPaths,siteUrl):
    data = {
        'Τίτλος': titlos,
        'Περιγραφή': abstract,
        'Τιμή': timh,
        'Οικογένια': familyFill,
        'Κατηγορία': varCategory,
        'Υποκατηγορία': subCategory,
        'Χρώμα': listCheckColour,
        'Διαδρομή(είκονα)': listImgPaths,
        'URL': siteUrl,
    }
    df = pd.DataFrame(data)
    df.to_excel(itemFileDir, index=False)
    itemFileDir,titlos,abstract,timh,familyFill,varCategory,subCategory,listCheckColour,listImgPaths,siteUrl = []
            
def fillList(listImgPaths,familyCount,listMenuFamily):
    x=[]
    for i in range(len(listImgPaths)):
        x.append(listMenuFamily[familyCount])
    return x
            
def page(familyCount,listMenuFamily):
    #Paths to Elems
    titlosPath = """//h1[@class="product-presentation__title"]"""
    abstractPath = """//p[@class="product-presentation__abstract product-presentation__abstract--large"]"""
    timhPath = """//span[@class='product-price__list']/span[not(@role)]"""
    buttonColourPath = """//*[@class='nav nav-tabs']/li/a"""
    prodCodePath = """//p[@class="product-presentation__code"]"""
    photoPath = """//*[@class='hooper-track']/li/img[@src]"""
    numOfPhotoPath = """//div[@role='tabpanel']/div/section/div/ul[@class='hooper-track']/following-sibling::div"""
    nextButtonPath = """//div[@class='product-presentation_colors']/div/div/div/div/div/button/following-sibling::button"""
    currentColourTitlePath = """//span[@class='product-presentation_colors__current-color']"""
    # rgbValuePath = """//i[contains(@style, 'color')]"""
    
    
    #subMain / Action order
    time.sleep(2)
    titlos,abstract,timh = staticVars(titlosPath,abstractPath,timhPath) #Extract Title,abs,timh
    siteUrl, varCategory, subCategory = category() #Extract category
    itemDir,itemFileDir = dirNFiles(varCategory,titlos) #Check/Create Files,Directories
    clickNextButton(numOfPhotoPath,nextButtonPath) #Click nextbutton to load image(s)
    listCheckColour,listImgPaths = codeImgRepeat(buttonColourPath,currentColourTitlePath,prodCodePath,photoPath,titlos,itemDir) #Extract code/img for all colours
    familyFill = fillList(listImgPaths,familyCount,listMenuFamily)
    writeFile1(itemFileDir,titlos,abstract,timh,familyFill,varCategory,subCategory,listCheckColour,listImgPaths,siteUrl)


    
#=== Page Loop Related // END // ===

def repeatPages(familyCount,listMenuFamily):#All urls and pages
    listHref = []
    allItemUrls = driver.find_elements(By.XPATH, "//ul[@class='listing__items']/li/a[contains(@class, 'card-product--accessory')]")
    for elem in allItemUrls:
        listHref.append(elem.get_attribute("href"))
    print (listHref)

    windows_before  = driver.current_window_handle
    for href in listHref:
        driver.execute_script("window.open('" + href +"');") # Open the hrefs one by one through execute_script method in a new tab
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2)) # Induce  WebDriverWait for the number_of_windows_to_be 2
        windows_after = driver.window_handles
        new_window = [x for x in windows_after if x != windows_before][0] # Identify the newly opened window
        # driver.switch_to_window(new_window) <!---deprecated>
        driver.switch_to.window(new_window) # switch_to the new window
        time.sleep(randomFloat)
        # perform your webscraping here

        page(familyCount,listMenuFamily)
        
        #print(driver.title) # print the page title or your perform your webscraping
        driver.close() # close the window
        # driver.switch_to_window(windows_before) <!---deprecated>
        driver.switch_to.window(windows_before) # switch_to the parent_window_handle

def listingMenus():
    #Listing Menus
    #List families from Menu
    listMenuFamily = []
    skipFirst = 0
    allFamilies = driver.find_elements(By.XPATH, "//*[@id='family']/option")
    allCategories = driver.find_elements(By.XPATH, "//*[@id='category']/option")
    for familyElem in allFamilies:
        if skipFirst == 0:
            skipFirst = 1
            continue
        else:
            listMenuFamily.append(familyElem.get_attribute('text'))
            print (listMenuFamily)
            
    #List Category from menu
    listCategoryFamily = []
    skipFirst = 0
    for categoryElem in allCategories:
        if skipFirst == 0:
            skipFirst = 1
            continue
        else:
            listCategoryFamily.append(categoryElem.get_attribute('text'))
            print (listCategoryFamily)
    return listMenuFamily, listCategoryFamily


service = Service(executable_path="chromedriver.exe")
options = webdriver.ChromeOptions() 
# options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2}) #DISABLE JS
options.add_argument("start-maximized")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options, service=service)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'})
print(driver.execute_script("return navigator.userAgent;"))

randomFloat = random.uniform(4,7)
smallRandomFloat = random.uniform(1,2)
print ("\nNote: At the time of writing the robot.txt allows crawling to the site, if it ain't, you should not use the scrapper\nCheck vespa.com/robots.txt before proceeding")

driver.get("https://www.vespa.com/gr_EL/accessories/")
time.sleep(randomFloat)
print ('Out of sleep') 
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)  # Scroll down
time.sleep(2)


listMenuFamily, listCategoryFamily = listingMenus()
 
#DropDown category
menuCategory = driver.find_element(By.XPATH, "//*[@id='category']")
for i in range(len(listCategoryFamily)): #Scroll through categories
    menuCategory.send_keys(Keys.ARROW_DOWN)
    menuCategory.send_keys(Keys.ENTER)
    if listCategoryFamily[i] == "Αξεσουάρ οχήματος":
        menuFamilies = driver.find_element(By.XPATH, "//*[@id='family']")
        for i in range(len(listMenuFamily)):
            time.sleep(1)
            menuFamilies.send_keys(Keys.ARROW_DOWN)
            menuFamilies.send_keys(Keys.ENTER)
            familyCount = i
            repeatPages(familyCount,listMenuFamily)

        for i in range(len(listMenuFamily)): #Go back to "All families" in menu
            menuFamilies.send_keys(Keys.ARROW_UP)
            time.sleep(1)
        menuFamilies.send_keys(Keys.ENTER)
    else:
        familyCount = 0
        listMenuFamily = ['Empty']
        repeatPages(familyCount,listMenuFamily)

   
time.sleep(1)


    
print ('Finished')
time.sleep(1000000)
driver.quit()

#https://devhints.io/xpath
#https://stackoverflow.com/questions/52277877/how-to-open-multiple-hrefs-within-a-webtable-to-scrape-through-selenium
