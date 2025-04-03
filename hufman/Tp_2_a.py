from bitarray import bitarray
import pickle

# Fonctions existantes inchangées (pour référence)
def lire_fichier_texte(nom_fichier):
    with open(nom_fichier, 'r', encoding='utf-8') as f:
        return f.read()

def construire_table_frequence(texte):
    freq = {}
    for caractere in texte:
        if caractere not in freq:
            freq[caractere] = 0
        freq[caractere] += 1
    total = len(texte)
    return list(freq.keys()), [freq[c] / total for c in freq], freq

def creer_noeuds(symboles, probabilites):
    noeuds = []
    for i in range(len(symboles)):
        noeuds.append({
            "symbole": symboles[i],
            "proba": probabilites[i],
            "gauche": None,
            "droite": None
        })
    return noeuds

def construire_arbre_huffman(noeuds):
    while len(noeuds) > 1:
        noeuds.sort(key=lambda n: n["proba"])
        gauche = noeuds.pop(0)
        droite = noeuds.pop(0)
        parent = {
            "symbole": None,
            "proba": gauche["proba"] + droite["proba"],
            "gauche": gauche,
            "droite": droite
        }
        noeuds.append(parent)
    return noeuds[0]
def verifier_prefixe(dictionnaire):
    codes = [format(info["code"], f'0{info["longueur"]}b') for info in dictionnaire.values()]
    codes.sort()  # Trier pour comparer les préfixes adjacents
    print(codes)

    for i in range(len(codes) - 1):
        if codes[i + 1].startswith(codes[i]):
            print(f"⚠️ Erreur : {codes[i]} est un préfixe de {codes[i + 1]}")
            return False
    return True


def generer_codes_binaires(noeud, code=0, longueur=0, dictionnaire=None):
    if dictionnaire is None:
        dictionnaire = {}

    if noeud["symbole"] is not None:
        dictionnaire[noeud["symbole"]] = {"code": code, "longueur": longueur}
    else:
        generer_codes_binaires(noeud["gauche"], code << 1, longueur + 1, dictionnaire)
        generer_codes_binaires(noeud["droite"], (code << 1) | 1, longueur + 1, dictionnaire)

    # Afficher les codes binaires générés
    verifier_prefixe(dictionnaire)
    return dictionnaire


# Nouvelle fonction d'encodage avec bitarray
def encoder_texte(texte, codes_binaires):
    bits = bitarray()
    for caractere in texte:
        code_info = codes_binaires[caractere]
        code = code_info["code"]
        longueur = code_info["longueur"]
        # Convertir le code en bits et l'ajouter au flux
        for i in range(longueur - 1, -1, -1):
            bits.append((code >> i) & 1)
    return bits

# Compression avec bitarray
def compresse(nom_fichier,out="out.bin"):
    texte = lire_fichier_texte(nom_fichier)
    symboles, probabilites, _ = construire_table_frequence(texte)
    noeuds = creer_noeuds(symboles, probabilites)
    arbre = construire_arbre_huffman(noeuds)
    codes = generer_codes_binaires(arbre)
    donnees_compressees = encoder_texte(texte, codes)

    with open(out, "wb") as f:
        # Sérialiser les codes avec pickle
        codes_bytes = pickle.dumps(codes)
        f.write(len(codes_bytes).to_bytes(4, 'big'))  # Taille des métadonnées
        f.write(codes_bytes)  # Table de codage
        
        # Nombre total de bits compressés
        nb_bits = len(donnees_compressees)
        f.write(nb_bits.to_bytes(4, 'big'))
        
        taille_finale = f.tell()
        # Écrire les données compressées
        donnees_compressees.tofile(f)

    print("✅ Compression avec bitarray terminée")
    print(f"Taille texte original     : {len(texte.encode('utf-8'))} octets")
    print(f"Taille fichier compressé  : {taille_finale} octets")
    print(f"Gain                      : {100 - (taille_finale * 100 // len(texte.encode('utf-8')))}%")

    return arbre, codes, nb_bits

def decompresse(nom_fichier_compressé, nom_fichier_sortie):
    with open(nom_fichier_compressé, "rb") as f:
        # Lire la taille des métadonnées
        taille_codes = int.from_bytes(f.read(4), 'big')
        codes = pickle.loads(f.read(taille_codes))  # Récupérer les codes
        
        # Nombre total de bits compressés
        nb_bits = int.from_bytes(f.read(4), 'big')
        
        # Lire les données compressées avec bitarray
        donnees_compressees = bitarray()
        donnees_compressees.fromfile(f)

    # Décoder les bits
    texte_decompresse = ""
    flux = bitarray()
    flux.extend(donnees_compressees[:nb_bits])  # Limiter à nb_bits
    
    i = 0
    while i < len(flux):
        for symbole, info in codes.items():
            longueur = info["longueur"]
            if i + longueur <= len(flux):
                code_courant = 0
                for j in range(longueur):
                    code_courant = (code_courant << 1) | flux[i + j]
                if code_courant == info["code"]:
                    texte_decompresse += symbole
                    i += longueur
                    break
        else:
            break  # Sortir si aucun code ne correspond (sécurité)

    # Écrire le fichier décompressé
    with open(nom_fichier_sortie, "w", encoding='utf-8') as f:
        f.write(texte_decompresse)
    
    print("✅ Décompression avec bitarray terminée")
    print(f"Taille fichier décompressé : {len(texte_decompresse.encode('utf-8'))} octets")
    
    return texte_decompresse



# # Exemple d'utilisation
# if __name__ == "__main__":
#     # Liste des pixels où le message est caché (doit être identique à l'encodage)
#     target_pixels = [(0, 0), (1, 1), (2, 2)]  
    
#     # Extraire le message
#     hidden_message = extract_hidden_message("output.png", target_pixels)
#     print("Message extrait:", hidden_message)
# # Test
if __name__ == "__main__":
     compresse("texte.txt")
    #  decompresse("out.bin", "texte_decompresse.txt")
