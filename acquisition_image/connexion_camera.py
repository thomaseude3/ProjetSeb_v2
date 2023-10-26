from pypylon import pylon
from PIL import Image

# Créez une instance de la caméra et ouvrez-la
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()

# Prenez une photo
grabResult = camera.GrabOne(100000)  # Capturez une seule image avec un délai de 1000 ms (1 seconde)

# Vérifiez si la capture a réussi
if grabResult.GrabSucceeded():
    # Enregistrez l'image au format png
    with open("captured_image.jpg", "wb") as f:
        f.write(grabResult.GetArray())

    # Affichez les informations sur l'image (facultatif)
    print(f"Image width: {grabResult.Width}")
    print(f"Image height: {grabResult.Height}")

# Libérez la ressource de la capture
grabResult.Release()

# Fermez la caméra
camera.Close()
