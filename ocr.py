import cv2
import pytesseract
from fuzzywuzzy import fuzz, process
import re

class ocr:
    # Fonction pour extraire les mots et les suites de chiffres
    def extraire_mots_et_chiffres(texte):
        mots = re.findall(r"\b[a-zA-Z0-9]+\b", texte)
        return mots

    # Fonction pour localiser les positions des mots dans une image
    def localiser_positions_mots(image, mots):
        positions = []
        resultats = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        for mot in mots:
            found = False
            for i, mot_resultat in enumerate(resultats["text"]):
                if mot.strip().lower() == mot_resultat.strip().lower():
                    x, y, w, h = resultats["left"][i], resultats["top"][i], resultats["width"][i], resultats["height"][i]
                    positions.append((x, y, w, h))
                    found = True
                    break
            if not found:
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
        mots1 = ocr.extraire_mots_et_chiffres(texte1)
        mots2 = ocr.extraire_mots_et_chiffres(texte2)

        # Liste des caractères à exclure
        caracteres_a_exclure = {"-", "_", ":", ";", "!", "?"}  # Ajoutez les caractères que vous souhaitez exclure

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

    """Fonction pour enregistrer l'image avec les rectangles
  def enregistrer_image_rectangles(image, positions, nom_fichier):
        for position in positions:
            if position is not None:
                x, y, w, h = position
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        cv2.imwrite(nom_fichier, image)"""
