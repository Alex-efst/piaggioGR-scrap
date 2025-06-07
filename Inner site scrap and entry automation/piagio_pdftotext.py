import re
import pypdf
import sys
import os

# ===FILE NAMING===
pdf_path = 'downloadcatalogpdf.pdf'
output_txt = 'downloadcatalogpdf.txt'
tempTxt = 'temp.txt'
finalTxt = 'result.txt'
# ===Global Paterns===
peri = re.compile(r'^Περιγραφή ([α-ω]|[Α-Ω]|[Ά-Ώ]|[ά-ώ]|[a-z]|[A-Z]|\d).*')
syst = re.compile(r'^Σύστημα ([α-ω]|[Α-Ω]|[Ά-Ώ]|[ά-ώ]|[a-z]|[A-Z]|\d).*')


def pdf_to_text(pdf_path, output_txt):
    # Open the PDF file in read-binary mode
    with open(pdf_path, 'rb') as pdf_file:
        # Create a PdfReader object instead of PdfFileReader
        pdf_reader = pypdf.PdfReader(pdf_file)

        # Initialize an empty string to store the text
        text = ''

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

    # Write the extracted text to a text file
    with open(output_txt, 'w', encoding='utf8') as txt_file:
        txt_file.write(text)


def EditTxt():
    print ('Starting Edit \n')
    with open(output_txt,'r', encoding='utf8')  as reader:
            numCode = re.compile(r'^((\d{1,2}\w)|(\w{1,2}))\s(\w*)') 
            #WARNING: Handle codes only up 2 digits, can't difrentiate it with names (e.g.MP3 300) (same for 2 digits e.g. SX 50)
            #Possible solution: \w{1,3}\s\w{6,X LIMIT Number} X seems to be 8-10. Risk of deleting codes
            dltFIlter = re.compile(r'^Σύστημα ([α-ω]|[Α-Ω]|[Ά-Ώ]|[ά-ώ]).*\d')
            for line in reader:
                searchNum = numCode.search(line)
                if dltFIlter.search(line):
                    print(line)
                elif syst.search(line):
                    with open (tempTxt,'a') as writeResult:
                        writeResult.write("\n"+line)
                elif peri.search(line):
                    with open (tempTxt,'a') as writeResult:
                        writeResult.write(line)
                elif searchNum:
                    modLine = searchNum.group(0) + "\n"
                    FinalLine = re.sub(" ", "|", modLine)
                    with open (tempTxt,'a') as writeResult:
                        writeResult.write(FinalLine)

def gamiountaiKounti():
    print ("\nGamiounte h kointi\n")


def cleanEmptyTitles():
    with open(tempTxt,'r+') as reader:
        lines = reader.readlines()
        reader.seek(0)
        counter = 0
        try:
            for line in lines:
                    checkSys = syst.search(line)
                    checkPeri = peri.search(line)
                    counter += 1 
                    if checkSys and lines[counter+1] == '\n':
                        print(counter)
                    elif checkPeri and lines[counter] == '\n':
                        print(counter)
                    else:
                        reader.write(line)
                        reader.truncate()
        except IndexError:
            print ("Hit last line, indexerror")

def dltNewLines():
    with open(tempTxt,'r+') as reader:
        lines = reader.readlines()
        reader.seek(0)
        for line in lines:
            if line != "\n":
                    reader.write(line)
                    reader.truncate()

def addNewLines():
    with open(tempTxt,'r+') as reader:
        lines = reader.readlines()
        reader.seek(0)
        for line in lines:
            checkSys = syst.search(line)
            if checkSys:
                    reader.write('\n'+ line)
                    reader.truncate()
            else:
                reader.write(line)
                reader.truncate()


