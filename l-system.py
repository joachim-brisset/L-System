actions = {
    'a': ["pd()", "fd({taille})"],
    'b': ["pu()", "fd({taille})"],
    '+': "right({angle})",
    '-': "left({angle})",
    '*': "right(180)",
    '[': "#TODO",
    ']': "#TODO"
}
def check(f):

    dico = {"axiome":None, "regles":{}, "angle":None, "taille":None, "niveau":None}
    filecorrect = True
    i = 0
    with open(f , "r") as fichier:
        lines = fichier.readlines()
        while i < len(lines):
            
            liste = lines[i].split("=")
            liste = list(map(lambda item: item.strip(" \"\n"),liste))

            if liste[0]=="regles":
                if liste[1] != "": dico["regles"][liste[1]]=liste[2]

                i +=1    
                while lines[i].startswith("\"") :
                    
                    liste = lines[i].split("=")
                    liste = list(map(lambda item: item.strip(" \"\n"),liste))
                    dico["regles"][liste[0]]=liste[1]
                    i +=1
            else: 
                if liste[0] in dico:  
                    if dico[liste[0]] != None:
                        print ("erreur , plusieurs occurences de la règle", liste[0])
                        filecorrect = False
                    dico[liste[0]]=liste[1]  
                i+=1 
    return dico,check2(dico) and filecorrect

def check2(dico):
    filecorrect = True

    if dico["axiome"] == None or dico["axiome"] =="":
        print("la règle 'axiome' est vide")
        filecorrect = False
    try:
        if  dico["taille"]== None or  int(dico["taille"])<0 :
            print("la règle 'taille' est vide ou a une valeur fausse (<0) ou a un caratere faux")
            filecorrect = False
    except ValueError:
        print("la règle 'taille' est vide ou a une valeur inférieur à 0 ou a un caratere faux")
        filecorrect = False

    try:
        if  dico["angle"]== None or not(int(dico["angle"])>=0 and int(dico["angle"])<360) :
            print("la règle 'angle' est vide ou a une valeur fausse (0-360) ou a un caratere faux")
            filecorrect = False
    except ValueError:
        print("la règle 'angle' est vide ou a une valeur inférieur à 0 ou a un caratere faux")
        filecorrect = False
    try:
        if int(dico["niveau"])<0 or dico["niveau"]== None :
            print("la règle 'niveau' est vide ou a une valeur inférieur à 0 ou a un caratere faux")
            filecorrect = False
    except ValueError:
        
        print("la règle 'niveau' est vide ou a une valeur inférieur à 0 ou à un caratere faux")
        filecorrect = False

    return filecorrect  

def generate_L_System_by_Level(dictionnaire,axiome,niveau):
    for loop in range(niveau):
        t=''
        for i in axiome:
            t += dictionnaire[i] if i in dictionnaire else i
        axiome = t    
    return(t)


def LSystemToPythonCode(axiome, f):
    ''' convert an axiome's L-System string to an executable Python code to draw the L-System '''

    openedFile = open(f, 'w')
    openedFile.write("from turtle import *\n")
    openedFile.write("speed(0)\n")
    for i in axiome:
        if isinstance(actions[i], list):
            for j in actions[i]:
                openedFile.write(j + "\n")
        else:
            openedFile.write(actions[i] + "\n")

    openedFile.write("done()\n")
    openedFile.close()


lsys,correct=check("input/Lsystem.txt")
''' replace all placeholder in actions '''
if correct:
    for key,value in actions.items():
        if isinstance(value, list):
            array = []
            for i in value:
                array.append(i.format(taille=lsys["taille"],angle=lsys["angle"]))
            actions.update({ key : array })
        else:
            actions.update({ key : value.format(taille=lsys["taille"],angle=lsys["angle"]) })       

    LSystemToPythonCode(generate_L_System_by_Level(dictionnaire = lsys["regles"],axiome= lsys["axiome"],niveau=int(lsys["niveau"])), "C:/Users/super/Desktop/projet_algo/L-System/test.py")
