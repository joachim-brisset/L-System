import sys
import getopt
import os

def inputFile(message="file's path : ", defaultFile = None, shouldExist = None):
    ''' handle user's file input validity '''

    filename = os.path.abspath(defaultFile or input(message))  # ask user for file path if no default file path proveided

    if shouldExist and not os.path.isfile(filename):                        # if file should exist check it
        print("Sorry but the path you provide for the file does not exist")
        return inputFile(message=message, shouldExist=True)
    
    if filename.find("<>:*?|") != -1:                                       # check naming normes
        print("Sorry but you provided a non valid filename ('<>:*?|')")
        return inputFile(message=message, shouldExist=shouldExist)

    if shouldExist == None and os.path.isfile(filename):                    # handle if file alredy exist
        print("The file you provided already exist should we continue ? (yes/no)")
        response = input()
        while not response in ("yes","no","Y","N"):
            print("The file you provided already exist should we continue ?")
            response = input()
        
        if response in ("no","N"): return inputFile(message=message, shouldExist=shouldExist)

    return filename
def choice(value, choice):
    for i,j in enumerate(choice):
        print(str(i) + " : " + j)
    response = input("Choose one >> ")
    while not response in [str(i) for i in range(len(choice))]:
        response = input("Choose one >> ")
    return value[int(response)]
def loadInput(filename, lsystem):
    ''' load from a file all L-System's parameters '''

    error = False   # True ther is a problem with L-System parameters
    currentDict = ''
    i = 0

    with open(filename, "r") as fichier:    #similaire to try/finally
        lines = fichier.readlines()
        while i < len(lines):
            elements = list(map(lambda item: item.strip(" \"\n"), lines[i].split("=")))

            if elements[0] == '': 
                i += 1
                continue
            if elements[0] in lsystem:
                if isinstance(lsystem[elements[0]], dict):
                    currentDict = elements[0]
                    if elements[1] != "": lsystem[currentDict][elements[1]] = elements[2]  # handle increasing rule on same line as 'regles'

                    i += 1    
                    while lines[i].strip().startswith("\"") :   # new loop handling rules with multiple line
                        
                        elements = list(map(lambda item: item.strip(" \"\n"), lines[i].split("=")))
                        if elements[0] in lsystem[currentDict]:
                            print("rules : " + elements[0] + " already exist in " + currentDict + ". Choose the correct one : ")
                            lsystem[currentDict][elements[0]] = choice(
                                [ lsystem[currentDict][elements[0]], elements[1] ],
                                [ elements[0] + " => " + lsystem[currentDict][elements[0]], elements[0] + " => " + elements[1] ]
                            )
                        lsystem[currentDict][elements[0]] = elements[1]
                        i += 1

                else:
                    if lsystem[ elements[0]] != None:
                        print ("erreur , plusieurs occurences de la règle", elements[0])
                        error = True
                    lsystem[elements[0]] = elements[1] 
                    i += 1 
            else:
                print("Unknow rules : " + elements[0])
                print("Error not severe, continue program ...")  
                i += 1
            '''
            if elements[0]=="regles":   # handle 'regles' rules 
                if elements[1] != "": lsystem["regles"][elements[1]] = elements[2]  # handle increasing rule on same line as 'regles'

                i += 1    
                while lines[i].strip().startswith("\"") :   # new loop handling increasing rules 
                    
                    elements = list(map(lambda item: item.strip(" \"\n"), lines[i].split("=")))
                    lsystem["regles"][elements[0]] = elements[1]
                    i += 1
            else: 
                if elements[0] in lsystem:  
                    if lsystem[ elements[0]] != None:
                        print ("erreur , plusieurs occurences de la règle", elements[0])
                        error = True
                    lsystem[elements[0]] = elements[1]  
                i+=1 
            '''

    return checkLSystem(lsystem) or error
