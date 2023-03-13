from huffman_light import *

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Huffman-light"
    )
    parser.add_argument("-e", "--encode", help="Encode a text file. output is written to a file named encoded.txt", action="store_true")
    parser.add_argument("-d", "--decode", help="Decode a text file, output is sent to the standard output", action="store_true")
    parser.add_argument("path_to_file")


    args = parser.parse_args()

    print(args)

    if args.encode and args.decode:
        print("Cannot encode and decode at the same time. You can only use one of these options per execution. For help do 'python3 main.py -h")
        exit(1)

    if not args.encode and not args.decode:
        print("Please specify action : encode (-e) or decode (-d). For help do 'python3 main.py -h")

    F = frequences()

    arbre = arbre_huffman(F)

    dico = code_huffman(arbre)


    if args.encode:
        print(encodage(dico, args.path_to_file))

    elif args.decode:
     print(decodage(arbre,args.path_to_file))
