#####################################################
######  Introduction à la cryptographie  	###
#####   Codes de Huffman             		###
####################################################
import os
from heapq import *
import binascii


###  distribution de proba sur les letrres

caracteres = [
    ' ', 'a', 'b', 'c', 'd', 'e', 'f',
    'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z', "NEXIST", "EOF"]

proba = [
    0.1835, 0.0640, 0.0064, 0.0259, 0.0260, 0.1486, 0.0078,
    0.0083, 0.0061, 0.0591, 0.0023, 0.0001, 0.0465, 0.0245,
    0.0623, 0.0459, 0.0256, 0.0081, 0.0555, 0.0697, 0.0572,
    0.0506, 0.0100, 0.0000, 0.0031, 0.0021, 0.0008, 0.0002, 0.0000001  ]

def frequences() :
    table = {}
    n = len(caracteres)
    for i in range(n) :
        table[caracteres[i]] = proba[i]
    return table


###  la classe Arbre

class Arbre :
    def __init__(self, lettre, gauche=None, droit=None):
        self.gauche=gauche
        self.droit=droit
        self.lettre=lettre
    def estFeuille(self):
        return self.gauche == None and self.droit == None
    def estVide(self):
        return self == None
    def __str__(self):
        return '<'+ str(self.lettre)+'.'+str(self.gauche)+'.'+str(self.droit)+'>'



###  Ex.1  construction de l'arbre d'Huffamn utilisant la structure de "tas binaire"
def arbre_huffman(frequences) :
    # Create a heap to store the trees with the lowest frequencies
    heap = []
    for lettre, freq in frequences.items():
        # Create a tree for each character with its frequency as the priority
        heappush(heap, (freq, Arbre(lettre)))

    # Combine the trees with the lowest frequencies until there is only one tree left
    while len(heap) > 1:
        # Get the two trees with the lowest frequencies
        (freq1, arbre1) = heappop(heap)
        (freq2, arbre2) = heappop(heap)
        # Create a new tree with no character as the root and link the two trees as its left and right children
        heappush(heap, (freq1 + freq2, Arbre(None, arbre1, arbre2)))

    # Return the root node of the resulting tree
    return heap[0][1]

###  Ex.2  construction du code d'Huffamn

def parcours(arbre,prefixe,dico) :
    if arbre.gauche is None and arbre.droit is None:
        # We've reached a leaf node, so add its character and compressed value to the dictionary
        dico[arbre.lettre] = prefixe
    else:
        # Traverse the left and right subtrees with the corresponding prefix values
        parcours(arbre.gauche, prefixe + '0', dico)
        parcours(arbre.droit, prefixe + '1', dico)


def code_huffman(arbre) :
    # on remplit le dictionnaire du code d'Huffman en parcourant l'arbre
    code = {}
    parcours(arbre,'',code)
    return code

###  Ex.3  encodage d'un texte contenu dans un fichier

def utf8_to_binarystring(char):
    # format as 8-digit binary, join each byte with space
    return ''.join([f'{i:08b}' for i in char.encode()])


def encodage(dico,fichier) :
    raw_text = ""
    res = ""
    filename, file_extension = os.path.splitext(fichier)
    output_path = filename + ".bin"

    with open(fichier,"r",encoding="utf8") as f:
        termine = False
        while not termine:
            char = f.read(1)
            if not char:
                termine = True
            else:
                raw_text = raw_text + char

    with open(output_path, "wb") as f:
        for char in raw_text:
            if char in dico.keys():
                res = res + dico[char]
            else:
                res = res + dico["NEXIST"]
                res = res + utf8_to_binarystring(char)

    res = res + dico["EOF"]

    if len(res) % 8 != 0:
        res = res + ('0' * (len(res) % 8) )

    to_encode = []

    for i in range(0, len(res) // 8):
        n = int(res[8*i:8*(i+1)],2)
        to_encode.append(n)


    with open(output_path, "wb") as f:
        f.write(bytes(to_encode))

    print("Encoded")



###  Ex.4  décodage d'un fichier compresse
def decode_arbre(root, binary_string):
    node = root
    for bit in binary_string:
        if bit == '0':
            node = node.gauche
        elif bit == '1':
            node = node.droit
        else:
            raise ValueError("Invalid binary string")
    if not node.estFeuille():
        return None
    else:
        return node.lettre

def binary_to_utf8(binary_str):
    # Read the first byte to determine the length of the character
    length_prefix = int(binary_str[:8], 2)

    # Determine the number of bytes needed to represent the character
    if length_prefix < 128:
        num_bytes = 1
    elif length_prefix < 224:
        num_bytes = 2
    elif length_prefix < 240:
        num_bytes = 3
    else:
        num_bytes = 4

    s = binary_str[:num_bytes*8]

    byte_str = bytes([int(s[i:i + 8], 2) for i in range(0, len(s), 8)])

    # Decode the bytes as utf8 and return the resulting string
    return byte_str.decode('utf8'),num_bytes


def decodage(arbre,fichierCompresse) :
    res = ""
    filename, file_extension = os.path.splitext(fichierCompresse)
    output_path = filename + "_decompressed" + ".txt"
    with open(fichierCompresse, "rb") as f:
        file_data = bytes(f.read())
        # Convert byte array to binary string
    binary_string = ""
    for byte in file_data:
        binary_string = binary_string + bin(byte)[2:].zfill(8)

    while len(binary_string) > 0:
        to_decode = ""
        to_decode = to_decode + binary_string[0]
        binary_string = binary_string[1:]
        decoded = decode_arbre(arbre,to_decode)

        #Tant que la série de bits à décoder ne correspond pas à un caractère valide, on rajoute un bit à la séquence
        while decoded is None:

            to_decode = to_decode + binary_string[0]
            binary_string = binary_string[1:]
            decoded = decode_arbre(arbre,to_decode)

            if decoded == "NEXIST":
                character, num_bytes = binary_to_utf8(binary_string)
                res = res + character
                binary_string = binary_string[(num_bytes*8):]
            # Si on atteint la fin du fichier, on force la sortie de boucle
            elif decoded == "EOF":
                binary_string = ""
            elif decoded is not None:
                res = res + decoded

    with open(output_path,"w+") as f:
        f.write(res)
    print("Decompressed")
    return res