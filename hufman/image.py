from PIL import Image
import numpy as np

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
def hide_message(image_path, target_pixels, message, output_path):
    img = Image.open(image_path)
    pixels = img.load()
    
    binary_message = ''.join(format(ord(c), '08b') for c in message)
    binary_index = 0
    
    for x, y in target_pixels:
        if binary_index >= len(binary_message):
            break
        
        r, g, b, *a = pixels[x, y]
        if binary_index < len(binary_message):
            r = (r & 0b11111110) | int(binary_message[binary_index])
            binary_index += 1
        if binary_index < len(binary_message):
            g = (g & 0b11111110) | int(binary_message[binary_index])
            binary_index += 1
        if binary_index < len(binary_message):
            b = (b & 0b11111110) | int(binary_message[binary_index])
            binary_index += 1
        
        pixels[x, y] = (r, g, b, *a) if a else (r, g, b)
    
    img.save(output_path)
    print(f"Message caché dans: {output_path}")

# 3. Extraire le message (comme précédemment)
def extract_hidden_message(image_path, target_pixels):
    img = Image.open(image_path)
    pixels = img.load()

    binary_message = ""
    for x, y in target_pixels:
        r, g, b, *a = pixels[x, y]
        binary_message += str(r & 1)
        binary_message += str(g & 1)
        binary_message += str(b & 1)

    message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if len(byte) == 8:
            message += chr(int(byte, 2))

    return message

# --- TEST COMPLET ---
if __name__ == "__main__":
    # 1. Créer l'image de test
    #create_test_image("test_image.png")
    
    # 2. Paramètres de stéganographie
    target_pixels = [(0, 0), (0, 1), (0, 2),(1, 0), (1, 1), (1, 2),(2, 0), (2, 1), (2, 2)]  # Diagonale de l'image
    message = "OK Milay"  # Message à cacher (2 caractères = 16 bits)
    
    # 3. Cacher le message
    hide_message("test_image.png", target_pixels, message, "hidden_message.png")
    
    # 4. Extraire le message
    extracted = extract_hidden_message("test_image.png", target_pixels)
    print(f"Message extrait: '{extracted}'")  # Devrait afficher "OK"