lecturesID = [("Limba","lang1"),
              ("Limba străină 1", "lang1"),
              ("Limbă străină I", "lang1"),
              ("Limbă engleză 1", "lang1"),
              ("Limba străină 2", "lang2"),
              ("Limbă străină II", "lang2"),
              ("Limbă engleză 2", "lang2"),
              ("Limba străină 3", "lang3"),
              ("Limbă străină III", "lang3"),
              ("Limbă engleză 3", "lang3"),
              ("Limba străină 4", "lang4"),
              ("Limbă străină IV", "lang4"),
              ("Limbă engleză 4", "lang4"),
              (" Limba engleză 4", "lang4"),
              ("Educaţie fizică 1", "sport1"),
              ("Educatie fizica 1", "sport1"),
              ("Educaţie fizică I", "sport1"),
              ("Educaţie fizică 2", "sport2"),
              ("Educatie fizica 2", "sport2"),
              ("Educaţie fizică II", "sport2"),
              ("Educaţie fizică 3", "sport3"),
              ("Educatie fizica 3", "sport3"),
              ("Educaţie fizică III", "sport3"),
              ("Educaţie fizică 4", "sport4"),
              ("Educatie fizica 4", "sport4"),
              ("Educaţie fizică IV", "sport4"),
              ("Fundamente de matematica", "algebra1"),
              ("Fundamente de matematică", "algebra1"),
              ("Algebră și geometrie analitică", "algebra1"),
              ("Proiect de programare", "PRJ"),
              ("Proiect individual", "PRJ"),
              ("Elemente de web design","web"),
              ("Elemente de web design/ Metode și practici în informatică","web"),
              ("Elemente de web design (EWD) / Programare vizuala", "web"),
              ("Securitate şi criptografie", "secCloud" ),
              ("Securitate și criptografie/ Prelucrarea imaginilor/ Cloud Computing și IoT", "secCloud"),
              ("Securitate şi criptografie (SC) / Medii de proiectare şi programare (MPP) / Vedere artificială pentru vehicule (VA)", "secCloud"),
              ("Administrarea bazelor de date/ Sisteme de operare II/ Programare pe dispozitive mobile/ Geometrie computațională", "DB_SO2"),
              ("Administrarea bazelor de date", "DB_SO2"),
              ("Programare logică și funcțională", "PLF"),
              ("Programare logică şi funcţional", "PLF"),
              ("Programare logică şi funcţională", "PLF"),
              ("Stagiu de practică", "Stagiu"),
              ("Stagiu de practică II", "Stagiu"),
              ("Toponomie şi etnografie", "Trans"),
              ("Disciplină complementară opţională care formează competenţe transversale II", "Trans2"),
              ("Disciplină complementară opţională care formează competenţe transversale III", "Trans3")
              ]

class Lecture:
    _name = ""
    _sem = ""
    _year = 0
    _nrHLec= 0
    _nrHPrac = 0
    _grade = 0
    _credit = 0
    _id = ""
    def __init__(self):
        pass

    def __init__(self, name, year, sem, nrHLec, nrHPrac, grade, credit):
        self._name= name
        self._year = year
        self._sem = sem
        self._nrHLec = nrHLec
        self._nrHPrac = nrHPrac
        self._grade = grade
        self._credit = credit
        self._name = self._name.replace("ș", "ş")        
        self._name = self._name.replace("ț", "ţ")        
        self.generateID()
    def generateID(self):
        lectureName = self._name
        if " / " not in lectureName:
            if "(" in lectureName:
                lectureName = lectureName[:lectureName.find("(")-1]
        foundID = False
        for (name, id) in lecturesID:
            if name==lectureName:
                self._id = id
                foundID = True
        if not foundID:
            self._id = lectureName
        
    def __str__(self):
        return " ".join([self._id, ":", self._name, "Year" + str(self._year), "Sem"+self._sem, str(self._nrHLec), str(self._nrHPrac), str(self._grade), str(self._credit)])

class StudentData:
    _name = ""
    _nr = ""
    _profile = ""
    _year = 0
    _years = []
    _listLecture = []
    def __init__(self):
        pass
    def __str__(self):
        return " ".join([self._name, self._nr, self._profile, str(self._year), " ".join(self._years)])
