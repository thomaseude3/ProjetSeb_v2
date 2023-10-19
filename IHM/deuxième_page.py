from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QImage
from traitement_image.binarisation import binarize_image
import os
from PIL import Image

class ImageReviewPage(QDialog):
    def __init__(self, image1_path, image2_path):
        super().__init__()

        image1_path = "acquisition_image/image_etiquette.png"
        image2_path = "acquisition_image/image_produit.png"

        self.setGeometry(100,100,1200,600)
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

        accept_button.clicked.connect(self.binarize_images)

        # Utilisez le signal showEvent pour obtenir la taille de la fenêtre une fois affichée
        self.showEvent = self.on_show
    def on_show(self, event):
        # Obtenez la taille de la fenêtre une fois qu'elle est affichée
        window_size = self.size()
        screen_width = window_size.width()
        screen_height = window_size.height()

        # Redimensionnez les images pour qu'elles correspondent à la taille de la fenêtre
        scaled_pixmap1 = self.pixmap1.scaled(screen_width // 2, screen_height, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        scaled_pixmap2 = self.pixmap2.scaled(screen_width // 2, screen_height, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)

        # Affichez les images dans les QLabel
        self.label1.setPixmap(scaled_pixmap1)
        self.label2.setPixmap(scaled_pixmap2)

    def binarize_images(self):

        image1_path = "acquisition_image/image_etiquette.png"
        image2_path = "acquisition_image/image_produit.png"

        binary_image1 = binarize_image(image1_path)
        binary_image2 = binarize_image(image2_path)

        # Convertissez les images binaires de type numpy.ndarray en QImage
        binary_qimage1 = QImage(binary_image1.data, binary_image1.shape[1], binary_image1.shape[0],
                                binary_image1.shape[1], QImage.Format.Format_Grayscale8)
        binary_qimage2 = QImage(binary_image2.data, binary_image2.shape[1], binary_image2.shape[0],
                                binary_image2.shape[1], QImage.Format.Format_Grayscale8)

        # Redimensionnez les images binaires pour qu'elles soient visibles
        max_width = 600  # Largeur maximale souhaitée
        max_height = 300  # Hauteur maximale souhaitée

        # Redimensionnez la première image
        scaled_width1 = min(binary_qimage1.width(), max_width)
        scaled_height1 = min(binary_qimage1.height(), max_height)
        binary_qimage1 = binary_qimage1.scaled(scaled_width1, scaled_height1)

        # Redimensionnez la deuxième image
        scaled_width2 = min(binary_qimage2.width(), max_width)
        scaled_height2 = min(binary_qimage2.height(), max_height)
        binary_qimage2 = binary_qimage2.scaled(scaled_width2, scaled_height2)

        # Créez des QPixmap à partir des images binaires redimensionnées
        binary_pixmap1 = QPixmap.fromImage(binary_qimage1)
        binary_pixmap2 = QPixmap.fromImage(binary_qimage2)

        # Mettez à jour les QLabel avec les images binaires redimensionnées
        self.label1.setPixmap(binary_pixmap1)
        self.label2.setPixmap(binary_pixmap2)

        # Obtenez les chemins de fichiers pour enregistrer les images binaires
        output_image1_path = os.path.splitext(image1_path)[0] + "_binaire.png"
        output_image2_path = os.path.splitext(image2_path)[0] + "_binaire.png"

        # Enregistrez les images binaires dans le même dossier que les images initiales
        binary_pixmap1.toImage().save(output_image1_path)
        binary_pixmap2.toImage().save(output_image2_path)
        