from doEquivalency import getNotEquivalent
from doEquivalency import getEquivelancy
from parseTemplate import parseTemplate
from parseStudent import parseFromXls
from parseStudent import parseFromPdf
from studentData import Lecture

#student = parseFromPdf("")
student = parseFromXls("inputFile/Szekely.xls")
print(student)

parser = parseTemplate("Template/5. Reinmatriculare.docx")
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
