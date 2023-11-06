import cv2
from pypylon import pylon
import os

tl_factory = pylon.TlFactory.GetInstance()
camera = pylon.InstantCamera()
camera.Attach(tl_factory.CreateFirstDevice())


camera.Open()
camera.StartGrabbing(1)
camera.ExposureTimeAbs.SetValue(2000)

grab = camera.RetrieveResult(1000, pylon.TimeoutHandling_ThrowException)
if grab.GrabSucceeded():
    print('Grab succeeded')
    image = grab.Array
    height, width = image.shape
    center_x = width // 2
    center_y = height // 2
    crop_size = 1100  # Taille du rectangle central en pixels (ajustez selon vos besoins)

    # Calculez les coordonnées du coin supérieur gauche du rectangle
    top_left_x = center_x - (crop_size // 2)
    top_left_y = center_y - (crop_size // 2)

    # Recadrez l'image au milieu
    cropped_image = image[top_left_y:top_left_y + crop_size, top_left_x:top_left_x + crop_size]

    # Enregistrez l'image recadrée sous format PNG en utilisant OpenCV
    image_path = "image_test.png"
    cv2.imwrite(image_path, image)

else:
    print('Grab unsucceeded')

grab.Release()

camera.Close()

