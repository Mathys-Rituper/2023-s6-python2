from huffman_light import *

if __name__ == "__main__":
    F = frequences()
    print(F)

    arbre = arbre_huffman(F)

    dico = code_huffman(arbre)
    print(dico)

    encode = encodage(dico, '../leHorla.txt')

    decode = decodage(arbre,'leHorlaEncoded.txt')
    print(decode)
