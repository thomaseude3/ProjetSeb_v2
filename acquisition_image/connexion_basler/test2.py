from pypylon import pylon
import cv2
import time
import os  # Importez la bibliothèque os pour la gestion des fichiers et des dossiers

# Configurez le dossier de destination pour enregistrer les images PNG
output_folder = "images"  # Nom du dossier de destination
os.makedirs(output_folder, exist_ok=True)  # Créez le dossier s'il n'existe pas

tl_factory = pylon.TlFactory.GetInstance()
camera = pylon.InstantCamera()
camera.Attach(tl_factory.CreateFirstDevice())

camera.Open()
camera.StartGrabbing(pylon.GrabStrategy_OneByOne)
i = 0
print('Starting to acquire')
t0 = time.time()
while camera.IsGrabbing():
    grab = camera.RetrieveResult(700, pylon.TimeoutHandling_ThrowException)
    if grab.GrabSucceeded():
        i += 1
        # Convertissez l'image en un tableau numpy pour l'utiliser avec OpenCV
        image = grab.Array
        # Enregistrez l'image sous format PNG dans le dossier de destination
        image_filename = os.path.join(output_folder, f"image_{i}.png")
        cv2.imwrite(image_filename, image)
    if i == 100:
        camera.StopGrabbing()
        break

print(f'Acquired {i} frames in {time.time()-t0:.0f} seconds')
camera.Close()

