#####################################################
######  Introduction à la cryptographie  	###
#####   Codes de Huffman             		###
####################################################

from heapq import *
import binascii


###  distribution de proba sur les letrres

caracteres = [
    ' ', 'a', 'b', 'c', 'd', 'e', 'f',
    'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z', "NEXIST" ]

proba = [
    0.1835, 0.0640, 0.0064, 0.0259, 0.0260, 0.1486, 0.0078,
    0.0083, 0.0061, 0.0591, 0.0023, 0.0001, 0.0465, 0.0245,
    0.0623, 0.0459, 0.0256, 0.0081, 0.0555, 0.0697, 0.0572,
    0.0506, 0.0100, 0.0000, 0.0031, 0.0021, 0.0008, 0.0002  ]

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

def parcours(arbre,prefixe,code) :
    if arbre.gauche is None and arbre.droit is None:
        # We've reached a leaf node, so add its character and compressed value to the dictionary
        code[arbre.lettre] = prefixe
    else:
        # Traverse the left and right subtrees with the corresponding prefix values
        parcours(arbre.gauche, prefixe + '0', code)
        parcours(arbre.droit, prefixe + '1', code)


def code_huffman(arbre) :
    # on remplit le dictionnaire du code d'Huffman en parcourant l'arbre
    code = {}
    parcours(arbre,'',code)
    return code

###  Ex.3  encodage d'un texte contenu dans un fichier

def bytes_to_binary(bytestring):
    hexstring = binascii.hexlify(bytestring).decode('utf-8')
    return bin(int(hexstring, 16))[2:]
def encodage(dico,fichier) :
    raw_text = ""
    res = ""

    with open(fichier,"r",encoding="utf8") as f:
        termine = False
        while not termine:
            char = f.read(1)
            if not char:
                termine = True
            else:
                raw_text = raw_text + char

    with open("leHorlaEncoded.txt", "wb") as f:
        for char in raw_text:
            if char in dico.keys():
                res = res + dico[char]
            else:
                res = res + dico["NEXIST"]
                encoded_char = char.encode('utf-8')
                res = res + bytes_to_binary(encoded_char).zfill(8)
                print(len(bytes_to_binary(encoded_char).zfill(8)))

    if len(res) % 8 != 0:
        res = res + ('0' * (len(res) % 8) )

    to_encode = []

    for i in range(0, len(res) // 8):
        n = int(res[8*i:8*(i+1)],2)
        to_encode.append(n)

    with open("leHorlaEncoded.txt", "wb") as f:
        f.write(bytes(to_encode))

    return "leHorlaEncoded.txt"


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

def read_utf8_char(binary_string):
    print(binary_string)
    # Calculate the number of bytes needed to represent the character
    num_bytes = 1
    for i in range(1, 5):
        if (ord(binary_string[0]) & (0xff >> i)) == (0xff << (8 - i)):
            num_bytes = i
            break
    print(f"Longueur à décoder : {num_bytes}")
    # Extract the character bytes from the binary string
    char_bytes = binary_string[:num_bytes*8]
    print(f"Décodage de {char_bytes}")
    num = int(char_bytes, 2)  # convert binary string to integer
    char = chr(num) # convert integer to character
    # Convert the character bytes to a Unicode string
    return (char,num_bytes)
def decodage(arbre,fichierCompresse) :
    res = ""
    with open(fichierCompresse, "rb") as f:
        file_data = bytes(f.read())
        # Convert byte array to binary string
    binary_string = ""
    for byte in file_data:
        binary_string = binary_string + bin(byte)[2:].zfill(8)

    print(binary_string)
    while len(binary_string) > 0:
        to_decode = ""
        to_decode = to_decode + binary_string[0]
        binary_string = binary_string[1:]
        decoded = decode_arbre(arbre,to_decode)
        print(f"Binary string head is {binary_string[:20]}")

        #Tant que la série de bits à décoder ne correspond pas à un caractère valide, on rajoute un bit à la séquence
        while decoded is None:

            to_decode = to_decode + binary_string[0]
            binary_string = binary_string[1:]
            decoded = decode_arbre(arbre,to_decode)

            if decoded == "NEXIST":
                print(f"Found {decoded} : {to_decode}")
                character, num_bytes = read_utf8_char(binary_string)
                print(f"Decoded UTF8 character : {character}, {num_bytes} bytes long")
                res = res + character
                binary_string = binary_string[(num_bytes*8):]

            elif decoded is not None:
                res = res + decoded
    return res