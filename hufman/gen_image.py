from PIL import Image
import numpy as np
from Tp_2_a import *
from bitarray import bitarray
# Crée une image vide en mode 'L' (grayscale) de taille 200x200 pixels
width, height = 200, 200
image = Image.new('L', (width, height))

# Remplit l'image avec un dégradé simple (valeurs de 0 à 255)
pixels = image.load()
for x in range(width):
    for y in range(height):
        # Crée un dégradé horizontal (valeur augmente avec x)
        pixels[x, y] = int(255 * x / width)

# Enregistre l'image en tant que fichier PNG
image.save("gradient_grayscale.png")

print("Image en mode 'L' créée et enregistrée sous 'gradient_grayscale.png'.")
print("Mode de l'image :", image.mode)
print("Bits par pixel : 8")




def hide_message_grayscale(image_path, target_pixels, message, output_path, codes_binaires):
    img = Image.open(image_path)
    pixels = img.load()

    # Étape 1: Encoder le message en Huffman
    binary_message = encoder_texte(message, codes_binaires).to01()
    print(f"Message binaire à cacher ({len(binary_message)} bits): {binary_message}")

    # Étape 2: Insérer dans l'image (LSB des pixels grayscale)
    binary_index = 0

    for x, y in target_pixels:
        if binary_index >= len(binary_message):
            break

        # Pour les images en mode 'L', chaque pixel est une seule valeur (0-255)
        current_pixel = pixels[x, y]
        
        # Modifier seulement le LSB
        new_pixel = (current_pixel & 0b11111110) | int(binary_message[binary_index])
        pixels[x, y] = new_pixel
        binary_index += 1

    img.save(output_path)
    print(f"✅ Message caché avec Huffman dans : {output_path}")
    print(f"Bits cachés: {binary_index}/{len(binary_message)}")
    

def extract_hidden_message_grayscale(image_path, target_pixels, codes):
    
    img = Image.open(image_path)
    pixels = img.load()

    # Étape 1: Extraire les bits LSB des pixels
    binary_message = ""
    for x, y in target_pixels:
        pixel_value = pixels[x, y]
        binary_message += str(pixel_value & 1)  # On prend seulement le LSB

    print(f"Bits extraits de l'image ({len(binary_message)} bits): {binary_message}")

    # Étape 2: Décompression Huffman
    texte_decompresse = ""
    flux = bitarray(binary_message)
    i = 0
    
    while i < len(flux):
        found = False
        for symbole, info in codes.items():
            longueur = info["longueur"]
            if i + longueur <= len(flux):
                code_courant = 0
                for j in range(longueur):
                    code_courant = (code_courant << 1) | flux[i + j]
                if code_courant == info["code"]:
                    texte_decompresse += symbole
                    i += longueur
                    found = True
                    break
        
        if not found:
            break  # Aucun code ne correspond (fin du message ou erreur)

    return texte_decompresse 
   
if __name__ == "__main__":
    # 1. Créer l'image de test
    #create_test_image("test_image.png")
    texte = lire_fichier_texte("texte.txt")
    symboles, probabilites, _ = construire_table_frequence(texte)
    noeuds = creer_noeuds(symboles, probabilites)
    arbre = construire_arbre_huffman(noeuds)
    codes = generer_codes_binaires(arbre)
    
    # 2. Paramètres de stéganographie
    target_pixels = [(0, 0), (0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,9),(0,10),(0,11),(0,12)]  # Diagonale de l'image
    message = "Aa"  # Message à cacher (2 caractères = 16 bits)
    
    # 3. Cacher le message
    hide_message_grayscale("gradient_grayscale.png", target_pixels, message, "hidden_message.png",codes)
    
    # 4. Extraire le message
    extracted = extract_hidden_message_grayscale("hidden_message.png", target_pixels,codes)
    print(f"Message extrait: '{extracted}'")  # Devrait afficher "OK"