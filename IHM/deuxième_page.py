from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QImage
from traitement_image.binarisation import ImageProcessor
import os
from PIL import Image

class ImageReviewPage(QDialog):
    def __init__(self, image1_path, image2_path):
        super().__init__()

        image1_path="acquisition_image/etiquette_basler.png"
        image2_path="acquisition_image/produit_basler.png"


        #image1_path = "acquisition_image/image_etiquette.png"
        #image2_path = "acquisition_image/image_produit.png"

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

        accept_button.clicked.connect(self.traitement_images)

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

    def traitement_images(self):

        #image1_path = "acquisition_image/image_etiquette.png"
        #image2_path = "acquisition_image/image_produit.png"

        image1_path = "acquisition_image/etiquette_basler.png"
        image2_path = "acquisition_image/produit_basler.png"

        image_processor = ImageProcessor()

        binary_image1 = image_processor.binarize_image(image1_path)
        binary_image2 = image_processor.binarize_image(image2_path)

        cleaned_binary_image1 = image_processor.remove_noise(binary_image1)
        cleaned_binary_image2 = image_processor.remove_noise(binary_image2)

        image_label_pairs = [(cleaned_binary_image1, self.label1),
                             (cleaned_binary_image2, self.label2)]

        # Redimensionnez les images binaires pour qu'elles soient visibles
        max_width = 650  # Largeur maximale souhaitée
        max_height = 450  # Hauteur maximale souhaitée

        # Convertissez les images binaires de type numpy.ndarray en QImage
        for binary_image, label in image_label_pairs:
            # Convertissez les images binaires en QImage
            binary_qimage = QImage(binary_image.data, binary_image.shape[1], binary_image.shape[0],
                                   binary_image.shape[1], QImage.Format.Format_Grayscale8)


            scaled_width = min(binary_qimage.width(), max_width)
            scaled_height = min(binary_qimage.height(), max_height)
            binary_qimage = binary_qimage.scaled(scaled_width, scaled_height)


            # Créez des QPixmap à partir des images binaires redimensionnées
            binary_pixmap = QPixmap.fromImage(binary_qimage)

            # Mettez à jour les QLabel avec les images binaires redimensionnées
            label.setPixmap(binary_pixmap)

            # Obtenez le chemin de fichier pour enregistrer l'image binaire
            if label == self.label1:
                original_image_path = "acquisition_image/image_etiquette.png"
            else:
                original_image_path = "acquisition_image/image_produit.png"
            output_image_path = os.path.splitext(original_image_path)[0] + "_binarized.png"

            # Enregistrez les images binaires dans le même dossier que les images initiales
            binary_pixmap.toImage().save(output_image_path)
        