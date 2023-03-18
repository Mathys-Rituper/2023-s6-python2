Utilisation :

Encodage d'un fichier texte en utilisant Huffman light :
    python3 main.py -e path_to_file
Le résultat est donné sous la forme d'un fichier encoded.txt écrit dans le même répertoire que le fichier source
Exemple (en étant positionné dans le dossier 1-huffman-light) :
```bash
python3 main.py -e ../4-test-dataset/laretraite.txt
```
Cette commande aura pour effet de créer un fichier binaire laretraite.bin, compressé avec l'algorithme de Huffman Light dans le même répertoire que le fichier d'entrée.

Décodage d'un fichier texte en utilisant Huffman light:
    python3 main.py -e path_to_file
Le résultat est écrit dans un fichier texte dans le même répertoire que le fichier source
Exemple (en étant positionné dans le dossier 1-huffman-light, et à condition d'avoir compressé le fichier laretraite.txt de l'étape précédente) :
```bash
python3 main.py -d ../4-test-dataset/laretraite.bin
```
Cette commande aura pour effet de créer un fichier texte décompressé dans le même répertoire que le fichier d'entrée.
