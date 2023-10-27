from pypylon import pylon
import matplotlib.pyplot as plt
import cv2  # Importez OpenCV

tl_factory = pylon.TlFactory.GetInstance()
camera = pylon.InstantCamera()
camera.Attach(tl_factory.CreateFirstDevice())

camera.Open()
camera.StartGrabbing(1)
camera.ExposureTimeAbs.SetValue(900000)

grab = camera.RetrieveResult(1000, pylon.TimeoutHandling_ThrowException)
if grab.GrabSucceeded():
    print('Grab succeeded')
    image = grab.Array

    # Enregistrez l'image sous format PNG en utilisant OpenCV
    image_filename = "captured_image.png"
    cv2.imwrite(image_filename,image)

grab.Release()

camera.Close()
