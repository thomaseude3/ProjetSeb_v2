import cv2
from pypylon import pylon

tl_factory = pylon.TlFactory.GetInstance()
camera = pylon.InstantCamera()
camera.Attach(tl_factory.CreateFirstDevice())

camera.Open()
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

cv2.namedWindow("Camera Live Feed", cv2.WINDOW_NORMAL)

try:
    while True:
        grab = camera.RetrieveResult(1000, pylon.TimeoutHandling_ThrowException)
        if grab.GrabSucceeded():
            image = grab.Array

            cv2.imshow("Camera Live Feed", image)

            # Vous pouvez ajouter ici du traitement supplémentaire de l'image si nécessaire

        key = cv2.waitKey(1)
        if key == 27:  # Appuyez sur la touche 'ESC' pour quitter la boucle
            break

finally:
    cv2.destroyAllWindows()
    camera.StopGrabbing()
    camera.Close()