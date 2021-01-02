import sys , getopt

def files_arg():
    input_file = ''
    output_file = ''

    argv=sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv,"i:o:" )
    except getopt.GetoptError:
        print("l-system.py -i <fichier d'entrée> -o <fichier de sortie>")
        sys.exit()

    for opt, arg in opts:
        if opt in ("-i"):
            input_file = arg
        elif opt in ("-o"):
            output_file = arg

    return (input_file, output_file)


files_arg()
