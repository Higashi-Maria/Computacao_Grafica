import io
import cv2
import numpy as np
import urllib.request
from PIL import Image
import matplotlib.pyplot as plt

path = r"C:\Users\Maria\Desktop\CG\sheep.jpeg"
image = np.array(Image.open(path))
image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

dft = np.fft.fft2(image)
dft_shift = np.fft.fftshift(dft)

# Write your code below
rows, cols = image.shape
ccrow,ccol = rows // 2, cols // 2

low_mask = np.zeros((rows, cols), np.uint8)
low_mask[ccrow-10:ccrow+10,ccol-10:ccol+10] = 1

high_mask = np.ones((rows, cols), np.uint8)
high_mask[ccrow-10:ccrow+10,ccol-10:ccol+10] = 0

lowpass_dft_filtered = dft_shift * low_mask
highpass_dft_filtered = dft_shift * high_mask

lowpass_dft_inverse = np.fft.ifftshift(lowpass_dft_filtered)
highpass_dft_inverse = np.fft.ifftshift(highpass_dft_filtered)

lowpass_image = np.fft.ifft2(lowpass_dft_inverse)
highpass_image = np.fft.ifft2(highpass_dft_inverse)

image_filtered = np.abs(lowpass_image)
high_pass_image = np.abs(highpass_image)

plt.figure(figsize=(12, 8))

plt.subplot(1, 3, 1)
plt.imshow(image, cmap="gray")
plt.title("Imagem original")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(image_filtered, cmap="gray")
plt.title("Passa-baixa")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(high_pass_image, cmap="gray")
plt.title("Passa-alta")
plt.axis("off")

plt.tight_layout()
plt.show()