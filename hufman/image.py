from PIL import Image
from Tp_2_a import *
import numpy as np
from bitarray import bitarray

# 1. Créer une image PNG de test (3x3 pixels)
def create_test_image(output_path):
    # Créer un tableau numpy avec des pixels RGBA (4 canaux)
    # Format: [R, G, B, A] (valeurs entre 0 et 255)
    pixels = np.array([
        [[255, 0, 0, 255], [0, 255, 0, 255], [0, 0, 255, 255]],    # Ligne 1 (Rouge, Vert, Bleu)
        [[128, 128, 128, 255], [255, 255, 0, 255], [0, 255, 255, 255]],  # Ligne 2 (Gris, Jaune, Cyan)
        [[255, 0, 255, 255], [128, 0, 0, 255], [0, 128, 0, 255]]   # Ligne 3 (Magenta, Rouge foncé, Vert foncé)
    ], dtype=np.uint8)

    # Convertir en image et sauvegarder
    img = Image.fromarray(pixels, 'RGBA')
    img.save(output_path)
    print(f"Image de test créée: {output_path}")

# 2. Utiliser notre exemple précédent pour cacher un message
from PIL import Image
from bitarray import bitarray
import pickle
import json

# ---------------------- CACHAGE DANS L'IMAGE ---------------------- #
def hide_message(image_path, target_pixels, message, output_path,codes_binaires):
    img = Image.open(image_path)
    pixels = img.load()

    

    # Étape 2 : Encoder le message en Huffman
    binary_message = encoder_texte(message, codes_binaires)
    

    # Étape 3 : Stocker le dictionnaire de Huffman

    # Séparateur pour éviter la confusion
    full_message =  binary_message.to01()  
    print(full_message)

    # Étape 4 : Insérer dans l’image
    binary_index = 0

    for x, y in target_pixels:
        if binary_index >= len(full_message):
            break

        r, g, b, *a = pixels[x, y]

        if binary_index < len(full_message):
            r = (r & 0b11111110) | int(full_message[binary_index])
            binary_index += 1
        if binary_index < len(full_message):
            g = (g & 0b11111110) | int(full_message[binary_index])
            binary_index += 1
        if binary_index < len(full_message):
            b = (b & 0b11111110) | int(full_message[binary_index])
            binary_index += 1

        pixels[x, y] = (r, g, b, *a) if a else (r, g, b)

    img.save(output_path)
    print(f"✅ Message caché avec Huffman dans : {output_path}")

# 3. Extraire le message (comme précédemment)
def extract_hidden_message(image_path, target_pixels,codes):
    img = Image.open(image_path)
    pixels = img.load()

    binary_message = ""
    for x, y in target_pixels:
        r, g, b, *a = pixels[x, y]
        binary_message += str(r & 1)
        binary_message += str(g & 1)
        binary_message += str(b & 1)

    texte_decompresse = ""
    print(f"Bits extraits de l'image: {binary_message}")

    flux = bitarray(binary_message)
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
    return texte_decompresse

# --- TEST COMPLET ---
if __name__ == "__main__":
    # 1. Créer l'image de test
    #create_test_image("test_image.png")
    texte = lire_fichier_texte("texte.txt")
    symboles, probabilites, _ = construire_table_frequence(texte)
    noeuds = creer_noeuds(symboles, probabilites)
    arbre = construire_arbre_huffman(noeuds)
    codes = generer_codes_binaires(arbre)
    
    # 2. Paramètres de stéganographie
    target_pixels = [(0, 0), (0, 1),(0,2),(1,0)]  # Diagonale de l'image
    message = "Aa"  # Message à cacher (2 caractères = 16 bits)
    
    # 3. Cacher le message
    hide_message("test_image.png", target_pixels, message, "hidden_message.png",codes)
    
    # 4. Extraire le message
    extracted = extract_hidden_message("hidden_message.png", target_pixels,codes)
    print(f"Message extrait: '{extracted}'")  # Devrait afficher "OK"