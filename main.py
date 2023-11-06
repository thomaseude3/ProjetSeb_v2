import sys
from PyQt6.QtWidgets import QApplication, QVBoxLayout
from IHM.accueil_ihm import ImageCaptureApp

def main():
    app = QApplication(sys.argv)
    #main_window = ImageCaptureApp()
    window=ImageCaptureApp()
    #camera_widget = CameraLiveFeedWidget()

    main_layout = QVBoxLayout()
    #main_layout.addWidget(camera_widget)
    main_layout.addWidget(window)
    window.setLayout(main_layout)

    #main_window.show()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()