import sys
from PyQt6.QtWidgets import QApplication
from IHM.accueil_ihm import ImageCaptureApp

def main():
    app = QApplication(sys.argv)
    window = ImageCaptureApp()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()