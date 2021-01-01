dico = {"axiome":None, "regles":{}, "angle":None, "taille":None, "niveau":None}
dico2 = {"axiome", "angle", "taille", "niveau"}

i = 0
with open("input/Lsystem.txt" , "r") as fichier:
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
                dico[liste[0]]=liste[1]  
            i+=1 
            
print(dico)       


    
        
        
"""
        if liste[0] == "angle" and  not liste[1]== "":  
            if not(int(liste[1])>=0 and int(liste[1])<=360):
                print ("pb ac angle")
        

        if liste[0] in dico2 and liste[1]== "":
            print ("pb avec",liste[0],": aucune donnée de renseignée")
"""

            
"""
        if liste[0] == "regles":
            bool = True
        elif liste[0] in dico:
            bool = False
        else :
            continue

        if bool :
            if liste[0]== "regles": 
                if liste[1] != "":
                    dico["regles"][liste[1]]=liste[2]
                
                continue
                
            dico["regles"][liste[0]]=liste[1]


        else:
            dico[liste[0]]=liste[1]
print(dico)
"""