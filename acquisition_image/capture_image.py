import os.path
import cv2
from IHM.deuxième_page import ImageReviewPage


class ImageCapture:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.label_captured = False
        self.product_captured = False
        self.image_folder="/Users/thomaseude/Desktop/ICAM/I5/MSI/GROUPE SEB/ProjetSeb_v2/acquisition_image"

    def capture_etiquette(self):
        # Capture de l'image d'étiquette
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            image_path = os.path.join(self.image_folder, "image_etiquette.png")
            cv2.imwrite(image_path, frame)
            print("Image de l'étiquette enregistrée.")
            self.label_captured = True

        if self.label_captured and self.product_captured:
            self.show_image_review_page("image_etiquette.png", "image_produit.png")


    def capture_gravure(self):
        # Capture de l'image de gravure
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            image_path=os.path.join(self.image_folder,"image_produit.png" )
            cv2.imwrite(image_path, frame)
            self.product_captured = True
            print("Image du produit enregistrée.")

        # Vérifier si les deux images ont été capturées
        if self.label_captured and self.product_captured:
            self.show_image_review_page("image_etiquette.png", "image_produit.png")

    def show_image_review_page(self, image1, image2):
        review_page = ImageReviewPage(image1, image2)
        review_page.exec()