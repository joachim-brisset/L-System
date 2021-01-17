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
def loadInput(filename, lsystem):
    ''' load from a file all L-System's parameters '''
    error = False
    currentDict = ''
    with open(filename, "r") as fichier:
        for i in fichier.readlines():
            indent = i.startswith(" ") or i.startswith("\"")
            elements = list(map(lambda item: item.strip(" \"\n"), i.split("=")))

            if elements[0] == '': continue
            if not indent and currentDict : currentDict = ''
            if currentDict:
                if elements[0] in lsystem[currentDict]:
                    print ("erreur , plusieurs occurences de la regle de complacement", elements[0], "dans", currentDict)
                    error = True
                else:
                    lsystem[currentDict][elements[0]] = elements[1]
            else:
                if elements[0] in lsystem:
                    if isinstance(lsystem[elements[0]], dict):
                        currentDict = elements[0]
                        if elements[1] != "": lsystem[currentDict][elements[1]] = elements[2]
                        continue
                    if lsystem[elements[0]] != None:
                        print ("erreur , plusieurs occurences de la regle", elements[0])
                        error = True
                    lsystem[elements[0]] = elements[1]
                else:
                    print("Unknow rules : " + elements[0])
                    print("Error not severe, continue program ...") 
    return checkLSystem(lsystem) or error
def checkLSystem(lsystem):
    ''' Check the validity of all L-System's parameters '''
    error = False
    if lsystem["axiome"] == None or lsystem["axiome"] == "":
        print("[Error] >> la regle 'axiome' est vide")
        error = True
    if lsystem["regles"] == {}:
        print("la regle 'regles' est vide")
        error = True

    try:
        if lsystem["taille"] == None or float(lsystem["taille"]) < 0:
            print("[Error] >> la regle 'taille' est vide ou a une valeur invalide (<0)")
            error = True
    except ValueError:
        print("[Error] >> la regle 'taille' n'est pas un nombre !")
        error = True

    try:
        if lsystem["angle"] == None or float(lsystem["angle"]) < 0 or float(lsystem["angle"]) > 360 :
            print("[Error] >> la regle 'angle' est vide ou a une valeur invalide (<0 or >360)")
            error = True
    except ValueError:
        print("[Error] >> la regle 'angle' n'est pas un nombre !")
        error = True

    try:
        if lsystem["niveau"] == None or int(lsystem["niveau"]) < 0 :
            print("[Error] >> la regle 'niveau' est vide ou a une valeur invalide (<0)")
            error = True
    except ValueError:
        print("[Error] >> la regle 'niveau' n'est pas un nombre !")
        error = True
    return error
def formatActions(lsystem, actions):
    ''' add custom rules and replace all placeholder in actions '''
    actions.update( lsystem["customrules"] )

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
def LSystemToPythonCode(axiome, action, f, verbose=False):
    ''' convert an axiome's L-System string to an executable Python code drawing the L-System '''
    def write(openf, msg):
        if verbose: print(msg.strip('\n'))
        openf.write(msg)

    openedFile = open(f, 'w')
    write(openedFile, "from turtle import *\n")      # needed for drawing
    write(openedFile, "speed(0)\n")                  # increase at maximum the drawing speed

    write(openedFile, "savedPos = [] \n")
    write(openedFile, "def savePos():\n\tsavedPos.append( (pos(), heading()) )\n")
    write(openedFile, "def getLastPos():\n\ttemp = savedPos.pop()\n\tgoto(temp[0])\n\tsetheading(temp[1])\n")

    for i in axiome:                                # for each symbol in axiome write the associated function(s)
        if not i in actions:
            print("[Error] >> le symbole " + i + " n'a pas d'action associee a lui")
            openedFile.close()
            os.remove(f)
            return True, None

        if isinstance(actions[i], list):            # handle multiples functions for 1 symbols 
            for j in actions[i]:
                write(openedFile, j + "\n")
        else:
            write(openedFile, actions[i] + "\n")

    write(openedFile, "done()\n")                    # to pause the program 
    openedFile.close()
    return False, f

if __name__ == "__main__":      # call main() if this file is the primary file
    actions = {                             # switcher by symbols
        'a': ["pd()", "fd({taille})"],
        'b': ["pu()", "fd({taille})"],
        '+': "right({angle})",
        '-': "left({angle})",
        '*': "right(180)",
        '[': "savePos()",
        ']': "getLastPos()"
    }

    def app(inFile = '', outFile = '', shouldDraw=True):
        ''' main function of the application '''
        lsystem = {"axiome":None, "regles":{}, "angle":None, "taille":None, "niveau":None, "customrules":{}}  # default L-System

        error = loadInput(
            inputFile(message="Please enter path to the input file : ", defaultFile=inFile, shouldExist=True),
            lsystem
        )
        if error: return error

        formatActions(lsystem, actions)

        error, outputFile = LSystemToPythonCode(
            generate_L_System_by_Level(rules = lsystem["regles"], axiome = lsystem["axiome"], level = lsystem["niveau"]),
            actions,
            inputFile(message="Please enter path to the output file : ", defaultFile=outFile),
            True
        )
        if error: return error
        if shouldDraw: os.execv(sys.executable, [sys.executable, '"' + outputFile + '"'])

    def showHelp():
        print("l-system.py est un programme pour generer des programme dessinant le L-System")
        print("SYNTAX : python l-system.py [options] ")
        print("")
        print("OPTIONS :")
        print("\t x -i <fichier> ou --inFile=<fichier>  : permet de definir le fichier d'entree")
        print("\t x -o <fichier> ou --outFile=<fichier> : permet de definit le fichier de sortie")
        print("\t x --nodraw : permet de ne pas dessiner a la fin du programme")

        sys.exit()
    def main():
        ''' function call at program start. It handle CMD argument '''
        def handleOptions():
            ''' function that handle command parameter '''
            input_file, output_file = '', ''
            draw = True
            
            try:
                options, args = getopt.getopt( sys.argv[1:], "i:o:?h", ['inFile=', 'outFile=', 'nodraw', 'help'])
            except getopt.GetoptError as error:
                print("Wrong syntax ! " + error.msg)
                showHelp()

            for param, arg in options:
                if param in ("-?", "-h", "--help"): showHelp()
                elif param in ("-i, --inFile"):
                    if input_file:
                        print("-i et --inFile ne doivent pas etre utilise ensemble ou apparaitre plusieurs fois")
                        sys.exit(-1)
                    else:
                        input_file = arg
                elif param in ("-o, --outFile"):
                    if output_file:
                        print("-o et --outFile ne doivent pas etre utilise ensemble ou apparaitre plusieurs fois")
                        sys.exit(-1)
                    else:
                        output_file = arg
                elif param in ("--nodraw"): draw = False
            return input_file, output_file, draw

        try:
            if app(*handleOptions()):
                print("Errors has occured. The program could not finish properly. Please contact the developpers !")
                sys.exit(-1)

        except KeyboardInterrupt:
            print("program interrupted ... ")

    main()