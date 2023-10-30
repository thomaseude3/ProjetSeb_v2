from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication
import sys
from acquisition_image.capture_image import ImageCapture
from IHM.deuxième_page import ImageReviewPage

class ImageCaptureApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Capture d'Images")
        self.setGeometry(100, 100, 600, 300)

        self.capture_label_button = QPushButton("Capturer l'étiquette")
        self.capture_label_button.clicked.connect(self.start_countdown_label)

        self.capture_product_button = QPushButton("Capturer le produit")
        self.capture_product_button.clicked.connect(self.start_countdown_product)

        layout = QVBoxLayout()
        layout.addWidget(self.capture_label_button)
        layout.addWidget(self.capture_product_button)
        self.setLayout(layout)

        self.image_capture = ImageCapture()

        self.timer_label = QTimer(self)
        self.timer_label.timeout.connect(self.update_countdown_label)
        self.countdown_label = 0

        self.timer_product = QTimer(self)
        self.timer_product.timeout.connect(self.update_countdown_product)
        self.countdown_product = 0

    def start_countdown_label(self):
        self.countdown_label = 3  # Set the initial countdown value
        self.timer_label.start(1000)  # Start the timer with a 1-second interval

    def start_countdown_product(self):
        self.countdown_product = 3  # Set the initial countdown value
        self.timer_product.start(1000)  # Start the timer with a 1-second interval

    def update_countdown_label(self):
        if self.countdown_label > 0:
            self.countdown_label -= 1
            self.capture_label_button.setText(f"Prise d'image dans {self.countdown_label}s")
        else:
            self.timer_label.stop()
            self.capture_label_button.setText("Autre prise d'image")
            self.image_capture.basler_etiquette()
            """self.capture_label()"""

    def update_countdown_product(self):
        if self.countdown_product > 0:
            self.countdown_product -= 1
            self.capture_product_button.setText(f"Prise d'image dans {self.countdown_product}s")
        else:
            self.timer_product.stop()
            self.capture_product_button.setText("Autre prise d'image")
            self.image_capture.basler_produit()
            """self.capture_product()"""

    def capture_label(self):
        self.image_capture.capture_etiquette()
    def capture_product(self):
        self.image_capture.capture_gravure()

    def show_image_review_page(self, image1, image2):
        review_page = ImageReviewPage(image1, image2)
        review_page.exec()