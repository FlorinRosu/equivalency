from studentData import Lecture

def getEquivelancy(student, listOfLectures):
    emptyLecture = Lecture("","","","","","","")
    equivalent = []
    for lectToEq in listOfLectures:
        found = False
        for lectStudent in student._listLecture:
    
            if lectToEq._id== lectStudent._id:
                lectToEq._sem = lectStudent._sem
                if lectStudent._grade!="-" and lectStudent._credit != "-":
                    equivalent.append([lectStudent, lectToEq])
                    found = True
                    break
    
        if found == False:
            equivalent.append([emptyLecture, lectToEq])
    return equivalent

def getNotEquivalent(student, equivalent):
    
    notEquivalent = []
    for lectStudent in student._listLecture:
        if lectStudent._grade == "-":
            continue
        found = False
        for eq in equivalent:
            if lectStudent._name == eq[0]._name:
                found = True
                break
        if not found:
            notEquivalent.append(lectStudent)
    return notEquivalent
