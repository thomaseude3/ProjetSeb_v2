import sys
from PyQt6.QtWidgets import QApplication
from IHM.accueil_ihm import ImageCaptureApp
from acquisition_image.capture_image import ImageCapture

def main():
    app = QApplication(sys.argv)
    window = ImageCaptureApp()
    window.show()

    image_capture = ImageCapture()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()