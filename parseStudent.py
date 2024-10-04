from studentData import Lecture
from studentData import StudentData
import xlrd

def parseFromPdf(fileName):
    s = StudentData()
    return s

def parseFromXls(fileName):
    s = StudentData()

    workbook = xlrd.open_workbook(fileName)
    sheet = workbook.sheet_by_index(0)
    nCol = sheet.ncols
    nRow = sheet.nrows
    year = 0

    i = 0

    #parse lectures
    idxName = 3 
    idxHLec = 7 
    idxHPrac = 8 #and 8 and 9 
    idxGrade = 11 #and 12 
    idxCredit = 14 #and 15 
    idxSem = 18 # or 18

    if True: 
        idxName = 3 
        idxHLec = 6 
        idxHPrac = 7 #and 8 and 9 
        idxGrade = 10 #and 12 
        idxCredit = 13 #and 15 
        idxSem = 17 # or 18

    while i< nRow:
        startRow = i
        #parse student name
        for j in range(nCol):
            text = str(sheet.cell_value(i,j))
            if "CNP" in text:
                s._name = text[text.find("Notele ob")+43:text.find("CNP")-1]
        #parse nr matricol
        for j in range(nCol):
            text = str(sheet.cell_value(i,j))
            if "Extras din Registrul matricol" in text:
                strIndex = text.find("nr. matric")
                strIndex = text.find(":",strIndex)+2
                s._nr = text[strIndex:text.find("\n",strIndex)]
        #parse program of study
        for j in range(nCol):
            text = str(sheet.cell_value(i,j))
            if "Programul de studii" in text:
                strIndex = text.find("Programul de studii")
                strIndex = text.find(":",strIndex)+2
                s._profile = text[strIndex:text.find("\n", strIndex)]
                if "limba engl" in s._profile:
                    idxName = 3 
                    idxHLec = 7 
                    idxHPrac = 8 #and 8 and 9 
                    idxGrade = 11 #and 12 
                    idxCredit = 14 #and 15 
                    idxSem = 18 # or 18


        for j in range(nCol):
            if ("Disciplina de" in str(sheet.cell_value(i,j))):
                previous = startRow - 1
                for j in range(nCol):
                    text = str(sheet.cell_value(previous, j))
                    if "Anul" in text:
                        s._years.append(text)
                startRow = i+1
                break
        if (startRow == i+1):
            i = i+2
            year = year + 1
            while ("PROMOVAT" not in str(sheet.cell_value(i,2))):
                for j in range(nCol):
                    print(str(j),sheet.cell_value(i,j), end = '|')
                #print(sheet.cell_value(i, idxName), sheet.cell_value(i, idxGrade), sheet.cell_value(i, idxGrade+1))
                grade = "0"
                sem = sheet.cell_value(i, idxSem)
                deltaIDX_FOR_grade_credit = 0
                if sem == "II":
                    deltaIDX_FOR_grade_credit = 2

                grade = str(sheet.cell_value(i, idxGrade+deltaIDX_FOR_grade_credit))
                if (grade.isnumeric() or grade == "P"):
                    if (grade.isnumeric()):
                        if int(grade) <5:
                            grade = "-"
                    print("OK")
                else:
                    grade = "-"
                    print("NOK")
                name = sheet.cell_value(i, idxName)
                toSplit = name.find(" - Echiv")#some names have a suffix " - Echivalat". Remove this
                if toSplit != -1:
                    name = name[:toSplit]
                nrHLec = sheet.cell_value(i, idxHLec)
                nrHPrac = 0
                for j in range(3):
                    nrHPrac = sheet.cell_value(i, idxHPrac + j)
                    if (str(nrHPrac).isnumeric()):
                        break
                credit = sheet.cell_value(i, idxCredit + deltaIDX_FOR_grade_credit)
                l = Lecture(name, year, sem, nrHLec, nrHPrac, grade, credit)
                s._listLecture.append(l) 


                i = i + 1
                if i == nRow:
                    break

        i = i+1
    s._year = year
    return s
