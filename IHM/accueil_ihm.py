from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication
import sys
from acquisition_image.capture_image import ImageCapture
from IHM import deuxième_page

class ImageCaptureApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Capture d'Images")
        self.setGeometry(100, 100, 600, 300)

        self.capture_label_button = QPushButton("Capturer l'étiquette")
        self.capture_label_button.clicked.connect(self.capture_label)

        self.capture_product_button = QPushButton("Capturer le produit")
        self.capture_product_button.clicked.connect(self.capture_product)

        layout = QVBoxLayout()
        layout.addWidget(self.capture_label_button)
        layout.addWidget(self.capture_product_button)
        self.setLayout(layout)

        self.image_capture = ImageCapture()

    def capture_label(self):
        self.image_capture.capture_etiquette()

    def capture_product(self):
        self.image_capture.capture_gravure()

    def show_image_review_page(self, image1, image2):
        review_page = ImageReviewPage(image1, image2)
        review_page.exec()