def checkLSystem(lsystem):
    ''' Check the validity of all L-System's parameters '''

    error = False
    if lsystem["axiome"] == None or lsystem["axiome"] == "":
        print("[Error] >> la règle 'axiome' est vide")
        error = True

    try:
        if lsystem["taille"] == None or int(lsystem["taille"]) < 0:
            print("[Error] >> la règle 'taille' est vide ou a une valeur invalide (<0)")
            error = True
    except ValueError:
        print("[Error] >> la règle 'taille' n'est pas un nombre !")
        error = True

    try:
        if lsystem["angle"] == None or int(lsystem["angle"]) < 0 or int(lsystem["angle"]) > 360 :
            print("[Error] >> la règle 'angle' est vide ou a une valeur invalide (<0 or >360)")
            error = True
    except ValueError:
        print("[Error] >> la règle 'angle' n'est pas un nombre !")
        error = True

    try:
        if int(lsystem["niveau"]) < 0 or lsystem["niveau"] == None :
            print("[Error] >> la règle 'niveau' est vide ou a une valeur invalide (<0)")
            error = True
    except ValueError:
        print("[Error] >> la règle 'niveau' n'est pas un nombre !")
        error = True

    return error
def formatActions(lsystem, actions):
    ''' replace all placeholder in actions '''

    for key,value in actions.items():
        if isinstance(value, list):
            array = []
            for i in value:
                array.append(i.format(taille=lsystem["taille"],angle=lsystem["angle"]))
            actions.update({ key : array })
        else:
            actions.update({ key : value.format(taille=lsystem["taille"],angle=lsystem["angle"]) })
def generate_L_System_by_Level(rules, axiome, level):
    ''' generate the L-System for the desired level '''

    for loop in range( int(level) ):
        temp = ''
        for i in axiome:
            temp += rules[i] if i in rules else i
        axiome = temp    
    return temp
def LSystemToPythonCode(axiome, action, f):
    ''' convert an axiome's L-System string to an executable Python code to draw the L-System '''

    openedFile = open(f, 'w')
    openedFile.write("from turtle import *\n")      # needed for drawing
    openedFile.write("speed(0)\n")                  # increase at maximum the drawing speed

    for i in axiome:                                # for each symbol in axiome write the associated function(s)
        if not i in actions:
            print("[Error] >> le symbole " + i + " n'a pas d'action associée a lui")
            openedFile.close()
            os.remove(f)
            return False

        if isinstance(actions[i], list):            # handle multiples functions for 1 symbols 
            for j in actions[i]:
                openedFile.write(j + "\n")
        else:
            openedFile.write(actions[i] + "\n")

    openedFile.write("done()\n")                    # to pause the program 
    openedFile.close()
    return True


    ''' function call at program start to handle CMD argument '''

    input_file, output_file = '', ''

    try:
        options, args = getopt.getopt( sys.argv[1:], "i:o:")
    except getopt.GetoptError as error:
        print("Wrong syntax !")
        print(error.msg)
        sys.exit()

    for param, arg in options:
        if param in ("-i"): input_file = arg
        elif param in ("-o"): output_file = arg

    if app(input_file, output_file):
        print("Errors has occured. The program could not finish properly.")
        return -1
    
if __name__ == "__main__":      # call main() if this file is the primary file
    actions = {                             # switcher by symbols
        'a': ["pd()", "fd({taille})"],
        'b': ["pu()", "fd({taille})"],
        '+': "right({angle})",
        '-': "left({angle})",
        '*': "right(180)",
        '[': "#TODO",
        ']': "#TODO"
    }

    def app(inFile = '', outFile = ''):
        ''' main function of the application '''
        lsystem = {"axiome":None, "regles":{}, "angle":None, "taille":None, "niveau":None, "customrules":{}}  # default L-System

        error = loadInput(
            inputFile(message="Please enter path to the input file : ", defaultFile=inFile, shouldExist=True),
            lsystem
        )
        if error: return error

        formatActions(lsystem, actions)

        error = LSystemToPythonCode(
            generate_L_System_by_Level(rules = lsystem["regles"], axiome = lsystem["axiome"], level = lsystem["niveau"]),
            actions,
            inputFile(message="Please enter path to the output file : ", defaultFile=outFile)
        )
        return error
        
    def main():
        ''' function call at program start to handle CMD argument '''

        input_file, output_file = '', ''

        try:
            options, args = getopt.getopt( sys.argv[1:], "i:o:")
        except getopt.GetoptError as error:
            print("Wrong syntax !")
            print(error.msg)
            sys.exit()

        for param, arg in options:
            if param in ("-i"): input_file = arg
            elif param in ("-o"): output_file = arg

        if not app(input_file, output_file):
            print("Errors has occured. The program could not finish properly.")
            return -1

    main()