import os.path
import cv2
from pypylon import pylon
from IHM.deuxième_page import ImageReviewPage


class ImageCapture:
    def __init__(self):
        # self.cap = cv2.VideoCapture(0)
        self.label_captured = False
        self.product_captured = False
        self.image_folder = "acquisition_image"

    '''def capture_etiquette(self):
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
            image_path = os.path.join(self.image_folder, "image_produit.png")
            cv2.imwrite(image_path, frame)
            self.product_captured = True
            print("Image du produit enregistrée.")

        # Vérifier si les deux images ont été capturées
        if self.label_captured and self.product_captured:
            self.show_image_review_page("image_etiquette.png", "image_produit.png")'''

    def show_image_review_page(self, image1, image2):
        review_page = ImageReviewPage(image1, image2)
        review_page.exec()

    def basler_etiquette(self):
        tl_factory = pylon.TlFactory.GetInstance()
        camera = pylon.InstantCamera()
        camera.Attach(tl_factory.CreateFirstDevice())

        camera.Open()
        camera.PixelFormat = "Mono8"
        camera.StartGrabbing(1)
        camera.ExposureTimeAbs.SetValue(2000)

        grab = camera.RetrieveResult(1000, pylon.TimeoutHandling_ThrowException)

        if grab.GrabSucceeded():
            print('Label grab succeeded')
            image = grab.Array

            # Ajoutez l'impression de la forme de l'image
            print("Shape de l'image :", image.shape)

            height, width = image.shape
            center_x = width // 2
            center_y = height // 2
            crop_size = 1100  # Taille du rectangle central en pixels (ajustez selon vos besoins)

            # Calculez les coordonnées du coin supérieur gauche du rectangle
            top_left_x = center_x - (crop_size // 2)
            top_left_y = center_y - (crop_size // 2)

            # Recadrez l'image au milieu
            cropped_image = image[top_left_y:top_left_y + crop_size, top_left_x:top_left_x + crop_size]

            # Enregistrez l'image sous format PNG en utilisant OpenCV
            image_path = os.path.join(self.image_folder, "etiquette_basler.png")
            cv2.imwrite(image_path, cropped_image)

            self.label_captured = True

        if self.label_captured and self.product_captured:
            self.show_image_review_page("etiquette_basler.png", "produit_basler.png")

        grab.Release()
        camera.Close()

    def basler_produit(self):
        tl_factory = pylon.TlFactory.GetInstance()
        camera = pylon.InstantCamera()
        camera.Attach(tl_factory.CreateFirstDevice())

        camera.Open()
        camera.PixelFormat = "Mono8"
        camera.StartGrabbing(1)
        camera.ExposureTimeAbs.SetValue(2000)

        grab = camera.RetrieveResult(1000, pylon.TimeoutHandling_ThrowException)

        if grab.GrabSucceeded():
            print('Product grab succeeded')
            image = grab.Array

            # Ajoutez l'impression de la forme de l'image
            print("Shape de l'image :", image.shape)


            height, width = image.shape
            center_x = width // 2
            center_y = height // 2
            crop_size = 1000  # Taille du rectangle central en pixels (ajustez selon vos besoins)

            # Calculez les coordonnées du coin supérieur gauche du rectangle
            top_left_x = center_x - (crop_size // 2)
            top_left_y = center_y - (crop_size // 2)

            # Recadrez l'image au milieu
            cropped_image = image[top_left_y:top_left_y + crop_size, top_left_x:top_left_x + crop_size]

            # Enregistrez l'image sous format PNG en utilisant OpenCV
            image_path = os.path.join(self.image_folder, "produit_basler.png")
            cv2.imwrite(image_path, cropped_image)

            self.product_captured = True

        if self.label_captured and self.product_captured:
            self.show_image_review_page("etiquette_basler.png", "produit_basler.png")

        grab.Release()
        camera.Close()
