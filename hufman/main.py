from node import Node

S = ['m', 'a', 'd', 'g', 's','c']
P = [0.30, 0.20, 0.15, 0.15, 0.10,0.10]
arbre =  Node.creer_arbre_huffman(S, P)

codes_dict = {}
arbre.afficher_code(codes_dict=codes_dict)
codes_table = [codes_dict[symbol] for symbol in S]

mot = "madagasca"

# Encodage du mot
mot_encode = Node.encoder_texte(mot, codes_dict)

print("\nMot original :", mot)
print("Mot encode :", mot_encode)

# print( [bin(code)[2:] for code in mot_encode])
# print("Codes de Huffman selon l'ordre des symboles :")
# print(codes_table)
# print(S)