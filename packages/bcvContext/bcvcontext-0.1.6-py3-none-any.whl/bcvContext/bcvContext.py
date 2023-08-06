import json
from subprocess import call

notarizationPath = ""
isAudit = 1

def init(_notarizationPath, _isAudit) :
    global notarizationPath, isAudit
    notarizationPath = _notarizationPath
    isAudit = _isAudit

def scriptContext(filename) :
    return filename

def notarizationContextRawfile():
    return "../.." + notarizationPath + "/../rawFile.csv"

def notarizationContext(filename) :
    return "../.." + notarizationPath + "/" + filename

def dayContext(_m, _filename) :
    if (_m >= 0) : raise Exception("No history at J", str(_m))
    day = json.load(open("../.." + notarizationPath + "/.config.json"))["day"] + _m
    if (day < 0) : raise Exception("No history at J", str(day))
    lastNotarization = json.load(open("../.." + notarizationPath + "/../../Day" + str(day) + "/.dayConfig.json"))["lastNotarization"]
    return "../.." + notarizationPath + "/../../Day" + str(day) + "/Notarization" + str(lastNotarization) + "/" + _filename

def finish(*args) :
    call(["rm", "-r","../__cache__"])
    if isAudit == 1 :
        call(["mkdir","../__cache__"])
        for i in args :
            call(["mv",str(i),"../__cache__"])
        print("Final result at :", "../__cache__")

    else : 
        for i in args : 
            call(["mv",str(i),"../.." + notarizationPath])
        print("Final result at :", "../.." + notarizationPath)