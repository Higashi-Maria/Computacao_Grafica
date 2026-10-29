import io
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

path = r"C:\Users\Maria\Desktop\CG\puppy.jpeg"

image = np.array(Image.open(path))

# write your code

# ensure image is RGB
if image.ndim == 2:
	image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

# resize to half the original size
resized = cv2.resize(image, (image.shape[1] // 2, image.shape[0] // 2), interpolation=cv2.INTER_AREA)

# prepare rotation (45 degrees around image center)
height, width = image.shape[:2]
center = (width // 2, height // 2)

rotation_matrix = cv2.getRotationMatrix2D(center, 45, 1.0)

rotated = cv2.warpAffine(image, rotation_matrix, (width, height), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

# crop the central region (central half of the image)
top = height // 4
left = width // 4
bottom = top + height // 2
right = left + width // 2
cropped = image[top:bottom, left:right]

plt.figure(figsize=(10, 10))

plt.subplot(2, 2, 1)
plt.imshow(image)
plt.title("Original")

plt.subplot(2, 2, 2)
plt.imshow(resized)
plt.title("Resized")

plt.subplot(2, 2, 3)
plt.imshow(rotated)
plt.title("Rotated")

plt.subplot(2, 2, 4)
plt.imshow(cropped)
plt.title("Cropped")

plt.tight_layout()
plt.show()