import cv2

class ImageProcessor:
    def binarize_image(self, image_path):
        gray_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        _, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)
        return binary_image

    def remove_noise(self, binary_image, kernel_size=3):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
        cleaned_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)
        return cleaned_image

