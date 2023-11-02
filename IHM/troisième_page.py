from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class ImageDifferencePage(QDialog):
    def __init__(self, image_path, mots_non_correspondants):
        super().__init__()

        self.setGeometry(100, 100, 1000, 800)
        self.setWindowTitle("Différences entre les images")

        layout = QVBoxLayout()

        # Chargez l'image "image_rectangles_rouges.png"
        pixmap = QPixmap(image_path)
        # Définissez la taille souhaitée (par exemple, largeur x hauteur)
        target_width = 400  # Remplacez par la largeur souhaitée
        target_height = 400  # Remplacez par la hauteur souhaitée

        # Redimensionnez l'image pour qu'elle s'adapte à la taille souhaitée
        scaled_pixmap = pixmap.scaled(target_width, target_height, Qt.AspectRatioMode.KeepAspectRatio)
        label = QLabel()
        label.setPixmap(scaled_pixmap)
        # Ajoutez le QLabel à la gauche de la fenêtre
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignLeft)

        # Affichez les mots non correspondants et leurs scores
        mots_non_correspondants_label = QLabel("Mots non correspondants et scores:")
        layout.addWidget(mots_non_correspondants_label)
        for mot, correspondance, score in mots_non_correspondants:
            label = QLabel(f"Mot sur l'étiquette:{mot}, Mot sur le produit: {correspondance}, Score {score}")
            layout.addWidget(label)

        button_layout = QVBoxLayout()
        back_button = QPushButton("Retour à la première page")
        back_button.clicked.connect(self.close)
        button_layout.addWidget(back_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)