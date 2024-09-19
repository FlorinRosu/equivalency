from studentData import Lecture
from docx import Document
from docx.enum.section import WD_ORIENT
from docx.shared import Inches


class parseTemplate():
    _listOfLecture = []
    _fileName = ""
    def __init__(self,fileName):
        self._fileName = fileName
        self.readListOfLectures()
    def getListOfLectures(self):
        return self._listOfLecture
    def readListOfLectures(self):
        temp = Document(self._fileName)
        tables = temp.tables
    
        paragraphs = temp.paragraphs
        i=0

        #debug printing
        for par in paragraphs:
            print(i, par.text)
            i=i+1

        for i in range(len(tables)-2):
            print("TABLE -----------  ")
            countRow = 0
            for row in tables[i].rows:
                j = 0
                toSkip = False
                for cell in row.cells:
                    print(j, cell.text, end = "|")
                    if "Disciplina promov" in cell.text:
                        toSkip = True
                    j = j+1
                print()
                if toSkip:
                    continue
                lectureName = row.cells[6].text
                l = Lecture(lectureName,i+1, "-",row.cells[7].text,row.cells[8].text,"-",row.cells[10].text)
                self._listOfLecture.append(l)
    
    def set_col_widths(self,table, widths):
        for row in table.rows:
            for idx, width in enumerate(widths):
                row.cells[idx].width = width
        return table
    def printTableEqui(self,doc, equivalent, y):
        nCol = 10
        nRow = 1 #starts from header
        for e in equivalent:
            if (e[1]._year == y):
                nRow = nRow+1
    
        t = doc.add_table(rows = 0, cols = nCol)
        t.style = "Table Grid"
        #add header
        cells = t.add_row().cells
        cells[0].text = "Disciplina promovata"
        cells[1].text = "Nr. ore curs"
        cells[2].text = "Nr. ore lab/sem"
        cells[3].text = "Nota"
        cells[4].text = "Nr. credite"
        cells[5].text = "Disciplina echivalata"
        cells[6].text = "Nr. ore curs"
        cells[7].text = "Nr. ore lab/sem"
        cells[8].text = "Nota"
        cells[9].text = "Nr. credite"
        
        for e in equivalent:
            if (e[1]._year == y):
                e[1]._grade = e[0]._grade
                cells = t.add_row().cells
                idx = 0
                for l in e:
                    cells[idx].text = l._name
                    cells[idx+1].text = l._nrHLec
                    cells[idx+2].text = l._nrHPrac
                    cells[idx+3].text = l._grade
                    cells[idx+4].text = l._credit
                    idx = 5
    
        widths = [Inches(2.55), Inches(0.425), Inches(0.425), Inches(0.425), Inches(0.425), Inches(2.55), Inches(0.425), Inches(0.425), Inches(0.425), Inches(0.425)]
        self.set_col_widths(t, widths)
        doc.add_paragraph()
    
    def printTableToRecontract(self,doc, equivalent):
        doc.add_paragraph()
        doc.add_paragraph("In urma echivalarii, studentul/studenta trebuie sa contracteze urmatoarele discipline")
        nCol = 4 
        t = doc.add_table(rows = 0, cols = nCol)
        t.style = "Table Grid"
        #add header
        cells = t.add_row().cells
        cells[0].text = "Nr."
        cells[1].text = "Disciplina"
        cells[2].text = "Anul"
        cells[3].text = "Nr. credite" 
    
        i = 0
    
        for e in equivalent:
            if (e[1]._grade== ""):
                i= i+1
                cells = t.add_row().cells
                cells[0].text = str(i) 
                cells[1].text = e[1]._name
                cells[2].text = str(e[1]._year)
                cells[3].text = str(e[1]._credit)
                
        widths = [Inches(0.5), Inches(4), Inches(0.5)]
        self.set_col_widths(t, widths)
    
    def printTableNotEquivalent(self,doc, notEquivalent):
        pass
    
    def writeDocument(self,student, equivalent, notEquivalent):
        doc = Document(self._fileName)

        countYear = 0
        for par in doc.paragraphs:
            text = par.text
            if text.find("Student/ă:") != -1:
                par.text = par.text + student._name
            if text == "Numărul matricol vechi:":
                par.text = par.text + student._nr
            if text.find("Anul de studiu _____")!=-1:
                par.text = student._years[countYear] +";"+" "*30+ text[text.find(";")+1:]
                countYear = countYear + 1

        countYear = 0
        for table in doc.tables:
            if countYear >= student._year:
                continue

            countNr= 1
            for row in table.rows:
                lectureName = row.cells[6].text
                
                found = False
                l = ""
                
                for equi in equivalent:
                    if equi[1]._name == lectureName:
                        l = equi[0]
                        found = True
                        break
                print("NOT FOUND:",lectureName)
                if found == False:
                    continue

                cells = row.cells
                cells[0].text = str(countNr)

                cells[1].text = l._name
                cells[2].text = l._nrHLec
                cells[3].text = l._nrHPrac
                cells[4].text = l._grade
                cells[5].text = l._credit
                cells[9].text = l._grade
                
                countNr = countNr + 1
            countYear = countYear+1

        doc.save("./inputFile/" + student._name+ ".docx")
