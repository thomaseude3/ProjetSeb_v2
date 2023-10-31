import cv2
import os
class traitement_etiquette:
    @staticmethod
    def enregistrer_image(image, nom_fichier):
        dossier_sortie = "acquisition_image"
        if not os.path.exists(dossier_sortie):
            os.makedirs(dossier_sortie)

        chemin_sortie = os.path.join(dossier_sortie, nom_fichier)
        cv2.imwrite(chemin_sortie, image)
        print(f"Image enregistrée sous {chemin_sortie}")

    @staticmethod
    def pre_traitement(image):
        # Convertir en niveaux de gris
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Appliquer un flou gaussien pour réduire le bruit
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        return blurred

    @staticmethod
    def binariser_image(image):
        # Appliquer un seuillage adaptatif
        binary_image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 5)

        return binary_image

class traitement_produit:
    @staticmethod
    def enregistrer_image(image, nom_fichier):
        dossier_sortie = "acquisition_image"
        if not os.path.exists(dossier_sortie):
            os.makedirs(dossier_sortie)

        chemin_sortie = os.path.join(dossier_sortie, nom_fichier)
        cv2.imwrite(chemin_sortie, image)
        print(f"Image enregistrée sous {chemin_sortie}")

    @staticmethod
    def pre_traitement(image):
        # Convertir en niveaux de gris
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Appliquer un flou gaussien pour réduire le bruit
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        return blurred

    @staticmethod
    def binariser_image(image):
        # Appliquer un seuillage adaptatif
        binary_image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 5)

        return binary_image