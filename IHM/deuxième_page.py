from typing import List, Tuple, Any

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QImage
from traitement import traitement_etiquette, traitement_produit
from ocr import ocr
import os
from PIL import Image
import cv2
import pytesseract
from fuzzywuzzy import fuzz, process
import re
from IHM.troisième_page import ImageDifferencePage


class ImageReviewPage(QDialog):
    def __init__(self, image1_path, image2_path):
        super().__init__()

        image1_path = "acquisition_image/etiquette_basler.png"
        image2_path = "acquisition_image/produit_basler.png"

        # image1_path = "acquisition_image/image_etiquette.png"
        # image2_path = "acquisition_image/image_produit.png"

        self.setGeometry(100, 100, 1200, 600)
        self.setWindowTitle("Examen des images")

        layout = QVBoxLayout()

        # Chargez les images à partir des fichiers PNG
        self.pixmap1 = QPixmap(image1_path)
        self.pixmap2 = QPixmap(image2_path)

        # Créez des QLabel pour afficher les images
        self.label1 = QLabel()
        self.label2 = QLabel()

        # Créez un widget pour contenir les images côte à côte
        image_container = QWidget()
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.label1)
        image_layout.addWidget(self.label2)
        image_container.setLayout(image_layout)

        layout.addWidget(image_container)

        # Ajoutez le message et les boutons
        message_label = QLabel("Les photos vous conviennent-elles ?")
        layout.addWidget(message_label)

        button_layout = QHBoxLayout()
        accept_button = QPushButton("Oui")
        decline_button = QPushButton("Non")
        button_layout.addWidget(accept_button)
        button_layout.addWidget(decline_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        accept_button.clicked.connect(self.traitement_plus_ocr)
        decline_button.clicked.connect(self.retour_premiere_page)

        # Utilisez le signal showEvent pour obtenir la taille de la fenêtre une fois affichée
        self.showEvent = self.on_show

    def on_show(self, event):
        # Obtenez la taille de la fenêtre une fois qu'elle est affichée
        window_size = self.size()
        screen_width = window_size.width()
        screen_height = window_size.height()

        # Redimensionnez les images pour qu'elles correspondent à la taille de la fenêtre
        scaled_pixmap1 = self.pixmap1.scaled(screen_width // 2, screen_height,
                                             aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        scaled_pixmap2 = self.pixmap2.scaled(screen_width // 2, screen_height,
                                             aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)

        # Affichez les images dans les QLabel
        self.label1.setPixmap(scaled_pixmap1)
        self.label2.setPixmap(scaled_pixmap2)

    def traitement_images(self):

        # image1_path = "acquisition_image/image_etiquette.png"
        # image2_path = "acquisition_image/image_produit.png"

        image1_path = "acquisition_image/etiquette_basler.png"
        image2_path = "acquisition_image/produit_basler.png"

        image1 = cv2.imread(image1_path)
        image2 = cv2.imread(image2_path)

        traitement_etiquette_instance = traitement_etiquette()
        traitement_produit_instance = traitement_produit()

        cleaned_binary_image1 = traitement_etiquette_instance.pre_traitement(image1)
        cleaned_binary_image2 = traitement_produit_instance.pre_traitement(image2)

        binary_image1 = traitement_etiquette_instance.binariser_image(cleaned_binary_image1)
        binary_image2 = traitement_produit_instance.binariser_image(cleaned_binary_image2)

        traitement_etiquette_instance.enregistrer_image(binary_image1, 'etiquette_basler_binarisee.png')
        traitement_etiquette_instance.enregistrer_image(binary_image2, 'produit_basler_binarise.png')

    @property
    def ocr(self):
        image_produit = cv2.imread("acquisition_image/produit_basler_binarise.png")
        image_etiquette = cv2.imread("acquisition_image/etiquette_basler_binarisee.png")

        texte_produit = pytesseract.image_to_string(image_produit)
        texte_etiquette = pytesseract.image_to_string(image_etiquette)

        mots_correspondants, scores = ocr.comparer_mots(texte_produit, texte_etiquette)
        # Créez une liste pour stocker les mots non correspondants et leurs scores
        mots_non_correspondants=[]


        print("Texte extrait de l'image du produit :")
        print(texte_produit)
        print("\nTexte extrait de l'image de l'étiquette :")
        print(texte_etiquette)

        # Localiser les positions des mots non correspondants dans l'image du produit
        positions_mots = ocr.localiser_positions_mots(image_produit, ocr.extraire_mots_et_chiffres(texte_produit))

        # Dessiner des rectangles rouges autour des mots non correspondants
        ocr.dessiner_rectangles(image_produit, positions_mots, ocr.extraire_mots_et_chiffres(texte_produit), scores)

        #cv2.imshow("Image du produit avec rectangles rouges", image_produit)
        # Enregistrez l'image résultante
        cv2.imwrite("image_rectangles_rouges.png", image_produit)

        # Afficher les mots correspondants et leurs scores
        print("\nMots correspondants entre les deux textes :")
        for mot, correspondance, score in mots_correspondants:
            print(f"Produit: {mot}, Étiquette: {correspondance} (Score: {score})")
            if score < 100:
                # Ajoutez les mots non correspondants à la liste
                mots_non_correspondants.append((mot, correspondance, score))
            print(mots_non_correspondants)

        # Display non-matching words and their positions in the product image
        """for i, (mot, correspondance, score) in enumerate(mots_correspondants):
            if score < 100:
                print(f"Non-matching word: {mot} (Score: {score})")
                if positions_mots[i] is not None:
                    print(f"Position in the product image: {positions_mots[i]}")
                else:
                    print("Position unknown")"""
        return mots_non_correspondants

    def retour_premiere_page(self):
        self.accept()  # Ferme la boîte de dialogue

    def traitement_plus_ocr(self):
        self.traitement_images()
        mots_non_correspondants = self.ocr
        image_difference_page = ImageDifferencePage("image_rectangles_rouges.png", mots_non_correspondants)
        image_difference_page.exec()