import cv2
import os

print("Répertoire de travail actuel :", os.getcwd())
def enregistrer_image(image, nom_fichier):
    dossier_sortie = "../acquisition_image"
    if not os.path.exists(dossier_sortie):
        os.makedirs(dossier_sortie)

    chemin_sortie = os.path.join(dossier_sortie, nom_fichier)
    cv2.imwrite(chemin_sortie, image)
    print(f"Image enregistrée sous {chemin_sortie}")
def pre_traitement(image):
    # Convertir en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Appliquer un flou gaussien pour réduire le bruit
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    return blurred
def binariser_image(image):
    # Appliquer un seuillage adaptatif
    binary_image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 5)

    return binary_image

# Charger l'image
image_path = '../acquisition_image/produit_basler.png'
image = cv2.imread(image_path)

# Appliquer le prétraitement pour améliorer la suppression du bruit
preprocessed_image = pre_traitement(image)

# Binariser l'image prétraitée
image_binarisee = binariser_image(preprocessed_image)

# Afficher l'image binarisée
cv2.imshow("Image binarisée", image_binarisee)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Enregistrer l'image binarisée dans le dossier "data"
enregistrer_image(image_binarisee, "produit_basler_binarisee.png")