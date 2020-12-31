actions = {
    'a': ["pd()", "fd({taille})"],
    'b': ["pu()", "fd({taille})"],
    '+': "right({angle})",
    '-': "left({angle})",
    '*': "right(180)",
    '[': "#TODO",
    ']': "#TODO"
}

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

    for i in axiome:
        if isinstance(actions[i], list):
            for j in actions[i]:
                openedFile.write(j + "\n")
        else:
            openedFile.write(actions[i] + "\n")

    openedFile.write("done()\n")
    openedFile.close()

''' replace all placeholder in actions '''
for key,value in actions.items():
    if isinstance(value, list):
        array = []
        for i in value:
            array.append(i.format(taille="25", angle="60"))
        actions.update({ key : array })
    else:
        actions.update({ key : value.format(taille="25", angle="60") })       

LSystemToPythonCode(generate_L_System_by_Level(dictionnaire = {"a":"a-a++a-a"},axiome= "-a++a++a",niveau=3), "C:/Users/jakem/Documents/codage python/L-System/test.py")
