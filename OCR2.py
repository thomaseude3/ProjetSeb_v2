import cv2
import pytesseract
from fuzzywuzzy import fuzz, process
import re

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
image_produit = cv2.imread("acquisition_image/PDF Scanner 061123 10.59.51.pdf")
image_etiquette = cv2.imread("acquisition_image/etiquette_basler_binarisee.png")

# Redimensionner les images (ajustez la valeur de scale_percent selon vos besoins)
scale_percent = 150  # Exemple : réduire de moitié
image_produit = redimensionner_image(image_produit, scale_percent)
image_etiquette = redimensionner_image(image_etiquette, scale_percent)

# Utiliser pytesseract pour extraire le texte des images
texte_produit = pytesseract.image_to_string(image_produit)
texte_etiquette = pytesseract.image_to_string(image_etiquette)

# Fonction pour extraire les mots et les suites de chiffres
def extraire_mots_et_chiffres(texte):
    mots = re.findall(r'\b[a-zA-Z0-9]+\b', texte)
    return mots

# Fonction pour localiser les positions des mots dans une image 
# Cette modification inspecte les résultats de Tesseract pour rechercher des mots qui "contienent" le mot recherché plutôt que de vérifier strictement 
# l'égalité exacte. Cela peut être utile si les résultats de Tesseract contiennent des variations ou des erreurs. Cela devrait aider à mieux localiser 
# les positions des mots dans l'image, même si les mots extraits ne correspondent pas exactement entre les deux images.
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
        if position is not None and scores[i] < 100:  # Entourer uniquement les mots avec un score inférieur à 100
            x, y, w, h = position
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Rouge

# Fonction pour comparer les mots extraits
def comparer_mots(texte1, texte2):
    mots1 = extraire_mots_et_chiffres(texte1)
    mots2 = extraire_mots_et_chiffres(texte2)

    # Liste des caractères à exclure
    caracteres_a_exclure = set(["-", "_", ":", ";", "!", "?","-—","—"])  # Ajoutez les caractères que vous souhaitez exclure

    mots_correspondants = []
    scores = []

    for mot1 in mots1:
        # Exclure les mots contenant des caractères spécifiques
        if any(char in mot1 for char in caracteres_a_exclure):
            continue

        correspondance = process.extractOne(mot1, mots2, scorer=fuzz.ratio)
        if correspondance:
            score = correspondance[1]
            scores.append(score)
            mots_correspondants.append((mot1, correspondance[0], score))

    return mots_correspondants, scores

# Comparer les mots extraits
mots_correspondants, scores = comparer_mots(texte_produit, texte_etiquette)

# Afficher les textes extraits
print("Texte extrait de l'image du produit :")
print(texte_produit)
print("\nTexte extrait de l'image de l'étiquette :")
print(texte_etiquette)

# Localiser les positions des mots non correspondants dans l'image du produit
positions_mots = localiser_positions_mots(image_produit, extraire_mots_et_chiffres(texte_produit))

# Dessiner des rectangles rouges autour des mots non correspondants
dessiner_rectangles(image_produit, positions_mots, extraire_mots_et_chiffres(texte_produit), scores)

# Afficher les résultats
cv2.imshow("Image du produit avec rectangles rouges", image_produit)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Afficher les mots correspondants et leurs scores
print("\nMots correspondants entre les deux textes :")
for mot, correspondance, score in mots_correspondants:
    print(f"Produit: {mot}, Étiquette: {correspondance} (Score: {score})")

# Display non-matching words and their positions in the product image
for i, (mot, correspondance, score) in enumerate(mots_correspondants):
    if score < 100:
        print(f"Non-matching word: {mot} (Score: {score})")
        if positions_mots[i] is not None:
            print(f"Position in the product image: {positions_mots[i]}")
        else:
            print("Position unknown")