def TitleChange():
    with open(tempTxt,'r+') as reader:
        lines = reader.readlines()
        reader.seek(0)
        for line in lines:
            #==Paterns==
            patPla = re.compile(r'^Σύστημα\sΠλαίσιο')
            patAma = re.compile(r'^Σύστημα\sΑμάξωμα')
            patTro = re.compile(r'^Σύστημα\sΤροχοί')
            patFota = re.compile(r'^Σύστημα\sΦΩΤΑ ΕΜΠΡΟΣ - Όργανα')
            patRez = re.compile(r'^Σύστημα\sΡΕΖΕΡΒΟΥΑΡ')
            patCold = re.compile(r'^Σύστημα\sΣύστημα ψύξης')
            
            #==Searches==
            checkPla = patPla.search(line)
            checkAma = patAma.search(line)
            checkTro = patTro.search(line)
            checkFota = patFota.search(line)
            checkRez = patRez.search(line)
            checkCold = patCold.search(line)
            #== Line Check ==
            if checkPla:
                subLine = re.sub(patPla,'ΠΛΑΣΤΙΚΑ',line)
                reader.write(subLine)
                reader.truncate()
            elif checkAma:
                subLine = re.sub(patAma,'ΠΛΑΣΤΙΚΑ',line)
                reader.write(subLine)
                reader.truncate()
            elif checkTro:
                subLine = re.sub(patTro,'ΑΝΑΡΤΗΣΗΣ',line)
                reader.write(subLine)
                reader.truncate()
            elif checkFota:
                subLine = re.sub(patFota,'ΗΛΕΚΤΡΙΚΑ',line)
                reader.write(subLine)
                reader.truncate()
            elif checkRez:
                subLine = re.sub(patRez,'ΠΛΑΣΤΙΚΑ',line)
                reader.write(subLine)
                reader.truncate()
            elif checkCold:
                subLine = re.sub(patCold,'Κινητήρας',line)
                reader.write(subLine)
                reader.truncate()
            else:
                reader.write(line)


def dltFIles():
    os.remove(pdf_path)
    os.remove(output_txt)

    

def dltCopyPeri():
    with open(tempTxt,'r') as reader, open(finalTxt,'a')as writeF:
        lines = reader.readlines()
        reader.seek(0)
        savePeri = ""
        # for line in lines:
        #     checkPeri = peri.search(line)
        #     if checkPeri:
        #         if line == savePeri and countPeri == 1:
        #             lineCopyCounter = counter
        #             while lines[lineCopyCounter+1] != savePeri:
        #                 lineCopyCounter += 1
        #             print ('dlt '+line)               
        #         elif line != savePeri and countPeri== 1:
        #             counter += 1
        #             savePeri += line
        #             countPeri = 1
        #             reader.write(line)
        #             print ('different '+line)
        #             reader.truncate()
        #         else:
        #             counter += 1
        #             countPeri += 1
        #             savePeri = line
        #             reader.write(line)
        #             print ('different 1 '+line)
        #             reader.truncate()
        #     else:
        #             counter +=1
        #             reader.write(line)
        #             print ('codes '+line)
        #             reader.truncate()



while True:
    try:
        inputCondition = input("1:PDF to text \n2:Edit txt \n3:Dlt Files \n4:Do all above steps \n")
        if inputCondition == '1':
            pdf_to_text(pdf_path,output_txt)
            print ('Pdf to text success')
        elif inputCondition == '2':
            EditTxt()
            cleanEmptyTitles()
            dltNewLines()
            addNewLines()
            TitleChange()
            #dltCopyPeri()
            print ('Edit done')
        elif inputCondition == '3':
            dltFIles()
            print ('Deletion done')
        elif inputCondition == '4':
            pdf_to_text(pdf_path,output_txt)
            print ('Pdf to text success')
            EditTxt()
            cleanEmptyTitles()
            dltNewLines()
            addNewLines()
            TitleChange()
            #dltCopyPeri()
            print ('Edit done')
            dltFIles()
            print ('Deletion done')
        elif inputCondition == '5':
            gamiountaiKounti()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
