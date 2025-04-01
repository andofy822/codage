from bitarray import bitarray

class Node:
    def __init__(self, symbol, probability):
        self.symbol = symbol
        self.probability = probability
        self.left = None
        self.right = None

    def creer_arbre_huffman(S, P):
        # Initialiser une liste de nœuds
        nodes = [Node(symbol, prob) for symbol, prob in zip(S, P)]
        
        # Fusionner jusqu'à ce qu'il ne reste qu'un seul nœud
        while len(nodes) > 1:
            # Trier les nœuds par probabilité
            nodes.sort(key=lambda x: x.probability)
            
            # Fusionner les deux nœuds avec les plus petites probabilités
            left = nodes.pop(0)
            right = nodes.pop(0)
            
            # Créer un nouveau nœud interne
            internal_node = Node(left.symbol + right.symbol, left.probability + right.probability)
            internal_node.left = left
            internal_node.right = right
            
            # Ajouter le nouveau nœud à la liste
            nodes.append(internal_node)
        
        # Retourner la racine de l'arbre de Huffman
        return nodes[0]

    def afficher_arbre(self, prefix=""):
        if self is not None:
            # Si le nœud est une feuille
            if self.left is None and self.right is None:
                print(f"{prefix}Leaf({self.symbol}, {self.probability})")
            else:
                print(f"{prefix}Node({self.symbol}, {self.probability})")
                if self.left:
                    self.left.afficher_arbre(prefix + "L--- ")
                if self.right:
                    self.right.afficher_arbre(prefix + "R--- ")
                    
    def afficher_code(self, code=0, codes_dict=None):
        if codes_dict is None:
            codes_dict = {}

    # Si c'est une feuille, on stocke directement l'entier (pas de conversion en texte)
        if self.left is None and self.right is None:
            codes_dict[self.symbol] = code  # Stocker l'entier brut
            print(f"{self.symbol}: {bin(code)[2:]}")  # Affichage en binaire pour visualisation
        else:
            if self.left:
                self.left.afficher_code(code << 1,  codes_dict)  # Décale à gauche (ajoute un 0)
            if self.right:
                self.right.afficher_code((code << 1) | 1, codes_dict)  # Décale et ajoute 1
        return codes_dict


    def encoder_texte(texte, codes_dict):
        bits = bitarray()
        for char in texte:
            bits.extend(bitarray(bin(codes_dict[char])[2:])) 
            #  bits.extend(bitarray(bin(codes_dict[char])[2:].zfill(8)))# Stocke directement en binaire
        return bits
    
    def construire_table_frequence(texte):
        freq = {}
        for caractere in texte:
            if caractere not in freq:
                freq[caractere] = 0
            freq[caractere] += 1
        total = len(texte)
        return list(freq.keys()), [freq[c] / total for c in freq], freq