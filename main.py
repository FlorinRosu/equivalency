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
for dir in listDirs:
    currDir = inputDirName+dir
    listOfStudents = [fileName for fileName in os.listdir(currDir) if ".xls" in fileName]
    print (listOfStudents)
    
    #listOfStudentsToCheck = [listOfStudents[0]]
    listOfStudentsToCheck = listOfStudents
    for studentFile in listOfStudentsToCheck:
        student = parseFromXls(currDir,studentFile)
        print(student)
        
        parser = parseTemplate(currDir + "/5. Reinmatriculare.docx")
        lecturesToBeEqui = parser.getListOfLectures() 
        
        print("STUDENT LECTURE")
        for l in student._listLecture:
            print(l)
        print("TO EQ")
        for l in lecturesToBeEqui:
            print(l)
        
        equivalencyPairs = getEquivelancy(student, lecturesToBeEqui) #list of pairs of lectures
        
        notEquivalent = getNotEquivalent(student, equivalencyPairs) #list of lectures promoted but not equivaled
        
        print("WHAT HAVE EQ")
        for eq in equivalencyPairs:
            print(eq[0], "<=>", eq[1])
        print("WHAT DOESNT HAVE")
        for noteq in notEquivalent:
            print(noteq)
        
        parser.writeDocument(student, equivalencyPairs, notEquivalent)
        print ("DONE for ", student._name)
