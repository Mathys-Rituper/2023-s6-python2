#####################################################
######  Introduction à la cryptographie  	###
#####   Codes de Huffman             		###
####################################################

from heapq import *

###  distribution de proba sur les letrres

caracteres = [
    ' ', 'a', 'b', 'c', 'd', 'e', 'f',
    'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z' ]

proba = [
    0.1835, 0.0640, 0.0064, 0.0259, 0.0260, 0.1486, 0.0078,
    0.0083, 0.0061, 0.0591, 0.0023, 0.0001, 0.0465, 0.0245,
    0.0623, 0.0459, 0.0256, 0.0081, 0.0555, 0.0697, 0.0572,
    0.0506, 0.0100, 0.0000, 0.0031, 0.0021, 0.0008  ]

def frequences() :
    table = {}
    n = len(caracteres)
    for i in range(n) :
        table[caracteres[i]] = proba[i]
    return table

F = frequences()
print(F)

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
    # à compléter

def code_huffman(arbre) :
    # on remplit le dictionnaire du code d'Huffman en parcourant l'arbre
    code = {}
    parcours(arbre,'',code)
    return code




###  Ex.3  encodage d'un texte contenu dans un fichier

def encodage(dico,fichier) :
    # à compléter

encode = encodage(dico,'leHorla.txt')
print(encode)


###  Ex.4  décodage d'un fichier compresse

def decodage(arbre,fichierCompresse) :
    # à compléter

decode = decodage(H,'leHorlaEncoded.txt')
print(decode)
