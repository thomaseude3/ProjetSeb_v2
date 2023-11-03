import cv2
from pypylon import pylon
import os
import time
import datetime


# Fonction pour enregistrer une image avec les métadonnées
def save_image_with_metadata(image, image_path):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image_with_metadata = {
        "timestamp": timestamp,
        "exposure_time": camera.ExposureTimeAbs.GetValue(),
    }
    # Enregistrez les métadonnées dans un fichier texte (par exemple)
    metadata_file = open("metadata.txt", "a")
    metadata_file.write(f"Timestamp: {timestamp}, Exposure Time: {image_with_metadata['exposure_time']}\n")
    metadata_file.close()

    # Enregistrez l'image avec un nom de fichier basé sur l'horodatage
    image_path = os.path.join(image_path, f"{timestamp}.png")
    cv2.imwrite(image_path, image)


# Paramètres de capture
image_path = "/Users/thomaseude/Desktop/Photos_produits/3"
total_images = 30  # Nombre total d'images à capturer
capture_interval = 1  # Intervalle de capture en secondes

# Initialisation de la caméra
tl_factory = pylon.TlFactory.GetInstance()
camera = pylon.InstantCamera()
camera.Attach(tl_factory.CreateFirstDevice())
camera.Open()
camera.StartGrabbing()

# Configuration de l'exposition
camera.ExposureTimeAbs.SetValue(2000)

try:
    for i in range(total_images):
        # Attendre l'intervalle de capture
        time.sleep(capture_interval)

        # Effectuer la capture de l'image
        grab = camera.RetrieveResult(1000, pylon.TimeoutHandling_ThrowException)
        if grab.GrabSucceeded():
            print(f"Capture de l'image {i + 1}/{total_images}")
            image = grab.Array

            # Enregistrez l'image avec les métadonnées
            save_image_with_metadata(image, image_path)

            grab.Release()
        else:
            print(f"Échec de la capture de l'image {i + 1}")

finally:
    # Fermeture de la caméra
    camera.Close()
