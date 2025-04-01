def tri_decroissant(S, P):
    # Trie les symboles S et les probabilités P en fonction des probabilités de manière décroissante
    sorted_pairs = sorted(zip(P, S))
    P[:], S[:] = zip(*sorted_pairs)  # Dézippe et remplace les valeurs originales dans P et S

def fusionner(S, P):
    while len(P) > 1:
        # Fusionner les deux premières probabilités les plus faibles
        p1 = P.pop(0)
        p2 = P.pop(0)
        s1 = S.pop(0)
        s2 = S.pop(0)
        
        # Créer un nouveau symbole combiné
        P.append(p1 + p2)
        S.append(s1 + s2)
        
        # Trier à nouveau les probabilités en ordre décroissant
        tri_decroissant(S, P)
