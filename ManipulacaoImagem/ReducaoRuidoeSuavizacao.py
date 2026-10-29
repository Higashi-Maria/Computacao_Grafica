import io
import cv2
import numpy as np
import urllib.request
from PIL import Image
import matplotlib.pyplot as plt

path = r"C:\Users\Maria\Desktop\CG\pup.jpeg"
image = np.array(Image.open(path))


# Write your code below
gaussian_blur = cv2.GaussianBlur(image, (5, 5), 0)

median_blur = cv2.medianBlur(image, 5)

# Display the results
plt.figure(figsize=(10, 10))
plt.subplot(1, 3, 1)
plt.imshow(image)
plt.title("Imagem Original")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(gaussian_blur)
plt.title("Gaussian Blur")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(median_blur)
plt.title("Median Blur")
plt.axis("off")

plt.tight_layout()
plt.show()
