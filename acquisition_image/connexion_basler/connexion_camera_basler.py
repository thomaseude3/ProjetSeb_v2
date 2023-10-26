from pypylon import pylon

tl_factory = pylon.TlFactory.GetInstance()
camera = pylon.InstantCamera()
camera.Attach(tl_factory.CreateFirstDevice())

# Ouvrir la caméra
camera.Open()

# Informations sur la caméra
print("Nom convivial de la caméra:", camera.GetDeviceInfo().GetFriendlyName())
print("Numéro de série de la caméra:", camera.GetDeviceInfo().GetSerialNumber())
print("Nom complet de la caméra:", camera.GetDeviceInfo().GetFullName())
print("Unité de temps d'exposition:", camera.ExposureTimeRaw.GetUnit())
print("Valeur d'exposition actuelle:", camera.ExposureTimeRaw.GetValue())
print("Exposition minimale:", camera.ExposureTimeRaw.GetMin())
print("Exposition maximale:", camera.ExposureTimeRaw.GetMax())

# Fermer la caméra
camera.Close()
