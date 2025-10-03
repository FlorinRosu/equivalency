import os
from doEquivalency import getNotEquivalent
from doEquivalency import getEquivelancy
from parseTemplate import parseTemplate
from parseStudent import parseFromXls
from parseStudent import parseFromPdf
from studentData import Lecture

#student = parseFromPdf("")
inputDirName = "./inputFile/"
listDirs = os.listdir(inputDirName)
print(listDirs)

dicForStudents = {}
dicForNames = {}
toCheck = []

for dir in listDirs:
    currDir = inputDirName+dir
    listOfStudents = [fileName for fileName in os.listdir(currDir) if ".xls" in fileName]
    print (listOfStudents)
    
    #listOfStudentsToCheck = [listOfStudents[0]]
    listOfStudentsToCheck = listOfStudents
    for studentFile in listOfStudentsToCheck:
        student = parseFromXls(currDir,studentFile)

        print("STUDENT:",student)
        
        parser = parseTemplate(currDir + "/" + dir + ".docx")
        lecturesToBeEqui = parser.getListOfLectures() 

        
        print("STUDENT's LECTURES:")
        for l in student._listLecture:
            print(l._name)
        print("TO EQ")
        for l in lecturesToBeEqui:
            print(l._name)
        exit
        
        equivalencyPairs = getEquivelancy(student, lecturesToBeEqui) #list of pairs of lectures
        
        notEquivalent = getNotEquivalent(student, equivalencyPairs) #list of lectures promoted but not equivaled
        
        print("WHAT HAVE EQ")
        count = 0
        for eq in equivalencyPairs:
            print(eq[0], "<=>", eq[1])
            if eq[0]._id == "":
                count = count+1
                if eq[1]._id in dicForStudents:
                    dicForStudents[eq[1]._id].append(student._name)
                    if (eq[1]._name not in dicForNames[eq[1]._id]):
                        dicForNames[eq[1]._id].append(eq[1]._name)
                else:
                    dicForStudents[eq[1]._id] = [student._name]
                    dicForNames[eq[1]._id] = [eq[1]._name]

        if count > len(equivalencyPairs) - 3:
            toCheck.append(student._name)


        print("WHAT DOESNT HAVE")
        for noteq in notEquivalent:
            print(noteq)
        
        parser.writeDocument(student, equivalencyPairs, notEquivalent)
        print ("DONE for ", student._name)



dataExcel = {}
max = 0
for el in dicForStudents:
    if len(dicForStudents[el])>max:
        max = len(dicForStudents[el])

for el in dicForStudents:
    id = ' $$ '.join(dicForNames[el])
    dataExcel[id] = dicForStudents[el]
    toAdd = max - len(dicForStudents[el])
    for i in range(toAdd):
        dataExcel[id].append("")

from openpyxl import load_workbook
import pandas as pd
writer = pd.ExcelWriter('test.xlsx')
wb = writer.book
df = pd.DataFrame(dataExcel)
df.to_excel(writer, index = False)
wb.save('test.xlsx')

print("TO CHECK:",toCheck)
