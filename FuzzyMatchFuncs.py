from cdifflib import CSequenceMatcher
import os
import csv
import string
import logging
from datetime import datetime
from pathlib import Path
from nltk.corpus import stopwords
import time
#change
#mlDir = Path(r"\\SGC\ML_Project\MLM")
mlDir = Path(r"\\SGC\ML_Project\MLM_1")
childrenCategory = []
itemDetails, itemDetailsWithModel = [], []
titleList = []
modelList = []
upperCatList = []
trashWords = ["envío", "gratis", "envio", "nuevo"]
punctTable = str.maketrans('', '', string.punctuation)
nullValues = ["null", "NULL", "no model", "NO MODEL", "No Model", "n/a", "N/A", "other", "Other", "/", "not_specified"]
now = datetime.now()

def processFiles(directory):
    ind = 1
    for itemFile in os.listdir(directory):
        ind += 1
        subCat = os.path.basename(itemFile)[:-4]

        itemDetails.clear()
        itemDetailsWithModel.clear()
        wFile = directory._str + "\\" + itemFile

        if (os.path.isdir(wFile)):
            continue
        
        pcent = getCurrentPercentage(directory, ind)
        print("Working in ", directory.parts[2], "-", itemFile, " ", pcent.__round__(2), "% complete")

        try:
            with open(wFile, encoding='iso-8859-2', newline='') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    if row[12].strip("'") in nullValues:
                        itemDetails.append(row)
                    else:
                        itemDetailsWithModel.append(row)
                
                totals = len(itemDetails)
                if totals == 0:
                    continue
                iDetailsIndex = 0
                titleList = [processString(row[1]) for row in itemDetails]
                
                while iDetailsIndex < totals:
                    productTitle = processString(itemDetails[iDetailsIndex][1])
                    if iDetailsIndex == (totals-1):
                        modelList.append(getInitials(productTitle))
                        break
                    for y in range(iDetailsIndex+1,len(titleList)):
                        ratio = CSequenceMatcher(None, productTitle, titleList[y]).ratio()
                        modelList.append(getInitials(productTitle))
                        if ratio <= 0.75:
                            iDetailsIndex += 1
                            break 
                        iDetailsIndex += 1

                for i in range(len(itemDetails)):
                    itemDetails[i][12] = "\'" + modelList[i] + subCat[3:] + "\'"
        except:
            logging.exception("Error processing file")
            print("Error with file. Skipping...")
            continue

        itemDetails.extend(itemDetailsWithModel)
        #outputFile = "OUT" + '\\' + dirString + '\\' + upperCat + '.csv'
        outputFile = directory._str + "\\" + subCat + '.csv'
        
        try:
            with open(outputFile, mode='w', newline='', encoding='iso-8859-2') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=',')
                for row in itemDetails:
                    csv_writer.writerow(row)
        except OSError:
            logging.exception("Could not write output file")
            print("Could not write output file. Skipping...")
            continue

def getInitials(fullstring):
    xs = (processString(fullstring))
    wordList = xs.split()
    wordCount = len(wordList)
    initials = ""

    for word in wordList:
        initials += word[0].upper()
    if wordCount <= 4:
        for word in wordList:
            initials += word[1].upper()

    return initials

def processString(string):
    commonWords = []
    importantWords = []
    file1 = open("spanish.txt","r+")
    spanish_list = file1.read().split("\n")
    file1.close()

    string = string.translate(punctTable)
    string = string.strip(' ')
    tokens = string.split()

    for i in range(len(tokens)): 
        tokens[i] = tokens[i].lower() 

        commonWords = tokens
        
    for word in commonWords:
        if len(word) >= 2:
            if (word not in stopwords.words('spanish') and word not in 
            stopwords.words('english') and word not in spanish_list
            and word not in trashWords):
                importantWords.append(word)

    separator = ', '
    importantWords = separator.join(importantWords)

    importantWords = str(importantWords).replace(",", "")
    return importantWords

def getCurrentPercentage(directory, ind):
    dLen = len(os.walk(directory).__next__()[2])
    pcent = (ind * 100) / (dLen + 1)
    return pcent

def timerFunc(startTime, endTime):
    elapsed_s = ((((startTime - endTime)) * -1).__round__(2))
    elapsed_m = elapsed_s/60
    elapsed_h = elapsed_m/60

    if elapsed_s <= 60:    
        print("Process ended in ", elapsed_s, "seconds")
    elif elapsed_m <= 60:
        print("Process ended in ", elapsed_m, "minutes and", elapsed_s%60, "seconds")
    elif elapsed_h == 1:
        print("Process ended in ", elapsed_h, "hour", elapsed_m%60, "minutes and", elapsed_s%60, "seconds")
    else: 
        print("Process ended in ", elapsed_h, "hours", elapsed_m%60, "minutes and", elapsed_s%60, "seconds")
"""
MAIN SNIPPET
if (chItem == "\\\\SGC\\ML_Project\\MLM\\MLM1747\\Transform") or flg:
    flg = True
    try:
        processFiles(Path(chItem))
    except FileNotFoundError:
        print("File or Directory not found")
        return
else:
    continue
"""