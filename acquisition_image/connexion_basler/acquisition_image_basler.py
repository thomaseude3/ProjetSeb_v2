import cv2
import numpy as np
import time
from pypylon import pylon
import os

width = 640  # Largeur en pixels de la zone d'acquisition
height = 480  # Hauteur en pixels de la zone d'acquisition
exposureTime = 1000  # Temps d'exposition en microsecondes (1 ms)
fps = 30  # Fréquence d'acquisition en images par seconde


def connectCamera(width, height, exposureTime, fps):
    """
    Fonction réalisant la connexion de la caméra Basler et le réglage de la zone d'acquisition.

    | Crée l'objet camera à partir de la première camera Basler connectée trouvée.
    | Règle la taille de la zone d'acquisition à l'aide des paramètres width et height (ROI centré sur l'image).
    | Règle la vitesse du capteur à "Fast".
    | Règle le temps d'exposition à 1 ms.

    | En fonctionnement classique, la fonction renvoie un objet camera de la librairie pypylon
    | En cas de problème de connexion, la fonction renvoie None.

    :param int width: largeur en pixel de la zone d'acquisition de la caméra
    :param int height: hauteur en pixel de la zone d'acquisition de la caméra

    :return: Objet camera (librairie pypylon)
    :rtype: pylon.InstantCamera
    """

    try:
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        camera.Open()  # Need to open camera before can use camera.ExposureTime
        camera.Width = width
        camera.Height = height

        camera.CenterX.SetValue(True)
        camera.CenterY.SetValue(True)

        # camera.SensorReadoutMode = "Fast"
        camera.AcquisitionFrameRateEnable.SetValue(True)
        camera.AcquisitionFrameRate.SetValue(fps)
        camera.ExposureTime.SetValue(exposureTime)

        camera.PixelFormat.SetValue("BGR8")

        return camera

    except:
        print("ERREUR : Problème de connexion Caméra")
        return None


def oneImage(camera):
    """
    Fonction réalisant la prise d'une image par un objet caméra Basler (pypylon)

    | Lance l'acquisition de la caméra
    | Récupère une image
    | Arrête l'acquisition de la caméra
    | Renvoie l'image acquise au format numpy.ndarray

    :param pylon.InstantCamera camera: Objet camera (librairie pypylon)

    :return: l'image prise par la caméra et enregistrée dans la matrice
    :rtype: numpy.ndarray
    """

    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    grabResult = camera.RetrieveResult(10000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        image = grabResult.GetArray().copy()
    else:
        image = 0

    camera.StopGrabbing()
    return image


camera = connectCamera(width, height, exposureTime, fps)

if camera is not None:
    try:
        # Appelez la fonction oneImage pour prendre une image
        image = oneImage(camera)

        # Vérifiez si l'image a été capturée avec succès
        if isinstance(image, int) and image == 0:
            print("Échec de la capture de l'image.")
        else:
            print("Image capturée avec succès!")

            # Affichez l'image à l'aide de la bibliothèque OpenCV (si installée)
            cv2.imshow("Image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    finally:
        # Fermez la caméra
        camera.Close()
else:
    print("La connexion à la caméra a échoué.")
