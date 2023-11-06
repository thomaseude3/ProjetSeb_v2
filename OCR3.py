import cv2
import pytesseract
from fuzzywuzzy import fuzz, process
import re
from Levenshtein import distance

# Fonction pour redimensionner une image
def redimensionner_image(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

# Fonction pour enregistrer l'image avec les rectangles
def enregistrer_image_rectangles(image, positions, nom_fichier):
    for position in positions:
        if position is not None:
            x, y, w, h = position
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.imwrite(nom_fichier, image)

# Charger les images
image_produit = cv2.imread("acquisition_image/produit_basler_binarise.png")
image_etiquette = cv2.imread("acquisition_image/etiquette_basler_binarisee.png")

# Utiliser pytesseract pour extraire le texte des images
texte_produit = pytesseract.image_to_string(image_produit)
texte_etiquette = pytesseract.image_to_string(image_etiquette)

# Fonction pour extraire les mots et les suites de chiffres
def extraire_mots_et_chiffres(texte):
    mots = re.findall(r'\b[a-zA-Z0-9]+\b', texte)
    return mots

# Fonction pour localiser les positions des mots dans une image
def localiser_positions_mots(image, mots):
    positions = []
    resultats = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    for mot in mots:
        mot_trouve = False
        for i, mot_resultat in enumerate(resultats["text"]):
            if mot.strip().lower() in mot_resultat.strip().lower():
                x, y, w, h = resultats["left"][i], resultats["top"][i], resultats["width"][i], resultats["height"][i]
                positions.append((x, y, w, h))
                mot_trouve = True
                break

        if not mot_trouve:
            # Si le mot n'est pas trouvé, ajouter une position None
            positions.append(None)

    return positions

# Fonction pour dessiner des rectangles rouges autour des mots non correspondants
def dessiner_rectangles(image, positions, mots_non_correspondants, scores):
    for i, position in enumerate(positions):
        if position is not None and scores[i] == 1.0:  # Modifier cette condition pour inclure les mots avec un score de 1.0
            x, y, w, h = position
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Rouge



# Fonction pour comparer les mots extraits en utilisant la distance de Levenshtein
def comparer_mots(texte1, texte2):
    mots1 = extraire_mots_et_chiffres(texte1)
    mots2 = extraire_mots_et_chiffres(texte2)

    mots_correspondants = []
    scores = []
    mots_deja_correspondants = set()  # Utiliser un ensemble pour stocker les mots déjà associés

    for mot1 in mots1:
        mot_correspondant = None
        score_max = 0

        if mot1 not in mots_deja_correspondants:  # Vérifier si le mot a déjà été associé
            for mot2 in mots2:
                score = 1 - (distance(mot1.lower(), mot2.lower()) / max(len(mot1), len(mot2)))
                if score > score_max:
                    score_max = score
                    mot_correspondant = mot2

                if score == 1.0:  # Si la similitude est parfaite, arrêter la comparaison
                    mots_deja_correspondants.add(mot1)  # Ajouter le mot à l'ensemble des mots associés
                    break

            if score_max == 1.0:  # Si le score est parfait, marquer le mot comme référence
                mots_correspondants.append((mot1, mot1, score_max))
            else:
                mots_correspondants.append((mot1, mot_correspondant, score_max))

            scores.append(score_max)

    return mots_correspondants, scores


   
# Comparer les mots extraits en utilisant la distance de Levenshtein
mots_correspondants, scores = comparer_mots(texte_produit, texte_etiquette)

# Comparer les mots extraits en utilisant la distance de Levenshtein
mots_correspondants, scores = comparer_mots(texte_produit, texte_etiquette)

# Comparer les mots extraits
mots_correspondants, scores = comparer_mots(texte_produit, texte_etiquette)

# Afficher les textes extraits
print("Texte extrait de l'image du produit :")
print(texte_produit)
print("\nTexte extrait de l'image de l'étiquette :")
print(texte_etiquette)

# Localiser les positions des mots non correspondants dans l'image du produit
positions_mots = localiser_positions_mots(image_produit, extraire_mots_et_chiffres(texte_produit))

# Dessiner des rectangles rouges autour des mots avec une similitude parfaite (score de 1.0)
dessiner_rectangles(image_produit, positions_mots, extraire_mots_et_chiffres(texte_produit), scores)

# Afficher les résultats
cv2.imshow("Image du produit avec rectangles rouges", image_produit)
cv2.waitKey(0)
cv2.destroyAllWindows()


# Afficher les mots correspondants et leurs scores
print("\nMots correspondants entre les deux textes :")
for mot, correspondance, score in mots_correspondants:
    print(f"Produit: {mot}, Étiquette: {correspondance} (Score: {score})")

# Afficher les mots non correspondants et leurs positions dans l'image du produit
for i, (mot, correspondance, score) in enumerate(mots_correspondants):
    if score < 100:
        print(f"Mot non correspondant: {mot} (Score: {score})")
        if positions_mots[i] is not None:
            print(f"Position dans l'image du produit: {positions_mots[i]}")
        else:
            print("Position inconnue")

# Afficher les résultats avec la distance de Levenshtein
print("\nMots correspondants entre les deux textes avec la distance de Levenshtein :")
for mot, correspondance, score in mots_correspondants:
    print(f"Produit: {mot}, Étiquette: {correspondance} (Score: {score})")
